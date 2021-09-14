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
    
    def dist(self, x, y):
        return 0 if x == y else 1

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
    
    def dist(self, x, y):
        if x == '?':
            y = self.normalizedNum(y)
            x = 0 if y > 0.5 else 1
        elif y == '?':
            x = self.normalizedNum(x)
            y = 0 if x > 0.5 else 1
        else:
            x, y = self.normalizedNum(x), self.normalizedNum(y)
        return abs(x-y)
