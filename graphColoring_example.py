#!/usr/bin/env python
import sys
sys.path.append("./src")
from graphColoring import graph_coloring, printGraph, processResult
from sat import SAT_solver, FlatCNF


#instance of sat solver
solver = SAT_solver()

#graph represented with adjacency matrix
graph = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]

#number of colors for graph coloring
colors = 3

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

#solve2 formula
solution2 = solver.solve(formula,True)

#flatcnf solution
solution3 = solver.solve(FlatCNF(formula))

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

print "SAT"
if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."

print "SAT - mt"
if solution2[0]:
    print processResult(solution2[1])
else:
    print "Formula is not satisfiable."

print "SAT - flat"
if solution3[0]:
    print processResult(solution3[1])
else:
    print "Formula is not satisfiable."

colors = 2

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

#solve2 formula
solution2 = solver.solve(formula,True)

#flatcnf solution
solution3 = solver.solve(FlatCNF(formula))

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."

print "SAT - mt"
if solution2[0]:
    print processResult(solution2[1])
else:
    print "Formula is not satisfiable."

print "SAT - flat"
if solution3[0]:
    print processResult(solution3[1])
else:
    print "Formula is not satisfiable."


graph = [
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0]
]

colors = 2

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

#solve2 formula
solution2 = solver.solve(formula,True)

#flatcnf solution
solution3 = solver.solve(FlatCNF(formula))

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."

print "SAT - mt"
if solution2[0]:
    print processResult(solution2[1])
else:
    print "Formula is not satisfiable."

print "SAT - flat"
if solution3[0]:
    print processResult(solution3[1])
else:
    print "Formula is not satisfiable."


graph=[
    [0, 1, 1, 1, 1],
    [1, 0, 1, 1, 0],
    [1, 1, 0, 1, 0],
    [1, 1, 1, 0, 1],
    [1, 0, 0, 1, 0]
]


colors = 3

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

#solve formula
solution2 = solver.solve(formula,True)

#flatcnf solution
solution3 = solver.solve(FlatCNF(formula))

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."

if solution2[0]:
    print processResult(solution2[1])
else:
    print "Formula is not satisfiable."

print "SAT - flat"
if solution3[0]:
    print processResult(solution3[1])
else:
    print "Formula is not satisfiable."

colors = 4

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

#solve2 formula
solution2 = solver.solve(formula,True)

#flatcnf solution
solution3 = solver.solve(FlatCNF(formula))

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."

if solution2[0]:
    print processResult(solution2[1])
else:
    print "Formula is not satisfiable."

print "SAT - flat"
if solution3[0]:
    print processResult(solution3[1])
else:
    print "Formula is not satisfiable."

