#!/usr/bin/env python3
"""
Railway PostgreSQL DB 공지사항 확인
"""
import os
from dotenv import load_dotenv
from core.db import get_conn

load_dotenv()

print("=" * 70)
print("🔍 Railway DB 공지사항 확인")
print("=" * 70)

# DATABASE_URL 확인
database_url = os.getenv("DATABASE_URL")
USE_POSTGRES = bool(database_url)

if USE_POSTGRES:
    print(f"\n✅ PostgreSQL 연결: {database_url[:50]}...")
else:
    print("\n⚠️  PostgreSQL 환경변수 없음 (로컬 SQLite 사용)")

print("\n" + "=" * 70)
print("📊 공지사항 통계")
print("=" * 70)

with get_conn() as conn:
    # 전체 공지 수
    if USE_POSTGRES:
        from psycopg2.extras import RealDictCursor
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT COUNT(*) as count FROM notices")
        result = cur.fetchone()
        total = result['count'] if result else 0
    else:
        cur = conn.execute("SELECT COUNT(*) FROM notices")
        total = cur.fetchone()[0]

    print(f"\n전체 공지 수: {total}개")

    # 부서별 분류
    if USE_POSTGRES:
        from psycopg2.extras import RealDictCursor
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT department, COUNT(*) as count
            FROM notices
            GROUP BY department
            ORDER BY count DESC
            LIMIT 10
        """)
        rows = cur.fetchall()
    else:
        cur = conn.execute("""
            SELECT department, COUNT(*) as count
            FROM notices
            GROUP BY department
            ORDER BY count DESC
            LIMIT 10
        """)
        rows = cur.fetchall()

    print("\n부서별 공지:")
    for row in rows:
        if USE_POSTGRES:
            dept = row['department']
            count = row['count']
        else:
            dept, count = row
        print(f"  {dept}: {count}개")

    # 최근 10개 공지 제목
    if USE_POSTGRES:
        from psycopg2.extras import RealDictCursor
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("""
            SELECT post_id, title, department, date
            FROM notices
            ORDER BY
                CASE
                    WHEN date IS NOT NULL THEN date::date
                    ELSE to_timestamp(created_at / 1000)::date
                END DESC,
                post_id DESC
            LIMIT 10
        """)
        rows = cur.fetchall()
    else:
        cur = conn.execute("""
            SELECT post_id, title, department, date
            FROM notices
            ORDER BY
                CASE
                    WHEN date IS NOT NULL THEN date
                    ELSE strftime('%Y-%m-%d', created_at/1000, 'unixepoch')
                END DESC,
                post_id DESC
            LIMIT 10
        """)
        rows = cur.fetchall()

    print("\n최근 공지 10개:")
    for row in rows:
        if USE_POSTGRES:
            post_id = row['post_id']
            title = row['title']
            dept = row['department']
            date = row['date']
        else:
            post_id, title, dept, date = row
        print(f"  [{post_id}] {title[:40]}... ({dept}) - {date}")

    # 키워드 검색 테스트
    print("\n" + "=" * 70)
    print("🔍 키워드 검색 테스트")
    print("=" * 70)

    keywords = ["교육", "연차", "협력업체", "인사평가", "휴가"]
    for keyword in keywords:
        if USE_POSTGRES:
            from psycopg2.extras import RealDictCursor
            cur = conn.cursor(cursor_factory=RealDictCursor)
            cur.execute("""
                SELECT COUNT(*) as count
                FROM notices
                WHERE title LIKE %s OR content LIKE %s
            """, (f"%{keyword}%", f"%{keyword}%"))
            result = cur.fetchone()
            count = result['count'] if result else 0
        else:
            cur = conn.execute("""
                SELECT COUNT(*) as count
                FROM notices
                WHERE title LIKE ? OR content LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            count = cur.fetchone()[0]

        print(f"\n'{keyword}' 검색 결과: {count}개")

        if count > 0:
            if USE_POSTGRES:
                from psycopg2.extras import RealDictCursor
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("""
                    SELECT post_id, title
                    FROM notices
                    WHERE title LIKE %s OR content LIKE %s
                    LIMIT 3
                """, (f"%{keyword}%", f"%{keyword}%"))
                rows = cur.fetchall()
            else:
                cur = conn.execute("""
                    SELECT post_id, title
                    FROM notices
                    WHERE title LIKE ? OR content LIKE ?
                    LIMIT 3
                """, (f"%{keyword}%", f"%{keyword}%"))
                rows = cur.fetchall()

            for row in rows:
                if USE_POSTGRES:
                    post_id = row['post_id']
                    title = row['title']
                else:
                    post_id, title = row
                print(f"  [{post_id}] {title}")

print("\n" + "=" * 70)
print("✅ 확인 완료!")
print("=" * 70)
