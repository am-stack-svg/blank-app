import streamlit as st
from datetime import date, datetime
from supabase import create_client

# ====================
# Supabase 接続
# ====================
supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)

# ====================
# Supabase から学習ログ取得（永続化の核心）
# ====================
response = supabase.table("study_logs").select("*").execute()
study_logs_db = response.data if response.data else []

# 合計コイン・レベルを再計算
total_coins = sum(log["coins"] for log in study_logs_db)
level = total_coins // 50 + 1

# session_state に反映
st.session_state.coins = total_coins
st.session_state.level = level
st.session_state.study_logs = study_logs_db

# ====================
# タイトル
# ====================
st.title("🎮 学習継続アプリ")
st.write("学習をゲーム感覚で進め、何度でも記録してコインを集めよう！")

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
# 学習完了ボタン（Supabaseに保存）
# ====================
if st.button("✅ 学習完了！"):
    if study_topic == "":
        st.warning("学習内容を入力してください")
    else:
        earned_coins = study_time // 10

        data = {
            "study_date": date.today().isoformat(),
            "study_time": datetime.now().strftime("%H:%M:%S"),
            "topic": study_topic,
            "minutes": study_time,
            "coins": earned_coins
        }

        supabase.table("study_logs").insert(data).execute()
        st.success(f"🎉 学習完了！ {earned_coins} コイン獲得！")

        # 再読み込みして最新状態を反映
        st.rerun()

# ====================
# 今日の学習履歴
# ====================
st.divider()
st.subheader("🗒️ 今日の学習履歴")

today = date.today().isoformat()
today_logs = [log for log in st.session_state.study_logs if log["study_date"] == today]

if today_logs:
    for i, log in enumerate(today_logs, 1):
        st.write(
            f"{i}. ⏰ {log['study_time']}｜📘 {log['topic']}｜"
            f"⏱️ {log['minutes']}分｜💰 {log['coins']}コイン"
        )
else:
    st.write("まだ今日の学習記録はありません。")

# ====================
# ご褒美システム
# ====================
st.divider()
st.subheader("🎁 ご褒美")

if st.session_state.coins >= 100:
    st.success("🏆 ご褒美獲得！")
    st.write("・好きなお菓子を1つ食べてOK")
    st.write("・10分休憩してもOK")
elif st.session_state.coins >= 50:
    st.info("🔓 ご褒美まであと少し！")
    st.write("50コイン達成：好きな動画を1本見る")
else:
    st.write("まだご褒美はありません。学習を続けよう！")

# ====================
# 設定（全削除）
# ====================
with st.expander("⚙️ 設定"):
    if st.button("すべてリセット（DB含む）"):
        supabase.table("study_logs").delete().neq("id", 0).execute()
        st.success("すべての学習データを削除しました")
        st.rerun()
