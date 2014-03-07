#!/usr/bin/env python
from janVaje1 import *


def evaluateFormula(expr, varlist, assignments={}):
    if len(varlist) == 0:

        value = expr.value(assignments)

        if value:
            return True

        return False

    r_value = False
    for i in [False, True]:
        assignments[varlist[0]] = i
        r_value = r_value or evaluateFormula(expr, varlist[1:], assignments)

    return r_value


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

    #simplifying formula
    main_formula.simplify()

    #constructing variable names
    variable_names = map(lambda x: x.name,
                         reduce(lambda x, y: x + y, variables))


    #evauating
    return evaluateFormula(main_formula, variable_names)



            

def main():
    graph = [
        [1, 1, 1],
        [1, 1, 1],
        [1, 1, 1],
    ]

    colors = 2

 #   print graph
#    print graph_coloring(graph, colors)

    graph = [
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ]

#    print graph
#    print graph_coloring(graph, colors)

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
    
    
    print graph_coloring(sod_cikel, 2)
 #   print graph_coloring(lih_cikel, 2)
#    print graph_coloring(g, 2)
#    print graph_coloring(g, 3)
#    print graph_coloring(g, 4)
 
if __name__ == '__main__':
    main()
