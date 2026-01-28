import streamlit as st
from datetime import date, datetime
from supabase import create_client

supabase = create_client(
    st.secrets["SUPABASE_URL"],
    st.secrets["SUPABASE_KEY"]
)
# ====================
# 初期化
# ====================
if "coins" not in st.session_state:
    st.session_state.coins = 0

if "level" not in st.session_state:
    st.session_state.level = 1

if "study_logs" not in st.session_state:
    st.session_state.study_logs = []  # 学習履歴を保存

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
# 学習完了ボタン
# ====================
if st.button("✅ 学習完了！"):
    if study_topic == "":
        st.warning("学習内容を入力してください")
    else:
        # 獲得コイン計算（10分 = 1コイン）
        earned_coins = study_time // 10
        st.session_state.coins += earned_coins

        # レベル更新
        st.session_state.level = st.session_state.coins // 50 + 1

        # 学習履歴を保存
        st.session_state.study_logs.append({
            "date": date.today(),
            "time": datetime.now().strftime("%H:%M"),
            "topic": study_topic,
            "minutes": study_time,
            "coins": earned_coins
        })

        st.success(f"🎉 学習完了！ {earned_coins} コイン獲得！")

# ====================
# 今日の学習履歴
# ====================
st.divider()
st.subheader("🗒️ 今日の学習履歴")

today_logs = [
    log for log in st.session_state.study_logs
    if log["date"] == date.today()
]

if today_logs:
    for i, log in enumerate(today_logs, 1):
        st.write(
            f"{i}. ⏰ {log['time']}｜📘 {log['topic']}｜⏱️ {log['minutes']}分｜💰 {log['coins']}コイン"
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
# 設定（リセット）
# ====================
with st.expander("⚙️ 設定"):
    if st.button("すべてリセット"):
        st.session_state.coins = 0
        st.session_state.level = 1
        st.session_state.study_logs = []
        st.success("データをリセットしました")


st.divider()
st.subheader("🔌 Supabase 接続テスト")

if st.button("テストで1件保存"):
    data = {
        "study_date": date.today().isoformat(),              # ← 文字列に
        "study_time": datetime.now().strftime("%H:%M:%S"),   # ← 文字列に
        "topic": "テスト",
        "minutes": 30,
        "coins": 3
    }

    result = supabase.table("study_logs").insert(data).execute()
    st.write(result)

