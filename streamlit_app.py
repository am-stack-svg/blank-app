import streamlit as st
from datetime import date, datetime
from supabase import create_client
import requests  # 外部Web API用
import random    # ← 追加（ランダム褒め用）

# ====================
# 褒めメッセージ（ご褒美）
# ====================
praise_messages = [
    "🔥 すごい！継続できてるのが一番えらい！",
    "👏 今日もちゃんと積み上げてるね！",
    "🌱 小さな一歩が大きな成長になるよ",
    "💯 自分との約束を守れてるのが最高",
    "🚀 この調子でいこう！"
]

# ====================
# Supabase 接続
# ====================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ====================
# 祝日API（外部Web API）
# ====================
HOLIDAY_API_URL = "https://holidays-jp.github.io/api/v1/date.json"

try:
    holiday_response = requests.get(HOLIDAY_API_URL)
    holidays = holiday_response.json()
except Exception:
    holidays = {}

today = date.today().isoformat()
is_holiday = today in holidays
holiday_name = holidays.get(today, "")

# ====================
# Supabase から学習ログ取得
# ====================
try:
    response = supabase.table("study_logs").select("*").execute()
    study_logs_db = response.data if response.data else []
except Exception:
    study_logs_db = []
    st.warning("⚠️ 学習データを取得できませんでした")

# ====================
# 合計コイン・レベル計算
# ====================
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

if is_holiday:
    st.info(f"🎌 今日は祝日（{holiday_name}）です！祝日ボーナスあり！")

st.divider()

# ====================
# ステータス表示
# ====================
st.subheader("🧑‍🎓 学習進捗状況")
st.write(f"💰 コイン：**{st.session_state.coins} 枚**")
st.write(f"⭐ レベル：**Lv.{st.session_state.level}**")

st.progress(min(st.session_state.coins / 100, 1.0))

st.divider()

# ====================
# 学習入力
# ====================
st.subheader("📘 学習を記録する（1日に何回でもOK）")

study_topic = st.text_input("学習内容")
study_time = st.number_input("学習時間（分）", min_value=0, step=10)

# ====================
# 学習完了ボタン
# ====================
if st.button("✅ 学習完了！"):
    if study_topic == "":
        st.warning("学習内容を入力してください")
    else:
        earned_coins = study_time // 10

        if is_holiday:
            earned_coins += 2

        data = {
            "study_date": date.today().isoformat(),
            "study_time": datetime.now().strftime("%H:%M:%S"),
            "topic": study_topic,
            "minutes": study_time,
            "coins": earned_coins
        }

        try:
            supabase.table("study_logs").insert(data).execute()

            # 🎉 褒めメッセージご褒美
            st.success(random.choice(praise_messages))

            if is_holiday:
                st.info(f"🎌 祝日ボーナス付き！ {earned_coins} コイン獲得！")
            else:
                st.info(f"💰 {earned_coins} コイン獲得！")

            st.rerun()

        except Exception:
            st.error("❌ 学習データの保存に失敗しました")

# ====================
# 今日の学習履歴
# ====================
st.divider()
st.subheader("🗒️ 今日の学習履歴")

today_logs = [
    log for log in st.session_state.study_logs
    if log["study_date"] == today
]

if today_logs:
    for i, log in enumerate(today_logs, 1):
        st.write(
            f"{i}. ⏰ {log['study_time']}｜📘 {log['topic']}｜"
            f"⏱️ {log['minutes']}分｜💰 {log['coins']}コイン"
        )
else:
    st.write("まだ今日の学習記録はありません。")
