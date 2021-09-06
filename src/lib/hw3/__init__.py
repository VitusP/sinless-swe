import sys
import re
import time
import csv

class Sample:
    table = {}
    cols_type = []

    def read(self, file):
        for row in file:
            self.add(row)
        return self

    def isKlass(self, str):
        return '!' in str

    def isGoal(self, str):
        return ('+' in str) or ('-' in str) or ('!' in str)

    def isNum(self, str):
        return str[0].isupper()

    def isWeight(self, str):
        pass

    def isSkip(self, str):
        return '?' in str

    def checkType(self, str):
        ## 1: Sym 2:Num 3: Skip
        if self.isSkip(str):
            return '3'
        if self.isNum(str):
            return '2'
        else:
            return '1'
        
    def add(self, row):
        pass

    def header(self, lst, what, new, tmp):
        pass

    def data(self, lst):
        pass

    def clone(self):
        pass

class Skip(Sample):
    def add(x):
        return x


class Num(Sample):
    pass


class Sym(Sample):
    pass
