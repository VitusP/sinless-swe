## HW7: Hyperparameter Optimization
**HyperOptimizer.py** </br>
```Python
```

### **Hyperparameter Optimization Output**
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
Here are the output for HW7 </br>
### FFT:
Below is the result of our hyperparameter optimization.
```Shell
----------
R = 30
Hyperparameter: 
p = 2, 
enough = 0.4821951863348146, 
samples = 64, 
far = 0.7233591657670192, 
cohen = 0.25926393723109414, 
bins = 0.4064227247158328, 
support = 3
y-values: 
-Weight, +Accleration, +Mpg, +N
[1996.8, 17.1, 34.5, 22]
----------
R = 60
Hyperparameter: 
p = 2, 
enough = 0.21143513879422898, 
samples = 128, 
far = 0.7268083952941969, 
cohen = 0.2021623082158378, 
bins = 0.6979268333628639, 
support = 2
y-values: 
-Weight, +Accleration, +Mpg, +N
[1926.8, 19.6, 34.2, 19]
----------
R = 125
Hyperparameter: 
p = , 
enough = , 
samples = , 
far = , 
cohen = , 
bins = , 
support = 
y-values: 
-Weight, +Accleration, +Mpg, +N
----------
R = 250
Hyperparameter: 
p = , 
enough = , 
samples = , 
far = , 
cohen = , 
bins = , 
support = 
y-values: 
-Weight, +Accleration, +Mpg, +N
----------
R = 500
Hyperparameter: 
p = , 
enough = , 
samples = , 
far = , 
cohen = , 
bins = , 
support = 
y-values: 
-Weight, +Accleration, +Mpg, +N
----------
R = 1000
Hyperparameter: 
p = , 
enough = , 
samples = , 
far = , 
cohen = , 
bins = , 
support = 
y-values: 
-Weight, +Accleration, +Mpg, +N

```

## What were the run times of your optimizer as you increased r?
## Does Hyperparameter optimization change a learner's behavior?
## Does Hyperparameter optimization improve a learner's behavior?
## Does the Villabos hypothesis hold for car design? If not, how many random staggers do you suggest?