import csv
import sys
import sqlite3  #SQLiteを使うために追加

INPUT_FILE = "data.csv"  #実行中に変えない名前は大文字の定数
OUTPUT_FILE = "pass.csv" 
FAIL_FILE = "fail.csv"  #不合格者を書き出すわいファイル

PASS_SCORE = 60 #ここを変えるだけで合格点が変わる

def load_and_filter(input_file, output_file, fail_file, pass_score):
    '''CSVを読み込んで(input_file)合格点以上の者(pass_score)を合格者を書き出す(output_file)'''

    pass_rows = []  #合格者を入れる空のリスト
    all_rows = []  #全員を入れる空のリスト（全員の中から最低点を出すために）
#withはdefの中に入るから段落を下げる
    with open(input_file, "r", encoding="utf-8") as f, \
         open(output_file, "w", encoding="utf-8", newline="")as f2, \
         open(fail_file, "w", encoding="utf-8", newline="")as f3:  #fail_fileを書き出すために追加

<<<<<<< HEAD
        reader = csv.DictReader(f) #next(reader)で飛ばす必要がない。DictReaderが１行目を列名として使う
        writer = csv.DictWriter(f2, fieldnames=reader.fieldnames)

        for row in reader:  #rowは一人分のデータ
            name = row["name"].capitalize() #.capitalize()は一文字目を大文字それ以降小文字
=======
        reader = csv.DictReader(f, skipinitialspace=True) #skipinitialspace=True　空白があっても書いてる文字で読めるようになる
        writer = csv.DictWriter(f2, fieldnames=reader.fieldnames)

        for row in reader:  #rowは一人分のデータ
            name = row["name"].capitalize() #csv.Dictreaderは列名で読むからrow[0]ではなく["name"]
>>>>>>> ab07412 (DictReader/DictWriter修正でCSV処理復旧)
            score = int(row["score"])  #CSVからとった文字を計算できる数字に変換
            all_rows.append((name, score))

            if score >= pass_score:  #スコアがパススコアより低かったら
                writer.writerow({"name": name,"score":score})  #skipinitialspaceを入れたので"name"の列はname,"score"の列はscoreに変更,[]はリストなのでエラー表示でる
                pass_rows.append((name, score))  #()は後から変更できない/ここでは一度入れたデータは変更する必要がない
            else:
                f3.write(f"{name},{score}\n")  #不合格者をf3に入れるため追加 \nは改行
    return pass_rows, all_rows  #合格者をmain()に渡す
             
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
    #SQLiteデータベースに接続（なければ自動で作られる）
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    print("DB接続Ok")  #確認用

    '''コマンドラインから合格点を受け取って実行時に数字を指定できる。指定がなければデフォルトの数字（pass_score=60）を使う'''
    if len(sys.argv) > 1:
        #pass_score = int(sys.argv[1]) #指定の数字を使うという指示
        pass_score = 60 #エラー回避。とりあえず固定の合格ラインを付ける。後で上に戻す。
    else:
        pass_score = PASS_SCORE #指定がなければデフォルトの数字
    
    pass_rows, all_rows = load_and_filter(INPUT_FILE, OUTPUT_FILE, FAIL_FILE, pass_score)  #合格者と全員のリストを同時に出す

    print("---合格者---")
    for name, score in pass_rows:  #pass_rowから１人ぶんずつ取り出して表示
        print(f"{name}:{score}点")

    stats = calc_stats(pass_rows)  #calc_stats()を呼び出して結果をstatsで受け取る
    all_stats = calc_stats(all_rows)  #全員の統計

    print('----統計----')
    if stats:
        print(f'受験者数：{all_stats["count"]}人')  #all_statsからcountで人数を計算
        print(f'合格者数：{stats["count"]}人')  #statsからcountdeで人数計算
        print(f'平均：{stats["avg"]}点')
        print(f'最高点：{stats["max"][1]}点 {stats["max"][0]}')
        print(f'最低点：{stats["min"][1]}点 {stats["min"][0]}')
    else:
        print("平均： データなし")
    
    if all_stats:
            print(f'全受験者の最低点:{all_stats["min"][1]}点 {all_stats["min"][0]}')
    save_stats(stats, all_stats)

    print("result.csvに統計を書き出しました")
    print("fail.csvに不合格者を書き出しました")

main()  #main()を呼び出してプログラムスタート
