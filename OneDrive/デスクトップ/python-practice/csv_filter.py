import csv

total = 0
count = 0
max_score = 0
min_score = 100

with open("data.csv", "r", encoding="utf-8") as f:
	reader = csv.reader(f)
	next(reader)

	with open("pass.csv", "w", encoding="utf-8", newline="")as f2:
		writer = csv.writer(f2)

		for row in reader:
			name = row[0]
			score = int(row[1])

			if score >=60:
				writer.writerow([name,score])
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
