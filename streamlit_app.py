import streamlit as st
from datetime import date

# タイトル
st.title("学習効率化アプリ")
st.write("学習内容を記録し、振り返ることで効率的に学習を進めることを目的としたアプリです。")

st.divider()

# 日付
today = date.today()
st.write(f"📅 日付：{today}")

# 学習内容入力
study_topic = st.text_input("① 今日の学習内容を入力してください")

# 学習時間
study_time = st.number_input(
    "② 学習時間（分）",
    min_value=0,
    step=10
)

# 理解度
understanding = st.slider(
    "③ 理解度（1〜5）",
    1, 5, 3
)

# 振り返り
reflection = st.text_area("④ 学習の振り返り・気づいたこと")

# 保存ボタン
if st.button("記録する"):
    if study_topic == "":
        st.warning("学習内容を入力してください。")
    else:
        st.success("学習記録を保存しました！")

        st.subheader("📘 今日の学習記録")
        st.write(f"**学習内容**：{study_topic}")
        st.write(f"**学習時間**：{study_time} 分")
        st.write(f"**理解度**：{understanding} / 5")
        st.write(f"**振り返り**：{reflection}")

