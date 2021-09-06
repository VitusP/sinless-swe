from dataStructure import Sample
from inputOutput import csv_reader
import sys

returnedSample = Sample.read(sys.argv[1])
# for row in returnedSample.rows:
#     print(row)

for col in returnedSample.cols:
    print(col.name)
