from src.inputOutput import csv_reader

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

class Sample:
    def __init__(self):
        self.cols = [] # List of tuples for columns
        self.rows = [] # List of rows
        self.y = [] # Goals column
        self.x = [] # Other column
        self.names = [] # row 1 names
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
        if len(self.names) > 0:
            self.data(lst)
        else:
            self.header(lst)

    def header(self, lst, what, new, tmp):
        self.names = lst
        for at,name in enumerate(lst):
            what = isSkip(name)

    def data(self, lst):
        pass

    def clone(self):
        pass

class Skip(Sample):
    def add(x):
        return x


class Num(Sample):
    lo = 0 # Highest number
    hi = 0 # Lowest number
    mu = 0 
    m2 = 0
    n = 0
    sd = 0

    def add1(self, x):
        if x < self.lo:
            self.lo = x
        if x > self.hi:
            self.hi = x
        self.n += 1
        delta = x - self.mu
        self.mu = self.mu + delta / self.n
        self.m2 = self.m2 + delta * (x - self.mu)
        if self.n > 1:
            self.sd = (self.m2 / (self.n - 1))**0.5


class Sym(Sample):
    has = {}
    most = 0
    mode = 0

    def add1(self, x):
        if x in self.has.keys():
            self.has[x] += 1
        if self.has[x] > self.most:
            self.most = self.has[x]
            self.mode = x
    

