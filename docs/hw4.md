## HW4: Distances
### Usage
```Shell
$ python3 tests/test_hw04.py
```
**Sample.py** </br>
```Python
# Distance calculation
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
```
```Python
# Neighbors calculation
def neighbors(self, r1, rows = {}):
        a = []
        rows = rows or self.rows
        for r2 in rows:
            a.append((self.dist(r1,r2),r2))
        return sorted(a, key=lambda tuple: tuple[0])
```
```Python
# faraway calculation
def faraway(self, r, rows):
        # shuffled = random.sample(self.rows, CONFIG['samples'])
        n = min(128,len(rows))
        shuffled = random.sample(rows, n)
        all = self.neighbors(r, shuffled)
        return all[math.floor(CONFIG['far']*n)][1]
```
```Python
# faraway calculation
def faraway(self, r):
        shuffled = random.sample(self.rows, CONFIG['samples'])
        all = self.neighbors(r, shuffled)
        # [(print(x)) for x in all]
        return all[math.floor(CONFIG['far']*len(all))][1]
```
```Python
# Divide the rows based on distances
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

def divs(self):
        leafs = []
        enough = pow(len(self.rows), CONFIG['enough'])
        self.recursive_divs(leafs, enough, self.rows, 0)
        return leafs

```

**Col.py**</br>
Contains the distance function for Sym and Num
```Python
# Sym Distance
def dist(self, x, y):
        return 0 if x == y else 1
```
```Python
# Num Distance
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
```
### **Runtime Analysis**
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
Here are the runtime result for HW4 functions </br>
1. **sample dist()**
```Shell
sample dist()
Runtime Sample Dist():  1.4781951904296875e-05  seconds
```

1. **sample nighbors()**
```Shell
sample nighbors()
Runtime Sample neighbors():  0.003120899200439453  seconds
```

1. **sample faraway()**
```Shell
sample faraway()
Runtime Sample faraway():  0.0011191368103027344  seconds
```

1. **sample divs()**
```Shell
sample divs()
Runtime Sample divs():  0.054943084716796875  seconds
```
