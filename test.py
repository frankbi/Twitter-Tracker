import csv
with open("test.csv", "r") as csvfile:
	readit = csv.reader(csvfile, delimiter=",")
	for row in readit:
		print row[0]
