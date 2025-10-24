import csv

csv_file = "iris dataset\Iris.csv"

with open(csv_file, "r") as f:
    for row in f:
        row = row.split(',')
        # print key value pairs of iris Species as key and PetalLengthCm as value
        species = row[5]
        petalLengthCm = row[3]
        #print(f"{species}\t{petalLengthCm}")
        a, b = f"{species}\t{petalLengthCm}".split('\t')
        print(a.strip(), b.strip())