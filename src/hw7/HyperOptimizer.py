"""
Class to help us find the best hyperparameter for FFT trees
"""
from src.hw6 import FFT
from src.hw7 import Config

class HyperOptimizer:

    def __init__(self, sample, r=20) :
        self.r = r
        self.sample = sample # Sample data
        self.treeSets = []
        self.samples = []
        self.bestHyperparameter = [0]
        # Read data and create uniqe r-size samples with unique hyperparameter
        for index in range(r):
            print("Index ", index)
            conf = Config()
            conf.build()
            samp = self.sample
            samp.use_config(conf)
            self.samples.append(samp)
            print(conf.getHyperparameters())
            # Generate best leaf in each iteration
            branches = []
            branch = []
            self.generateBestLeafFromSample(samp, conf, branch, branches)
        
        # Get best hyperparameter
        self.bestHyperparameter = self.getBestHyperparameter()
    
    def generateBestLeafFromSample(self, sample, conf, branch = [], branches = []):
        FFT(sample, conf, branch, branches)
        xyRow = conf.getHyperparameters() + [] if self.sortTrees(branches) else self.sortTrees(branches)
        self.treeSets.append(xyRow)

    ## TODO
    def sortTrees(self, fftBranches):
        # Input fft branches to find the best tree.
        # Return the [best -Weight, +Mpg, +Accleration, +N]
        pass

    ## TODO
    def sortBestHyperparameter(self):
        # Input treeSets to sort
        # Return the best[p, enough, samples, far, cohen, bins, support, best -Weight, +Mpg, +Accleration, +N]
        pass

    def getBestHyperparameter(self):
        return self.bestHyperparameter