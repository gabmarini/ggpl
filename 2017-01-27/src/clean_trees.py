import csv

tree = open("../lines/trees.lines", "w")
with open("../lines/t.lines") as f:
	r = csv.reader(f, delimiter=",")
	for row in r:
		if(row[0] == row[2] and row[1] == row[3]):
			pass
		else:
			tree.write(",".join(row)+"\n")