#!/usr/bin/env python
import sys
sys.path.append("./src")
from graphColoring import graph_coloring, printGraph, processResult
from sat import SAT_solver


#instance of sat solver
solver = SAT_solver()

#graph represented with adjecency matrix
graph = [
    [1, 1, 1],
    [1, 1, 1],
    [1, 1, 1],
]

#nuber of colors for graph coloring
colors = 3

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."

colors = 2

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
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

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
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

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."

colors = 4

#construct formula for certain graph and number of colors
formula = graph_coloring(graph, colors)

#solve formula
solution = solver.solve(formula)

print "Graph (" + str(colors) + " colors):"

print printGraph(graph)

if solution[0]:
    print processResult(solution[1])
else:
    print "Formula is not satisfiable."
