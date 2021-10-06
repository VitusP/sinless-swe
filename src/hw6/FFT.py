from src.hw3.col import o
from copy import deepcopy

"""
    all : Seems like a Sample.
    bin : Seems like a Col.

"""

class FFT():
    def __init__(self, all, conf, branch,branches,stop = None, level=0):

        self.my = conf
        stop = stop or 2*len(all.rows)**self.my.bins
        
        tmp = all.clone()
        for row in all.rows:
            tmp.add(row)
        tmp = tmp.divs()
        tmp = sorted(tmp)

        best, rest = tmp[0], tmp[-1]
        bins = [bin for xbest,xrest in zip(best.x, rest.x) 
                for bin in xbest.discretize(xrest, self.my)]

        bestIdea = None
        worstIdea = None
        # print("bins", bins)
        bestValues = self.values("plan", bins)
        worstValues = self.values("monitor", bins)

        if len(bestValues)>0 and len(worstValues)>0:
            bestIdea   = bestValues[-1][1]
            worstIdea  = worstValues[-1][1]
            
            for yes,no,idea in [(1,0,bestIdea), (0,1,worstIdea)]:
                leaf,tree = all.clone(), all.clone()
                for row in all.rows:
                    if self.match(idea, row):
                        leaf.add(row)
                    else:
                        tree.add(row)
                b1 = deepcopy(branch)
                b1 += [o(at=idea.at, lo=idea.lo, hi=idea.hi,
                                type=yes, txt="if "+self.show(idea)+" then", 
                                then=leaf.ys(), n=len(leaf.rows))]
                # print("b1: ", b1)
                # print("len of tree rows: ", len(tree.rows)) [1909.9, 17.9, 35.6]
                # print(stop)
                if len(tree.rows) <= stop:
                    b1  += [o(type=no, txt="  ", then=tree.ys(), n= len(tree.rows))]
                    branches += [b1]
                else:
                    # print("Recurse FFT")
                    FFT(tree,conf,b1,branches,stop=stop,level=level+1)
            
    
    def match(self, bin, row):
        # print("row: ", row)
        v=row[bin.at]              # Q: where does `at` come from?
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
        # for val in tmp:
        #     print("values: ", val)
        # print("length of tmp: ", len(tmp))
        return sorted(tmp, key=lambda tuple: tuple[0]) #What is the first here? It should be a sorting rule