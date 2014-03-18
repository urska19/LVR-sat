from logConstructs import *


class SAT_solver:

    @staticmethod
    def up(formula):
        #forall Or nodes with size of clause == 1 add variable name and value to dictionary
        #if variable has True and False add special value
        #return dictionary
        pass

    @staticmethod
    def purge(formula):
        pass

    def solve(formula):
        #convert to NNF
        #convert to CNF
        #call solve_cnf
        pass

    def solve_cnf(formula):
        #while call up != []
            #dictinary = up(formula)
            #if dictionary contains special value return False
            #formula = formula.evaluate(dictionary)

        #while call purge != []
            #dictionary = purge(formula)
            #formula = formula.evaluate(dictionary)

        #scan for remaining variables

        #=============================================
        #multithreading - spliting search
        #=============================================
        #heuristic - some heuristic for variable selection
        #=============================================
        #select a variable v
        #set v to false, evaluate and call solve_cnf
        #if return == True return True
        #set v to true, evaluate and call solve_cnf
        #if return == True return True
        #return False

        pass


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
