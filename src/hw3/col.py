"""
This is a python script to implement Col, Sym, Num,
and Skip class for HW3 
"""
from abc import abstractproperty
import math
import statistics

"""
Column class implementation
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

"""
Skip class implementation
"""
class Skip(Col):
    pass

"""
Symbol class implementation
"""
class Sym(Col):

    def __init__(self, at, name):
        super().__init__(at, name)
        self.has = {}
        self.most = 0
        self.mode = 0
    
    def mid(self):
        return self.mode

    def add(self, x):
        if x in self.has.keys():
            self.has[x] = 1 + self.has.get(x,0)
        else:
            self.has[x] = 1

        if self.has[x] > self.most:
            self.most, self.mode = self.has[x], x
    
    def dist(self, x, y):
        return 0 if x == y else 1

    def discretize(self,j,_):
        "Query: `Return values seen in  i` is good and `j` is bad"
        for x in set(self.has | j.has): # for each key in either group
            yield o(at=self.at, name=self.name, lo=x, hi=x, 
                best= self.has.get(x,0), rest=j.has.get(x,0))

    def merge(self,j):
        "Copy: merge two symbol counters"
        k = Sym(n=self.at, s=self.name)
        for x,n in self.has.items(): k.add(x,n)
        for x,n in j.has.items(): k.add(x,n)
        return k

    def var(self):
        "Query: variability"
        return - sum(v/self.n * math.log2(v/self.n) for v in self.has.values())

"""
Num class implementation
"""
class Num(Col):
    def __init__(self, at, name):
        super().__init__(at, name)
        self.lo = float('inf') # Highest number
        self.hi = float('-inf') # Lowest number
        self.mu = 0 
        self.m2 = 0
        self.n = 0
        self.sd = 0
        self.w = self.getWeight()
        self.all = []

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
        self.all.append(x)
    
    def mid(self):
        return round(self.mu, 1)
    
    def norm(self, inputNum):
        return 0 if abs(self.lo - self.hi) < 1E-31 else (inputNum - self.lo)/(self.hi - self.lo)
    
    def getWeight(self):
        if self.name[-1] == '+':
            return 1
        else:
            return -1
    
    def getAll(self):
        return self.all

    def dist(self, x, y):
        if x == '?':
            y = self.norm(y)
            x = 0 if y > 0.5 else 1
        elif y == '?':
            x = self.norm(x)
            y = 0 if x > 0.5 else 1
        else:
            x, y = self.norm(x), self.norm(y)
        return abs(x-y)

    def discretize(self,j, my):
        "Query: `Return values seen in  i` is good and `j` is bad"
        best, rest = 1,0
        # list of (number, class)
        xys=[(good,best) for good in self.getAll()] + [ (bad, rest) for bad  in j.getAll()]
        #
        # find a minimum break span (.3 * expected value of standard deivation)
        n1,n2 = len(self.getAll()), len(j.getAll())
        # print(self.getAll())
        iota = my.cohen * (self.var()*n1 + j.var()*n2) / (n1 + n2)
        #
        # all the real work is in unsuper and merge... which is your problem
        ## TODO: Merge method and unsuper method.
        ranges = self.merge(self.unsuper(xys, len(xys)**my.bins, iota))
        # 
        if len(ranges) > 1:  
            for r in ranges:
                # print("ranges: ", r)
                yield o(at=self.at, name=self.name, lo=self.getLowestorHighestFromTuple(r, True), hi=self.getLowestorHighestFromTuple(r, False), 
                        best= self.getBestorRestfromTuple(r,best), rest=self.getBestorRestfromTuple(r,rest))
    
    def unsuper(self, xys, myBinSize, iota):
        # sort xys
        xys.sort(key=lambda index:index[0])
        # print(xys)
        listSplit = []
        a = 0
        b = 0

        while len(xys) - a > myBinSize and a < len(xys) - 1:
            if((len(xys)-1 <= b or xys[b][0] != xys[b + 1][0]) and (abs(a-b) > iota) and (len(xys) - b - 1 > myBinSize)):
                tempList = []
                for index in range(a, b + 1):
                    tempList.append(xys[index])
                a = b + 1
                b = a + 1
                listSplit.append(tempList)
            elif b < len(xys):
                b += 1
            else:
                a += 1
        finalList = []
        for index in range(a, len(xys)):
            finalList.append(xys[index])
        listSplit.append(finalList)
        return listSplit


    def merge(self, item):
        index = 0
        while index < len(item) - 1:
            a, b = item[index], item[index + 1]
            c = a + b
            # print("a:", a)
            varianceA = self.getVariance(a)
            varianceB = self.getVariance(b)
            varianceC = self.getVariance(c)
            if (varianceC*.95) <= (varianceA*len(a) + varianceB*len(b))/(len(a) + len(b)):
                item[index] = item[index] + item[index+1]
                item.pop(index+1)
            else:
                index += 1
        return item

    def var(self):
        return self.sd
    
    def getVariance(self, listTuple):
        temp = []
        for val in listTuple:
            temp.append(val[0])
        return statistics.variance(temp)
    
    def getLowestorHighestFromTuple(self, listTuple, minTrue):
        temp = []
        for val in listTuple:
            temp.append(val[0])
        if minTrue:
            return min(temp)
        return max(temp)
    
    def getBestorRestfromTuple(self, listTuple, indicator):
        counter = 0
        for val in listTuple:
            if val[1] == indicator:
                counter += 1
        return counter

class o:
  """`o` is just a class that can print itself (hiding "private" keys)
  and which can hold methods."""
  def __init__(self, **d)  : self.__dict__.update(d)
  def __repr__(self) : return "{"+ ', '.join( 
    [f":{k} {v}" for k, v in self.__dict__.items() if  k[0] != "_"])+"}"