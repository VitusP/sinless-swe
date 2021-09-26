from src.hw3.col import o
from copy import copy

"""
    all : Seems like a Sample.
    bin : Seems like a Col.

"""

class FFT():
    def __init__(self, all, conf, branch,branches,stop = None, level=0):

        branch = branch or []
        branches = branches or []

        self.my = conf
        stop = stop or 2*len(all.rows)**self.my.bins
        
        tmp = all.clone()
        for row in all.rows:
            tmp.add(row)
        tmp = tmp.divs()
        
        best, rest = tmp[0], tmp[-1]

        bins = [bin for xbest,xrest in zip(best.x, rest.x) 
                for bin in xbest.discretize(xrest, self.my)]

        bestIdea   = self.values("", bins)[-1][1]
        worstIdea  = self.values("", bins)[-1][1]
        pre = "|.. " *level
        
        for yes,no,idea in [(1,0,bestIdea), (0,1,worstIdea)]:
            leaf,tree = all.clone(), all.clone()
            for row in all.rows:
                if self.match(idea, row):
                    leaf.add(row)
                else:
                    tree.add(row)
        b1 = copy(branch)
        b1 += [o(at=idea.at, lo=idea.lo, hi=idea.hi,
                          type=yes, txt="if "+self.show(idea)+" then", 
                          then=leaf.ys(), n=len(leaf.rows))]
        if len(tree.rows) <= stop:
            b1  += [o(type=no, txt="  ", then=tree.ys(), n= len(tree.rows))]
            branches += [b1]
        else:
            FFT(tree,conf,b1,branches,stop=stop,level=level+1)
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
        tmp = [(n,bin) for n,bin in bins if n > 0]
        return sorted(tmp, key=tmp[0]) #What is the first here? It should be a sorting rule