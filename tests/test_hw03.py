import os
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.dataStructure import Sample

# Set the right file system
dataPath = os.path.dirname(os.path.abspath(__file__))
dataPath = dataPath[:dataPath.rindex("/")]

# Call Sample
returnedSample = Sample.read("data/auto93.csv")
sortedSample = returnedSample.sort()

top = sortedSample[:5]

bot = sortedSample[-5:]

for cols in returnedSample.cols:
    print(cols.name, "  ", end = '')
print()    

for t in top:
    [(print("    ",x, "    ",end = '')) for x in t]
    print()

    #print(t)

print('-----------------------------------------------------------------')

for b in bot:   
    [(print("    ",x, "    ",end = '')) for x in b]
    print()