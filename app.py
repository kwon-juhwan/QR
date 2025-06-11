import streamlit as st
from datetime import datetime
from urllib.parse import parse_qs
import pytz
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials


st.set_page_config(page_title="QR 퇴근 기록", page_icon="🕒")
st.title("🚪 퇴근 확인")

LOG_FILE = "log.csv"

# 이름 입력
name = st.text_input("👤 층수_이름을 입력해주세요")

# 현재 시각
timestamp = datetime.now(pytz.timezone("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")

# 기록 저장 함수
def save_log(name, timestamp):
    log_data = {"name": name, "timestamp": timestamp}
    df = pd.DataFrame([log_data])
    
    if os.path.exists(LOG_FILE):
        df_existing = pd.read_csv(LOG_FILE)
        df = pd.concat([df_existing, df], ignore_index=True)
    
    df.to_csv(LOG_FILE, index=False)

# 버튼으로 기록 저장
if st.button("✅ 출퇴근 기록 남기기"):
    if name:
        save_log(name, timestamp)
        st.success(f"📝 {name} 님의 기록이 저장되었습니다! ({timestamp})")
    else:
        st.warning("이름을 입력해주세요.")

# 기록 조회 영역
st.markdown("---")
st.header("📋 퇴근 기록")

if os.path.exists(LOG_FILE):
    df_log = pd.read_csv(LOG_FILE)
    df_log = df_log.sort_values(by="timestamp", ascending=False)
    st.dataframe(df_log)
    
    # 다운로드 버튼
    csv = df_log.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📥 CSV 다운로드", csv, file_name="scan_log.csv", mime="text/csv")
else:
    st.info("아직 저장된 로그가 없습니다.")


# Google Sheets 인증 설정
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('keyword-456501-6844a82c52d0.json', scope)
client = gspread.authorize(creds)

# Google Sheets 열기
sheet = client.open('층별 보안점검 확인').sheet1

# 사용자 입력 받기
st.title("QR 코드 스캔 기록")
name = st.text_input("이름을 입력하세요:")
if st.button("기록 저장"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sheet.append_row([name, timestamp])
    st.success("기록이 저장되었습니다.")
