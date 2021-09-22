## HW5: Discretization
### Usage
```Shell
$ python3 tests/test_hw05.py
```
**Sample.py** </br>
```Python
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

class Sample():
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
```

**Col.py**</br>
```Python
class Sym(Col):
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
```
```Python
class Num(Col):
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

        xys_size = len(xys)-1
        
        start = 0
        end = 0

        while start <= xys_size and end <= xys_size:
            if((xys_size <= end or xys[end][0] != xys[end + 1][0]) and (abs(end-start) > iota) and (xys_size - end > myBinSize)):
                start = end + 1
                end = start + 1
                listSplit.append(xys[start:end + 1])
            elif end < len(xys):
                end += 1
            else:
                start += 1

        listSplit.append(xys[start:])

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
```
```Python
class o:
  """`o` is just a class that can print itself (hiding "private" keys)
  and which can hold methods."""
  def __init__(self, **d)  : self.__dict__.update(d)
  def __repr__(self) : return "{"+ ', '.join( 
    [f":{k} {v}" for k, v in self.__dict__.items() if  k[0] != "_"])+"}"
```

### **Discretization Output**
Data used: ```auto93.csv```</br>
```csv
Cylinders,Displacement,Horsepower,Weight-,Acceleration+,Model,Origin,Mpg+
8,304,193,4732,18.5,70,1,10
8,360,215,4615,14,70,1,10
8,307,200,4376,15,70,1,10
8,318,210,4382,13.5,70,1,10
8,429,208,4633,11,72,1,10
....
4,90,48,2335,23.7,80,2,40
4,97,52,2130,24.6,82,2,40
4,90,48,2085,21.7,80,2,40
4,91,67,1850,13.8,80,3,40
4,86,65,2110,17.9,80,3,50
```
Here are the output for HW5 functions </br>
### Dendogram:
```Shell
|..  n= 398 c=0.63
|.. |..  n= 199 c=0.48
|.. |.. |..  n= 99 c=0.47
|.. |.. |.. |..  n= 49 c=0.42
|.. |.. |.. |.. |..  n= 24 c=0.40
|.. |.. |.. |.. |.. |..  n= 12 goal= [2064.1, 18.5, 30.0]
|.. |.. |.. |.. |.. |..  n= 12 goal= [2487.6, 15.2, 22.5]
|.. |.. |.. |.. |..  n= 25 c=0.18
|.. |.. |.. |.. |.. |..  n= 12 goal= [2364.3, 15.0, 22.5]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2012.2, 17.6, 29.2]
|.. |.. |.. |..  n= 50 c=0.36
|.. |.. |.. |.. |..  n= 25 c=0.30
|.. |.. |.. |.. |.. |..  n= 12 goal= [2356.7, 17.9, 30.0]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2667.2, 19.7, 35.4]
|.. |.. |.. |.. |..  n= 25 c=0.29
|.. |.. |.. |.. |.. |..  n= 12 goal= [2737.8, 15.1, 24.2]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2051.8, 14.6, 30.0]
|.. |.. |..  n= 100 c=0.40
|.. |.. |.. |..  n= 50 c=0.27
|.. |.. |.. |.. |..  n= 25 c=0.26
|.. |.. |.. |.. |.. |..  n= 12 goal= [2661.1, 14.8, 28.3]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2239.6, 15.8, 26.9]
|.. |.. |.. |.. |..  n= 25 c=0.15
|.. |.. |.. |.. |.. |..  n= 12 goal= [2077.0, 15.7, 36.7]
|.. |.. |.. |.. |.. |..  n= 13 goal= [1988.2, 17.8, 38.5]
|.. |.. |.. |..  n= 50 c=0.23
|.. |.. |.. |.. |..  n= 25 c=0.24
|.. |.. |.. |.. |.. |..  n= 12 goal= [2635.4, 18.8, 26.7]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2704.2, 17.0, 28.5]
|.. |.. |.. |.. |..  n= 25 c=0.19
|.. |.. |.. |.. |.. |..  n= 12 goal= [2094.7, 15.4, 32.5]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2366.2, 14.6, 31.5]
|.. |..  n= 199 c=0.49
|.. |.. |..  n= 99 c=0.32
|.. |.. |.. |..  n= 49 c=0.21
|.. |.. |.. |.. |..  n= 24 c=0.22
|.. |.. |.. |.. |.. |..  n= 12 goal= [4266.1, 13.6, 13.3]
|.. |.. |.. |.. |.. |..  n= 12 goal= [3854.8, 13.2, 17.5]
|.. |.. |.. |.. |..  n= 25 c=0.15
|.. |.. |.. |.. |.. |..  n= 12 goal= [4005.7, 13.1, 20.0]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3875.9, 14.6, 17.7]
|.. |.. |.. |..  n= 50 c=0.24
|.. |.. |.. |.. |..  n= 25 c=0.17
|.. |.. |.. |.. |.. |..  n= 12 goal= [4611.3, 10.8, 10.8]
|.. |.. |.. |.. |.. |..  n= 13 goal= [4470.2, 12.4, 11.5]
|.. |.. |.. |.. |..  n= 25 c=0.19
|.. |.. |.. |.. |.. |..  n= 12 goal= [4345.8, 13.8, 10.0]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3707.5, 10.6, 16.2]
|.. |.. |..  n= 100 c=0.40
|.. |.. |.. |..  n= 50 c=0.36
|.. |.. |.. |.. |..  n= 25 c=0.28
|.. |.. |.. |.. |.. |..  n= 12 goal= [2500.9, 17.2, 24.2]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2440.4, 15.4, 22.3]
|.. |.. |.. |.. |..  n= 25 c=0.18
|.. |.. |.. |.. |.. |..  n= 12 goal= [3090.6, 15.4, 20.0]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3251.8, 17.2, 20.0]
|.. |.. |.. |..  n= 50 c=0.29
|.. |.. |.. |.. |..  n= 25 c=0.21
|.. |.. |.. |.. |.. |..  n= 12 goal= [3506.4, 18.8, 20.8]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3480.2, 17.5, 20.0]
|.. |.. |.. |.. |..  n= 25 c=0.28
|.. |.. |.. |.. |.. |..  n= 12 goal= [3029.2, 15.4, 24.2]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3202.6, 15.5, 20.0]
```
### Sorted Goals:
```Shell
#Lbs-,   Acc+, Mpg+
[1988.2, 17.8, 38.5]
[2077.0, 15.7, 36.7]
[2667.2, 19.7, 35.4]
[2064.1, 18.5, 30.0]
[2012.2, 17.6, 29.2]
[2094.7, 15.4, 32.5]
[2356.7, 17.9, 30.0]
[2051.8, 14.6, 30.0]
[2366.2, 14.6, 31.5]
[2635.4, 18.8, 26.7]
[2239.6, 15.8, 26.9]
[2704.2, 17.0, 28.5]
[2500.9, 17.2, 24.2]
[2661.1, 14.8, 28.3]
[2364.3, 15.0, 22.5]
[2440.4, 15.4, 22.3]
[2487.6, 15.2, 22.5]
[2737.8, 15.1, 24.2]
[3029.2, 15.4, 24.2]
[3251.8, 17.2, 20.0]
[3090.6, 15.4, 20.0]
[3506.4, 18.8, 20.8]
[3480.2, 17.5, 20.0]
[3202.6, 15.5, 20.0]
[3875.9, 14.6, 17.7]
[3854.8, 13.2, 17.5]
[4005.7, 13.1, 20.0]
[3707.5, 10.6, 16.2]
[4266.1, 13.6, 13.3]
[4345.8, 13.8, 10.0]
[4470.2, 12.4, 11.5]
[4611.3, 10.8, 10.8]
```
### Discretization
```Shell
{:at 1, :name Displacement, :lo 86, :hi 86, :best 2, :rest 0}
{:at 1, :name Displacement, :lo 383, :hi 400, :best 0, :rest 2}
{:at 1, :name Displacement, :lo 429, :hi 440, :best 0, :rest 2}
{:at 1, :name Displacement, :lo 429, :hi 455, :best 0, :rest 6}

{:at 2, :name Horsepower, :lo 65, :hi 65, :best 2, :rest 0}
{:at 2, :name Horsepower, :lo 67, :hi 67, :best 2, :rest 0}
{:at 2, :name Horsepower, :lo 180, :hi 190, :best 0, :rest 2}
{:at 2, :name Horsepower, :lo 180, :hi 230, :best 0, :rest 9}

{:at 5, :name Model, :lo 71, :hi 71, :best 0, :rest 2}
{:at 5, :name Model, :lo 72, :hi 72, :best 0, :rest 2}
{:at 5, :name Model, :lo 73, :hi 73, :best 0, :rest 2}
{:at 5, :name Model, :lo 78, :hi 78, :best 2, :rest 0}
{:at 5, :name Model, :lo 79, :hi 80, :best 2, :rest 0}
{:at 5, :name Model, :lo 79, :hi 81, :best 11, :rest 0}

{:at 6, :name origin, :lo 3, :hi 3, :best 13, :rest 0}
{:at 6, :name origin, :lo 1, :hi 1, :best 0, :rest 12}
```
### Best, Rest rows:
```Shell
worst:  [4611.3, 10.8, 10.8]
[8, 454, 220, 4354, 9, 70, '1', 10]
[8, 440, 215, 4312, 8.5, 70, '1', 10]
[8, 455, 225, 4425, 10, 70, '1', 10]
[8, 429, 208, 4633, 11, 72, '1', 10]
[8, 455, 225, 4951, 11, 73, '1', 10]
[8, 440, 215, 4735, 11, 73, '1', 10]
[8, 383, 180, 4955, 11.5, 71, '1', 10]
[8, 400, 170, 4746, 12, 71, '1', 10]
[8, 400, 190, 4422, 12.5, 72, '1', 10]
[8, 400, 175, 5140, 12, 71, '1', 10]
[8, 400, 230, 4278, 9.5, 73, '1', 20]
[8, 400, 175, 4385, 12, 72, '1', 10]
best:  [1988.2, 17.8, 38.5]
[4, 81, 60, 1760, 16.1, 81, '3', 40]
[4, 89, 62, 2050, 17.3, 81, '3', 40]
[4, 79, 58, 1755, 16.9, 81, '3', 40]
[4, 97, 67, 2065, 17.8, 81, '3', 30]
[4, 86, 65, 2019, 16.4, 80, '3', 40]
[4, 85, 65, 1975, 19.4, 81, '3', 40]
[4, 97, 67, 2145, 18, 80, '3', 30]
[4, 86, 65, 2110, 17.9, 80, '3', 50]
[4, 89, 60, 1968, 18.8, 80, '3', 40]
[4, 85, 65, 2110, 19.2, 80, '3', 40]
[4, 91, 60, 1800, 16.4, 78, '3', 40]
[4, 85, 65, 2020, 19.2, 79, '3', 30]
[4, 85, 70, 2070, 18.6, 78, '3', 40]
```