from logConstructs import *


class SAT_solver:

    @staticmethod
    def up(formula):
        """Return None if there is contradiction and dictionary otherwise."""
        #filter cluses which contains one element
        fformula = filter(lambda x: len(x.clause) == 1, formula)

        result = {}
        #if there are elements in formula then they are Variable or
        #Not class
        for element in fformula:
            if element.clause.__class__.__name__ == "Var":
                name = element.clause.name
                eresult = True
            else:
                name = element.clause.clause.name
                eresult = False

            #check if formula contains contradiction
            if name in result and result[name] != eresult:
                return None
            else:
                result[name] = eresult

        return result

    #return all elements values which can be purged
    def filterElements(element):
        result = {}
        for el in element:
            if el.__class__.__name__ == "Var":
                name = el.name
                eresult = True
            else:
                name = el.clause.name
                eresult = False

            if name in result[name] and result[name] != eresult:
                result[name] = None
            else:
                result[name] = eresult

        return {i: j for i, j in result.items() if j is not None}

    @staticmethod
    def purge(formula):
        """Return None if there is no elements which can be"""
        """purged or dictionary otherwise."""
        #get all variables in clauses
        assignments = filterElements(reduce(lambda x, y: x + y,
                                            map(lambda x: x.clause, formula)))

        #if there is no element for purging return None
        if assignments == {}:
            return None

        #return purged formula
        return formula.evaluate(assignments)

    def solve(formula):
        #convert to NNF
        #convert to CNF
        #call solve_cnf
        pass

    def solve_cnf(formula):
        #while call values = up != {}
            #if values = None return False
            #formula = formula.evaluate(values)

        #while call purge != None

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
