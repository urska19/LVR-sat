#!/usr/bin/env python
import unittest
from logConstructs import *
from sat import SAT_solver
from sudoku import sudoku, printSudoku, processResult


def logTests():
    # first task
    expr1 = Not(And([Var("p"), Var("q")]))
    expr2 = Or([Not(Var("p")), Not(Var("q"))])

    print unicode(expr1)
    print unicode(expr2)

    # third task
    print unicode(expr1.simplify())
    print unicode(expr2.simplify())

    # examples

    expr = Or([false(), Var("p")])
    print unicode(expr) + " => " + unicode(expr.simplify())
    expr = And([true(), Var("p")])
    print unicode(expr) + " => " + unicode(expr.simplify())
    expr = Not(false())
    print unicode(expr) + " => " + unicode(expr.simplify())

    # test cases
    def pretty(expr):
        print unicode(expr) + " => " + unicode(expr.simplify())

    expr = Or([
        Var("p"),
        And([
            Var("q"),
            Var("p")
            ])
    ])

    print "================================================="
    print "CNF"
    print "================================================="
    expr = Or([
        Var("p"),
        And([
            Var("q"),
            Var("p")
            ])
    ])
    expr2 = Var("p")
    expr3 = Or([Var("p"), Var("q")])
    expr4 = Or([And([Var("p"), Var("q")]), Var("h"), And([Var("g"), Var("k")])])
    expr5 = true()
    expr6 = false()
    expr7 = And([Var("p"), Var("q")])

    print "Expression: " + unicode(expr2)
    print "Expression (CNF): "+ unicode(expr2.cnf())
    print "Expression: " + unicode(expr5)
    print "Expression (CNF): "+ unicode(expr5.cnf())
    print "Expression: " + unicode(expr6)
    print "Expression (CNF): "+ unicode(expr6.cnf())
    print "Expression: " + unicode(expr3)
    print "Expression (CNF): "+ unicode(expr3.cnf())
    print "Expression: " + unicode(expr7)
    print "Expression (CNF): "+ unicode(expr7.cnf())
    print "Expression: " + unicode(expr)
    print "Expression (CNF): "+ unicode(expr.cnf())
    print "Expression: " + unicode(expr4)
    print "Expression (CNF): "+ unicode(expr4.cnf())
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
    print "================================================="
    print "Testing simplify method."
    print "================================================="
    print "Expression: " + unicode(expr)
    print "Expression (p -> False): " + unicode(expr.evaluate({"p": False}))
    print "Expression (p -> True): " + unicode(expr.evaluate({"p": True}))
    print "================================================="

logTests()

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

board=[[4, 8, None, 1, 6, None, None, None, 7],
 [1, None, 7, 4, None, 3, 6, None, None],
 [3, None, None, 5, None, None, 4, 2, None],
 [None, 9, None, None, 3, 2, 7, None, 4],
 [None, None, None, None, None, None, None, None, None],
 [2, None, 4, 8, 1, None, None, 6, None],
 [None, 4, 1, None, None, 8, None, None, 6],
 [None, None, 6, 7, None, 1, 9, None, 3],
 [7, None, None, None, 9, 6, None, 4, None]]

print printSudoku(board)

import sys
formula = sudoku(board)
# sys.stderr.write( unicode(sudoku(board)[0].nnf().cnf().simplify()).encode("utf-8") )
result = solver.solve(formula)
print printSudoku(processResult(result[1]))



print "================================================="
print "================================================="
print "SAT Solver - mt - Testing"
print "================================================="
solver = SAT_solver()
for i in globals().keys():
    if i[:4] == "expr":
        print i, ":", unicode(globals()[i]), "->", solver.solve(globals()[i],True)

print unicode(true()), "->", solver.solve(true(),True)
print "================================================="
print "sudoku"

board=[[4, 8, None, 1, 6, None, None, None, 7],
 [1, None, 7, 4, None, 3, 6, None, None],
 [3, None, None, 5, None, None, 4, 2, None],
 [None, 9, None, None, 3, 2, 7, None, 4],
 [None, None, None, None, None, None, None, None, None],
 [2, None, 4, 8, 1, None, None, 6, None],
 [None, 4, 1, None, None, 8, None, None, 6],
 [None, None, 6, 7, None, 1, 9, None, 3],
 [7, None, None, None, 9, 6, None, 4, None]]

print printSudoku(board)

import sys
formula = sudoku(board)
# sys.stderr.write( unicode(sudoku(board)[0].nnf().cnf().simplify()).encode("utf-8") )
result = solver.solve(formula, True)
print printSudoku(processResult(result[1]))

