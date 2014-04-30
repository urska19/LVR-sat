from logConstructs import *
from random import shuffle
import time
import threading


class SAT_solver:


    def __init__(self):
        self.maxThreadCount = 5
        self.solutionDict = {}
        self.threads = []
        self.threadsToBe = []
        self.solutionLock = threading.Lock()
        self.addThreadLock = threading.Lock()
        self._stop = threading.Event()
        self.initialize()

    def setMaxThreadCount(self, count):
        """
        Set upper bound for number of threads.
        """

        if count < 2:
            return

        self.maxThreadCount = count

    def initialize(self):
        for thread in self.threads:
            thread.join()
        self.solutionDict = {}
        self.solution = False
        self.threads = []
        self.threadsToBe = []
        self._stop.clear()


    def stop(self):
        """
        Signalize threads to stop execution.
        """

        self._stop.set()

    def stopped(self, mthreading):
        """
        Check if stop signal is raised.

        :mthreading: boolean value indicating if it is multithreading mode of
        operation
        :return: boolean
        """
        if not mthreading:
            return False

        return self._stop.isSet()

    def setSolution(self, dictionary, solution2):
        """
        Set solution in multithreading mode.

        :dictionary: dictionary of variable-value
        :solution2: boolean if dictionary satisfies formula
        :return: void
        """
        if self.solution or not solution2:
            return

        self.solutionLock.acquire()
        self.solutionDict = dictionary
        self.solution = solution2
        self.solutionLock.release()

    def addWorkingThread(self, formula, dictionary):
        """
        Add worker thread in the queue.

        :formula: formula to be satisfied
        :dictionary: dictionary of current variable-value
        """

        self.addThreadLock.acquire()
        self.threadsToBe.append((formula, dictionary, True))
        self.addThreadLock.release()

    def canSetThread(self):
        if len(self.threads) + len(self.threadsToBe) > self.maxThreadCount or self.stopped(True):
            return False
        return True

    def runThreads(self):
        """
        Run threads from the queue.
        """

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
        """
        Run maintainance thread.

        :timeout: period in seconds
        """

        self.addThreadLock.acquire()

        thread = threading.Thread(target=self.maintainanceOfThreads,
                args=(timeout, ))

        thread.daemon = True
        self.threads.append(thread)
        thread.start()

        self.addThreadLock.release()

    def maintainanceOfThreads(self, timeout):
        """
        Thread maintainance.

        :timeout: period in seconds
        """
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
        """
        Up DPLL method.

        :formula: bolean formula
        :return: None if contradiction and dictionary otherwise.
        """
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
        """
        Purge DPLL method.

        :formula: bolean formula
        :return: dictionary of variable-values or None
        """
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
        """
        Helper method for determine if we should return.

        :formula: bolean formula
        :result_dict: dictionary of variable-value
        """
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
        """
        Solve boolean formula.

        :formula: boolean formula
        :mthreading: multithread mode of execution

        :return: (boolean - is formula satisfiable, dictionary - assig values) 
        """
        formula = formula.nnf().cnf().simplify().deduplicate()

        if not mthreading:
            return self.solve_cnf(formula, {})

        #initialize
        self.initialize()

        #add meintanence thread
        self.addMaintainanceThread(0.5)

        #add working thread
        self.addWorkingThread(formula.evaluate(), {})

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

        #return solution
        return (self.solution, self.solutionDict)

    #setting solution dependant of mode of execution
    def returnSolution(self, solution, dictionary, mthreading):
        """
        Return solution based on mode of execution.
        """
        if solution and mthreading:
            self.setSolution(dictionary, solution)

        return (solution, dictionary)

    def findVariable(self, formula):
        """
        Find variable and value which cancels most clauses.
        
        :formula: boolean formula
        :return: (variable, boolean)
        """

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

        return maxvar_name, value

    def solve_cnf(self, formula, result_dict, mthreading=False):
        """
        DPLL algorithm.
        
        :formula: boolean formula.
        :result_dict: dictionary
        :mthreading: (boolean) multithreading mode of execution.
        :return: (boolean - is formula satisfiable, dictionary - values of
        variables)
        """
        temp = result_dict.copy()

        #upping
        while True:

            #if thread is stopped
            if self.stopped(mthreading):
                return self.returnSolution(False, {}, mthreading)

            flag, temp = SAT_solver.canreturn(formula, temp)

            if flag:
                if formula.__class__.__name__ == "true":
                    return self.returnSolution(True, temp, mthreading)
                else:
                    # return self.returnSolution(False, temp, mthreading)
                    return self.returnSolution(False, {}, mthreading)

            result = SAT_solver.up(formula)
            if result is None:
                return self.returnSolution(False, {}, mthreading)
            if result == {}:
                break
            formula = formula.evaluate(result)
            temp.update(result)

        # purging
        while True:
            if self.stopped(mthreading):
                return self.returnSolution(False, {}, mthreading)

            flag, temp = SAT_solver.canreturn(formula, temp)

            if flag:
                if formula.__class__.__name__ == "true":
                    return self.returnSolution(True, temp, mthreading)
                else:
                    # return self.returnSolution(False, temp, mthreading)
                    return self.returnSolution(False, {}, mthreading)

            values = SAT_solver.purge(formula)
            if values == {}:
                break
            formula = formula.evaluate(values)
            temp.update(values)

        if self.stopped(mthreading):
            return self.returnSolution(False, {}, mthreading)

        #heuristic
        maxvar_name, value = self.findVariable(formula)

        #multithreading mode
        literals = [value, not value]
        temp[maxvar_name] = not value

        #seperating check and setting of new thread
        #quicker but larger variation from upper bound
        if(mthreading and self.canSetThread()):
            self.addWorkingThread(formula.evaluate({maxvar_name: not value}), temp.copy())
            literals = [value]

        #recursive calls
        for val in literals:
            if self.stopped(mthreading):
                return self.returnSolution(False, {}, mthreading)

            temp[maxvar_name] = val
            ret = (self.solve_cnf(formula.evaluate({maxvar_name: val}),
                temp, mthreading))[1]

            if ret != {}:
                temp.update(ret)
                return self.returnSolution(True, temp, mthreading)

        return self.returnSolution(False, {}, mthreading)
