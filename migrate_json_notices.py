#!/usr/bin/env python3
"""
notices_migration.json 파일의 공지사항을 PostgreSQL 데이터베이스에 마이그레이션
"""
import json
import os
from datetime import datetime
from core.db import get_conn
from dotenv import load_dotenv

load_dotenv()

def parse_created_at(created_at_str):
    """
    created_at 문자열을 epoch milliseconds로 변환

    Args:
        created_at_str: "2025-12-26 11:47:17" 형식의 문자열

    Returns:
        int: epoch milliseconds
    """
    try:
        dt = datetime.strptime(created_at_str, "%Y-%m-%d %H:%M:%S")
        return int(dt.timestamp() * 1000)
    except Exception as e:
        print(f"  ⚠️  날짜 파싱 오류: {created_at_str} - {e}")
        # 기본값으로 현재 시간 반환
        return int(datetime.now().timestamp() * 1000)


def migrate_notices_from_json(json_file_path):
    """
    JSON 파일에서 공지사항을 읽어 PostgreSQL에 마이그레이션

    Args:
        json_file_path: notices_migration.json 파일 경로
    """
    # JSON 파일 읽기
    print("=" * 70)
    print("📄 JSON 파일 읽기 중...")
    print("=" * 70)

    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    notices = data.get('notices', [])
    total_count = data.get('total_count', len(notices))
    export_date = data.get('export_date', 'Unknown')

    print(f"📊 총 공지사항: {total_count}개")
    print(f"📅 Export 날짜: {export_date}")
    print()

    # PostgreSQL 연결 확인
    USE_POSTGRES = bool(os.getenv("DATABASE_URL"))

    if not USE_POSTGRES:
        print("⚠️  경고: PostgreSQL 환경변수가 설정되지 않았습니다.")
        print("   로컬 SQLite DB (groupware.db)에 마이그레이션됩니다.")
    else:
        print("✅ PostgreSQL 연결 확인됨 (Railway 프로덕션)")

    print()
    print("=" * 70)
    print("🚀 마이그레이션 시작")
    print("=" * 70)

    # 통계
    inserted_count = 0
    skipped_count = 0
    error_count = 0

    with get_conn() as conn:
        for idx, notice in enumerate(notices, 1):
            notice_id = notice.get('id')
            title = notice.get('title')
            content = notice.get('content')
            department = notice.get('department', '전체')
            date = notice.get('date')
            created_at_str = notice.get('created_at')

            # created_at을 epoch milliseconds로 변환
            created_at = parse_created_at(created_at_str)

            print(f"\n[{idx}/{total_count}] 공지 ID {notice_id}: {title[:40]}...")

            try:
                # 중복 확인
                if USE_POSTGRES:
                    cur = conn.cursor()
                    cur.execute("SELECT post_id FROM notices WHERE post_id = %s", (notice_id,))
                    existing = cur.fetchone()
                else:
                    cur = conn.execute("SELECT post_id FROM notices WHERE post_id = ?", (notice_id,))
                    existing = cur.fetchone()

                if existing:
                    print(f"  ⏭️  이미 존재함 (SKIP)")
                    skipped_count += 1
                    continue

                # 공지사항 삽입
                if USE_POSTGRES:
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO notices (
                            post_id, title, content, type, author,
                            department, date, views, created_at
                        ) VALUES (
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s
                        )
                    """, (
                        notice_id,
                        title,
                        content,
                        '일반',  # 기본값: 일반 공지
                        'admin',  # 기본 작성자
                        department,
                        date,
                        0,  # 조회수 0
                        created_at
                    ))
                    conn.commit()
                else:
                    conn.execute("""
                        INSERT INTO notices (
                            post_id, title, content, type, author,
                            department, date, views, created_at
                        ) VALUES (
                            ?, ?, ?, ?, ?,
                            ?, ?, ?, ?
                        )
                    """, (
                        notice_id,
                        title,
                        content,
                        '일반',
                        'admin',
                        department,
                        date,
                        0,
                        created_at
                    ))

                print(f"  ✅ 삽입 완료")
                inserted_count += 1

            except Exception as e:
                print(f"  ❌ 오류 발생: {str(e)}")
                error_count += 1
                continue

    # 결과 요약
    print()
    print("=" * 70)
    print("📊 마이그레이션 완료")
    print("=" * 70)
    print(f"✅ 삽입: {inserted_count}개")
    print(f"⏭️  스킵: {skipped_count}개 (중복)")
    print(f"❌ 오류: {error_count}개")
    print(f"📝 총계: {total_count}개")
    print("=" * 70)


if __name__ == "__main__":
    json_file = "notices_migration.json"

    if not os.path.exists(json_file):
        print(f"❌ 파일을 찾을 수 없습니다: {json_file}")
        exit(1)

    migrate_notices_from_json(json_file)
    print("\n✅ 마이그레이션 스크립트 실행 완료!")
