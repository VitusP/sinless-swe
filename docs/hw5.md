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
            print("Variance a: ", varianceA)
            print("Variance b: ", varianceB)
            print("Variance C: ", varianceC*.95)
            print("Variance a + b: ", (varianceA*len(a) + varianceB*len(b))/(len(a) + len(b)))
            if (varianceC*.95) <= (varianceA*len(a) + varianceB*len(b))/(len(a) + len(b)):
                # item[index] = item[index] + item[index+1]
                # item.pop(index+1)
                print("Merge: ", item[index])
                print("Merge: ",item[index + 1])
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
|..  n= 398 c=0.64
|.. |..  n= 199 c=0.51
|.. |.. |..  n= 99 c=0.37
|.. |.. |.. |..  n= 49 c=0.25
|.. |.. |.. |.. |..  n= 24 c=0.27
|.. |.. |.. |.. |.. |..  n= 12 goal= [2335.3, 17.2, 23.3]
|.. |.. |.. |.. |.. |..  n= 12 goal= [3003.0, 17.0, 20.0]
|.. |.. |.. |.. |..  n= 25 c=0.18
|.. |.. |.. |.. |.. |..  n= 12 goal= [3237.2, 16.7, 20.0]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2926.1, 14.9, 20.0]
|.. |.. |.. |..  n= 50 c=0.43
|.. |.. |.. |.. |..  n= 25 c=0.19
|.. |.. |.. |.. |.. |..  n= 12 goal= [3283.5, 17.4, 20.8]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3545.6, 18.3, 20.0]
|.. |.. |.. |.. |..  n= 25 c=0.43
|.. |.. |.. |.. |.. |..  n= 12 goal= [3020.8, 15.3, 24.2]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3369.6, 16.5, 20.0]
|.. |.. |..  n= 100 c=0.31
|.. |.. |.. |..  n= 50 c=0.23
|.. |.. |.. |.. |..  n= 25 c=0.19
|.. |.. |.. |.. |.. |..  n= 12 goal= [4425.3, 10.7, 11.7]
|.. |.. |.. |.. |.. |..  n= 13 goal= [4630.5, 13.2, 10.0]
|.. |.. |.. |.. |..  n= 25 c=0.16
|.. |.. |.. |.. |.. |..  n= 12 goal= [3692.8, 10.8, 18.3]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3987.7, 12.4, 11.5]
|.. |.. |.. |..  n= 50 c=0.22
|.. |.. |.. |.. |..  n= 25 c=0.18
|.. |.. |.. |.. |.. |..  n= 12 goal= [4138.9, 12.3, 15.8]
|.. |.. |.. |.. |.. |..  n= 13 goal= [4105.5, 14.0, 11.5]
|.. |.. |.. |.. |..  n= 25 c=0.16
|.. |.. |.. |.. |.. |..  n= 12 goal= [4227.7, 13.9, 19.2]
|.. |.. |.. |.. |.. |..  n= 13 goal= [3852.4, 14.7, 20.0]
|.. |..  n= 199 c=0.49
|.. |.. |..  n= 99 c=0.41
|.. |.. |.. |..  n= 49 c=0.40
|.. |.. |.. |.. |..  n= 24 c=0.19
|.. |.. |.. |.. |.. |..  n= 12 goal= [1938.9, 17.9, 30.8]
|.. |.. |.. |.. |.. |..  n= 12 goal= [2238.0, 16.0, 25.8]
|.. |.. |.. |.. |..  n= 25 c=0.42
|.. |.. |.. |.. |.. |..  n= 12 goal= [2576.9, 15.0, 20.8]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2192.3, 16.3, 28.5]
|.. |.. |.. |..  n= 50 c=0.31
|.. |.. |.. |.. |..  n= 25 c=0.27
|.. |.. |.. |.. |.. |..  n= 12 goal= [2237.4, 18.8, 37.5]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2027.8, 16.1, 29.2]
|.. |.. |.. |.. |..  n= 25 c=0.38
|.. |.. |.. |.. |.. |..  n= 12 goal= [2732.3, 18.1, 29.2]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2593.8, 15.8, 23.8]
|.. |.. |..  n= 100 c=0.40
|.. |.. |.. |..  n= 50 c=0.28
|.. |.. |.. |.. |..  n= 25 c=0.20
|.. |.. |.. |.. |.. |..  n= 12 goal= [1965.2, 17.1, 40.8]
|.. |.. |.. |.. |.. |..  n= 13 goal= [1985.4, 17.0, 33.1]
|.. |.. |.. |.. |..  n= 25 c=0.25
|.. |.. |.. |.. |.. |..  n= 12 goal= [2680.5, 13.9, 25.0]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2275.8, 15.9, 32.3]
|.. |.. |.. |..  n= 50 c=0.22
|.. |.. |.. |.. |..  n= 25 c=0.17
|.. |.. |.. |.. |.. |..  n= 12 goal= [2435.0, 17.9, 32.5]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2550.0, 14.8, 30.0]
|.. |.. |.. |.. |..  n= 25 c=0.21
|.. |.. |.. |.. |.. |..  n= 12 goal= [2198.9, 16.9, 29.2]
|.. |.. |.. |.. |.. |..  n= 13 goal= [2558.8, 15.7, 29.2]
```
### Sorted Goals:
```Shell
#Lbs-,   Acc+, Mpg+
[1965.2, 17.1, 40.8]
[2237.4, 18.8, 37.5]
[1938.9, 17.9, 30.8]
[1985.4, 17.0, 33.1]
[2435.0, 17.9, 32.5]
[2027.8, 16.1, 29.2]
[2275.8, 15.9, 32.3]
[2198.9, 16.9, 29.2]
[2192.3, 16.3, 28.5]
[2732.3, 18.1, 29.2]
[2238.0, 16.0, 25.8]
[2558.8, 15.7, 29.2]
[2335.3, 17.2, 23.3]
[2550.0, 14.8, 30.0]
[2593.8, 15.8, 23.8]
[2576.9, 15.0, 20.8]
[2680.5, 13.9, 25.0]
[3003.0, 17.0, 20.0]
[3020.8, 15.3, 24.2]
[3237.2, 16.7, 20.0]
[2926.1, 14.9, 20.0]
[3283.5, 17.4, 20.8]
[3545.6, 18.3, 20.0]
[3369.6, 16.5, 20.0]
[3852.4, 14.7, 20.0]
[4227.7, 13.9, 19.2]
[3692.8, 10.8, 18.3]
[4105.5, 14.0, 11.5]
[4138.9, 12.3, 15.8]
[3987.7, 12.4, 11.5]
[4630.5, 13.2, 10.0]
[4425.3, 10.7, 11.7]
```
### Discretization
```Shell
{:at 1, :name Displacement, :lo 79, :hi 86, :best 6, :rest 0}
{:at 1, :name Displacement, :lo 89, :hi 91, :best 6, :rest 0}
{:at 1, :name Displacement, :lo 360, :hi 455, :best 0, :rest 12}

{:at 2, :name Horsepower, :lo 58, :hi 68, :best 12, :rest 0}
{:at 2, :name Horsepower, :lo 190, :hi 230, :best 0, :rest 12}

{:at 5, :name Model, :lo 70, :hi 73, :best 0, :rest 12}
{:at 5, :name Model, :lo 80, :hi 82, :best 12, :rest 0}

{:at 6, :name origin, :lo 1, :hi 1, :best 0, :rest 12}
{:at 6, :name origin, :lo 3, :hi 3, :best 12, :rest 0}
```
### Best, Rest rows:
```Shell
worst:  [4425.3, 10.7, 11.7]
[8, 400, 230, 4278, 9.5, 73, '1', 20]
[8, 455, 225, 3086, 10, 70, '1', 10]
[8, 454, 220, 4354, 9, 70, '1', 10]
[8, 455, 225, 4425, 10, 70, '1', 10]
[8, 455, 225, 4951, 11, 73, '1', 10]
[8, 440, 215, 4312, 8.5, 70, '1', 10]
[8, 429, 198, 4341, 10, 70, '1', 20]
[8, 440, 215, 4735, 11, 73, '1', 10]
[8, 429, 208, 4633, 11, 72, '1', 10]
[8, 429, 198, 4952, 11.5, 73, '1', 10]
[8, 360, 215, 4615, 14, 70, '1', 10]
[8, 400, 190, 4422, 12.5, 72, '1', 10]
best:  [1965.2, 17.1, 40.8]
[4, 86, 65, 2110, 17.9, 80, '3', 50]
[4, 91, 68, 2025, 18.2, 82, '3', 40]
[4, 91, 67, 1995, 16.2, 82, '3', 40]
[4, 85, 65, 1975, 19.4, 81, '3', 40]
[4, 91, 67, 1965, 15, 82, '3', 40]
[4, 89, 62, 2050, 17.3, 81, '3', 40]
[4, 79, 58, 1755, 16.9, 81, '3', 40]
[4, 81, 60, 1760, 16.1, 81, '3', 40]
[4, 85, 65, 2110, 19.2, 80, '3', 40]
[4, 89, 60, 1968, 18.8, 80, '3', 40]
[4, 86, 65, 2019, 16.4, 80, '3', 40]
[4, 91, 67, 1850, 13.8, 80, '3', 40]
```