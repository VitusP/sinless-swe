"""
This is the main Sample class used for HW3 and HW4
Implementation.
"""
import random
import math

from .col import Num, Sym, Skip
from src.hw2 import csv_reader
from functools import cmp_to_key

"""
CONFIG variables
"""
CONFIG = {
    'p':2,
    'enough':0.4,
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
"""
Sample class stores each row in a 
data structure.
"""
class Sample:
    """
    Sample constructors
    """
    def __init__(self, initialized = []):
        self.hasHeader = False
        self.cols = [] # List of tuples for columns
        self.rows = [] # List of rows
        self.y = [] # Goals column
        self.x = [] # Other column
        self.names = [] # row 1 names
        self.typeMap = [] # header type
        self.klass = []
        for initVal in initialized:
            self.add(initVal)
    
    """
    Sort tables by their mid values.
    """
    def __lt__(self,j):
        return  Row(self.mid(),self) < Row(j.mid(), j)

    """
    Read the csv file and create Sample class
    :param filePath: csv file name
    """
    @staticmethod
    def read(filePath):
        sample = Sample()
        cleanedData = csv_reader(filePath) # Read csv data from given path
        for row in cleanedData: # Add each row to the Sample
            sample.add(row)
        return sample
    
    """
    Add each row to the Sample class
    :param lst: a row of data
    """
    def add(self, lst):
        if not self.hasHeader:
            self.header(lst)
        else:
            self.data(lst)

    """
    Add first row to the Sample
    :param lst: a row of column names
    """
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

    """
    Add each data row to the Sample class
    :param lst: a row of data
    """
    def data(self, list):
        for at,col in enumerate(self.cols):
            col.add(list[at])
        self.rows.append(list)

    """
    Clone the current sample class
    :return Sample: Sample class
    """
    def clone(self):
        newSample = Sample([self.names])
        return newSample

    """
    get the mid of the goal
    :return goal mid: mid goal
    """
    def ys(self):
        return [goal.mid() for goal in self.y]
    
    """
    get the mid of the all columns
    :return goal mid: mid goal
    """
    def mid(self):
        return [goal.mid() for goal in self.cols]
    
    """
    Sorting rows based on Zitler
    :param row1: a row of data
    :param row1: a row of data
    """
    def zitler(self, row1, row2):
        goals = self.y
        s1, s2, e, n = 0, 0, 2.71828, len(goals)
        for goal in goals:
            w = goal.getWeight()
            x = goal.norm(row1[goal.at])
            y = goal.norm(row2[goal.at])
            s1 = s1 - e**(w * (x-y)/n)
            s2 = s2 - e**(w * (y-x)/n)
        return 0 if (s1/n < s2/n) else 1
    
    """
    Sorting rows using Zitler
    :return sorted: sorted rows
    """
    def sort(self):
        return sorted(self.rows, key = cmp_to_key(self.zitler))
    
    """
    Find distance between two rows
    :param row1: a row of data
    :param row1: a row of data
    :return dist: distance between rows
    """
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
    
    """
    Get tuple of neighbor of row r1 and the 
    distance.
    :param r1: a row of data
    :param rows: rows available
    :return list of tuples: tuples of neighbor and distance
    """
    def neighbors(self, r1, rows = {}):
        a = []
        rows = rows or self.rows
        for r2 in rows:
            a.append((self.dist(r1,r2),r2))
        return sorted(a, key=lambda tuple: tuple[0])

    """
    Find points that is _CONFIG['far']_ away
    :param r: a row of data
    :param rows: rows available
    :return a row:
    """
    def faraway(self, r, rows):
        # shuffled = random.sample(self.rows, CONFIG['samples'])
        n = min(128,len(rows))
        shuffled = random.sample(rows, n)
        all = self.neighbors(r, shuffled)
        return all[math.floor(CONFIG['far']*n)][1]
    
    """
    Divide a sample into two based on distances
    :param rows: rows to divide
    :return left, right: rows left and right
    """
    def div1(self, rows):
        one = self.faraway(rows[random.randrange(0, len(rows) - 1)], rows)
        # one = rows[random.randrange(0, len(rows) - 1)]
        two = self.faraway(one, rows)
        c = self.dist(one, two)

        rowPlusProjections = []
        for row in rows:
            a = self.dist(row, one)
            b = self.dist(row, two)
            projection = (a**2 + c**2 - b**2) / (2*c)
            rowPlusProjections.append((projection, row))

        rowPlusProjections = sorted(rowPlusProjections, key=lambda proj:proj[0])
        mid = len(rows)/2
        left = [proj[1] for proj in rowPlusProjections[0:math.floor(mid)]]
        right = [proj[1] for proj in rowPlusProjections[math.floor(mid):]]
        return left, right

    """
    Divide the rows into clusters
    :param leafs: original leaf to put the result to
    :param enough: config
    :param rows: rows of data
    :param lvl: depth of the tree
    """
    def recursive_divs(self, leafs, enough, rows, lvl):
        if CONFIG['loud']:
            pass
        if len(rows) < 2 * enough:
            # Add leaf to Sample
            tempSample = self.clone()
            for row in rows:
                tempSample.add(row)
            self.printGoals(tempSample, lvl + 1)
            leafs.append(tempSample)          
        else:
            self.printDendogram(rows, lvl + 1)
            l,r = self.div1(rows)
            self.recursive_divs(leafs, enough, l, lvl + 1)
            self.recursive_divs(leafs, enough, r, lvl + 1)

    """
    Divide the rows into clusters
    """
    def divs(self):
        leafs = []
        enough = pow(len(self.rows), CONFIG['enough'])
        self.recursive_divs(leafs, enough, self.rows, 0)
        return leafs

    """
    Helper function to print dendogram
    :param leafs: original leaf to put the result to
    :param lvl: depth of the tree
    """
    def printDendogram(self, leaf, lvl):
        one = self.faraway(leaf[random.randrange(0, len(leaf) - 1)], leaf)
        two = self.faraway(one, leaf)
        c = self.dist(one, two)
        print("|.. "*lvl,"n=", len(leaf), "c=%.2f" % c)
    
    """
    Helper function to print goal median
    :param leafs: original leaf to put the result to
    :param lvl: depth of the tree
    """
    def printGoals(self, leaf, lvl):
        print("|.. "*lvl,"n=", len(leaf.rows), end="")
        print(" goal=", leaf.ys())

"""
Row class implementation
"""
class Row():
    def __init__(self,lst,sample): 
        self.sample,self.cells, self.ranges = sample, lst,[None]*len(lst)
        
    def __lt__(self,j):
        "Does row1 win over row2?"
        loss1, loss2, n = 0, 0, len(self.sample.y)
        for col in self.sample.y:
            a   = col.norm(self.cells[col.at])
            b   = col.norm(j.cells[col.at])  # bug fix: MUST be j.cells
            loss1 -= math.e**(col.getWeight() * (a - b) / n)
            loss2 -= math.e**(col.getWeight() * (b - a) / n)
        return loss1 / n < loss2 / n