#!/usr/bin/env python

from logConstructs import *

# boxes: (row, col, num)

# ensure that every box is filled with one or more values
def fill_conditions(a):
    ret=[]
    for i in range(9): # row
        for j in range(9): # col
            disj = []
            if a[i][j] is not None:
                disj.append(Var("%d%d%d" % (i, j, a[i][j])))
            else:
                disj = map(lambda x: Var("%d%d%d" % (i, j, x)), range(1, 10))

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

def printSudoku(a):

    i = j = 0
    result = ""

    for i in range(9):

        if i % 3 == 0:
            for j in range(13):
                result += "---"
            result += "\n"

        result += "|| "

        for j in range(9):

            if j % 3 == 0 and j != 0:
                result += " | "

            if a[i][j] is None:
                result += " - "
            else:
                result += " " + str(a[i][j]) + " "

        result += " ||"

        result += "\n"

    for j in range(13):
        result += "---"
    result += "\n"

    return result

def processResult(result):
    #=====================================================================
    #initialize empty board
    #initialize posibility board

    #for all keys in result
    #   construct coordinates and number
    #   if empty board is empty on coordinates
        #   if key is true
        #       set number to coordinates in the empty board
        #   else
        #       remove number from posibility board
        #       if posibility board in coordinates contains one element
        #           set element to coordinates in the empty board
    #return empty board
    #=====================================================================

    #initialize empty board
    eboard = []
    for i in range(9):
        eboard.append([])
        for j in range(9):
            eboard[i].append(None)

    #initialize posibility board
    pboard = []
    for i in range(9):
        pboard.append([])
        for j in range(9):
            pboard[i].append([])
            for k in range(1, 10):
                pboard[i][j].append(k)

    for key in result:
        value = result[key]
        (row, column, number) = (int(key[0]), int(key[1]), int(key[2]))

        if eboard[row][column] is None:
            if value:
                eboard[row][column] = number
            else:
                pboard[row][column].remove(number)
                if len(pboard[row][column]) == 1:
                    eboard[row][column] = pboard[row][column][0]

    return eboard
