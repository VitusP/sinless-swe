from dataStructure import Sample
from inputOutput import csv_reader
import sys

returnedSample = Sample.read(sys.argv[1]).sort()

top = returnedSample[:5]

bot = returnedSample[-5:]

for t in top:   
    print(t)

print('-----------------------------------')

for b in bot:   
    print(b)