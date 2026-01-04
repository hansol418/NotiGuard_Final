#!/usr/bin/env python3
"""
챗봇이 실제로 조회하는 공지사항 컨텍스트 디버그
"""
import os
from dotenv import load_dotenv
from core.chatbot_engine import ChatbotEngine

load_dotenv()

# Railway DB 사용
os.environ["DATABASE_URL"] = "postgresql://postgres:EUxzTKqEvybegsaRhWsySxVcgCRvyZHA@mainline.proxy.rlwy.net:47312/railway"

print("=" * 70)
print("🔍 챗봇 컨텍스트 디버그 (Railway DB)")
print("=" * 70)

# 챗봇 엔진 초기화
engine = ChatbotEngine(user_id="debug_user")

# 1. 챗봇이 가져오는 공지 확인
print("\n📊 Step 1: _get_recent_notices() 확인")
print("=" * 70)

recent_notices = engine._get_recent_notices(limit=50)
print(f"조회된 공지 수: {len(recent_notices)}개\n")

# 처음 20개만 표시
print("처음 20개 공지:")
for i, notice in enumerate(recent_notices[:20], 1):
    print(f"[{i}] ID:{notice['post_id']} - {notice['title'][:50]} ({notice.get('department', 'N/A')})")

# 2. 컨텍스트 구성 확인
print("\n" + "=" * 70)
print("📝 Step 2: _build_context() 확인")
print("=" * 70)

context = engine._build_context(recent_notices)
print(f"컨텍스트 길이: {len(context)} 문자")
print(f"\n컨텍스트 미리보기 (처음 1000자):")
print(context[:1000])
print("...")

# 3. 키워드로 공지 검색 테스트
print("\n" + "=" * 70)
print("🔍 Step 3: 키워드 검색 테스트")
print("=" * 70)

keywords = ["교육", "연차", "협력업체", "인사평가"]
for keyword in keywords:
    results = engine.search_notices(keyword, limit=3)
    print(f"\n'{keyword}' 검색 결과: {len(results)}개")
    for notice in results:
        print(f"  [{notice['post_id']}] {notice['title']}")

# 4. 실제 챗봇 질의 테스트
print("\n" + "=" * 70)
print("💬 Step 4: 실제 챗봇 ask() 테스트")
print("=" * 70)

test_queries = [
    "교육 일정 알려주세요",
    "연차 관련 안내해주세요",
    "협력업체 관련 공지 보여줘",
]

for query in test_queries:
    print(f"\n질문: {query}")
    print("-" * 70)

    # 컨텍스트에 해당 키워드가 포함되어 있는지 확인
    query_keywords = query.split()
    context_check = []
    for keyword in query_keywords:
        if keyword in context:
            context_check.append(f"✅ '{keyword}' in context")
        else:
            context_check.append(f"❌ '{keyword}' NOT in context")

    print("컨텍스트 키워드 확인:")
    for check in context_check:
        print(f"  {check}")

    # 챗봇 응답
    result = engine.ask(query)
    print(f"\n응답 타입: {result['response_type']}")
    print(f"응답 (처음 200자): {result['response'][:200]}...")
    print(f"참조 공지: {result['notice_refs']}")

print("\n" + "=" * 70)
print("✅ 디버그 완료!")
print("=" * 70)
