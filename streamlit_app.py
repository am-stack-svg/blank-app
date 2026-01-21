import streamlit as st
from datetime import date

# --------------------
# 初期設定（コイン管理）
# --------------------
if "coins" not in st.session_state:
    st.session_state.coins = 0

if "level" not in st.session_state:
    st.session_state.level = 1

# --------------------
# タイトル
# --------------------
st.title("🎮 学習ゲーミフィケーションアプリ")
st.write("学習をゲーム感覚で進め、コインを集めてご褒美を獲得しよう！")

st.divider()

# --------------------
# ステータス表示
# --------------------
st.subheader("🧑‍🎓 プレイヤーステータス")
st.write(f"💰 コイン：**{st.session_state.coins} 枚**")
st.write(f"⭐ レベル：**Lv.{st.session_state.level}**")

st.progress(min(st.session_state.coins / 100, 1.0))

st.divider()

# --------------------
# 学習入力
# --------------------
st.subheader("📘 今日の学習")

study_topic = st.text_input("学習内容")
study_time = st.number_input("学習時間（分）", min_value=0, step=10)

# --------------------
# 学習完了ボタン
# --------------------
if st.button("✅ 学習完了！"):
    if study_topic == "":
        st.warning("学習内容を入力してください")
    else:
        # コイン計算
        earned_coins = study_time // 10  # 10分 = 1コイン
        st.session_state.coins += earned_coins

        # レベルアップ判定
        st.session_state.level = st.session_state.coins // 50 + 1

        st.success(f"🎉 学習完了！ {earned_coins} コイン獲得！")

# --------------------
# ご褒美システム
# --------------------
st.divider()
st.subheader("🎁 ご褒美")

if st.session_state.coins >= 100:
    st.success("🏆 ご褒美獲得！")
    st.write("・好きなお菓子を1つ食べてOK")
    st.write("・10分休憩してもOK")
elif st.session_state.coins >= 50:
    st.info("🔓 次のご褒美まであと少し！")
    st.write("50コイン達成：好きな動画を1本見る")
else:
    st.write("まだご褒美はありません。学習を進めよう！")

# --------------------
# リセット（デバッグ用）
# --------------------
with st.expander("⚙️ 設定"):
    if st.button("コインをリセット"):
        st.session_state.coins = 0
        st.session_state.level = 1
        st.success("リセットしました")
