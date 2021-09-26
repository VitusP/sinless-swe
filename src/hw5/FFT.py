from hw3.col import o

class FFT():
    def __init__(self, all, conf, branch,branches,stop = None, level=0):
        self.my = conf
        stop = stop or 2*len(all.rows)**self.my.bins
        pass
    
    def match(self, bin, row):
        v=row.cells[bin.at]              # Q: where does `at` come from?
        if   v=="?"   : return True      # Q: what should we do for missing values
        elif bin.first: return v <= bin.hi
        elif bin.last : return v >= bin.lo
        else          : return bin.lo <= v <= bin.hi

    def show(self,bin):
        if   bin.lo == bin.hi: return f"{bin.name} == {bin.lo}"  # Q: how we detect symbolic ranges
        elif bin.first: return f"{bin.name} <= {bin.hi}"
        elif bin.last : return f"{bin.name} >= {bin.lo}"
        else          : return f"{bin.lo} <= {bin.name} <= {bin.hi}"

    def value(self, rule, bin):
        s = self.my.support
        rules = o(plan    = lambda b,r: b**s/(b+r) if b>r else 0,  # good things to make you smile
                monitor = lambda b,r: r**s/(b+r) if r>b else 0,  # bad things to make your cry.
                novel   = lambda b,r: 1/(b+r))                   # Q: when would i select for "novel"?
        return rules[rule](bin.best/bin.bests, bin.rest/bin.rests)
  
    def values(self,rule,bins):
        bins = [(self.value(rule,bin), bin) for bin in bins]
        return sorted([(n,bin) for n,bin in bins if n > 0], key=first) #What is the first here?