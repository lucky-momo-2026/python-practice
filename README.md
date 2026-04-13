# 📊 CSV Score Filter（SQLite版）

学生の試験スコアをCSVから読み込み、  
**SQLiteを使って合格者の抽出と統計集計を行うPythonスクリプト**です。

---

## 💡 できること

- CSVファイルから学生データを読み込む
- SQLiteデータベースにデータを登録する
- SQL（WHERE句）を使って合格者を抽出する
- SQLで合格者数・平均・最高・最低点を集計する（COUNT / AVG / MAX / MIN）
- 合格者を `pass.csv` に書き出す
- 不合格者を `fail.csv` に書き出す
- 統計結果を `result.csv` に書き出す
- 実行時に合格点をコマンドラインから指定できる

---

## 🧠 技術ポイント（就職用）

- Pythonの条件分岐（if）ではなく、SQLの `WHERE` 句で合格者抽出を実装
- 集計処理をPythonからSQLへ移行
- SQLiteを使ったデータ処理の基本構成を理解
  - INSERT（データ登録）
  - SELECT（抽出）
  - WHERE（条件）
  - COUNT / AVG / MAX / MIN（集計）

---

## 🗂️ ファイル構成

```
python-practice/
├── csv_filter.py # メインスクリプト
├── data.csv # 入力データ（学生名・スコア）
├── pass.csv # 出力：合格者一覧
├── fail.csv # 出力：不合格者一覧
├── result.csv # 出力：統計結果
└── students.db # SQLiteデータベース
```

---

## ▶️ 使い方

### 基本の実行（合格点：デフォルト60点）

```bash
python csv_filter.py
```

### 合格点を指定して実行

```bash
python csv_filter.py 70
```

---

## 📄 入力ファイルの形式（data.csv）

```
name,score
suzuki,80
saitou,90
tanaka,45
```

---

## 📄 出力ファイルの形式

### pass.csv（合格者一覧）

```
name,score
Suzuki,80
Saitou,90
```

### result.csv（統計結果）

```
項目,値,氏名
合格者平均点,85.0,
合格者最高点,90,Saitou
合格者最低点,80,Suzuki
全受験者最低点,45,Tanaka
```

---

## 🛠️ 動作環境

- Python 3.13以上
- 標準ライブラリのみ使用（追加インストール不要）

---

## 👩‍💻 作者

GitHub: [lucky-momo-2026](https://github.com/lucky-momo-2026)