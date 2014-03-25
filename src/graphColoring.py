#!/usr/bin/env python
from logConstructs import *
from sat import *

def graph_coloring(graph, colors):

    if len(graph) < colors:
        return False
    #variables = [[None] * colors] * len(graph)
    variables=[[None for i in range(colors)] for j in range(len(graph))]

    #construct variables
    for i in range(len(graph)):
        for j in range(colors):
            variables[i][j] = Var("X" + str(i) + "" + str(j))

    #construct first subformula
    main_formula = And(map(lambda x: Or(x), variables))

    #construct second subformula
    subformula = []
    for k in range(colors - 1):
        for l in range(k + 1, colors):
            subformula += map(lambda x: Not(And([x[k], x[l]])), variables)

    #construct third subformula
    for i in range(len(graph) - 1):
        for j in range(i + 1, len(graph)):
            if graph[i][j] == 1:
                subformula += map(lambda x: Not(And([variables[i][x], variables[j][x]])), range(colors))

    main_formula = And(subformula + main_formula.clause)

    #constructing variable names
    variable_names = map(lambda x: x.name,
                         reduce(lambda x, y: x + y, variables))

    #simplifying formula
    return (main_formula.simplify(), variable_names)


def solveGraphColoring(graph, colors):
    (formula, variableNames) = graph_coloring(graph, colors)
    return evaluateFormula(formula, variableNames)


def main():
    graph = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]

    colors = 2

#    print graph
    print solveGraphColoring(graph, colors)

    graph = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]

#     print graph
    print solveGraphColoring(graph, colors)

    lih_cikel=[
        [0, 1, 1],
        [1, 0, 1],
        [1, 1, 0],
    ]

    sod_cikel=[
        [0, 1, 0, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 0, 1, 0],
    ]

    g=[
        [0, 1, 1, 1, 1],
        [1, 0, 1, 1, 0],
        [1, 1, 0, 1, 0],
        [1, 1, 1, 0, 1],
        [1, 0, 0, 1, 0]
    ]


    print solveGraphColoring(sod_cikel, 2)
    print solveGraphColoring(lih_cikel, 2)
    print solveGraphColoring(g, 2)
    print solveGraphColoring(g, 3)
    print solveGraphColoring(g, 4)

if __name__ == '__main__':
    main()
