#!/usr/bin/env python
import sys
sys.path.append("./src")
from sat import SAT_solver
from sudoku import sudoku, printSudoku, processResult


print "================================================="
print "SUDOKU"
print "================================================="

solver = SAT_solver()

# define board as follows.
# board is array with nine arrays (rows).
# rows are arrays of nine elements.
# elements are None or int in [1,9].
# None - empty square.
board = [[None, 8, None, 1, 6, None, None, None, 7],
        [1, None, 7, 4, None, 3, 6, None, None],
        [3, None, None, 5, None, None, 4, 2, None],
        [None, 9, None, None, 3, 2, 7, None, 4],
        [None, None, None, None, None, None, None, None, None],
        [2, None, 4, 8, 1, None, None, 6, None],
        [None, 4, 1, None, None, 8, None, None, 6],
        [None, None, 6, 7, None, 1, 9, None, 3],
        [7, None, None, None, 9, 6, None, 4, None]]

# print sudoku from board definition.
print "Lab exercise:"
print printSudoku(board)

# construct logical formula from board definition.
formula = sudoku(board)

# solve formula using SAT solver(multithreading)
result = solver.solve(formula, True)

print "Solution:"
# process and print result of sat solver.
print printSudoku(processResult(result[1]))

medium_board = [[None, None, 5, None, 6, 3, 1, 2, None],
        [None, None, 9, None, None, 1, None, 5, None],
        [1, None, None, None, None, 8, 9, None, 6],
        [None, None, None, None, 5, None, 8, None, 2],
        [None, 5, None, None, None, None, None, 1, None],
        [6, None, 1, None, 9, None, None, None, None],
        [9, None, 6, 2, None, None, None, None, 1],
        [None, 1, None, 6, None, None, 4, None, None],
        [None, 4, 7, 3, 1, None, 2, None, None]]

print "Medium problem:"
print printSudoku(medium_board)

result = solver.solve(sudoku(medium_board), True)

print "Solution:"
# process and print result of sat solver.
print printSudoku(processResult(result[1]))

hard_board = [[None, None, 2, None, 8, None, None, 3, None],
        [None, None, 5, 1, 9, None, None, None, 2],
        [None, 8, None, None, None, None, None, 4, None],
        [None, 9, 6, None, 5, None, None, None, None],
        [2, None, 8, None, None, None, 3, None, 4],
        [None, None, None, None, 3, None, 6, 9, None],
        [None, 3, None, None, None, None, None, 2, None],
        [8, None, None, None, 4, 6, 7, None, None],
        [None, 6, None, None, 1, None, 5, None, None]]

print "Hard problem:"
print printSudoku(hard_board)

result = solver.solve(sudoku(hard_board), True)

print "Solution:"
# process and print result of sat solver.
print printSudoku(processResult(result[1]))

evil_board = [[None, 3, 6, None, 9, None, None, None, None],
        [None, None, None, None, None, None, None, 4, 1],
        [None, None, None, 7, 4, None, None, None, 3],
        [None, 9, 1, None, None, None, None, None, None],
        [2, None, None, 5, None, 3, None, None, 6],
        [None, None, None, None, None, None, 2, 1, None],
        [5, None, None, None, 2, 4, None, None, None],
        [6, 8, None, None, None, None, None, None, None],
        [None, None, None, None, 7, None, 6, 2, None]]

print "Evil problem:"
print printSudoku(evil_board)

result = solver.solve(sudoku(evil_board), True)

print "Solution:"
# process and print result of sat solver.
print printSudoku(processResult(result[1]))

#no solution sudoku
evil_board = [[None, 3, 6, None, 9, None, None, None, 3],
        [None, None, None, None, None, None, None, 4, 1],
        [None, None, None, 7, 4, None, None, None, 3],
        [None, 9, 1, None, None, None, None, None, None],
        [2, None, None, 5, None, 3, None, None, 6],
        [None, None, None, None, None, None, 2, 1, None],
        [5, None, None, None, 2, 4, None, None, None],
        [6, 8, None, None, None, None, None, None, None],
        [None, None, None, None, 7, None, 6, 2, None]]

print "Evil problem (no solution):"
print printSudoku(evil_board)

result = solver.solve(sudoku(evil_board), True)

print "Solution:"

if not result[0]:
    print "No solution."
else:
    # process and print result of sat solver.
    print printSudoku(processResult(result[1]))
