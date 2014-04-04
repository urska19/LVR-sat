from logConstructs import *
from random import shuffle

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
    
    @staticmethod
    def canreturn(formula, result_dict):
        if formula.__class__.__name__ == "true":
            return True, result_dict
        elif formula.__class__.__name__ == "false":
            return True, {}
        elif formula.__class__.__name__ != "And":
            return True, {}
        elif len(formula.clause) == 0:
            return True, result_dict
        return False, result_dict
    
    def solve(self, formula):
        formula = formula.nnf().cnf().simplify().deduplicate()
        return self.solve_cnf(formula, {})

    def solve_cnf(self, formula, result_dict):
        temp = result_dict.copy()
        while True:
            flag, temp = SAT_solver.canreturn(formula, temp)

            if flag:
                if formula.__class__.__name__ == "true":
                    return (True, temp)
                else:
                    return (False, temp)

            result = SAT_solver.up(formula)
            if result is None:
                return (False, {})
            formula = formula.evaluate(result)
            if result == {}:
                break
            temp.update(result)

        flag, temp = SAT_solver.canreturn(formula, temp)
        if flag: return (True, temp)

        while True:
            flag, temp = SAT_solver.canreturn(formula, temp)

            if flag:
                if formula.__class__.__name__ == "true":
                    return (True, temp)
                else:
                    return (False, temp)

            values = SAT_solver.purge(formula)
            if values == {}: break
            formula = formula.evaluate(values)
            temp.update(values)

        flag, temp = SAT_solver.canreturn(formula, temp)
        if flag:
            if formula.__class__.__name__ == "true":
                return (True, temp)
            else:
                return (False, temp)


        # calculate the occurence count for each variable and return the max one
        #print "formula:", unicode(formula), temp
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
        if maxvar_name == "":
            print "maxvar_name is empty", len(formula.clause), unicode(formula)
            #return {}

        literals = [True, False]
        shuffle(literals)
        for val in literals:
            temp[maxvar_name] = val
            ret = (self.solve_cnf(formula.evaluate({maxvar_name: val}), temp))[1]
            if ret != {}:
                temp.update(ret)
                return (True, temp)

        return (False, {})

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
