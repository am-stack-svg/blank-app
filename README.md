# 🎮 学習継続アプリ（Study Coin App）

学習を「ゲーム感覚」で継続できるようにするための Web アプリです。  
学習内容と時間を記録するとコインがもらえ、学習のモチベーション維持を目的としています。

---

## 🚀 アプリのURL（誰でも試せます）

👉 https://（ここにStreamlit CloudのURLを貼る）

※ 他人のブラウザからアクセスできることを確認済み

---

## ✨ 主な機能

- 📘 学習内容・学習時間を何回でも記録可能
- 💰 学習時間に応じてコインを獲得
- ⭐ コイン数に応じてレベル表示
- 🗒️ 今日の学習履歴を一覧表示
- ☁ Supabase を使って学習データを永続保存  
  （ページを再読み込みしてもデータが消えない）

---

## 🛠 使用技術

- **Python**
- **Streamlit**（UI作成）
- **Supabase**（データベース）
- **GitHub**
- **Streamlit Cloud**（デプロイ）

---

## 🤖 AI（ChatGPT）の活用方法

- Streamlit と Supabase を連携するコードの生成
- エラー発生時の原因特定と修正方法の提案
- データベース設計（テーブル構成）の相談
- README.md の構成案作成

AIには  
「初心者向けに」「なぜそのエラーが出るのか理由も説明して」  
といった形で具体的に指示しました。

---

## 😣 大変だった点と解決方法

### Supabase が接続できなかった
- `ModuleNotFoundError: supabase` が発生
- 👉 `requirements.txt` に `supabase` を追加して解決

### コインやレベルが保存されなかった
- 表示はされるが、再読み込みでリセットされてしまった
- 👉 学習ログを Supabase に保存し、合計値を毎回計算する方式に変更

---

## 📂 実行方法（ローカルで動かす場合）

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
