#!/usr/bin/env python3
"""
limit 수정 후 챗봇 테스트
"""
import os
from dotenv import load_dotenv
from core.chatbot_engine import ChatbotEngine

load_dotenv()

# Railway DB 사용
os.environ["DATABASE_URL"] = "postgresql://postgres:EUxzTKqEvybegsaRhWsySxVcgCRvyZHA@mainline.proxy.rlwy.net:47312/railway"

print("=" * 70)
print("🤖 챗봇 수정 후 테스트 (limit: 50 → 100)")
print("=" * 70)

engine = ChatbotEngine(user_id="test_user")

# 1. 컨텍스트 확인
print("\n📊 컨텍스트 확인")
print("=" * 70)

recent_notices = engine._get_recent_notices()
print(f"조회된 공지 수: {len(recent_notices)}개")

# "연차" 포함 여부 확인
context = engine._build_context(recent_notices)
has_연차 = '연차' in context
print(f"'연차' 키워드 in context: {'✅ YES' if has_연차 else '❌ NO'}")

# 2. 실제 질문 테스트
print("\n" + "=" * 70)
print("💬 챗봇 테스트")
print("=" * 70)

test_queries = [
    "교육 일정 확인",
    "연차 관련 안내해주세요",
    "협력업체 공지 보여줘",
    "인사평가 일정 알려주세요",
]

for query in test_queries:
    print(f"\n질문: {query}")
    print("-" * 70)

    result = engine.ask(query)

    print(f"응답 타입: {result['response_type']}")
    if result['response_type'] == "NORMAL":
        print(f"✅ 성공!")
        print(f"참조 공지: {result['notice_refs']}")
        print(f"응답 (처음 150자): {result['response'][:150]}...")
    else:
        print(f"❌ 실패: {result['response'][:100]}")

print("\n" + "=" * 70)
print("✅ 테스트 완료!")
print("=" * 70)
