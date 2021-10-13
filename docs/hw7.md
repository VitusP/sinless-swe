## HW7: Hyperparameter Optimization

### **Hyperparameter Optimization Output**
Data used: ```auto93.csv```
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
Here are the output for HW7 
### FFT:
Below is the result of our hyperparameter optimization.
```Shell

==============================================================
r is:  30
0   if Bins == 0.3036885228877272 then  [2188.1, 17.0, 31.8, 114.8] (n: 75 )
1   if Support == 2 then  [2160.1, 17.5, 32.2, 57.2] (n: 1245 )
0   if Bins == 0.4789782659135171 then  [2155.4, 16.9, 31.4, 76.7] (n: 43 )
0   if Bins == 0.37282013290608906 then  [2158.8, 17.4, 32.1, 49.4] (n: 32 )
0   if Bins == 0.20898066420395198 then  [2116.1, 17.8, 31.4, 43.1] (n: 126 )
0   if Bins == 0.18365974367071966 then  [2108.0, 17.1, 32.5, 57.8] (n: 49 )
0   if Cohen == 0.11401806921804686 then  [2060.6, 18.0, 32.8, 29.7] (n: 128 )
0   if Bins == 0.2886577250844603 then  [2157.8, 17.0, 31.1, 55.6] (n: 59 )
1   else:  [2159.3, 17.0, 31.8, 80.4] (n: 125 )
************** r is:  30
Best Hyperparameters:  [2, 0.4706232848599011, 64, 0.8938946646160938, 0.5982234078712435, 0.37282013290608906, 3, 2072.0, 22.0, 40.0, 5]
Runtime: 63.13 seconds

==============================================================
r is:  60
0   if Enough == 0.13421265760566872 then  [2158.0, 17.4, 31.7, 49.3] (n: 102 )
0   if Enough == 0.21574356739589248 then  [2133.4, 17.3, 32.9, 42.6] (n: 183 )
0   if Support == 3 then  [2147.4, 17.3, 31.8, 67.8] (n: 915 )
0   if Samples == 64 then  [2166.8, 17.3, 32.0, 63.0] (n: 464 )
0   if Bins == 0.26643983346983036 then  [2155.1, 17.3, 32.0, 41.7] (n: 164 )
0   if 0.7457575697694332 <= Enough <= 0.7503792520080964 then  [2159.3, 17.1, 31.6, 89.8] (n: 70 )
0   if Bins == 0.2159170485680586 then  [2097.7, 17.7, 32.9, 42.8] (n: 194 )
0   if Bins == 0.1070534593516805 then  [2258.6, 16.3, 29.8, 77.3] (n: 27 )
1   else:  [2113.3, 17.5, 32.4, 64.6] (n: 392 )
************** r is:  60
Best Hyperparameters:  [2, 0.22585669351974974, 128, 0.8225209879204565, 0.305093878258856, 0.2159170485680586, 2, 2133.8, 22.9, 40.0, 4]
Runtime: 99.39 seconds

==============================================================
r is:  125
0   if Samples == 128 then  [2159.2, 17.3, 31.8, 68.1] (n: 2769 )
0   if 0.6161697989929007 <= Enough <= 0.6385314580063823 then  [2174.2, 17.1, 31.4, 69.4] (n: 416 )
0   if 0.6531788837269638 <= Enough <= 0.6837102525129048 then  [2150.5, 17.0, 32.0, 89.9] (n: 304 )
0   if Bins == 0.11247232184015146 then  [2057.0, 17.6, 33.4, 29.2] (n: 170 )
0   if Support == 3 then  [2160.0, 17.3, 31.8, 60.3] (n: 1266 )
1   if Bins == 0.2415708898606154 then  [2135.9, 17.0, 31.7, 86.1] (n: 124 )
0   if Cohen == 0.3238241058659437 then  [2089.5, 17.6, 33.0, 40.1] (n: 190 )
0   if Far == 0.7168310279697048 then  [2219.8, 17.5, 32.3, 63.7] (n: 185 )
0   if 0.6339637425314906 <= Far <= 0.6710149249065632 then  [2174.6, 17.1, 31.2, 90.7] (n: 205 )
0   if Bins == 0.20059762052857863 then  [2135.8, 17.6, 31.0, 45.0] (n: 110 )
1   else:  [2152.0, 17.3, 32.2, 53.4] (n: 622 )
************** r is:  125
Best Hyperparameters:  [2, 0.45570685035774705, 64, 0.8814627046144068, 0.10893551825019375, 0.19333752069975538, 3, 2183.3, 23.3, 40.0, 3]
Runtime: 225.42 seconds

==============================================================
r is:  250
0   if Far == 0.5807682337366304 then  [2151.1, 18.0, 31.0, 48.2] (n: 209 )
0   if Bins == 0.40632720813075374 then  [2124.1, 17.7, 32.0, 42.0] (n: 162 )
0   if Bins == 0.18431666444071274 then  [2067.9, 17.3, 32.4, 50.7] (n: 221 )
0   if Support == 3 then  [2159.2, 17.3, 31.8, 58.9] (n: 5936 )
0   if Samples == 128 then  [2152.6, 17.3, 31.9, 66.6] (n: 3843 )
1   if 0.4108301595934798 <= Bins <= 0.4930072419375965 then  [2183.5, 17.0, 31.4, 84.5] (n: 481 )
0   if 0.8414218749882322 <= Cohen <= 0.8492438956393397 then  [2178.3, 17.4, 31.2, 49.8] (n: 92 )
1   else:  [2146.4, 17.4, 31.9, 64.1] (n: 2011 )
************** r is:  250
Best Hyperparameters:  [2, 0.43637744952353474, 64, 0.5310127511595982, 0.5654640799310717, 0.10525123741426556, 3, 2130.0, 24.6, 40.0, 1]
Runtime: 620.69 seconds

==============================================================
r is:  500
0   if Samples == 128 then  [2158.8, 17.3, 31.8, 66.7] (n: 13068 )
0   if Enough == 0.21701620563126778 then  [2195.9, 17.3, 32.0, 49.9] (n: 199 )
0   if 0.29117445133634845 <= Enough <= 0.3865697202323424 then  [2143.7, 17.5, 32.2, 51.0] (n: 2153 )
0   if Support == 3 then  [2153.4, 17.3, 31.8, 67.2] (n: 3704 )
0   if 0.4220253644071337 <= Cohen <= 0.4951339179058726 then  [2184.9, 17.2, 31.8, 63.7] (n: 557 )
0   if 0.5552610107223646 <= Far <= 0.5684712175875375 then  [2169.2, 17.1, 31.5, 81.3] (n: 239 )
0   if Cohen == 0.10803621292379716 then  [2216.4, 16.9, 30.9, 132.4] (n: 178 )
0   if 0.33761577811195376 <= Bins <= 0.41465432857741913 then  [2174.4, 17.4, 31.4, 76.6] (n: 582 )
1   else:  [2154.5, 17.4, 31.9, 63.9] (n: 3312 )
************** r is:  500
Best Hyperparameters:  [2, 0.2236342977008862, 64, 0.7156563259591495, 0.17539752625801164, 0.30159574603098377, 3, 2183.3, 23.3, 40.0, 3]
Runtime: 1239.10 seconds

==============================================================
r is:  1000
0   if Samples == 64 then  [2150.9, 17.3, 31.9, 63.7] (n: 25865 )
0   if Support == 3 then  [2161.9, 17.3, 31.8, 66.6] (n: 10403 )
0   if 0.4398516084993358 <= Enough <= 0.4972439319737486 then  [2143.0, 17.4, 31.9, 55.4] (n: 1936 )
0   if 0.5427690107720676 <= Far <= 0.5493144411455059 then  [2171.9, 17.3, 31.5, 56.9] (n: 397 )
0   if 0.5318321053075019 <= Far <= 0.5765339672862766 then  [2135.6, 17.9, 32.4, 50.0] (n: 1138 )
1   if 0.5447603261080574 <= Cohen <= 0.5749709051481854 then  [2178.4, 17.2, 31.8, 88.8] (n: 387 )
0   if 0.18195719913639474 <= Cohen <= 0.22693244104108556 then  [2149.1, 17.3, 31.8, 66.3] (n: 564 )
0   if Bins == 0.12617058456505112 then  [2241.6, 16.8, 30.7, 56.8] (n: 65 )
0   if 0.3644823399088335 <= Cohen <= 0.40215752673098193 then  [2145.2, 17.5, 31.9, 62.4] (n: 767 )
1   else:  [2159.7, 17.3, 31.9, 68.0] (n: 7828 )
************** r is:  1000
Best Hyperparameters:  [2, 0.42056238219926567, 64, 0.7482450473076699, 0.6031931335474933, 0.2519773949422416, 2, 2183.3, 23.3, 40.0, 3]
Runtime: 2031.83 seconds

```

### What were the run times of your optimizer as you increased r?
The run time increases near the same rate as the the r increases. When r doubles, the runtime also doubles.
<<<<<<< HEAD
### Does Hyperparameter optimization change a learner's behavior?
Yes, the hyper parameter optimization changes learner's behavior. It helps the learners
to try different hyperparameters and choose a set of hyperparameters that produce the best results.
### Does Hyperparameter optimization improve a learner's behavior?
Yes, the hyperparameter optimization does improve a learner's behavior. I think when the amount of hyperparameters are big, the optimization could help us find the right set automatically without trying it one by one which is not efficient.
### Does the Villabos hypothesis hold for car design? If not, how many random staggers do you suggest?
Yes, it seems that after 60 random probes, the result does not change significantly. 60 seems to be the right number to probe the hyperparameter.
## Source Code
```Python
"""
Class to help us find the best hyperparameter for FFT trees
"""
from src.hw6 import FFT
from src.hw7 import Config
from src.hw3 import Sample
from copy import copy

class HyperOptimizer:

    def __init__(self, sample, r=20) :
        self.r = r
        self.sample = sample
        self.treeSets = []
        self.samples = []
        self.bestHyperparameter = [0]
        # Read data and create uniqe r-size samples with unique hyperparameter
        for index in range(r):
            # print("Index ", index)
            conf = Config()
            conf.build()
            samp = self.sample
            samp.use_config(conf)
            self.samples.append(samp)
            # print("Hyper: ", conf.getHyperparameters())
            # Generate best leaf in each iteration
            branches = []
            branch = []
            self.generateBestLeafFromSample(samp, conf, branch, branches)
        
        # Get best hyperparameter
        # [print(x) for x in self.treeSets]
        self.bestHyperparameter = self.sortBestHyperparameter()
    
    def generateBestLeafFromSample(self, sample, conf, branch = [], branches = []):
        try:
            FFT(sample, conf, branch, branches)
            for i,goal in enumerate(self.sortTrees(branches).rows):
                xyRow = copy(conf.getHyperparameters()) + goal
                # print("xyRow: ", xyRow)
                self.treeSets.append(xyRow)
        except:
            print("Error generating FFT at one point")

    def sortTrees(self, fftBranches):
        # Input fft branches to find the best tree.
        # Return the [-Weight, +Mpg, +Accleration, +N]
        fftBranchSample = Sample([["Weight-", "Accleration+", "Mpg+", "N+"]])
        for i, branch in enumerate(fftBranches):
            branchingSample = Sample([["Weight-", "Accleration+", "Mpg+", "N+"]])
            for k,val in enumerate(branch):
                if val['type'] == 1:
                    row = val['then'] + [val['n']]
                    branchingSample.add(row)
            fftBranchSample.add(branchingSample.sort()[0])     
        return fftBranchSample
                
    def sortBestHyperparameter(self):
        # Input treeSets to sort
        # Return the best[p, enough, samples, far, cohen, bins, support, "Weight-", "Accleration+", "Mpg+", "N+"]
        branches = []
        branch = []
        treeSetsSample = Sample([["P","Enough", "Samples", "Far", "Cohen", "Bins","Support", "Weight-", "Accleration+", "Mpg+", "N+"]] + self.treeSets)
        conf = Config()
        treeSetsSample.use_config(conf)
        """
        for i in range(50):
            print(treeSetsSample.sort()[i])
        """
        FFT(treeSetsSample, conf, branch, branches)
        # print(branches)
        b = branches[len(branches) - 1]
        for k,val in enumerate(b):
            if len(b) - 1 == k:
                print(val['type'], '  else: ', val['then'], '(n:', val['n'], ')')
            else:
                print(val['type'], ' ', val['txt'], '', val['then'], '(n:', val['n'], ')')
        return treeSetsSample.sort()[0]

    def getBestHyperparameter(self):
        return self.bestHyperparameter
```