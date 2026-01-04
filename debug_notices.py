#!/usr/bin/env python3
"""
챗봇이 조회하는 공지사항 디버깅
"""
from core.chatbot_engine import ChatbotEngine

print("=" * 70)
print("🔍 챗봇 공지사항 조회 디버깅")
print("=" * 70)

# 챗봇 엔진 초기화
engine = ChatbotEngine(user_id="test_user")

# 최근 공지 조회
print("\n📊 최근 공지 50개 조회 중...")
notices = engine._get_recent_notices(limit=50)

print(f"\n✅ 조회된 공지: {len(notices)}개\n")

# 처음 20개 공지 표시
for i, notice in enumerate(notices[:20], 1):
    print(f"[{i}] ID: {notice['post_id']}")
    print(f"    제목: {notice['title']}")
    print(f"    부서: {notice.get('department', 'N/A')}")
    print(f"    날짜: {notice.get('date', 'N/A')}")
    print()

# 부서별 분류
departments = {}
for notice in notices:
    dept = notice.get('department', '미분류')
    if dept not in departments:
        departments[dept] = 0
    departments[dept] += 1

print("\n" + "=" * 70)
print("📊 부서별 공지 분류")
print("=" * 70)
for dept, count in sorted(departments.items(), key=lambda x: x[1], reverse=True):
    print(f"{dept}: {count}개")

# 키워드 검색 테스트
print("\n" + "=" * 70)
print("🔍 키워드 검색 테스트")
print("=" * 70)

keywords = ["인사평가", "연말정산", "재택근무", "VPN"]
for keyword in keywords:
    results = engine.search_notices(keyword, limit=5)
    print(f"\n'{keyword}' 검색 결과: {len(results)}개")
    for i, notice in enumerate(results, 1):
        print(f"  [{i}] {notice['title']} (부서: {notice.get('department', 'N/A')})")

print("\n" + "=" * 70)
print("✅ 디버깅 완료!")
print("=" * 70)
