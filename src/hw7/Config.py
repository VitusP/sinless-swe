from ctypes import LibraryLoader
import random

class Config:

    p, enough, samples, far, cohen, bins, support = 2, 0.4, 128, 0.9, 0.35, 0.4, 2

    def __init__(self):
        self.listOfHyperParams = []
        self.bond = {
        'p': (2, 3),
        'enough': (0.1, 0.7),
        'samples': (6, 8),
        'far':  (0.1, 1.0),
        'cohen': (0.1, 0.5),
        'bins': (0.1, 0.5),
        'support': (2, 6),
        }

    def set_bond(self, key, low, hi):
        if key not in self.bond.keys():
            Exception
        if low > hi:
            Exception
        self.bond[key] = (low, hi)
    
    def getHyperparameters(self):
        return self.listOfHyperParams

    def build(self):

        self.__class__.p = random.randrange(self.bond['p'][0], self.bond['p'][1], 1)
        self.__class__.enough = random.uniform(self.bond['enough'][0], self.bond['enough'][1])
        self.__class__.samples = 2**random.randrange(self.bond['samples'][0], self.bond['samples'][1], 1)
        self.__class__.far = random.uniform(self.bond['far'][0], self.bond['far'][1])
        self.__class__.cohen = random.uniform(self.bond['cohen'][0], self.bond['cohen'][1])
        self.__class__.bins = random.uniform(self.bond['bins'][0], self.bond['bins'][1])
        self.__class__.support = random.randrange(self.bond['support'][0], self.bond['support'][1], 1)

        self.listOfHyperParams.append(self.p)
        self.listOfHyperParams.append(self.enough)
        self.listOfHyperParams.append(self.samples)
        self.listOfHyperParams.append(self.far)
        self.listOfHyperParams.append(self.cohen)
        self.listOfHyperParams.append(self.bins)
        self.listOfHyperParams.append(self.support)