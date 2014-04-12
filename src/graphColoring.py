#!/usr/bin/env python
from logConstructs import *


def graph_coloring(graph, colors):

    if len(graph) < colors:
        return False
    variables=[[None for i in range(colors)] for j in range(len(graph))]

    #construct variables
    for i in range(len(graph)):
        for j in range(colors):
            variables[i][j] = Var("X" + str(i) + "" + str(j))

    #construct first subformula - node must be colored
    main_formula = And(map(lambda x: Or(x), variables))

    #construct second subformula - node must be colored with one color
    subformula = []
    for k in range(colors - 1):
        for l in range(k + 1, colors):
            subformula += map(lambda x: Not(And([x[k], x[l]])), variables)

    #construct third subformula - conected nodes have different colors
    for i in range(len(graph) - 1):
        for j in range(i + 1, len(graph)):
            if graph[i][j] == 1:
                subformula += map(lambda x: Not(And([variables[i][x], variables[j][x]])), range(colors))

    main_formula = And(subformula + main_formula.clause)

    return main_formula.simplify()

def printGraph(graph):

    result = ""

    for i in range(len(graph)):
        for j in range(len(graph)):
            result += " " + str(graph[i][j]) + " "

        result += "\n"

    return result


def processResult(result):

    mappings = {}

    for key in result:
        node = key[1]
        color = key[2]

        if result[key]:
            mappings[int(node)] = int(color)

    return mappings
