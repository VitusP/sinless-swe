"""
This is the main Sample class used for HW3 and HW4
Implementation.
"""
import random
import math

from .col import Num, Sym, Skip
from src.hw2 import csv_reader
from functools import cmp_to_key

CONFIG = {
    'p':2,
    'enough':0.5,
    'samples':128,
    'far': 0.9,
    'loud': False
}

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

    def header(self, lst):
        self.names = lst

        for at,name in enumerate(lst):
            new = makeCol(at, name)

            if isGoal(name):
                self.y.append(new)
            else:
                self.x.append(new)

            if isKlass(name):
                self.klass = new

            self.cols.append(new)
            self.hasHeader = True

    def data(self, list):
        for at,col in enumerate(self.cols):
            col.add(list[at])
        self.rows.append(list)

    def clone(self):
        return Sample().add(self.names)
    
    def zitler(self, row1, row2):
        goals = self.y
        s1, s2, e, n = 0, 0, 2.71828, len(goals)
        for goal in goals:
            w = goal.getWeight()
            x = goal.normalizedNum(row1[goal.at])
            y = goal.normalizedNum(row2[goal.at])
            s1 = s1 - e**(w * (x-y)/n)
            s2 = s2 - e**(w * (y-x)/n)
        return -1 if (s1/n < s2/n) else 1
    
    def sort(self):
        return sorted(self.rows, key = cmp_to_key(self.zitler))
    
    def dist(self, row1, row2):
        d, n = 0, 1E-32
        for col in self.cols:
            n = n + 1
            a, b = row1[col.at], row2[col.at]
            if a=='?' and b=='?':
                d = d + 1
            else:
                d = d + col.dist(a, b)**CONFIG['p']
        return (d/n)**(1/CONFIG['p'])
    
    def neighbors(self, r1, rows = {}):
        a = []
        rows = rows or self.rows
        for r2 in rows:
            a.append((self.dist(r1,r2),r2))
        return sorted(a, key=lambda tuple: tuple[0])

    def faraway(self, r):
        shuffled = random.sample(self.rows, CONFIG['samples'])
        all = self.neighbors(r, shuffled)
        # [(print(x)) for x in all]
        return all[math.floor(CONFIG['far']*len(all))][1]
        
    def div1(self, rows):
        one = self.faraway(rows[random.randrange(0, len(rows) - 1)])
        two = self.faraway(one)
        c = self.dist(one, two)

        rowPlusProjections = []
        for row in rows:
            a = self.dist(row, one)
            b = self.dist(row, two)
            projection = (a**2 + c**2 - b**2) / (2*c)
            rowPlusProjections.append((projection, row))

        rowPlusProjections = sorted(rowPlusProjections, key=lambda proj:proj[0])
        mid = len(rows)/2
        left = [proj[1] for proj in rowPlusProjections[1:math.floor(mid)]]
        right = [proj[1] for proj in rowPlusProjections[math.floor(mid) + 1:]]
        return left, right

    def recursive_divs(self, leafs, enough, rows, lvl):
        if CONFIG['loud']:
            pass

        if len(rows) < 2 * enough:
            leafs.append(rows)
        else:
            l,r = self.div1(rows)
            self.recursive_divs(leafs, enough, l, lvl + 1)
            self.recursive_divs(leafs, enough, r, lvl + 1)

    def divs(self):
        leafs = []
        enough = pow(len(self.rows), CONFIG['enough'])
        self.recursive_divs(leafs, enough, self.rows, 0)
        return leafs




