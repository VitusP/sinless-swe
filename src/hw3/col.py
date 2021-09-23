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
        # for row in xys:
        #     print(row)
        #
        # find a minimum break span (.3 * expected value of standard deivation)
        n1,n2 = len(self.getAll()), len(j.getAll())
        # print(self.getAll())
        iota = my.cohen * (self.var()*n1 + j.var()*n2) / (n1 + n2)
        #
        # all the real work is in unsuper and merge... which is your problem
        # Merge method and unsuper method.
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
        # for row in xys:
        #     print(row)
        listSplit = []

        xys_size = len(xys)-1
        
        start = 0
        end = 0

        while start <= xys_size and end <= xys_size:
            if((xys_size <= end or xys[end][0] != xys[end + 1][0]) and (abs(end-start) > iota) and (xys_size - end > myBinSize)):
                listSplit.append(xys[start:end + 1])
                start = end + 1
                end = start + 1
            elif end < len(xys):
                end += 1
            else:
                start += 1

        listSplit.append(xys[start:])
        for row in listSplit:
            print(row)
        return listSplit


    def merge(self, item):
        index = 0
        possibleCluster = []
        while index < len(item) - 1:
            a, b = item[index], item[index + 1]
            c = a + b
            # print("a:", a)
            varianceA = self.getVar(a)
            varianceB = self.getVar(b)
            varianceC = self.getVar(c)
            # print("Variance a: ", varianceA)
            # print("Variance b: ", varianceB)
            # print("Variance C: ", varianceC*.95)
            # print("Variance a + b: ", (varianceA*len(a) + varianceB*len(b))/(len(a) + len(b)))
            if (varianceC*.95) <= (varianceA*len(a) + varianceB*len(b))/(len(a) + len(b)):
                # item[index] = item[index] + item[index+1]
                # item.pop(index+1)
                # print("Merge: ", item[index])
                # print("Merge: ",item[index + 1])
                possibleCluster.append(item[index] + item[index+1])
                index +=2
            else:
                possibleCluster.append(item[index])
                index += 1
        # handle last group
        if index == len(item) - 1:
            possibleCluster.append(item[index])
        # Recursive merge
        if len(possibleCluster) < len(item):
            return self.merge(possibleCluster)
        return item

    def var(self):
        return self.sd
    
    def getVar(self, listTuple):
        n = len(listTuple)
        return listTuple[ int(.9*n) ][0] - listTuple[ int(.1*n) ][0] / 2.56
    
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