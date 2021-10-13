# import os
# import sys
# import time
# sys.path.append(os.path.realpath(os.path.dirname(__file__)+"/.."))
# from src.hw7 import HyperOptimizer
# from src.hw3 import Sample

# # Set the right file system
# dataPath = os.path.dirname(os.path.abspath(__file__))

# # Call Sample
# # samp = Sample.read("data/auto93.csv")

# #n = 60
# #res1 = HyperOptimizer("data/auto93.csv", n)

# #print("************** r is: ", n)
# #print("Best Hyperparameters: ", res1.getBestHyperparameter())

# #exit()

# for i in [30, 60, 125, 250, 500, 1000]:
#     success = False
#     print(f'==============================================================')
#     start = time.time()
#     while (success == False):
#         try:
#             res1 = HyperOptimizer(Sample.read("data/auto93.csv"), i)
#             print("************** r is: ", i)
#             print("Best Hyperparameters: ", res1.getBestHyperparameter())
#             success = True
#         except:
#             pass
#     print(f'Runtime: %.2f seconds' % (time.time() - start))