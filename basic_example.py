#!/usr/bin/env python
import sys
sys.path.append("./src")
from logConstructs import *
from sat import SAT_solver

#==========================================
# Construct formulas
#==========================================
# true() - true constant
# false() - false constant
# Var( str name) - variable
# Not( logical object ) - negation
# And( [ logical objects ] ) - and
# Or( [ logical objects ] ) - or
#==========================================
print "================================================="
print "Construct formulas"
print "================================================="
#
# true constant
expr1 = true()
print "Expression 1: ", unicode(expr1)
#
# variable x
expr2 = Var("x")
print "Expression 2: ", unicode(expr2)
#
# x and false
expr3 = And([Var("x"), false()])
print "Expression 3: ", unicode(expr3)
#
# (x and y) or false
expr4 = Or([And([Var("x"), Var("y")]), false()])
print "Expression 4: ", unicode(expr4)
#
expr5 = Not(Or([And([Var("x"), Var("y")]), false()]))
print "Expression 5: ", unicode(expr5)
#
#==========================================
# Set to nnf
#==========================================
#returns - new formula in nnf
#==========================================
print "================================================="
print "Change to NNF"
print "================================================="
#
expr5 = Not(Or([And([Var("x"), Var("y")]), false()]))
print "expr: ", unicode(expr5)
print "expr in  nnf: ", unicode(expr5.nnf())
#
#
#==========================================
# Change to cnf
#==========================================
#- Assumes that formula is in nnf.
#
#returns - new formula in cnf.
#==========================================
#Algorithm is design by reducing complexity recursively.
#Could be faster by using Cartesian product.
#==========================================
print "================================================="
print "Change to CNF"
print "================================================="
expr8 = Or([Var("p"), And([Var("q"), Var("p")])])
expr9 = Var("p")
expr10 = Or([Var("p"), Var("q")])
expr11 = Or([And([Var("p"), Var("q")]), Var("h"), And([Var("g"), Var("k")])])
expr12 = true()
expr6 = false()
expr7 = And([Var("p"), Var("q")])
#
print "Expression: " + unicode(expr9)
print "Expression (CNF): " + unicode(expr9.cnf())
print "Expression: " + unicode(expr12)
print "Expression (CNF): " + unicode(expr12.cnf())
print "Expression: " + unicode(expr6)
print "Expression (CNF): " + unicode(expr6.cnf())
print "Expression: " + unicode(expr10)
print "Expression (CNF): " + unicode(expr10.cnf())
print "Expression: " + unicode(expr7)
print "Expression (CNF): " + unicode(expr7.cnf())
print "Expression: " + unicode(expr8)
print "Expression (CNF): " + unicode(expr8.cnf())
print "Expression: " + unicode(expr11)
print "Expression (CNF): " + unicode(expr11.cnf())
#
print "================================================="
print "Simplify formula."
print "================================================="
#
tmpexpr1 = expr8.setVariables({"p": False})
tmpexpr2 = expr8.setVariables({"p": True})
#
print "Expression: " + unicode(tmpexpr1)
print "Simplifyed expression: " + unicode(tmpexpr1.simplify())
print "Expression: " + unicode(tmpexpr2)
print "Simplifyed expression: " + unicode(tmpexpr2.simplify())
#
#==========================================
# Remove duplicate variables
#==========================================
# - Assume cnf.
# returns - new formula without duplications.
#==========================================
print "================================================="
print "Deduplicate."
print "================================================="
dedupexpr = And([Or([Var("x1"), Var("x2")])])
print "Expession: " + unicode(dedupexpr) + " -> " + unicode(dedupexpr.deduplicate())
dedupexpr = And([Or([Var("x1"), Var("x1")])])
print "Expession: " + unicode(dedupexpr) + " -> " + unicode(dedupexpr.deduplicate())
#
#
#==========================================
# Set variables
#==========================================
# argument - dictionary of variable name: boolean value
#          - dictionary can represent subset of variables
# returns  new formula
#==========================================
#Inconsistency in using logical constructs and boolean types.
#==========================================
print "================================================="
print "Set variables"
print "================================================="
print "Expression: " + unicode(expr4)
print "Expression (x->False): " + unicode(expr4.setVariables({"x": False}))
print "Expression (x->True): " + unicode(expr4.setVariables({"x": True}))
print "Making copy with setVariables: " + unicode(expr4.setVariables())
#
#==========================================
# Evaluate
#==========================================
# Same interface as setVariables method.
# Set variables + simplify
#==========================================
print "================================================="
print "Evaluate"
print "================================================="
print "Expression: " + unicode(expr4)
print "Evaluate (x->False): " + unicode(expr4.nnf().cnf().deduplicate().evaluate({"x": False}))
print "Evaluate (x->True): " + unicode(expr4.nnf().cnf().deduplicate().evaluate({"x": True}))
#
#==========================================
# SAT solver
#==========================================
# argument - formula
# returns - (boolean value, dictionary)
#         - value indicates if formula is satisfiable.
#         - dictionary represents mapping of variables.
#==========================================
print "================================================="
print "SAT Solver"
print "================================================="
solver = SAT_solver()
for i in globals().keys():
    if i[:4] == "expr":
        print i, ":", unicode(globals()[i]), "-------->", solver.solve(globals()[i])
        print i, ":", unicode(globals()[i]), "--flat-->", solver.solve(FlatCNF(globals()[i]))
#
#
#==========================================
# Sudoku example
#==========================================
# assume 9x9 board
#==========================================
# - cnf method takes too long.
# - Classes take to much space and memory exception can occur
# depending on system memory and sudoku board configuration.
#==========================================
