#!/usr/bin/env python
import unittest
from logConstructs import *
from sat import SAT_solver


expr7 = And([Var("p"), Var("q")])
expr8 = And([Var("x1"),Or([Var("x2"),And([Var("x3"),Var("x4")])])])
expr9 = Or([Var("x1"),Not(Var("x2")),And([Var("x2"),Var("x3")]),Var("x4")])
expr10 = Or([And([Var("x1"),Var("x2"),Var("x3")]),And([Not(Var("x4")),Var("x1")])])
expr11 = Or([And([Var("x1"),Var("x2")]),And([Var("x3"),Var("x4")]),And([Var("x2"),Var("x3"),Not(Var("x4"))])])
expr12 = And([Var("x1"), Not(Var("x1"))])
expr13 = Or([ And([Var("a"), Not(Var("b"))]), And([Not(Var("a")), Var("b")]) ])

expr = And([
    Or([
        Not(Var("p")),
        Var("q")
    ]),
    Var("p")
])
print "================================================="
print "================================================="
print "Testing setVariables method."
print "================================================="
print "Testing setVariables method - proper copy."
print "================================================="
newexpr = expr.setVariables()
newexpr2 = expr.setVariables({"p": False})

print "Expression: " + unicode(expr)
print "Expression (setVariables-empty): " + unicode(newexpr)
print "Expression (setVariables- p->False): " + unicode(newexpr2)

print "================================================="
print "Testing setVariables method - independent copy."
print "================================================="

newexpr1 = expr.setVariables({"p": False})
newexpr2 = expr.setVariables({"p": True})
newexpr3 = expr.setVariables({"z": True})

print "Expression: " + unicode(expr)
print "Expression (p->False): " + unicode(newexpr1)
print "Expression (p->True): " + unicode(newexpr2)
print "Expression (z->True): " + unicode(newexpr3)

print "================================================="
print "Testing deduplicate method."
print "================================================="
dedupexpr = And([ Or([Var("x1"), Var("x2")]) ])
print "Expession: " + unicode(dedupexpr) + " -> " + unicode(dedupexpr.deduplicate())
dedupexpr = And([ Or([Var("x1"), Var("x1")]) ])
print "Expession: " + unicode(dedupexpr) + " -> " + unicode(dedupexpr.deduplicate())

print "================================================="
print "================================================="
print "SAT Solver Testing"
print "================================================="
solver = SAT_solver()
for i in globals().keys():
    if i[:4] == "expr":
        print i, ":", unicode(globals()[i]), "->", solver.solve(globals()[i])

print unicode(true()), "->", solver.solve(true())
print "================================================="
print "sudoku"
from sudoku import sudoku
def printsudoku(a):
    for line in a:
        for col in line:
            print " %d "%(col) if col else " _ ",
        print ""

board=[[None, 8, None, 1, 6, None, None, None, 7],
 [1, None, 7, 4, None, 3, 6, None, None],
 [3, None, None, 5, None, None, 4, 2, None],
 [None, 9, None, None, 3, 2, 7, None, 4],
 [None, None, None, None, None, None, None, None, None],
 [2, None, 4, 8, 1, None, None, 6, None],
 [None, 4, 1, None, None, 8, None, None, 6],
 [None, None, 6, 7, None, 1, 9, None, 3],
 [7, None, None, None, 9, 6, None, 4, None]]
printsudoku(board)
import sys
formula = sudoku(board)[0]
sys.stderr.write( unicode(sudoku(board)[0].nnf().cnf().simplify()).encode("utf-8") )
result = solver.solve(sudoku(board)[0])
evaluated = formula.nnf().cnf().deduplicate().evaluate(result)
print result, unicode(evaluated)

print "================================================="
print "graph coloring"
from graphColoring import graph_coloring

graph = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]
colors = 2
f = graph_coloring(graph, colors)[0]
print "graph:", unicode(f), "->", solver.solve(f)
solution = solver.solve(f)
#del solution['']
solved=f.nnf().cnf().evaluate(solution)
print unicode(solved)
print "solution: \033[31;1m"+`solution`+"\033[0m"

graph = [
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
]
f = graph_coloring(graph, colors)[0]
print "graph: ", unicode(f), "->", solver.solve(f)

sod_cikel=[
    [0, 1, 0, 1],
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
]
f = graph_coloring(sod_cikel, colors)[0]
print "sod_cikel:", unicode(f), "->", solver.solve(f)

lih_cikel=[
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
]
f = graph_coloring(lih_cikel, colors)[0]
print "lih_cikel:", unicode(f), "->", solver.solve(f)

g=[
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 0],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0]
]
f = graph_coloring(g, 2)[0]
print "g2:", unicode(f), "->", solver.solve(f)
f = graph_coloring(g, 3)[0]
print "g3:", unicode(f), "->", solver.solve(f)
f = graph_coloring(g, 4)[0]
print "g4:", unicode(f), "->", solver.solve(f)

if __name__ == "__main__":
    unittest.main()
