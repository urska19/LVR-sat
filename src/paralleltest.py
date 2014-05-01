from sat import SAT_solver
from sudoku import sudoku
from logConstructs import FlatCNF
from time import time

solver = SAT_solver()
board=[[None, None, 9, None, 6, 4, None, None, 1],
    [None, None, None, None, 5, None, None, None, None],
    [4, 6, None, 1, None, 7, None, None, 8],
    [None, None, None, None, None, None, None, 9, None],
    [None, None, None, None, 3, None, None, 1, None],
    [3, None, None, None, None, None, None, 4, None],
    [None, 4, 8, None, None, None, 2, None, None],
    [2, None, 7, None, 4, 5, None, 8, 6],
    [5, None, None, None, None, None, None, None, None]]
#board=[[None, None, None, 4, None, None, None, 5, None],
#    [None, None, None, None, 1, None, 3, 6, None],
#    [None, None, 8, None, None, 6, 9, 4, 7],
#    [1, None, 2, None, None, None, None, 9, 5],
#    [None, 9, None, 2, None, 1, None, None, None],
#    [None, None, None, 5, 9, 3, None, None, None],
#    [4, None, None, None, None, None, 1, 7, 9],
#    [7, 2, None, 1, None, None, None, None, None],
#    [None, 8, None, None, None, 9, None, 2, None]]

formula = FlatCNF(sudoku(board))
i = 1
while i <= 8:
    start = time()
    solution = solver.solve(formula, force_nprocs=i)
    end = time()
    print "%d threads: %.3f seconds (solvable: %s)"%(i, end-start, solution[0])
    i *= 2
