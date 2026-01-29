import streamlit as st
from datetime import date, datetime
from supabase import create_client
import requests  # 外部Web API用

# ====================
# Supabase 接続
# ====================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ====================
# 祝日API（外部Web API）【← try-except はここ】
# ====================
HOLIDAY_API_URL = "https://holidays-jp.github.io/api/v1/date.json"

try:
    res = requests.get(HOLIDAY_API_URL, timeout=5)
    holidays = res.json()   # 成功時：祝日データ取得
except:
    holidays = {}           # 失敗時：空にしてアプリ継続

today = date.today().isoformat()
is_holiday = today in holidays
holiday_name = holidays.get(today, "")

# ====================
# Supabase から学習ログ取得
# ====================
response = supabase.table("study_logs").select("*").execute()
study_logs_db = response.data if response.data else []

total_coins = sum(log["coins"] for log in study_logs_db)
level = total_coins // 50 + 1

st.session_state.coins = total_coins
st.session_state.level = level
st.session_state.study_logs = study_logs_db

# ====================
# タイトル
# ====================
st.title("🎮 学習継続アプリ")
st.write("学習をゲーム感覚で進め、何度でも記録してコインを集めよう！")

# 祝日表示
if is_holiday:
    st.info(f"🎌 今日は祝日（{holiday_name}）です！祝日ボーナスあり！")

st.divider()

# ====================
# ステータス
# ====================
st.subheader("🧑‍🎓 学習進捗状況")
st.write(f"💰 コイン：**{st.session_state.coins} 枚**")
st.write(f"⭐ レベル：**Lv.{st.session_state.level}**")

st.progress(min(st.session_state.coins / 100, 1.0))

# ====================
# 学習入力
# ====================
st.subheader("📘 学習を記録する")

study_topic = st.text_input("学習内容")
study_time = st.number_input("学習時間（分）", min_value=0, step=10)

if st.button("✅ 学習完了！"):
    if study_topic == "":
        st.warning("学習内容を入力してください")
    else:
        earned_coins = study_time // 10

        if is_holiday:
            earned_coins += 2  # 祝日ボーナス

        data = {
            "study_date": today,
            "study_time": datetime.now().strftime("%H:%M:%S"),
            "topic": study_topic,
            "minutes": study_time,
            "coins": earned_coins
        }

        supabase.table("study_logs").insert(data).execute()
        st.success(f"🎉 {earned_coins} コイン獲得！")
        st.rerun()
