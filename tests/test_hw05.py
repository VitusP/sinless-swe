import os
from random import random
import sys
import time
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw3 import Sample

# Set the right file system
dataPath = os.path.dirname(os.path.abspath(__file__))
dataPath = dataPath[:dataPath.rindex("/")]

# Call Sample
samp = Sample.read("data/auto93.csv")

leafs = samp.divs()
sampleLeafs = []
# for leaf in leafs:
#     print(leaf)
#     print("-------------")
