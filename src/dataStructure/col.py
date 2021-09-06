class Col:
    def __init__(self, at, name):
        self.at = at
        self.name = name
    
    def add(self, x):
        pass

class Skip(Col):
    pass

class Sym(Col):

    def __init__(self, at, name):
        super().__init__(at, name)
        self.has = {}
        self.most = 0
        self.mode = 0

    def add(self, x):
        if x in self.has.keys():
            self.has[x] += 1
        else:
            self.has[x] = 1

        if self.has[x] > self.most:
            self.most, self.mode = self.has[x], x

class Num(Col):
    def __init__(self, at, name):
        super().__init__(at, name)
        self.lo = 0 # Highest number
        self.hi = 0 # Lowest number
        self.mu = 0 
        self.m2 = 0
        self.n = 0
        self.sd = 0

    def add(self, x):
        if x < self.lo:
            self.lo = x
        if x > self.hi:
            self.hi = x
        self.n += 1
        delta = x - self.mu
        self.mu = self.mu + delta / self.n
        self.m2 = self.m2 + delta * (x - self.mu)
        if self.n > 1:
            self.sd = (self.m2 / (self.n - 1))**0.5
