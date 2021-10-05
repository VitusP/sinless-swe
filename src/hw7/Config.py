from ctypes import LibraryLoader
import random

class Config:

    p, enough, samples, far, cohen, biins, support = None, None, None, None, None, None, None

    def __init__(self):

        self.dict = {
        'p': (2, 3),
        'enough': (0.4, 0.6),
        'samples': (6, 8),
        'far':  (0.7, 0.9),
        'cohen': (0.30, 0.35),
        'bins': (0.4, 0.5),
        'support': (2, 3),
        }

    def set_bond(self, key, low, hi):
        if key not in self.dict.keys():
            Exception
        if low > hi:
            Exception
        self.dict[key] = (low, hi)

    def build(self):

        self.__class__.p = random.randrange(self.dict['p'][0], self.dict['p'][1], 1)
        self.__class__.enough = random.uniform(self.dict['enough'][0], self.dict['enough'][1])
        self.__class__.samples = 2**random.randrange(self.dict['samples'][0], self.dict['samples'][1], 1)
        self.__class__.far = random.uniform(self.dict['far'][0], self.dict['far'][1])
        self.__class__.cohen = random.uniform(self.dict['cohen'][0], self.dict['cohen'][1])
        self.__class__.bins = random.uniform(self.dict['bins'][0], self.dict['bins'][1])
        self.__class__.support = random.randrange(self.dict['support'][0], self.dict['support'][1], 1)