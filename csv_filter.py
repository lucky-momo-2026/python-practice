import csv
import sys
import sqlite3  #SQLiteを使うために追加
import os #ファイルが存在するか確認するために使用（入力ミス防止）

INPUT_FILE = "data.csv"  #実行中に変えない名前は大文字の定数
OUTPUT_FILE = "pass.csv" 
FAIL_FILE = "fail.csv"  #不合格者を書き出すわいファイル
DB_FILE = "sutudents.db" #SQLiteで使うデータベースファイル名

PASS_SCORE = 60 #ここを変えるだけで合格点が変わる

# ===== 旧実装（接続とテーブル作成を1つにまとめていた）=====
# 今は役割を分ける設計に変更したため未使用
# 理由：処理の流れ（接続→テーブル→INSERT→SELECT）を分かりやすくするため
#def steup_database(db_file):
#    """SQLiteに接続し、学生データを入れるテーブルを作る"""
#    conn = sqlite3.connect(db_file)  #students.dbに接続。なければ自動で作る
#   cursor = conn.cursor()
#    cursor.execute("""
#        CREATE TABLE IF NOT EXISTS students (
#            id INTEGER PRIMARY KEY AUTOINCREMENT,
#            name TEXT,
#            score INTEGER
#        )
#    """)
#    conn.commit()  #テーブル作成を保存
#    conn.close()  #接続を閉じる


def create_students_table(cursor):
    #受験者データを入れるstudentsテーブルを作る/すでに同じ名前のテーブルがある場合は作り直さずそのまま使う
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                   score INTEGER
        )
    """)
    
    #既存のデータを全部削除する（毎回リセット）テーブル作成後に実行することでエラーを防ぐ
    cursor.execute("DELETE FROM students")

def load_and_filter(input_file, output_file, fail_file, pass_score, cursor):  #cursorを追加して使えるようにする
    '''CSVを読み込んで(input_file)合格点以上の者(pass_score)を合格者を書き出す(output_file)'''
    
    pass_rows = []  #合格者を入れる空のリスト
    all_rows = []  #全員を入れる空のリスト（全員の中から最低点を出すために）
#withはdefの中に入るから段落を下げる
    with open(input_file, "r", encoding="utf-8") as f, \
         open(output_file, "w", encoding="utf-8", newline="")as f2, \
         open(fail_file, "w", encoding="utf-8", newline="")as f3:  #fail_fileを書き出すために追加

        reader = csv.DictReader(f, skipinitialspace=True) #skipinitialspace=True　空白があっても書いてる文字で読めるようになる
        writer = csv.DictWriter(f2, fieldnames=reader.fieldnames)

        for row in reader:  #rowは一人分のデータ
            name = row["name"].capitalize() #csv.Dictreaderは列名で読むからrow[0]ではなく["name"]
            score_text = row["score"].strip()  #storip() score列の前後の空白を取り除いてから確認する
            
            #scoreが数字として変換できるか確認する/int()だとvalueErrorだけが出て原因がわかりにくくなるため
            try:
                score = int(score_text)  #確認後に計算できる整数へ変換
            except ValueError:
                print(f"エラー：score が数字ではありません name={name}, score={row['score']}")
                print("対処：data.csv の score列に整数を入れてください")
                return None, None
             
            all_rows.append((name, score))

            #CSVから読んだ一人分のデータをSQLiteのstudentsテーブルに入れる
            cursor.execute(
                "INSERT INTO students (name, score) values (?, ?)",
                (name, score)
            )

        #CVSデータに１件もない時は、この先のSQL集計を止める機能
        if not all_rows:
            print("エラー：data.csv に受験者データがありません")
            print("対策：ヘッダーだけでなく name と score のデータを１件以上入力してください")
            return None, FileNotFoundError
   
   #SQLを使って合格者を取得する(scoreが合格点以上)
    cursor.execute(
       "SELECT name, score FROM students WHERE score >= ?",
       (pass_score,)
   )

    sql_pass_rows = cursor.fetchall()  #SQLで取得した合格者一覧

    #SQLで合格者数を取得する
    cursor.execute(
        "SELECT COUNT(*) FROM students WHERE score >= ?",
        (pass_score,)
    )
    sql_pass_count = cursor.fetchone()[0]  #件数は１つだけ返るので[0] で取り出す

    #SQLで合格者平均点を出す
    cursor.execute(
        "SELECT AVG(score) FROM students WHERE score >= ?",
        (pass_score,)
    )
    sql_pass_avg = cursor.fetchone()[0]  #平均点を１つ取り出す

    #SQLで合格者の最高点を取得する
    cursor.execute(
        """
        SELECT name, score
        FROM students
        WHERE score = (
            SELECT MAX(score) FROM students WHERE score >= ?
        )
        """,
        (pass_score,)
    )
    sql_max_person = cursor.fetchone()  #一人分の(name,score)

    #SQLで合格者の最低点を取得する
    cursor.execute(
        """
        SELECT name, score
        FROM students
        WHERE score = (
            SELECT MIN(score) FROM students WHERE score >= ?
        )
        """,
        (pass_score,)
    )
    sql_min_person =cursor.fetchone()  #一人分の(name,score)取り出す

    #SQLで「最低得点を取った人の名前と点数」を取得する
    cursor.execute(
        """
        SELECT name, score
        From students
        WHERE score = (SELECT MAX(score) FROM students)
    """
    )
    sql_all_max_person = cursor.fetchone()  #一人分取得（name,score)

    #SQLで「最低得点を取った人の名前と点数」を取得する
    cursor.execute(
        """
        SELECT name, score
        FROM students
        WHERE score = (SELECT MIN(score) FROM students)
        """
    )
    sql_all_min_person = cursor.fetchone()  #一人分取得(name,score)

    #SQLで取得した合格者を確認表示する(これでPythonとSQLで確認できる)
    print("【SQLで集計結果】")
    for name, score in sql_pass_rows:
        print(f"{name}:{score}点")

    #SQLで取得した合格者数を確認表示
    print(f"SQL合格者数：{sql_pass_count}人")

    #SQLで取得した不合格者数を確認表示
    sql_fail_count = len(all_rows) - sql_pass_count  #len(all_rows)でcvsから全受験者の人数を出してaql_pass_countで引く
    print(f"SQL不合格者数：{sql_pass_count}人")

    #spl_pass_countを見て合格者が０かどうかを判定
    if sql_pass_count == 0:
        print("SQL合格者平均点：対象なし")
    else:
        print(f"SQL合格者平均点：{sql_pass_avg:.1f}点")  #.1fが小数点１桁表示
    
    #spl_pass_countを見て合格者の最高/最低得点があるかどうかを判定
    if sql_pass_count == 0:
        print("SQL合格者最高点：対象なし")
        print("SQL合格者最低点：対象なし")
    else:
        print(f"SQL合格者最高点：{sql_max_person[1]}点 {sql_max_person[0]}")
        print(f"SQL合格者最低点：{sql_min_person[1]}点 {sql_min_person[0]}") 
    
    #一人いる前提なので必ず結果が返るのでIF文にする必要はない。
    print(f"SQL全受験者最高点：{sql_all_max_person[1]}点 {sql_all_max_person[0]}")
    print(f"SQL全受験者最低点：{sql_all_min_person[1]}点 {sql_all_min_person[0]}")

    return sql_pass_rows, all_rows  #合格者をmain()に渡す/SQL版に切り替え

             
def calc_stats(rows):  #rowsは複数
    '''合格者のリストから平均・最高・採点を計算する'''
    
    if not rows:
        return None  #合格者がいなかったらここで終了
    total = sum(score for _, score in rows)  #for _,は点数を出すとき名前はいらないので_に捨てる
    avg = total / len(rows)  #len(lows)で合格者の人数を取得して平均を計算する
    max_name,max_score = max(rows, key=lambda r: r[1])  #r[1](スコア)を基準に最高得点を出す
    min_name,min_score = min(rows, key=lambda r: r[1])  #r[1](スコア)を基準に合格者の一番低い点を出す
    
    return {  #結果を辞書にまとめてmain()に出す
        "avg": avg,
        "max":(max_name, max_score),
        "min":(min_name, min_score),
        "count":len(rows),
    }
def save_stats(pass_stats, all_stats, output_file="result.csv"):
    '''統計結果をCSVファイルに書く'''
    with open(output_file, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["項目", "値", "氏名"])  #ヘッダー

        if pass_stats:
            writer.writerow(["合格者平均点", f'{pass_stats["avg"]:.1f}', ""])  #:1fは小数点１桁で表示する　""は平均に氏名はつかないので空欄
            writer.writerow(["合格者最高点", pass_stats["max"][1], pass_stats["max"][0]])
            writer.writerow(["合格者最低点", pass_stats["min"][1], pass_stats["min"][0]])
        else:
            writer.writerow(["合格者", "データなし", ""])

        if all_stats:
            writer.writerow(["全受験者最低点", all_stats["min"][1], all_stats["min"][0]])
def main():
    #処理を開始する前に、指定したCSVファイルが存在するか確認する(事前に検知してわかりやすくするため)
    if not os.path.exists(INPUT_FILE):
        print(f"エラー：入力ファイル '{INPUT_FILE}'が見つかりません")
        print("原因：CSVファイルが存在しない、またはファイル名が違います")
        print("対処：csv_filter.py と同じフォルダに data.csv を置いてください")
        return  #これ以上処理を進めない（安全に終了）

    #SQLiteデータベースに接続（DB_FILEは上で定義たデータベースの名前）
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    #受験者データを入れるstudentsテーブルを作る
    create_students_table(cursor)

    #SQLiteへの接続が成功したか確認するために表示する
    print("SQLiteデータベースに接続しました")

    '''コマンドラインから合格点を受け取って実行時に数字を指定できる。指定がなければデフォルトの数字（pass_score=60）を使う'''
    if len(sys.argv) > 1:   #pass_score = int(sys.argv[1]) #指定の数字を使うという指示   
        pass_score = int(sys.argv[1])  #実行時に入力した数字を合格点として使う
    else:
        pass_score = PASS_SCORE #指定がなければデフォルトの数字
    
    pass_rows, all_rows = load_and_filter(INPUT_FILE, OUTPUT_FILE, FAIL_FILE, pass_score, cursor)  #合格者と全員のリストを同時に出す/cursorでも出せるようにする
    
    # load_and_filterでエラーがあった場合はNoneが返るのでここで止める
    if pass_rows is None or all_rows is None:
        conn.close() #DBを開いたままにしないため閉じる
        return

    #テーブル作成をSQLiteに保存する
    conn.commit()
    conn.close()

    print("【合格者一覧】")
    for name, score in pass_rows:  #pass_rowから１人ぶんずつ取り出して表示
        print(f"{name}:{score}点")

    stats = calc_stats(pass_rows)  #calc_stats()を呼び出して結果をstatsで受け取る
    all_stats = calc_stats(all_rows)  #全員の統計

    print("【統計情報】")
    #if文から出すことで、合格者が0でも受験者数は必ず出るようにする。
    print(f"受験者数：{all_stats["count"]}人")  #all_statsからcountで人数を計算
    
    #合格者数
    if stats:  #合格者数の後に不合格者数を取り出したいので、ifを分ける
        print(f"合格者数：{stats["count"]}人")  #statsからcountdeで人数計算
    else:
        print("合格者数：0人")
    
    #不合格者数
    fail_count = all_stats["count"] - (stats["count"] if stats else 0)
    print(f"不合格者数：{fail_count}人")
    
    #統計
    if stats:
        print(f"平均：{stats["avg"]}点")
        print(f"合格最高点：{stats["max"][1]}点 {stats["max"][0]}")
        print(f"合格最低点：{stats["min"][1]}点 {stats["min"][0]}")
    else:  #合格者0人の時統計が空欄にならない対策。
        print("平均：対象者なし")
        print("合格最高点：対象なし")
        print("合格最低点：対象なし")

    if all_stats:
            print(f"全受験者最高点：{all_stats["max"][1]}点 {all_stats["max"][0]}")
            print(f"全受験者最低点：{all_stats["min"][1]}点 {all_stats["min"][0]}")
    save_stats(stats, all_stats)

    print("result.csvに統計を書き出しました")
    print("fail.csvに不合格者を書き出しました")

main()  #main()を呼び出してプログラムスタート
