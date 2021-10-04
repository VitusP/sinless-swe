import random

class Config:

    def __init__(self):

        self.dict = {
        'p': (2, 2),
        'enough': (0.4, 0.4),
        'samples': (128, 128),
        'far':  (0.9, 0.9),
        'cohen': (0.35, 0.35),
        'bins': (0.5, 0.5),
        'support': (2, 2),
        }

    def set_bond(self, key, low, hi):
        if key not in self.dict.keys():
            Exception
        self.dict[key] = (low, hi)

    def __getitem__(self, key):
        if key not in self.dict.keys:
            Exception
        elif key == 'p':
            return random.randrange(self.dict['p'][0], self.dict['p'][1], 1)
        elif key == 'enough':
            return random.randrange(self.dict['enough'][0], self.dict['enough'][1], 0.1)
        elif key == 'samples':
            return random.randrange(self.dict['samples'][0], self.dict['samples'][1], 16)
        elif key == 'far':
            return random.randrange(self.dict['far'][0], self.dict['far'][1], 0.1)
        elif key == 'cohen':
            return random.randrange(self.dict['cohen'][0], self.dict['cohen'][1], 0.5)
        elif key == 'bins':
            return random.randrange(self.dict['bins'][0], self.dict['bins'][1], 0.1)
        else:
            return random.randrange(self.dict['support'][0], self.dict['support'][1], 1)
        