# 📊 CSV Score Filter（SQLite版）

学生の試験スコアをCSVから読み込み、  
**SQLiteを使って合格者抽出/統計集計/CSV出力までを行うPythonスクリプト**です。

Pythonの `if` による単純な抽出ではなく、  
**SQLの `WHERE` 句や集計関数（COUNT / AVG / MAX / MIN）を使って処理する構成**にすることで、  
データ処理とSQLの基礎をまとめて学べる作品として仕上げました。

---

## 💡 この作品でできること

- CSVファイルから学生データを読み込む
- SQLiteデータベースにデータを登録する
- SQL（`WHERE` 句）を使って合格者を抽出する
- SQLで合格者数・平均点・最高点・最低点を集計する
- 合格者を `pass.csv` に書き出す
- 不合格者を `fail.csv` に書き出す
- 統計結果を `result.csv` に書き出す
- 実行時に合格点をコマンドライン引数で変更できる
- 空データ・不正データ・合格者0人のケースでも安全に動作する

---

## 🧠 この作品の工夫ポイント

### 1. PythonのifではなくSQLで合格者を抽出
合格判定をPython側で分岐するのではなく、  
SQLの `WHERE score >= ?` を使って抽出しています。

### 2. 集計処理もSQLで実装
合格者数・平均点・最高点・最低点は、Pythonで手計算するのではなく、  
SQLの集計関数を使って処理しています。

- `COUNT(*)`
- `AVG(score)`
- `MAX(score)`
- `MIN(score)`

### 3. SQLiteを使った基本的なデータ処理の流れを実装
この作品では、以下の流れを1本のスクリプトで実装しています。

1. CSVを読み込む  
2. SQLiteへ登録する  
3. SQLで抽出する  
4. SQLで集計する  
5. CSVへ結果を書き出す  

### 4. エラー処理を入れて実務寄りに調整
以下のケースでもエラーで止まりっぱなしにならないようにしています。

- 入力ファイルが存在しない
- `score` が数値でない
- CSVに受験者データがない
- 合格者が0人で平均点や最高点が出せない

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
sato,50
```

---

## 📄 出力ファイルの形式

### pass.csv（合格者一覧）

```
name,score
Suzuki,80
Saitou,90
```
### fail.csv（不合格者一覧）

```
name,score
Tanaka,45
Sato,50
```


### result.csv（統計結果）

```
項目,値,氏名
受験者数,4,
合格者数,2,
不合格者数,2,
合格者平均点,85.0,
合格最高点,90,Saitou
合格最低点,80,Suzuki
全受験者最高点,90,Saitou
全受験者最低点,45,Tanaka
```

---

## 🛠️ 動作環境

- Python 3.13以上
- 標準ライブラリのみ使用（追加インストール不要）

---

## 👩‍💻 作者

GitHub: [lucky-momo-2026](https://github.com/lucky-momo-2026)