from src.inputOutput import csv_reader
from src.dataStructure import col
from enum import Enum

def isKlass(str):
    return '!' in str

def isGoal(str):
    return ('+' in str) or ('-' in str) or ('!' in str)

def isNum(str):
    return str[0].isupper()

def isWeight(str):
    pass

def isSkip(str):
    return '?' in str

def makeCol(at, name):
    if isSkip(str):
        return Skip(at, name)
    elif isNum(str):
        return ColType.Num
    else:
        return ColType.Sym    

class Sample:
    def __init__(self):
        self.hasHeader = False
        self.cols = [] # List of tuples for columns
        self.rows = [] # List of rows
        self.y = [] # Goals column
        self.x = [] # Other column
        self.names = [] # row 1 names
        self.typeMap = [] # header type
        self.klass = []
        self.keep = True
        self.rowsPos = 0

    @staticmethod
    def read(filePath):
        sample = Sample()
        cleanedData = csv_reader(filePath) # Read csv data from given path
        for row in cleanedData: # Add each row to the Sample
            sample.add(row)
        return sample
        
    def add(self, lst):
        if not self.hasHeader:
            self.header(lst)
        else:
            self.data(lst)

    def header(self, lst, what, new, tmp):
        self.names = lst

        for at,name in enumerate(lst):

            #what = isSkip(name)

            self.cols.append()

    def data(self, lst):
        pass

    def clone(self):
        pass

