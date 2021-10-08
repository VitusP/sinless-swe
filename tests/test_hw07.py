import os
from random import random
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw7 import HyperOptimizer

# Set the right file system
dataPath = os.path.dirname(os.path.abspath(__file__))

# Call Sample
# samp = Sample.read("data/auto93.csv")

# listOfHyperparams = []
# r = [30,60,125,250,500,1000]
# for index in range(1):
#     listOfHyperparams.append(HyperOptimizer("data/auto93.csv", r[index]))
#     print("************** r is: ", r[index])
#     print("Best Hyperparameters: ", listOfHyperparams[index].getBestHyperparameter())
n = 125
res1 = HyperOptimizer("data/auto93.csv", n)
print("************** r is: ", n)
print("Best Hyperparameters: ", res1.getBestHyperparameter())

success = False
while (success == False):
    try:
        res1 = HyperOptimizer("data/auto93.csv", n)
        print("************** r is: ", n)
        print("Best Hyperparameters: ", res1.getBestHyperparameter())
        success = True
    except:
        success = False