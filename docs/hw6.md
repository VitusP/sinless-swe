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
```
tree:  0
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
1   if 72 <= Horsepower <= 110 then  [3256.1, 16.7, 20.0] (n: 61 )
1   if 231 <= Displacement <= 318 then  [3926.3, 13.5, 15.9] (n: 41 )
1   if 350 <= Displacement <= 360 then  [4256.2, 12.8, 12.5] (n: 24 )
0   else:  [4405.5, 10.9, 13.1] (n: 26 )
tree:  1
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
1   if 72 <= Horsepower <= 110 then  [3256.1, 16.7, 20.0] (n: 61 )
1   if 231 <= Displacement <= 318 then  [3926.3, 13.5, 15.9] (n: 41 )
0   if 400 <= Displacement <= 455 then  [4480.2, 11.1, 12.7] (n: 22 )
1   else:  [4218.8, 12.3, 12.9] (n: 28 )
tree:  2
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
1   if 72 <= Horsepower <= 110 then  [3256.1, 16.7, 20.0] (n: 61 )
0   if 360 <= Displacement <= 455 then  [4429.4, 11.2, 12.9] (n: 28 )
1   if 120 <= Horsepower <= 150 then  [3961.4, 13.3, 15.9] (n: 44 )
0   else:  [4176.2, 12.8, 12.1] (n: 19 )
tree:  3
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
1   if 72 <= Horsepower <= 110 then  [3256.1, 16.7, 20.0] (n: 61 )
0   if 360 <= Displacement <= 455 then  [4429.4, 11.2, 12.9] (n: 28 )
0   if 160 <= Horsepower <= 210 then  [4141.7, 12.7, 12.9] (n: 14 )
1   if 120 <= Horsepower <= 140 then  [3863.4, 13.6, 16.5] (n: 17 )
0   else:  [4062.1, 13.1, 14.7] (n: 32 )
tree:  4
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
1   if 72 <= Horsepower <= 110 then  [3256.1, 16.7, 20.0] (n: 61 )
0   if 360 <= Displacement <= 455 then  [4429.4, 11.2, 12.9] (n: 28 )
0   if 160 <= Horsepower <= 210 then  [4141.7, 12.7, 12.9] (n: 14 )
0   if 145 <= Horsepower <= 153 then  [4037.4, 13.1, 15.0] (n: 30 )
1   else:  [3923.3, 13.6, 15.8] (n: 19 )
tree:  5
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
0   if 167 <= Horsepower <= 225 then  [4354.4, 11.9, 12.7] (n: 33 )
1   if Cylinders == 6 then  [3253.5, 16.6, 20.0] (n: 59 )
1   if 72 <= Model <= 78 then  [4065.9, 13.5, 15.0] (n: 50 )
0   else:  [3734.4, 11.3, 16.0] (n: 10 )
tree:  6
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
0   if 167 <= Horsepower <= 225 then  [4354.4, 11.9, 12.7] (n: 33 )
1   if Cylinders == 6 then  [3253.5, 16.6, 20.0] (n: 59 )
0   if 70 <= Model <= 71 then  [3734.4, 11.3, 16.0] (n: 10 )
1   if 74 <= Model <= 78 then  [4016.2, 13.9, 16.2] (n: 29 )
0   else:  [4134.7, 13.0, 13.3] (n: 21 )
tree:  7
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
0   if 167 <= Horsepower <= 225 then  [4354.4, 11.9, 12.7] (n: 33 )
1   if Cylinders == 6 then  [3253.5, 16.6, 20.0] (n: 59 )
0   if 70 <= Model <= 71 then  [3734.4, 11.3, 16.0] (n: 10 )
0   if 72 <= Model <= 73 then  [4134.7, 13.0, 13.3] (n: 21 )
1   else:  [4016.2, 13.9, 16.2] (n: 29 )
tree:  8
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
0   if 167 <= Horsepower <= 225 then  [4354.4, 11.9, 12.7] (n: 33 )
0   if Cylinders == 8 then  [4010.7, 13.1, 15.2] (n: 60 )
1   if 70 <= Model <= 73 then  [2986.7, 15.4, 20.0] (n: 19 )
1   if 200 <= Displacement <= 225 then  [3369.0, 17.2, 20.0] (n: 12 )
0   else:  [3385.1, 17.2, 20.0] (n: 28 )
tree:  9
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
0   if 167 <= Horsepower <= 225 then  [4354.4, 11.9, 12.7] (n: 33 )
0   if Cylinders == 8 then  [4010.7, 13.1, 15.2] (n: 60 )
1   if 70 <= Model <= 73 then  [2986.7, 15.4, 20.0] (n: 19 )
0   if 105 <= Horsepower <= 110 then  [3553.9, 17.3, 20.0] (n: 14 )
1   else:  [3286.8, 17.2, 20.0] (n: 26 )
tree:  10
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
0   if 167 <= Horsepower <= 225 then  [4354.4, 11.9, 12.7] (n: 33 )
0   if Cylinders == 8 then  [4010.7, 13.1, 15.2] (n: 60 )
0   if 74 <= Model <= 77 then  [3399.7, 17.4, 20.0] (n: 30 )
1   else:  [3102.3, 15.8, 20.0] (n: 29 )
tree:  11
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
0   if Cylinders == 8 then  [4146.3, 12.6, 14.2] (n: 92 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
1   if 72 <= Horsepower <= 98 then  [3112.3, 17.0, 20.0] (n: 25 )
0   else:  [3343.6, 16.3, 20.0] (n: 35 )
tree:  12
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
0   if Cylinders == 8 then  [4146.3, 12.6, 14.2] (n: 92 )
1   if Cylinders == 4 then  [2336.6, 16.9, 26.5] (n: 34 )
0   if 100 <= Horsepower <= 105 then  [3300.7, 16.3, 20.0] (n: 25 )
1   else:  [3209.0, 16.8, 20.0] (n: 35 )
tree:  13
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
1   if 79 <= Model <= 82 then  [2879.1, 16.0, 27.0] (n: 63 )
0   if Cylinders == 8 then  [4146.3, 12.6, 14.2] (n: 92 )
0   if 90 <= Horsepower <= 165 then  [3176.9, 16.5, 20.7] (n: 56 )
1   else:  [2536.0, 17.0, 24.7] (n: 38 )
tree:  14
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if 85 <= Displacement <= 151 then  [2460.8, 16.4, 29.3] (n: 56 )
1   if 156 <= Displacement <= 318 then  [3452.0, 16.0, 20.1] (n: 87 )
0   else:  [4240.8, 13.6, 18.2] (n: 17 )
tree:  15
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if 85 <= Displacement <= 151 then  [2460.8, 16.4, 29.3] (n: 56 )
0   if Cylinders == 8 then  [4012.9, 14.1, 17.8] (n: 45 )
1   if 156 <= Displacement <= 173 then  [2719.2, 13.9, 26.2] (n: 8 )
1   if 181 <= Displacement <= 232 then  [3269.1, 16.9, 20.3] (n: 35 )
0   else:  [3478.8, 17.7, 21.2] (n: 16 )
tree:  16
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if 85 <= Displacement <= 151 then  [2460.8, 16.4, 29.3] (n: 56 )
0   if Cylinders == 8 then  [4012.9, 14.1, 17.8] (n: 45 )
1   if 156 <= Displacement <= 173 then  [2719.2, 13.9, 26.2] (n: 8 )
0   if 250 <= Displacement <= 262 then  [3478.8, 17.7, 21.2] (n: 16 )
1   else:  [3269.1, 16.9, 20.3] (n: 35 )
tree:  17
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
1   if 85 <= Displacement <= 151 then  [2460.8, 16.4, 29.3] (n: 56 )
0   if Cylinders == 8 then  [4012.9, 14.1, 17.8] (n: 45 )
0   if 181 <= Displacement <= 250 then  [3328.2, 17.2, 20.2] (n: 46 )
1   else:  [2979.5, 15.2, 25.4] (n: 13 )
tree:  18
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 138 <= Horsepower <= 180 then  [4015.6, 13.7, 17.4] (n: 34 )
1   if Cylinders == 4 then  [2458.8, 16.3, 29.5] (n: 58 )
1   if 225 <= Displacement <= 250 then  [3402.2, 17.3, 20.0] (n: 36 )
0   else:  [3393.6, 15.9, 21.3] (n: 32 )
tree:  19
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 138 <= Horsepower <= 180 then  [4015.6, 13.7, 17.4] (n: 34 )
1   if Cylinders == 4 then  [2458.8, 16.3, 29.5] (n: 58 )
0   if 258 <= Displacement <= 304 then  [3578.1, 16.1, 20.0] (n: 15 )
1   if Cylinders == 6 then  [3287.1, 16.9, 20.6] (n: 48 )
0   else:  [3924.0, 15.8, 22.0] (n: 5 )
tree:  20
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 138 <= Horsepower <= 180 then  [4015.6, 13.7, 17.4] (n: 34 )
1   if Cylinders == 4 then  [2458.8, 16.3, 29.5] (n: 58 )
0   if 258 <= Displacement <= 304 then  [3578.1, 16.1, 20.0] (n: 15 )
0   if Cylinders == 8 then  [3924.0, 15.8, 22.0] (n: 5 )
1   if 77 <= Model <= 82 then  [3217.8, 16.5, 21.2] (n: 25 )
0   else:  [3362.4, 17.2, 20.0] (n: 23 )
tree:  21
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 138 <= Horsepower <= 180 then  [4015.6, 13.7, 17.4] (n: 34 )
1   if Cylinders == 4 then  [2458.8, 16.3, 29.5] (n: 58 )
0   if 258 <= Displacement <= 304 then  [3578.1, 16.1, 20.0] (n: 15 )
0   if Cylinders == 8 then  [3924.0, 15.8, 22.0] (n: 5 )
0   if 74 <= Model <= 76 then  [3362.4, 17.2, 20.0] (n: 23 )
1   else:  [3217.8, 16.5, 21.2] (n: 25 )
tree:  22
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 138 <= Horsepower <= 180 then  [4015.6, 13.7, 17.4] (n: 34 )
0   if 6 <= Cylinders <= 8 then  [3398.1, 16.6, 20.6] (n: 68 )
1   if 86 <= Displacement <= 98 then  [2083.5, 16.8, 32.3] (n: 13 )
1   if 85 <= Displacement <= 122 then  [2380.7, 16.7, 30.6] (n: 16 )
0   else:  [2670.2, 15.9, 27.6] (n: 29 )
tree:  23
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 138 <= Horsepower <= 180 then  [4015.6, 13.7, 17.4] (n: 34 )
0   if 6 <= Cylinders <= 8 then  [3398.1, 16.6, 20.6] (n: 68 )
1   if 86 <= Displacement <= 98 then  [2083.5, 16.8, 32.3] (n: 13 )
0   if 80 <= Horsepower <= 96 then  [2627.4, 16.2, 28.5] (n: 33 )
1   else:  [2402.0, 16.1, 29.2] (n: 12 )
tree:  24
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
1   if origin == 2 then  [2423.3, 16.8, 28.6] (n: 70 )
0   if 70 <= Model <= 73 then  [3673.1, 13.5, 15.8] (n: 89 )
0   if 138 <= Horsepower <= 180 then  [4015.6, 13.7, 17.4] (n: 34 )
0   if 6 <= Cylinders <= 8 then  [3398.1, 16.6, 20.6] (n: 68 )
0   if 105 <= Displacement <= 156 then  [2579.4, 16.0, 28.6] (n: 44 )
1   else:  [2080.0, 17.2, 32.1] (n: 14 )
tree:  25
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if 68 <= Displacement <= 97 then  [2026.3, 17.4, 31.7] (n: 29 )
1   if 98 <= Displacement <= 122 then  [2521.2, 15.7, 26.8] (n: 31 )
0   else:  [3271.0, 18.4, 25.0] (n: 10 )
tree:  26
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if 68 <= Displacement <= 97 then  [2026.3, 17.4, 31.7] (n: 29 )
0   if 131 <= Displacement <= 168 then  [3253.8, 18.6, 25.0] (n: 8 )
1   else:  [2570.8, 15.8, 26.7] (n: 33 )
tree:  27
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 116 <= Displacement <= 168 then  [2844.4, 16.6, 24.8] (n: 27 )
1   if 75 <= Model <= 82 then  [2154.0, 16.5, 33.2] (n: 25 )
0   else:  [2165.7, 17.4, 27.8] (n: 18 )
tree:  28
1   if origin == 3 then  [2221.2, 16.2, 30.1] (n: 79 )
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 116 <= Displacement <= 168 then  [2844.4, 16.6, 24.8] (n: 27 )
0   if 70 <= Model <= 74 then  [2165.7, 17.4, 27.8] (n: 18 )
1   else:  [2154.0, 16.5, 33.2] (n: 25 )
tree:  29
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
1   if Cylinders == 4 then  [2237.7, 16.6, 30.2] (n: 132 )
0   else:  [2925.1, 15.1, 23.5] (n: 17 )
tree:  30
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 134 <= Displacement <= 168 then  [2980.3, 15.9, 25.0] (n: 18 )
1   if origin == 3 then  [2132.8, 16.5, 31.0] (n: 68 )
1   if 48 <= Horsepower <= 69 then  [2096.7, 19.0, 34.4] (n: 16 )
1   if 46 <= Horsepower <= 81 then  [2150.7, 15.8, 29.6] (n: 23 )
0   else:  [2642.4, 15.6, 24.6] (n: 24 )
tree:  31
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 134 <= Displacement <= 168 then  [2980.3, 15.9, 25.0] (n: 18 )
1   if origin == 3 then  [2132.8, 16.5, 31.0] (n: 68 )
1   if 48 <= Horsepower <= 69 then  [2096.7, 19.0, 34.4] (n: 16 )
0   if 87 <= Horsepower <= 115 then  [2692.0, 15.5, 23.8] (n: 21 )
1   else:  [2167.3, 15.8, 29.6] (n: 26 )
tree:  32
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 134 <= Displacement <= 168 then  [2980.3, 15.9, 25.0] (n: 18 )
1   if origin == 3 then  [2132.8, 16.5, 31.0] (n: 68 )
0   if 105 <= Displacement <= 131 then  [2615.3, 15.6, 25.2] (n: 27 )
1   else:  [2106.1, 17.2, 31.7] (n: 36 )
tree:  33
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 134 <= Displacement <= 168 then  [2980.3, 15.9, 25.0] (n: 18 )
0   if origin == 2 then  [2324.3, 16.5, 28.9] (n: 63 )
1   if Cylinders == 4 then  [2116.2, 16.7, 31.7] (n: 64 )
0   else:  [2398.5, 13.2, 20.0] (n: 4 )
tree:  34
0   if origin == 1 then  [3361.9, 15.0, 20.5] (n: 249 )
0   if 134 <= Displacement <= 168 then  [2980.3, 15.9, 25.0] (n: 18 )
0   if origin == 2 then  [2324.3, 16.5, 28.9] (n: 63 )
0   if 75 <= Horsepower <= 110 then  [2326.2, 15.3, 27.0] (n: 30 )
1   else:  [1980.2, 17.5, 34.2] (n: 38 )
```