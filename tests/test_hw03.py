import os
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw3 import Sample

def testHw3():
    # Set the right file system
    dataPath = os.path.dirname(os.path.abspath(__file__))
    dataPath = dataPath[:dataPath.rindex("/")]

    # Call Sample
    returnedSample = Sample.read("data/auto93.csv")
    sortedSample = returnedSample.sort()

    top = sortedSample[:5]

    bot = sortedSample[-5:]

    for cols in returnedSample.cols:
        print(cols.name, "  ", end='')
    print()

    expectedTop = [[4, 97, 52, 2130, 24.6, 82, 2, 40],
                   [4, 90, 48, 2335, 23.7, 80, 2, 40],
                   [4, 86, 65, 2110, 17.9, 80, 3, 50],
                   [4, 90, 48, 1985, 21.5, 78, 2, 40],
                   [4, 90, 48, 2085, 21.7, 80, 2, 40]]
    for i, t in enumerate(top):
        assert t == expectedTop[i]
        [(print("    ", x, "    ", end='')) for x in t]
        print()

        # print(t)

    print('-----------------------------------------------------------------')

    expectedBottom = [
        [8, 440, 215, 4312, 8.5, 70, 1, 10],
        [8, 429, 198, 4952, 11.5, 73, 1, 10],
        [8, 383, 180, 4955, 11.5, 71, 1, 10],
        [8, 400, 175, 5140, 12, 71, 1, 10],
        [8, 455, 225, 4951, 11, 73, 1, 10]]

    for i, b in enumerate(bot):
        assert b == expectedBottom[i]
        [(print("    ", x, "    ", end='')) for x in b]
        print()
