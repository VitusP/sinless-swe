import os
from random import random
import sys
import time
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw3 import Sample

class Config:
    p=2
    enough=0.4
    samples=128
    far= 0.9
    loud=False
    cohen=.3
    bins = .5

# Set the right file system
dataPath = os.path.dirname(os.path.abspath(__file__))
dataPath = dataPath[:dataPath.rindex("/")]

# Call Sample
samp = Sample.read("data/auto93.csv")

leafs = samp.divs()
clusters = sorted(leafs)

"""
for sample in clusters:
    print(sample.ys())

for leaf in leafs:
     print(leaf)
     print("-------------")
"""
worst, best = clusters[-1], clusters[0] # as done above

"""
print("worst: ",worst.ys())
for row in worst.rows:
    print(row)
print("best: ",best.ys())
for row in best.rows:
    print(row)
print()
"""

for good,bad in zip(best.x,worst.x): 
    for d in good.discretize(bad, Config()):
       print(d)
    print()


