import csv

filename = "C:/data/test.csv"
with open(filename,encoding="utf-8") as f:
    reader = csv.reader(f)
    #print(list(reader))

    for row in reader:
        print(reader.line_num,row)