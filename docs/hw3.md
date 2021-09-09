## HW3: Sample, Col, Sym, Skip, Num
### Usage
```Shell
$ python3 tests/test_hw03.py
```
**Sample.py**</br>
Contains the main Sample class
```Python
"""
This is the main Sample class used for HW3 
Implementation.
"""

from .col import Num, Sym, Skip
from src.inputOutput import csv_reader
from functools import cmp_to_key


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
```

**Sample.py**</br>
Contains the main Col, Sym, Skip, and Num class
```Python
"""
This is a python script to implement Col, Sym, Num,
and Skip class for HW3 
"""

class Col:
    #: Class for column
    #: param: the index of column
    #: param: the name of column
    #: return: new column

    def __init__(self, at, name):
        self.at = at
        self.name = name
    
    def add(self, x):
        pass

class Skip(Col):
    pass

class Sym(Col):

    def __init__(self, at, name):
        super().__init__(at, name)
        self.has = {}
        self.most = 0
        self.mode = 0

    def add(self, x):
        if x in self.has.keys():
            self.has[x] = 1 + self.has.get(x,0)
        else:
            self.has[x] = 1

        if self.has[x] > self.most:
            self.most, self.mode = self.has[x], x

class Num(Col):
    def __init__(self, at, name):
        super().__init__(at, name)
        self.lo = float('inf') # Highest number
        self.hi = float('-inf') # Lowest number
        self.mu = 0 
        self.m2 = 0
        self.n = 0
        self.sd = 0

    def add(self, x):
        if x == '?':
            return
        if x < self.lo:
            self.lo = x
        if x > self.hi:
            self.hi = x
        self.n += 1
        delta = x - self.mu
        self.mu = self.mu + delta / self.n
        self.m2 = self.m2 + delta * (x - self.mu)
        if self.n > 1 and self.m2 > 0:
            self.sd = (self.m2 / (self.n - 1))**0.5
    
    def normalizedNum(self, inputNum):
        return (inputNum - self.lo)/(self.hi - self.lo)
    
    def getWeight(self):
        if self.name[-1] == '+':
            return 1
        else:
            return -1

```
### **Output**
Here is the output of our code
```Shell
Size of data 399  rows
Cylinders   Displacement   Horsepower   Weight-   Acceleration+   Model       Origin       Mpg+   
     4          97          52          2130          24.6          82          2          40     
     4          90          48          2335          23.7          80          2          40     
     4          86          65          2110          17.9          80          3          50     
     4          90          48          1985          21.5          78          2          40     
     4          90          48          2085          21.7          80          2          40     
--------------------------------------------------------------------------
     8          440          215          4312          8.5         70          1          10     
     8          429          198          4952          11.5        73          1          10     
     8          383          180          4955          11.5        71          1          10     
     8          400          175          5140          12          71          1          10     
     8          455          225          4951          11          73          1          10
```