class Sample:
    table = {}
    rows = []
    cols = []
    
    def isKlass(str):
        return '!' in str

    def isGoal(str):
        return ('+' in str) or ('-' in str) or ('!' in str)

    def isNum(str):
        return str[0].isupper()

    def isWeight(str):
        pass

    def isSkip(str):
        return '?' in str

    def add(x):
        pass

class Skip(Sample):
    def add(x):
        return x

class Num(Sample):
    pass

class Sym(Sample):
    pass