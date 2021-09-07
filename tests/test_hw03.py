import os
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.dataStructure import Sample

dataPath = os.path.dirname(os.path.abspath(__file__))
dataPath = dataPath[:dataPath.rindex("/")]
returnedSample = Sample.read("data/auto93.csv").sort()

top = returnedSample[:5]

bot = returnedSample[-5:]

for t in top:   
    print(t)

print('-----------------------------------')

for b in bot:   
    print(b)