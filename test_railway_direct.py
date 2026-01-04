#!/usr/bin/env python3
"""
Railway 환경과 동일하게 테스트 (DATABASE_URL 강제 설정)
"""
import os
import sys

# Railway 환경변수 강제 설정
os.environ["DATABASE_URL"] = "postgresql://postgres:EUxzTKqEvybegsaRhWsySxVcgCRvyZHA@mainline.proxy.rlwy.net:47312/railway"

print("=" * 70)
print("🔍 Railway 환경 시뮬레이션 테스트")
print("=" * 70)

# 환경변수 확인
print(f"\n✅ DATABASE_URL: {os.getenv('DATABASE_URL')[:50]}...")
print(f"✅ USE_POSTGRES: {bool(os.getenv('DATABASE_URL'))}")

# chatbot_engine import 전에 환경변수 설정 완료
from core.chatbot_engine import ChatbotEngine
from core.db import USE_POSTGRES, get_conn

print(f"\n📊 DB 설정 확인")
print("=" * 70)
print(f"USE_POSTGRES (from core.db): {USE_POSTGRES}")

# DB 연결 테스트
try:
    with get_conn() as conn:
        if USE_POSTGRES:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) as count FROM notices")
            result = cur.fetchone()
            from psycopg2.extras import RealDictCursor
            if isinstance(result, dict):
                count = result['count']
            else:
                count = result[0]
        else:
            cur = conn.execute("SELECT COUNT(*) FROM notices")
            count = cur.fetchone()[0]

        print(f"✅ DB 연결 성공")
        print(f"✅ 전체 공지 수: {count}개")
except Exception as e:
    print(f"❌ DB 연결 실패: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 챗봇 엔진 테스트
print(f"\n🤖 챗봇 엔진 테스트")
print("=" * 70)

try:
    engine = ChatbotEngine(user_id="railway_test")

    # 공지 조회 테스트
    notices = engine._get_recent_notices(limit=100)
    print(f"✅ _get_recent_notices() 성공: {len(notices)}개")

    if len(notices) > 0:
        print(f"\n처음 5개 공지:")
        for i, n in enumerate(notices[:5], 1):
            print(f"  [{i}] {n['title'][:40]}...")
    else:
        print("❌ 공지가 없습니다!")

    # 컨텍스트 구성
    context = engine._build_context(notices)
    print(f"\n✅ _build_context() 성공: {len(context)}자")
    print(f"컨텍스트 미리보기: {context[:200]}...")

    # 실제 질문 테스트
    print(f"\n💬 실제 질문 테스트")
    print("=" * 70)

    result = engine.ask("최근 공지사항 뭐가 있어?")
    print(f"\n응답 타입: {result['response_type']}")
    print(f"응답:\n{result['response'][:300]}...")

    if result['response_type'] == "NORMAL":
        print(f"\n✅ 성공! 참조 공지: {result['notice_refs']}")
    else:
        print(f"\n❌ 실패! 공지를 찾지 못했습니다.")

except Exception as e:
    print(f"❌ 챗봇 테스트 실패: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("✅ 테스트 완료!")
print("=" * 70)
