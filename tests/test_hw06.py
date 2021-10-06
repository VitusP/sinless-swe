import os
from random import random
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw3 import Sample
from src.hw6 import FFT
from src.hw7 import Config

conf = Config()
conf.build()

# Set the right file system
dataPath = os.path.dirname(os.path.abspath(__file__))
#dataPath = dataPath[:dataPath.rindex("/")]

# Call Sample
samp = Sample.read("data/auto93.csv")
samp.use_config(conf)

leafs = samp.divs()
clusters = sorted(leafs)


for sample in clusters:
    print(sample.ys())

worst, best = clusters[-1], clusters[0] # as done above


print("worst: ",worst.ys())
for row in worst.rows:
    print(row)
print("best: ",best.ys())
for row in best.rows:
    print(row)
print()

for good,bad in zip(best.x,worst.x): 
    for d in good.discretize(bad, conf):
       print(d)
    print()
print("HW6*********************************************************")
branches = []
branch = []
FFT(samp, conf, branch, branches)
for i, b in enumerate(branches):
    print("tree: ", i)
    for k,val in enumerate(b):
        if len(b) - 1 == k:
            print(val['type'], '  else: ', val['then'], '(n:', val['n'], ')')
        else:
            print(val['type'], ' ', val['txt'], '', val['then'], '(n:', val['n'], ')')
# Print config
print("Hyperparameter: ", conf.getHyperparameters())
   



