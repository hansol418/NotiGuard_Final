#!/usr/bin/env python3
"""
공지사항 정렬 순서 확인 및 "연차" 공지 위치 찾기
"""
import os
from dotenv import load_dotenv
from core.chatbot_engine import ChatbotEngine

load_dotenv()

# Railway DB 사용
os.environ["DATABASE_URL"] = "postgresql://postgres:EUxzTKqEvybegsaRhWsySxVcgCRvyZHA@mainline.proxy.rlwy.net:47312/railway"

print("=" * 70)
print("🔍 공지사항 정렬 순서 및 '연차' 공지 위치 확인")
print("=" * 70)

engine = ChatbotEngine(user_id="debug_user")

# 모든 공지 조회 (limit을 크게 설정)
all_notices = engine._get_recent_notices(limit=100)

print(f"\n총 조회된 공지: {len(all_notices)}개\n")

# "연차" 키워드가 포함된 공지 찾기
print("=" * 70)
print("📌 '연차' 관련 공지 위치")
print("=" * 70)

for idx, notice in enumerate(all_notices, 1):
    if '연차' in notice['title'] or '연차' in notice['content']:
        print(f"[{idx}번째] ID:{notice['post_id']} - {notice['title']}")
        print(f"  부서: {notice.get('department', 'N/A')}")
        print(f"  날짜: {notice.get('date', 'N/A')}")
        print()

# 50번째 전후 공지 확인
print("=" * 70)
print("📊 45~55번째 공지 (50개 범위 경계)")
print("=" * 70)

for idx in range(44, min(55, len(all_notices))):
    notice = all_notices[idx]
    marker = "⚠️  50개 LIMIT" if idx == 49 else "  "
    print(f"{marker} [{idx+1}] ID:{notice['post_id']} - {notice['title'][:40]} (날짜: {notice.get('date', 'N/A')})")

print("\n" + "=" * 70)
print("💡 분석")
print("=" * 70)
print(f"현재 limit: 50개")
print(f"전체 공지: {len(all_notices)}개")

# 연차 공지가 50개 안에 있는지 확인
연차_in_50 = any('연차' in n['title'] or '연차' in n['content'] for n in all_notices[:50])
print(f"'연차' 공지가 최근 50개에 포함: {'✅ YES' if 연차_in_50 else '❌ NO'}")

if not 연차_in_50:
    print("\n⚠️  해결방법: limit을 60개 이상으로 증가시켜야 합니다!")
