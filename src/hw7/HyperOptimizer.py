"""
Class to help us find the best hyperparameter for FFT trees
"""
from src.hw6 import FFT
from src.hw7 import Config
# from src.hw3 import Sample
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