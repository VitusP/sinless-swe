## HW6: FFT Trees
### Usage

```Shell
$ python3 tests/test_hw06.py
```
**FFT.py** </br>

```Python
from src.hw3.col import o
from copy import deepcopy

"""
    all : Seems like a Sample.
    bin : Seems like a Col.

"""

class FFT():
    def __init__(self, all, conf, branch,branches,stop = None, level=0):

        self.my = conf
        stop = stop or 2*len(all.rows)**self.my.bins
        
        tmp = all.clone()
        for row in all.rows:
            tmp.add(row)
        tmp = tmp.divs()
        tmp = sorted(tmp)

        best, rest = tmp[0], tmp[-1]
        bins = [bin for xbest,xrest in zip(best.x, rest.x) 
                for bin in xbest.discretize(xrest, self.my)]

        bestIdea = None
        worstIdea = None
        # print("bins", bins)
        if (len(bins) > 1):
            bestIdea   = self.values("plan", bins)[-1][1]
            worstIdea  = self.values("monitor", bins)[-1][1]
        
            for yes,no,idea in [(1,0,bestIdea), (0,1,worstIdea)]:
                leaf,tree = all.clone(), all.clone()
                for row in all.rows:
                    if self.match(idea, row):
                        leaf.add(row)
                    else:
                        tree.add(row)
                b1 = deepcopy(branch)
                b1 += [o(at=idea.at, lo=idea.lo, hi=idea.hi,
                                type=yes, txt="if "+self.show(idea)+" then", 
                                then=leaf.ys(), n=len(leaf.rows))]
                print("b1: ", b1)
                if len(tree.rows) <= stop:
                    b1  += [o(type=no, txt="  ", then=tree.ys(), n= len(tree.rows))]
                    branches += [b1]
                else:
                    print("Recurse FFT")
                    FFT(tree,conf,b1,branches,stop=stop,level=level+1)
            
    
    def match(self, bin, row):
        # print("row: ", row)
        v=row[bin.at]              # Q: where does `at` come from?
        if   v=="?"   : return True      # Q: what should we do for missing values
        elif bin.first: return v <= bin.hi
        elif bin.last : return v >= bin.lo
        else          : return bin.lo <= v <= bin.hi

    def show(self,bin):
        if   bin.lo == bin.hi: return f"{bin.name} == {bin.lo}"  # Q: how we detect symbolic ranges
        elif bin.first: return f"{bin.name} <= {bin.hi}"
        elif bin.last : return f"{bin.name} >= {bin.lo}"
        else          : return f"{bin.lo} <= {bin.name} <= {bin.hi}"

    def value(self, rule, bin):
        s = self.my.support
        rules = o(plan    = lambda b,r: b**s/(b+r) if b>r else 0,  # good things to make you smile
                monitor = lambda b,r: r**s/(b+r) if r>b else 0,  # bad things to make your cry.
                novel   = lambda b,r: 1/(b+r))                   # Q: when would i select for "novel"?
        return rules[rule](bin.best/bin.bests, bin.rest/bin.rests)
  
    def values(self,rule,bins):
        bins = [(self.value(rule,bin), bin) for bin in bins]
        tmp = [(n,bin) for n,bin in bins if n > 0]
        # for val in tmp:
        #     print("values: ", val)
        return sorted(tmp, key=lambda tuple: tuple[0]) #What is the first here? It should be a sorting rule
```
```Python
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
Here are the output for HW6 functions </br>
### FFT:
Below is the result of our fft generation. We have 27 leafs in total for this experiment, and the best trees seems to be 
a 000001 tree. The best tree has Weight-,Mpg+,Acc+,N+ of 1937.1, 17.8, 34.8, and n: 21 respectively.
```
tree:  0
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 76 <= Model <= 82 then  [3096.0, 15.8, 24.2] (n: 125 )
1   if Cylinders == 4 then  [2310.1, 17.3, 24.7] (n: 17 )
1   if Cylinders == 6 then  [3178.1, 16.4, 20.0] (n: 38 )
0   if 165 <= Horsepower <= 225 then  [4384.1, 11.7, 11.6] (n: 31 )
1   else:  [4057.2, 12.9, 14.2] (n: 38 )
tree:  1
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 76 <= Model <= 82 then  [3096.0, 15.8, 24.2] (n: 125 )
1   if Cylinders == 4 then  [2310.1, 17.3, 24.7] (n: 17 )
0   if Cylinders == 8 then  [4204.1, 12.4, 13.0] (n: 69 )
1   else:  [3178.1, 16.4, 20.0] (n: 38 )
tree:  2
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 76 <= Model <= 82 then  [3096.0, 15.8, 24.2] (n: 125 )
0   if Cylinders == 8 then  [4204.1, 12.4, 13.0] (n: 69 )
1   if Cylinders == 4 then  [2310.1, 17.3, 24.7] (n: 17 )
0   else:  [3178.1, 16.4, 20.0] (n: 38 )
tree:  3
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 76 <= Model <= 82 then  [3096.0, 15.8, 24.2] (n: 125 )
0   if Cylinders == 8 then  [4204.1, 12.4, 13.0] (n: 69 )
0   if Cylinders == 6 then  [3178.1, 16.4, 20.0] (n: 38 )
1   else:  [2310.1, 17.3, 24.7] (n: 17 )
tree:  4
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
1   if 72 <= Horsepower <= 110 then  [3345.2, 17.3, 20.7] (n: 54 )
1   if Cylinders == 6 then  [3038.3, 13.8, 23.3] (n: 6 )
1   if 125 <= Horsepower <= 135 then  [3779.3, 14.8, 17.5] (n: 8 )
0   else:  [4142.4, 13.3, 17.2] (n: 32 )
tree:  5
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
1   if 72 <= Horsepower <= 110 then  [3345.2, 17.3, 20.7] (n: 54 )
1   if Cylinders == 6 then  [3038.3, 13.8, 23.3] (n: 6 )
0   if 142 <= Horsepower <= 190 then  [4219.8, 13.3, 16.5] (n: 23 )
1   else:  [3866.8, 14.1, 18.2] (n: 17 )
tree:  6
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
1   if 72 <= Horsepower <= 110 then  [3345.2, 17.3, 20.7] (n: 54 )
0   if Cylinders == 8 then  [4069.7, 13.6, 17.2] (n: 40 )
1   else:  [3038.3, 13.8, 23.3] (n: 6 )
tree:  7
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
0   if 140 <= Horsepower <= 170 then  [4120.7, 13.7, 16.7] (n: 27 )
1   if 85 <= Horsepower <= 115 then  [3320.1, 16.8, 21.1] (n: 53 )
0   else:  [3721.8, 14.9, 19.0] (n: 20 )
tree:  8
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
0   if 140 <= Horsepower <= 170 then  [4120.7, 13.7, 16.7] (n: 27 )
0   if 120 <= Horsepower <= 190 then  [3828.8, 13.7, 18.8] (n: 16 )
1   if 72 <= Horsepower <= 81 then  [3294.0, 19.8, 20.0] (n: 4 )
1   if 173 <= Displacement <= 232 then  [3231.6, 16.6, 20.9] (n: 35 )
0   else:  [3492.3, 17.2, 21.7] (n: 18 )
tree:  9
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
0   if 140 <= Horsepower <= 170 then  [4120.7, 13.7, 16.7] (n: 27 )
0   if 120 <= Horsepower <= 190 then  [3828.8, 13.7, 18.8] (n: 16 )
1   if 72 <= Horsepower <= 81 then  [3294.0, 19.8, 20.0] (n: 4 )
0   if 250 <= Displacement <= 258 then  [3551.9, 17.2, 20.0] (n: 11 )
1   if 85 <= Horsepower <= 90 then  [3178.1, 17.7, 21.7] (n: 12 )
0   else:  [3292.0, 16.3, 21.3] (n: 30 )
tree:  10
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
0   if 140 <= Horsepower <= 170 then  [4120.7, 13.7, 16.7] (n: 27 )
0   if 120 <= Horsepower <= 190 then  [3828.8, 13.7, 18.8] (n: 16 )
1   if 72 <= Horsepower <= 81 then  [3294.0, 19.8, 20.0] (n: 4 )
0   if 250 <= Displacement <= 258 then  [3551.9, 17.2, 20.0] (n: 11 )
0   if 95 <= Horsepower <= 110 then  [3360.9, 16.8, 20.8] (n: 26 )
1   else:  [3094.5, 16.7, 22.5] (n: 16 )
tree:  11
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if Cylinders == 4 then  [2475.9, 16.3, 29.2] (n: 60 )
0   if 140 <= Horsepower <= 170 then  [4120.7, 13.7, 16.7] (n: 27 )
0   if 120 <= Horsepower <= 190 then  [3828.8, 13.7, 18.8] (n: 16 )
0   if 100 <= Horsepower <= 110 then  [3448.2, 16.8, 20.7] (n: 30 )
1   else:  [3173.9, 17.3, 21.5] (n: 27 )
tree:  12
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 6 <= Cylinders <= 8 then  [3616.6, 15.6, 19.5] (n: 100 )
1   if 63 <= Horsepower <= 70 then  [2227.2, 16.2, 31.4] (n: 14 )
1   if 85 <= Displacement <= 98 then  [2094.8, 17.8, 30.0] (n: 6 )
1   if Displacement == 112 then  [2553.8, 18.1, 30.0] (n: 4 )
0   else:  [2627.4, 16.0, 28.1] (n: 36 )
tree:  13
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 6 <= Cylinders <= 8 then  [3616.6, 15.6, 19.5] (n: 100 )
1   if 63 <= Horsepower <= 70 then  [2227.2, 16.2, 31.4] (n: 14 )
1   if 85 <= Displacement <= 98 then  [2094.8, 17.8, 30.0] (n: 6 )
0   if 151 <= Displacement <= 156 then  [2736.3, 16.2, 26.9] (n: 13 )
1   else:  [2564.1, 16.1, 28.9] (n: 27 )
tree:  14
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 6 <= Cylinders <= 8 then  [3616.6, 15.6, 19.5] (n: 100 )
1   if 63 <= Horsepower <= 70 then  [2227.2, 16.2, 31.4] (n: 14 )
0   if 151 <= Displacement <= 156 then  [2736.3, 16.2, 26.9] (n: 13 )
1   else:  [2478.8, 16.4, 29.1] (n: 33 )
tree:  15
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 6 <= Cylinders <= 8 then  [3616.6, 15.6, 19.5] (n: 100 )
0   if 80 <= Horsepower <= 92 then  [2620.4, 16.2, 28.3] (n: 36 )
1   else:  [2259.1, 16.5, 30.4] (n: 24 )
tree:  16
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if Cylinders == 4 then  [2330.0, 16.7, 28.9] (n: 63 )
0   else:  [3262.9, 17.4, 25.7] (n: 7 )
tree:  17
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 97 <= Displacement <= 183 then  [2574.8, 16.7, 27.1] (n: 51 )
1   else:  [2016.7, 17.1, 32.6] (n: 19 )
tree:  18
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if 46 <= Horsepower <= 70 then  [2115.0, 18.9, 33.2] (n: 22 )
1   if 89 <= Displacement <= 101 then  [2116.8, 14.9, 30.0] (n: 13 )
0   else:  [2730.9, 16.2, 25.1] (n: 35 )
tree:  19
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if 46 <= Horsepower <= 70 then  [2115.0, 18.9, 33.2] (n: 22 )
0   if 121 <= Displacement <= 168 then  [2924.8, 16.0, 23.9] (n: 18 )
1   else:  [2348.5, 15.7, 28.0] (n: 30 )
tree:  20
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if 95 <= Horsepower <= 120 then  [2715.3, 15.1, 24.0] (n: 15 )
1   if 79 <= Displacement <= 90 then  [2019.8, 17.0, 32.0] (n: 15 )
1   if 70 <= Model <= 73 then  [2260.6, 17.9, 25.7] (n: 14 )
0   else:  [2575.2, 17.0, 30.8] (n: 26 )
tree:  21
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if 95 <= Horsepower <= 120 then  [2715.3, 15.1, 24.0] (n: 15 )
1   if 79 <= Displacement <= 90 then  [2019.8, 17.0, 32.0] (n: 15 )
0   if 78 <= Model <= 81 then  [2847.1, 17.7, 31.5] (n: 13 )
1   else:  [2281.2, 17.1, 27.8] (n: 27 )
tree:  22
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if 95 <= Horsepower <= 120 then  [2715.3, 15.1, 24.0] (n: 15 )
0   if 97 <= Displacement <= 183 then  [2497.8, 17.3, 28.6] (n: 37 )
1   else:  [2026.8, 17.1, 32.2] (n: 18 )
tree:  23
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if Cylinders == 4 then  [2153.5, 16.6, 31.3] (n: 69 )
0   else:  [2688.6, 13.4, 22.0] (n: 10 )
tree:  24
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 119 <= Displacement <= 168 then  [2622.7, 14.7, 26.2] (n: 21 )
1   if 52 <= Horsepower <= 65 then  [1909.9, 17.9, 35.6] (n: 18 )
1   if 91 <= Displacement <= 108 then  [2142.2, 16.4, 31.1] (n: 28 )
0   else:  [2170.0, 15.6, 26.7] (n: 12 )
tree:  25
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 119 <= Displacement <= 168 then  [2622.7, 14.7, 26.2] (n: 21 )
1   if 52 <= Horsepower <= 65 then  [1909.9, 17.9, 35.6] (n: 18 )
0   if 68 <= Horsepower <= 110 then  [2190.7, 16.1, 28.7] (n: 32 )
1   else:  [1990.0, 16.5, 33.8] (n: 8 )
tree:  26
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 119 <= Displacement <= 168 then  [2622.7, 14.7, 26.2] (n: 21 )
0   if 92 <= Horsepower <= 110 then  [2378.4, 14.8, 23.3] (n: 9 )
1   if 78 <= Displacement <= 85 then  [1960.3, 18.2, 34.5] (n: 11 )
0   else:  [2037.7, 16.7, 32.6] (n: 38 )
tree:  27
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 119 <= Displacement <= 168 then  [2622.7, 14.7, 26.2] (n: 21 )
0   if 92 <= Horsepower <= 110 then  [2378.4, 14.8, 23.3] (n: 9 )
0   if 91 <= Displacement <= 108 then  [2082.7, 16.5, 31.8] (n: 28 )
1   else:  [1937.1, 17.8, 34.8] (n: 21 )
```
