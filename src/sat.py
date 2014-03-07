from logConstructs import *


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
