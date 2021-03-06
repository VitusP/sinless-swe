import os
import sys
sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
from src.hw2 import csv_reader

def testCsvReader():
    expectedResult = [['outlook', 'Temp', '?Humidity', 'windy', 'Wins+', 'Play-'],
                     ['sunny', 85, 85, 'FALSE', 10, 20],
                     ['sunny', 80, 90, 'TRUE', 12, 40],
                     ['overcast', 83, 86, 'FALSE', 40, 40],
                     ['rainy', 70, 96, 'FALSE', 40, 50],
                     ['rainy', 65, 70, 'TRUE', 4, 10],
                     ['overcast', 64, 65, 'TRUE', 30, 60],
                     ['sunny', 72, 95, 'FALSE', 7, 20],
                     ['sunny', 69, 70, 'FALSE', 70, 70],
                     ['rainy', 75, 80, 'FALSE', 80, 40],
                     ['sunny', 75, 70, 'TRUE', 30, 50],
                     ['overcast', 72, 90, 'TRUE', 60, 50],
                     ['overcast', 81, 75, 'FALSE', 30, 60],
                     ['rainy', 71, 91, 'TRUE', 50, 40]]
    dataPath = os.path.dirname(os.path.abspath(__file__))
    dataPath = dataPath[:dataPath.rindex("/")]
    result = csv_reader("data/windy.csv")
    for i,row in enumerate(result):
        assert row == expectedResult[i]
