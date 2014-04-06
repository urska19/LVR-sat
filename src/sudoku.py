#!/usr/bin/env python

from logConstructs import *

# boxes: (row, col, num)

# ensure that every box is filled
def fill_conditions(a):
    ret=[]
    for i in range(1): # row
        for j in range(1): # col
            r=[a[i][j]] if a[i][j] else range(1,10) # all the possible values for this box
            disj=[]
            for k in r: # fix one value for this box
                conj=[Var("%d%d%d"%(i,j,k))]
                for l in range(1,10): # other values for this box
                    v=Var("%d%d%d"%(i,j,l))
                    if k!=l:
                        conj.append(Not(v))
                disj.append(And(conj))
            ret.append(Or(disj))
    return And(ret)
def row_conditions():
    ret=[]
    for i in range(9): # row
        for a in range(9): # first box
            for b in range(a+1,9): # second box
                ret+=map(lambda x: Not(And([Var("%d%d%d"%(i,a,x)), Var("%d%d%d"%(i,b,x))])), range(1,10))
    return And(ret)
def col_conditions():
    ret=[]
    for i in range(9): # col
        for a in range(9): # first box
            for b in range(a+1,9): # second box
                ret+=map(lambda x: Not(And([Var("%d%d%d"%(a,i,x)), Var("%d%d%d"%(b,i,x))])), range(1,10))
    return And(ret)

def square_conditions():
    ret=[]
    for base in range(9): # base square coordinates
        for a in range(9): # first box
            for b in range(a+1,9): # second box
                xa=base%3*3+a%3
                ya=base/3*3+a/3
                xb=base%3*3+b%3
                yb=base/3*3+b/3
                ret+=map(lambda x: Not(And([Var("%d%d%d"%(ya,xa,x)), Var("%d%d%d"%(yb,xb,x))])), range(1,10))
    return And(ret)

def sudoku(a):
    return And([fill_conditions(a),row_conditions(),col_conditions(),square_conditions()])
