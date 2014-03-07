#!/usr/bin/env python

from logConstructs import *
from sat import *

# boxes: (row, col, num)

def fill_conditions(a):
	ret=[]
	for i in range(9): # row
		for j in range(9): # col
			r=[a[i][j]] if a[i][j] else range(1,10)
			disj=[]
			for k in r: # value in this box
				conj=[Var("%d%d%d"%(i,j,k))]
				for l in range(9): # other values for this box
					v=Var("%d%d%d"%(i,j,k))
					if k!=l:
						conj.append(Not(v))
				disj.append(And(conj))
			ret+=disj
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
	formula=And([fill_conditions(a),row_conditions(),col_conditions(),square_conditions()])
	return evaluateFormula(formula,[ "%d%d%d"%(y,x,v) for v in range(1,10) for x in range(9) for y in range(9) ])


a=[[None, 8, None, 1, 6, None, None, None, 7],
 [1, None, 7, 4, None, 3, 6, None, None],
 [3, None, None, 5, None, None, 4, 2, None],
 [None, 9, None, None, 3, 2, 7, None, 4],
 [None, None, None, None, None, None, None, None, None],
 [2, None, 4, 8, 1, None, None, 6, None],
 [None, 4, 1, None, None, 8, None, None, 6],
 [None, None, 6, 7, None, 1, 9, None, 3],
 [7, None, None, None, 9, 6, None, 4, None]]
print sudoku(a)
