#!/usr/bin/env python
from logConstructs import *


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

    return main_formula.simplify()
