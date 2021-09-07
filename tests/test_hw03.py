import os
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.dataStructure import Sample


returnedSample = Sample.read(sys.argv[1]).sort()

top = returnedSample[:5]

bot = returnedSample[-5:]

for t in top:   
    print(t)

print('-----------------------------------')

for b in bot:   
    print(b)