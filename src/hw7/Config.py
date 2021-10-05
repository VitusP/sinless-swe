from ctypes import LibraryLoader
import random

class Config:

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
        return {
            'p': random.randrange(self.dict['p'][0], self.dict['p'][1], 1),
            'enough': random.uniform(self.dict['enough'][0], self.dict['enough'][1]),
            'samples': 2**random.randrange(self.dict['samples'][0], self.dict['samples'][1], 1),
            'far':  random.uniform(self.dict['far'][0], self.dict['far'][1]),
            'cohen': random.uniform(self.dict['cohen'][0], self.dict['cohen'][1]),
            'bins': random.uniform(self.dict['bins'][0], self.dict['bins'][1]),
            'support': random.randrange(self.dict['support'][0], self.dict['support'][1], 1),
        }
        