# 📊 CSV Score Filter

学生の試験スコアを読み込み、合格者の抽出と統計集計をするPythonスクリプトです。

---

## 💡 できること

- CSVファイルから学生データを読み込む
- 合格点以上の学生を `pass.csv` に書き出す
- 合格者の平均・最高・最低点を集計する
- 全受験者の最低点を集計する
- 統計結果を `result.csv` に書き出す
- 実行時に合格点をコマンドラインから指定できる
- 不合格者を `fail.csv` に書き出す
- 受験者数と合格者数を集計する

---

## 🗂️ ファイル構成

```
python-practice/
├── csv_filter.py   # メインスクリプト
├── data.csv        # 入力データ（学生名・スコア）
├── pass.csv        # 出力：合格者一覧
└── result.csv      # 出力：統計結果
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