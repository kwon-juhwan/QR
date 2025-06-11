import streamlit as st
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pytz

# 페이지 설정
st.set_page_config(page_title="QR 퇴근 기록", page_icon="🕒")
st.title("🚪 퇴근 확인")

# 현재 시각 (한국 시간 기준)
timestamp = datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")

# 이름 입력
name = st.text_input("👤 층수_이름을 입력해주세요")

# Google Sheets 인증
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds_dict = st.secrets["gcp_service_account"]
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Google Sheet 열기 (시트명은 직접 변경 가능)
sheet = client.open('층별 보안점검 확인').sheet1

# 버튼 클릭 시 기록 저장
if st.button("✅ 출퇴근 기록 남기기"):
    if name:
        sheet.append_row([name, timestamp])
        st.success(f"📝 {name} 님의 기록이 저장되었습니다! ({timestamp})")
    else:
        st.warning("이름을 입력해주세요.")

# 기록 조회 영역
st.markdown("---")
st.header("📋 퇴근 기록 (Google Sheets 연동)")

try:
    data = sheet.get_all_records()
    if data:
        import pandas as pd
        df = pd.DataFrame(data)
        df = df.sort_values(by="timestamp", ascending=False)
        st.dataframe(df)
    else:
        st.info("아직 저장된 기록이 없습니다.")
except Exception as e:
    st.error(f"기록을 불러오는 중 오류 발생: {e}")
