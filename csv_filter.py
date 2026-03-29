import csv

INPUT_FILE = "data.csv"  #大文字は変わらない値・読み込むファイルを変えるだけでつかえる
OUTPUT_FILE = "pass.csv"  #小文字は変数（ループの中で変わる値）・書き出すファイルを変えるだけで使える
PASS_score = 60　#ここを変えるだけで合格点が変わる

def load_and_filter(infut_filter, output_file, pass_score)
'''CSVを読み込んで(input_file)合格点以上の者(pass_score)を合格者を書き出しす(output_file)'''

	pass_rows = []  #合格者を入れる空のリスト
#withはdefの中に入るから段落を下げる
	with open("data.csv", "r", encoding="utf-8") as f, \
		 open("pass.csv", "w", encoding="utf-8", newline="")as f2:

		reader = csv.reader(f)
		writer = csv.writer(f2)

		header = next(reader)  #ヘッダー飛ばす
		writer.writerow(header)  #ヘッダーを出力ファイルにも書く

		for row in reader:  #rowは一人分のデータ
			name = row[0].capitalize() #.capitalize()は一文字目を大文字それ以降小文字
			score = int(row[1])  #CSVからとった文字を計算できる数字に変換

			if score >= pass_score:
				writer.writerow([name,score])  #[]は後から変更できる/CSVに書き出すwriterowは[]で渡す
                pass_rows.append((name, score))  #()は後から変更できない/ここでは一度入れたデータは変更する必要がない
		return pass_rows  #合格者をmain()に渡す
			 
def calc_stats(rows):  #rowsは複数
	'''合格者のリストから平均・最高・採点を計算する'''
	
	if not rows:
		return None  #合格者がいなかったらここで終了
	total = sum(score for _, score in rows)  #for _,は点数を出すとき名前はいらないので_に捨てる
	avg = total / len(lows)  #len(lows)で合格者の人数を取得して平均を計算する
	max_name =  name,max_score = max(rows, key=lambda r: r[1]  #r[1](スコア)を基準に最高得点を出す
	min_name =  name,min_score = min(rows, key=lambda r: r[1]  	#r[1](スコア)を基準に合格者の一番低い点を出す
		return{  #結果を辞書にまとめてmain()に出す
			"avg": avg
			"max":(max_name, max_score),
			"min":(min_name, min_score),
}

def main():
	'''load_and_filter()で合格者を呼びだしpass_rowsで受け取って統計を表示する'''
	pass_rows = load_and_filter(INPUT_FILE, OUTPUT_FILE, PASS_SCORE)

	print("---合格者---")
	for name, score in pass_rows:  #pass_rowから１人ぶんずつ取り出して表示
		print(f'{name}:{score}点')

	stats = calac_stats(pass_rows)  #clac_stats()を呼び出して結果をstatsで受け取る
	print('----統計----')
	if stats:
		print(f"平均：{stats["ave"]}点")
		print(f"最高点：,{stats["max"][1]点}{stats["max"][0]}")
		print(f"最低点：,{stats["min"][1]点}{stats["min"][0]}")
	else:
		print("平均： データなし")

main()  #main()を呼び出してプログラムスタート
