#!/usr/bin/env python3
"""
챗봇 UX 개선 테스트
- 세션 요약 기능
- 개선된 시스템 프롬프트
"""
from core.chatbot_engine import ChatbotEngine

print("=" * 70)
print("🤖 챗봇 UX 개선 테스트")
print("=" * 70)

# 챗봇 엔진 초기화
engine = ChatbotEngine(user_id="test_user")

# 1. 세션 요약 테스트
print("\n📝 세션 요약 기능 테스트")
print("=" * 70)

test_queries = [
    "이번 주 안전교육 일정 알려줘",
    "인사평가 일정은 언제인가요?",
    "연말정산 관련 안내해주세요",
    "재택근무 규정이 어떻게 되나요?",
    "VPN 접속 방법 알려줘",
]

for query in test_queries:
    summary = engine.summarize_query(query)
    print(f"질문: {query}")
    print(f"요약: {summary} (길이: {len(summary)}자)")
    print()

# 2. 챗봇 응답 테스트 (개선된 프롬프트)
print("\n" + "=" * 70)
print("💬 개선된 프롬프트 응답 테스트")
print("=" * 70)

test_question = "인사평가 일정 알려주세요"
print(f"\n질문: {test_question}\n")

result = engine.ask(test_question)

print(f"✅ 응답 타입: {result['response_type']}")
print(f"\n📝 응답:\n{result['response']}")
print(f"\n📎 참조 공지: {result['notice_refs']}")
print(f"🔑 키워드: {result['keywords']}")

# 응답에 "다른 질문 있으신가요?" 같은 문구가 있는지 확인
closing_phrases = ["다른 질문", "예시 질문", "더 궁금", "추가로"]
has_closing = any(phrase in result['response'] for phrase in closing_phrases)

if has_closing and result['response_type'] == 'NORMAL':
    print("\n⚠️  경고: 일반 응답에 불필요한 종료 멘트가 포함되어 있습니다!")
else:
    print("\n✅ 응답 형식 검증 통과!")

print("\n" + "=" * 70)
print("✅ 테스트 완료!")
print("=" * 70)
