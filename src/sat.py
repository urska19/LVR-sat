from logConstructs import *
from random import shuffle
import time
import threading


class SAT_solver:

    threads = []
    threadsToBe = []
    maxThreadCount = 5
    addThreadLock = threading.Lock()
    _stop = threading.Event()

    #solution variables for mthreading
    solutionDict = {}
    solution = False
    solutionLock = threading.Lock()

    def __init__(self):
        solutionDict = {}
        threads = []
        threadsToBe = []
        solutionLock = threading.Lock()
        addThreadLock = threading.Lock()
        _stop = threading.Event()
        self.initialize()

    def initialize(self):
        self.solutionDict = {}
        self.solution = False
        self.threads = []
        self.threadsToBe = []
        self._stop.clear()

    def stop(self):
        self._stop.set()

    def stopped(self, mthreading):
        if not mthreading:
            return False

        return self._stop.isSet()

    def setSolution(self, dictionary, solution2):
        if self.solution or not solution2:
            return

        self.solutionLock.acquire()
        self.solutionDict = dictionary
        self.solution = solution2
        self.solutionLock.release()

    def addWorkingThread(self, formula, dictionary):
        if len(self.threads) + len(self.threadsToBe) > self.maxThreadCount:
            return False
        else:
            self.addThreadLock.acquire()
            self.threadsToBe.append((formula, dictionary, True))
            self.addThreadLock.release()
            return True

    def runThreads(self):

        if(len(self.threadsToBe) == 0):
            return

        self.addThreadLock.acquire()
        thrds = self.threadsToBe
        self.threadsToBe = []
        self.addThreadLock.release()

        for argument in thrds:
            thread = threading.Thread(target=self.solve_cnf, args=argument)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)



    def addMaintainanceThread(self, timeout):
        self.addThreadLock.acquire()

        thread = threading.Thread(target=self.maintainanceOfThreads,
                args=(timeout, ))

        thread.daemon = True
        self.threads.append(thread)
        thread.start()

        self.addThreadLock.release()

    def maintainanceOfThreads(self, timeout):
        while(True):
            if self.stopped(True):
                break

            before = len(self.threads)
            self.addThreadLock.acquire()
            self.threads = filter(lambda x: x.isAlive(), self.threads)
            self.addThreadLock.release()
            time.sleep(timeout)


    @staticmethod
    def up(formula):
        """Return None if there is contradiction and dictionary otherwise."""
        #filter clauses which contains one element
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

    def solve(self, formula, mthreading=False):
        formula = formula.nnf().cnf().simplify().deduplicate()

        if not mthreading:
            return self.solve_cnf(formula, {})

        #initialize
        self.initialize()

        #add meintanence thread
        self.addMaintainanceThread(2)

        #add working thread
        self.addWorkingThread(formula, {})

        #wait untill solution is found or all threads exit
        while(True):

            self.runThreads()

            if(self.solution or (len(self.threads) + len(self.threadsToBe) ==
                1)):
                break

            #if there exist maximum number of threads sleep longer
            if len(self.threads) > self.maxThreadCount:
                time.sleep(2)
            else:
                time.sleep(0.1)

        #kill all threads
        self.stop()
        for thread in self.threads:
            thread.join()

        self._stop.clear()

        #return solution
        return (self.solution, self.solutionDict)

    #setting solution dependant of mode of execution
    def returnSolution(self, solution, dictionary, mthreading):
        if solution and mthreading:
            self.setSolution(dictionary, solution)

        return (solution, dictionary)

    def solve_cnf(self, formula, result_dict, mthreading=False):
        temp = result_dict.copy()

        #upping
        while True:

            #if thread is stopped
            if self.stopped(mthreading):
                self.returnSolution(False, {}, mthreading)

            flag, temp = SAT_solver.canreturn(formula, temp)

            if flag:
                if formula.__class__.__name__ == "true":
                    return self.returnSolution(True, temp, mthreading)
                else:
                    return self.returnSolution(False, temp, mthreading)

            result = SAT_solver.up(formula)
            if result is None:
                return self.returnSolution(False, {}, mthreading)
            formula = formula.evaluate(result)
            if result == {}:
                break
            temp.update(result)


        flag, temp = SAT_solver.canreturn(formula, temp)
        if flag:
            return self.returnSolution(True, temp, mthreading)

        # purging
        while True:
            if self.stopped(mthreading):
                self.returnSolution(False, {}, mthreading)

            flag, temp = SAT_solver.canreturn(formula, temp)

            if flag:
                if formula.__class__.__name__ == "true":
                    return self.returnSolution(True, temp, mthreading)
                else:
                    return self.returnSolution(False, temp, mthreading)

            values = SAT_solver.purge(formula)
            if values == {}:
                break
            formula = formula.evaluate(values)
            temp.update(values)

        flag, temp = SAT_solver.canreturn(formula, temp)
        if flag:
            if formula.__class__.__name__ == "true":
                return self.returnSolution(True, temp, mthreading)
            else:
                return self.returnSolution(False, temp, mthreading)

        if self.stopped(mthreading):
            self.returnSolution(False, {}, mthreading)
        # heuristic - find variable which cancels max num of clauses.
        # take into account negation
        freq = {}
        maxvar_name = ""
        maxvar_count = -1
        value = True
        for or_clause in formula.clause:
            for elt in or_clause.clause:
                #get name
                lvalue = False
                if elt.__class__.__name__ == "Not":
                    name = elt.clause.name
                else:
                    name = elt.name
                    lvalue = True

                #add one to variable count depending if it is negation or not
                num = freq.get(name, (0, 0))
                if lvalue:
                    num = (num[0] + 1, num[1])
                else:
                    num = (num[0], num[1] + 1)

                #check if this variable is maximum occurring variable for now.
                freq[name] = num
                if num[0] > maxvar_count:
                    maxvar_name = name
                    maxvar_count = num[0]
                    value = True
                elif num[1] > maxvar_count:
                    maxvar_name = name
                    maxvar_count = num[1]
                    value = False

        # recursive call
        literals = [value, not value]

        #multithreading mode
        temp[maxvar_name] = not value
        if(mthreading and self.addWorkingThread(formula.evaluate({maxvar_name:
            not value}), temp)):
            literals = [value]

        #recursive calls
        for val in literals:
            if self.stopped(mthreading):
                self.returnSolution(False, {}, mthreading)

            temp[maxvar_name] = val
            ret = (self.solve_cnf(formula.evaluate({maxvar_name: val}), temp))[1]

            if ret != {}:
                temp.update(ret)
                return self.returnSolution(True, temp, mthreading)

        return self.returnSolution(False, {}, mthreading)
