import os
from random import random
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw3 import Sample
from src.hw7 import HyperOptimizer

# Set the right file system
dataPath = os.path.dirname(os.path.abspath(__file__))

# Call Sample
samp = Sample.read("data/auto93.csv")

listOfHyperparams = []
r = [30,60,125,250,500,1000]
for index in range(1):
    listOfHyperparams.append(HyperOptimizer(samp, r[index]))
    print(listOfHyperparams[index].getBestHyperparameter())



