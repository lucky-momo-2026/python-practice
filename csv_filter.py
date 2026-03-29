import csv

total = 0
count = 0
max_score = float('-inf') #全員がゼロでもおかしくないように
min_score = float('inf')  #最高点がいくつか１００点満点とは限らないから
max_name = ""
min_name = ""

#見やすいようにｆとｆ２を統一
with open("data.csv", "r", encoding="utf-8") as f, \
	 open("pass.csv", "w", encoding="utf-8", newline="")as f2:

	reader = csv.reader(f)
	writer = csv.writer(f2)

	header = next(reader)  #ヘッダー飛ばす
	writer.writerow(header)  #ヘッダーを出力ファイルにも書く

	for row in reader:
		name = row[0].capitalize()
		score = int(row[1])

		if score >=60:
			writer.writerow([name,score])  #.capitalize()は一文字目を大文字それ以降小文字
			print([name,score])
			total += score
			count += 1

		if score > max_score:
			max_score = score
			max_name =  name

		if score < min_score:
			min_score = score
			min_name = name
if count > 0:
	print("平均：", total/ count)
	print("最高点：", max_score, max_name)
	print("最低点：", min_score, min_name)

else:
	print("平均： データなし")
