from src.dataStructure.col import Num, Sym
from src.inputOutput import csv_reader
from src.dataStructure import Skip
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
    if isSkip(name):
        return Skip(at, name)
    elif isNum(name):
        return Num(at, name)
    else:
        return Sym(at, name)  

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
            new = makeCol(at, name)

            if isGoal(at, name):
                self.y.append(new)
            else:
                self.x.append(new)

            if isKlass(name):
                self.klass = new

            self.cols.append(new)

    def data(self, list):
        ##Double check line 71-72.
        for at,col in enumerate(self.cols):
            col.add(list[at])
        self.rows.append(list)



    def clone(self):
        return Sample().add(self.names)

