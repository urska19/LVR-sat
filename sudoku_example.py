#!/usr/bin/env python
import sys
sys.path.append("./src")
from sat import SAT_solver
from sudoku import sudoku, printSudoku, processResult


print "================================================="
print "SUDOKU"
print "================================================="

solver = SAT_solver()

# define bord as follows.
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
print "Problem:"
print printSudoku(board)

# construct logical formula from board definition.
formula = sudoku(board)

# solve formula using SAT solver.
result = solver.solve(formula)

print "Solution:"
# process and print result of sat solver.
print printSudoku(processResult(result[1]))
