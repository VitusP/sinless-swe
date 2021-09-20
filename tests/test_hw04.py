import os
from random import random
import sys
import time
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw3 import Sample

def testSampleDistance():
    samp1 = Sample()
    samp1.add(["sym1", "Num1+"])
    assert len(samp1.names) == 2
    samp1.add(["tst1", 1])
    samp1.add(["tst2", 2])

    assert samp1.dist(["tst1", 1], ["tst1", 1]) == 0
    assert samp1.dist(["tst1", 1], ["tst2", 2]) == 1
    assert samp1.dist(["tst1", 1], ["tst2", 1]) == (1/2)**(1/2)

def testSampFaraway():
    # Set the right file system
    dataPath = os.path.dirname(os.path.abspath(__file__))
    dataPath = dataPath[:dataPath.rindex("/")]

    # Call Sample
    samp2 = Sample.read("data/auto93.csv")
    neighbors = samp2.neighbors(samp2.rows[1])
    faraway = samp2.faraway(samp2.rows[0],samp2.rows)
    assert len(faraway) == 8

def testNeighbors():
    samp3 = Sample()
    samp3.add(["sym1", "Num1+"])
    rows = [
        ["tst1", 1], 
        ["tst2", 2],
        ["tst3", 3], 
        ["tst4", 4]
    ]
    [(samp3.add(row)) for row in rows]
    neighbors = samp3.neighbors(["tst1", 1])
    assert neighbors[3][1] == ["tst4", 4]

def testDivs():
    # Set the right file system
    dataPath = os.path.dirname(os.path.abspath(__file__))
    dataPath = dataPath[:dataPath.rindex("/")]

    # Call Sample
    samp4 = Sample.read("data/auto93.csv")

    divResult = samp4.divs()

    assert len(divResult) == 32

## Runtime report
dataPath = os.path.dirname(os.path.abspath(__file__))
dataPath = dataPath[:dataPath.rindex("/")]
runtimeSample = Sample.read("data/auto93.csv")

# Measure runtime
startTime = time.time()
runtimeSample.dist(runtimeSample.rows[0], runtimeSample.rows[397])
totalDuration = time.time() - startTime
print("Runtime Sample Dist(): ", totalDuration, " seconds")

# Measure runtime
startTime = time.time()
runtimeSample.faraway(runtimeSample.rows[0], runtimeSample.rows)
totalDuration = time.time() - startTime
print("Runtime Sample faraway(): ", totalDuration, " seconds")

# Measure runtime
startTime = time.time()
runtimeSample.neighbors(runtimeSample.rows[0])
totalDuration = time.time() - startTime
print("Runtime Sample neighbors(): ", totalDuration, " seconds")

# Measure runtime
startTime = time.time()
runtimeSample.divs()
totalDuration = time.time() - startTime
print("Runtime Sample divs(): ", totalDuration, " seconds")