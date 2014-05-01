# vim: et:sts=4:sw=4:

from logConstructs import *
from random import shuffle
import multiprocessing as mp
import cPickle

class QueueWrapper:
    def __init__(self, poolsize):
        self.q = mp.Queue()
        self.limit = poolsize
        self.counter = mp.Value('L', 0)
        self.waiters = mp.Value('L', 0)
        self.cond = mp.Condition()
        self.killed = mp.Event()

    def put(self, obj):
        self.cond.acquire()
        if self.killed.is_set():
            self.cond.release()
            return
        with self.counter.get_lock():
            self.counter.value += 1
        self.q.put(cPickle.dumps(obj))
        self.cond.notify()
        self.cond.release()

    def get(self):
        self.cond.acquire()
        if self.killed.is_set():
            self.cond.release()
            return None

        with self.waiters.get_lock():
            self.waiters.value += 1
        if self.waiters.value == self.limit and self.counter.value == 0:
            with self.waiters.get_lock():
                self.waiters.value -= 1
            self.cond.release()
            return None

        while self.counter.value == 0 and not self.killed.is_set():
            self.cond.wait()

        if self.killed.is_set():
            with self.counter.get_lock():
                while self.counter.value > 0:
                    self.q.get()
                    self.counter.value -= 1
            self.cond.release()
            return None

        ret = cPickle.loads(self.q.get())
        with self.counter.get_lock():
            self.counter.value -= 1
        self.cond.release()
        return ret

    def kill(self):
        self.cond.acquire()
        self.killed.set()
        self.cond.notify_all()
        self.cond.release()

class SAT_solver:

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
    
    def solve(self, formula, force_nprocs = None):
        if formula.__class__.__name__ == "FlatCNF":
            return self.solve_flat_toplevel(formula, force_nprocs = force_nprocs)
        formula = formula.nnf().cnf().simplify().deduplicate()
        return self.solve_cnf(formula, {})

    def solve_cnf(self, formula, result_dict):
        temp = result_dict.copy()

        #print "solving CNF"
        
        #upping
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

        #print "after upping"

        flag, temp = SAT_solver.canreturn(formula, temp)
        if flag: return (True, temp)

        # purging
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

        #print "after purging"

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
        #print "branching on", maxvar_name
        for val in literals:
            temp[maxvar_name] = val
            ret = (self.solve_cnf(formula.evaluate({maxvar_name: val}), temp))[1]
            if ret != {}:
                temp.update(ret)
                return (True, temp)

        return (False, {})

    def solve_flat_toplevel(self, formula, force_nprocs = None):
        try:
            nprocs = mp.cpu_count()
        except:
            nprocs = 2
        if force_nprocs is not None: nprocs = force_nprocs
        nprocs = 2

        # manage our own process "pool", since the waiting requirements would make
        # it impractical to use the builtin one
        resultlock = mp.Lock()
        result = mp.Queue(1)
        q = QueueWrapper(nprocs)
        #formula.dump("formula.cnf")
        pool = [mp.Process(name="sat", target=SAT_solver.queue_worker, args=(q, resultlock, result)) for i in range(nprocs)]
        q.put({"formula":formula, "assignments":{}})
        map(mp.Process.start, pool)

        d = result.get()

        map(mp.Process.terminate, pool)
        map(mp.Process.join, pool)

        #s = []
        #for k in d:
        #    if d[k]: s.append(k)
        #print sorted(s)
        return (len(d) > 0, d)

    @staticmethod
    def queue_worker(q, resultlock, result):
        # make it easier to break execution when we find a contradiction/etc., so we don't
        # have to make tons of flags and if's in place of goto's
        # if we get a final boolean result here, return that; otherwise return None
        def work_section(formula, assignments):

            # sanity check: do we have any subnodes?
            if len(formula.clauses) < 1: return True, 0

            # check for empty clauses
            for or_node in formula.clauses:
                if len(or_node)==0:
                    return False, 0

            # unit propagation; check for contradictions between single-element or-clauses
            # and partially evaluate
            flag = True
            while flag:
                flag = False
                contraset = set()
                for or_node in formula.clauses:
                    if len(or_node) != 1:
                        continue
                    var = or_node.pop()
                    if -var in contraset:
                        return False, 0
                    contraset.add(var)
                    assignments[abs(var)] = (var>=0)
                    flag = True
                for var in contraset:
                    if formula.evaluate(var, (var>=0)) == False:
                        return False, 0
            if len(formula.clauses) < 1: return True, 0

            # pure literal elimination; check if any variable appears with only one polarity
            polarset = set(reduce(set.union, formula.clauses))
            for i in polarset:
                if -i in polarset:
                    continue
                assignments[abs(i)] = (i>=0)
                formula.evaluate(i, (i>=0))
            if len(formula.clauses) < 1: return True, 0

            # determine the most common variable and tell the caller to branch on it
            var_counts = {}
            maxvar = -1
            var_counts[-1] = 0
            for or_node in formula.clauses:
                for var in or_node:
                    var_counts[var] = var_counts.get(var,0) + 1
                    if var_counts[var] > var_counts[maxvar]: maxvar = var
            return None, maxvar

        while True:
            work = q.get()
            if work is None:
                if resultlock.acquire(False):
                    result.put({})
                break

            assignments = work["assignments"]
            formula = work["formula"]

            solvable, maxvar = work_section(formula, assignments)
            #print solvable, maxvar, assignments

            # check if we can terminate already
            if solvable == True:
                if resultlock.acquire(False):
                    # assign all the remaining variables to a default value
                    # since the formula is solvable anyway, it doesn't matter what the value really is
                    for or_node in formula.clauses:
                        for var in or_node:
                            if abs(var) not in assignments: assignments[abs(var)] = True
                    result.put(formula.rename(assignments))
                    q.kill()
                    print "found solution, terminating"
                break
            if solvable == False:
                print "dead branch, next"
                continue

            # now enqueue both branches
            #print "branching on", maxvar
            assignments[abs(maxvar)] = (maxvar>=0)
            newformula = formula.clone().evaluate(maxvar, maxvar>=0)
            if newformula != False:
                q.put({"formula":newformula, "assignments":assignments})
            #print "  > > put in two new works", assignments, maxvar, unicode(formula)

            assignments[abs(maxvar)] = (maxvar<0)
            newformula = formula.clone().evaluate(maxvar, maxvar<0)
            if newformula != False:
                q.put({"formula":newformula, "assignments":assignments})
            #print "  >>> put in two new works", assignments, maxvar, unicode(formula)
        print "worker terminating, bye"
