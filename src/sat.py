from logConstructs import *


class SAT_solver:

    @staticmethod
    def up(formula):
        """Return None if there is contradiction and dictionary otherwise."""
        #filter cluses which contains one element
        fformula = filter(lambda x: len(x.clause) == 1, formula.clause)

        result = {}
        #if there are elements in formula then they are Variable or
        #Not class
        for or_clause in fformula:
            for element in or_clause.clause:
                if element.__class__.__name__ == "Var":
                    name = element.name
                    eresult = True
                else:
                    name = element.clause.name
                    eresult = False

                #check if formula contains contradiction
                if name in result and result[name] != eresult:
                    return None
                else:
                    result[name] = eresult

        return result

    @staticmethod
    def purge(formula):
        """Return None if there is no elements which can be"""
        """purged or dictionary otherwise."""
        #get all variables in clauses
        element = reduce(lambda x, y: x + y,
                    map(lambda x: x.clause, formula.clause), [])

        result = {}
        for el in element:
            if el.__class__.__name__ == "Var":
                name = el.name
                eresult = True
            else:
                name = el.clause.name
                eresult = False

            if name in result and result[name] != eresult:
                result[name] = None
            else:
                result[name] = eresult

        return {i: j for i, j in result.items() if j is not None}
    
    def solve(self, formula):
        formula = formula.nnf().cnf().simplify().deduplicate()
        return self.solve_cnf(formula, {})

    def solve_cnf(self, formula, result_dict):
        temp = result_dict.copy()
        while True:
            if formula.__class__.__name__ != "And": return temp
            result = SAT_solver.up(formula)
            if result is None: return {}
            if result == {}: break
            formula = formula.evaluate(result)
            temp.update(result)

        while True:
            if formula.__class__.__name__ != "And": return temp
            values = SAT_solver.purge(formula)
            if values == {}: break
            formula = formula.evaluate(values)
            temp.update(values)

        freq = {}
        maxvar_name = ""
        maxvar_count = -1
        for or_clause in formula.clause:
            for elt in or_clause.clause:
                if elt.__class__.__name__ == "Not":
                    name = elt.clause.name
                else:
                    name = elt.name
                num = freq.get(name,0) + 1
                freq[name] = num
                if num>maxvar_count:
                    maxvar_name = name
                    maxvar_count = num

        for val in [True, False]:
            temp[maxvar_name] = val
            ret = self.solve_cnf(formula.evaluate({maxvar_name: val}), temp)
            if ret != {}:
                temp.update(ret)
                return temp

        return {}

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
