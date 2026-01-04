#!/usr/bin/env python3
"""
새로 추가된 공지사항 검색 테스트
"""
from core.chatbot_engine import ChatbotEngine

print("=" * 70)
print("🔍 신규 공지사항 검색 테스트")
print("=" * 70)

# 챗봇 엔진 초기화
engine = ChatbotEngine(user_id="test_user")

# 새로 추가된 공지사항 관련 질문들
test_queries = [
    "인사평가 일정 알려주세요",
    "연말정산은 언제인가요?",
    "재택근무 규정이 어떻게 되나요?",
    "설 명절 귀향 여비 지급 안내",
    "AI 세미나 일정 알려줘",
]

for i, query in enumerate(test_queries, 1):
    print(f"\n{'='*70}")
    print(f"[테스트 {i}] 질문: {query}")
    print(f"{'='*70}")

    try:
        result = engine.ask(query)

        print(f"\n✅ 응답 성공!")
        print(f"\n📝 응답:")
        print(f"{result['response'][:500]}...")  # 처음 500자만 표시
        print(f"\n📊 메타데이터:")
        print(f"   - 응답 타입: {result['response_type']}")
        print(f"   - 참조 공지: {len(result['notice_refs'])}개")
        if result['notice_refs']:
            print(f"   - 공지 ID: {result['notice_refs']}")

    except Exception as e:
        print(f"\n❌ 에러 발생: {str(e)}")
        import traceback
        traceback.print_exc()

print(f"\n{'='*70}")
print(f"✅ 테스트 완료!")
print(f"{'='*70}")
