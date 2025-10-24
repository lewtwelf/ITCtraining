#!/usr/bin/env python3
import sys

# iris dataset looks like this:
# Id,SepalLengthCm,SepalWidthCm,PetalLengthCm,PetalWidthCm,Species
# 1,5.1,3.5,1.4,0.2,Iris-setosa

for row in sys.stdin:
    row = row.split(',')
    print(row)
    # print key value pairs of iris Species as key and PetalLengthCm as value
    species = row[5]
    petalLengthCm = row[3]
    print(f"{species}\t{petalLengthCm}")