import streamlit as st
from urllib.parse import parse_qs, urlparse
from datetime import datetime
import pandas as pd
import os

LOG_FILE = "log.csv"

# URL 쿼리 파라미터에서 id 추출
query_params = st.experimental_get_query_params()
user_id = query_params.get("id", [None])[0]

# 현재 시각
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# 로그 저장 함수
def log_access(user_id, timestamp):
    if not user_id:
        return
    log_data = {"id": user_id, "timestamp": timestamp}
    df = pd.DataFrame([log_data])

    if os.path.exists(LOG_FILE):
        df_existing = pd.read_csv(LOG_FILE)
        df = pd.concat([df_existing, df], ignore_index=True)

    df.to_csv(LOG_FILE, index=False)

# 기록 저장 시도
if user_id:
    log_access(user_id, timestamp)
    st.success(f"✅ 접속 기록 저장 완료: {user_id} / {timestamp}")
else:
    st.warning("📭 QR 코드 또는 유효한 id 파라미터가 필요합니다.")

# 관리자용 로그 보기
st.markdown("---")
st.header("📋 스캔 기록 보기 (관리자용)")

if os.path.exists(LOG_FILE):
    df_log = pd.read_csv(LOG_FILE)
    st.dataframe(df_log)
else:
    st.info("아직 저장된 로그가 없습니다.")
