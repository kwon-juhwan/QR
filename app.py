import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz
import pandas as pd

# ▶️ 1. Streamlit UI 설정
st.set_page_config(page_title="QR 퇴근 기록", page_icon="🕒")
st.title("🚪 층별 보안점검")

# ▶️ 2. 현재 시간 (Asia/Seoul)
kst = pytz.timezone("Asia/Seoul")
timestamp = datetime.now(kst).strftime("%Y-%m-%d %H:%M:%S")
today_date = datetime.now(kst).strftime("%Y-%m-%d")

# ▶️ 3. 이름 입력
st.subheader("👤 보안점검 대상자 선택")


floor = st.selectbox("🏢 층수를 선택해주세요", ["1층", "2층", "3층", "4층", "5층", "6층"])

# 층별 이름 사전 정의
names_by_floor = {
    "B1층":  [ ],
    "1층": [ ],
    "3층": [ ],
    "4층": ["정영진"],
    "5층": ["권주환", "이재훈", "정유리", "오민성", "최문석", "김주현", "김가영", "김슬기", "김성은", "송정호", "채민석"],
    "6층": ["이유정", "윤소희", "김수진", "안승일"]
}

# ❗️ 여기가 빠져 있었음: 층에 따라 이름 선택 UI 구성
name = st.selectbox("👤 이름을 선택해주세요", names_by_floor.get(floor, []))


# ▶️ 4. Google Sheets 인증 및 열기
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# 현재 날짜를 통해 다른 시트(날짜별 필드) 확장
try:
    sheet = client.open("층별 보안점검 확인").worksheet(today_date)
except gspread.exceptions.WorksheetNotFound:
    sheet = client.open("층별 보안점검 확인").add_worksheet(title=today_date, rows="100", cols="2")
    sheet.append_row(["name", "timestamp"])  # 헤더 추가

# ▶️ 5. 기록 저장 버튼
if st.button("✅ 보안점검 완료"):
    if name:
        sheet.append_row([name, timestamp])
        st.success(f"📝 {name} 님의 기록이 저장되었습니다! ({timestamp})")
    else:
        st.warning("이름을 입력해주세요.")

# ▶️ 6. 오늘 기억 목록 표시
st.markdown("---")
st.header("📋 층별 보안점검 기록")
try:
    data = sheet.get_all_records()
    if data:
        df = pd.DataFrame(data)
        df = df.sort_values(by="timestamp", ascending=False)
        st.dataframe(df)
    else:
        st.info("아직 저장된 기록이 없습니다.")
except Exception as e:
    st.error(f"기록 보기 오류: {e}")
