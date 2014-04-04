#!/usr/bin/env python


class Var:

    def __init__(self, name):
        self.name = name

    def evaluate(self, assignments={}):
        return (self.setVariables(assignments))

    def setVariables(self, assignments={}):
        '''Returns true(), false() or copy of itself
        depending on assignments.'''

        if(self.name in assignments):
            if(assignments[self.name]):
                return true()
            else:
                return false()

        return Var(self.name)

    def simplify(self):
        return self

    def nnf(self):
        return self

    def cnf(self):
        #assume NNF
        return And([Or([self])])

    def __unicode__(self):
        return unicode(self.name)


class Or:

    def __init__(self, l):
        self.clause = l

    def evaluate(self, assignments={}):
        return (self.setVariables(assignments)).simplify()

    def setVariables(self, assignments={}):
        return Or(map(lambda x: x.setVariables(assignments), self.clause))

    def simplify(self):
        if len(self.clause) == 0:
            return false()

        ret = Or(map(lambda x: x.simplify(), self.clause))

        ret.clause = filter(lambda x: x.__class__.__name__ != "false",
                            ret.clause)

        if "true" in map(lambda x: x.__class__.__name__, ret.clause):
            return true()

        if len(ret.clause) == 0:
            return false()

        return ret

    def deduplicate(self):
        # eliminate duplicate variable instances (and treat negations separately)
        i = 0
        varlist = set()
        negvars = set()
        while i<len(self.clause):
            if self.clause[i].__class__.__name__ == "Var":
                if self.clause[i].name in varlist:
                    del self.clause[i]
                    i-=1
                else:
                    varlist.add(self.clause[i].name)
            if self.clause[i].__class__.__name__ == "Not" and self.clause[i].clause.__class__.__name__ == "Var":
                if self.clause[i].clause.name in negvars:
                    del self.clause[i]
                    i-=1
                else:
                    negvars.add(self.clause[i].clause.name)
            i+=1
        return self

    def nnf(self):
        return Or(map(lambda x: x.nnf(), self.clause))

    def cnf(self):
        #assume NNF

        #PSEUDOCODE
        #remove all nested or classes
        #apply distribution if there are and classes
        #if there are no and classes only thing which remains are literals
            #return and(or(literals))

        #remove nested ors
        newselfclauses = self.clause
        ors = True
        while ors:
            ors = False

            newclause = []

            for i in xrange(len(newselfclauses)):
                if newselfclauses[i].__class__.__name__ == "Or":
                    newclause += newselfclauses[i].clause
                    ors = True
                else:
                    newclause.append(newselfclauses[i])

            newselfclauses = newclause


        #apply distribution
        for i in xrange(len(newclause)):
            if newclause[i].__class__.__name__ == "And":
                complement = newclause[:i] + newclause[i+1:]
                return And(map(lambda x: Or(complement+[x]).deduplicate(), newclause[i].clause)).cnf()

        #return cnf
        return And([Or(newclause).deduplicate()])

    def __unicode__(self):
        return "(" + u" \u2228 ".join(map(unicode, self.clause)) + u")"


class And:

    def __init__(self, l):
        self.clause = l

    def evaluate(self, assignments={}):
        return (self.setVariables(assignments)).simplify()

    def setVariables(self, assignments={}):
        return And(map(lambda x: x.setVariables(assignments), self.clause))

    def simplify(self):

        if len(self.clause) == 0:
            return true()

        ret = And(map(lambda x: x.simplify(), self.clause))

        ret.clause = filter(lambda x: x.__class__.__name__ != "true",
                            ret.clause)

        if "false" in map(lambda x: x.__class__.__name__, ret.clause):
            return false()

        if len(ret.clause) == 0:
            return true()

        return ret

    def deduplicate(self):
        self.clause = map(lambda x: x.deduplicate(), self.clause)
        return self

    def nnf(self):
        return And(map(lambda x: x.nnf(), self.clause))

    def cnf(self):
        #assume NNF

        #PSEUDOCODE
        #propagate cnf
        #remove all nested ands
        #onley thing which remains are or classes - return And(ors)

        #propagate cnf
        newselfclauses = map(lambda x: x.cnf(), self.clause)

        #remove all nested Ands
        ands = True
        while ands:
            ands = False

            newclause = []
            for i in xrange(len(newselfclauses)):
                if newselfclauses[i].__class__.__name__ == "And":
                    newclause += newselfclauses[i].clause
                    ands = True
                else:
                    newclause.append(newselfclauses[i])

            newselfclauses = newclause

        #return cnf
        return And(newclause)

    def __unicode__(self):
        return u"(" + u" \u2227 ".join(map(unicode, self.clause)) + u")"


class Not:
    def __init__(self, l):
        self.clause = l

    def evaluate(self, assignments={}):
        return (self.setVariables(assignments)).simplify()

    def setVariables(self, assignments={}):
        return Not(self.clause.setVariables(assignments))

    def simplify(self):
        formula = self.clause.simplify()
        name = formula.__class__.__name__

        if name == "false":
            return true()
        elif name == "true":
            return false()
        else:
            return Not(formula)

    def deduplicate(self): return self

    def nnf(self):
        if self.clause.__class__.__name__ == "And":
            return Or(map(lambda x: Not(x), self.clause.clause)).nnf()

        if self.clause.__class__.__name__ == "Or":
            return And(map(lambda x: Not(x), self.clause.clause)).nnf()

        if self.clause.__class__.__name__ == "Not":
            return self.clause.clause.nnf()

        if self.clause.__class__.__name__ == "false":
            return true()

        if self.clause.__class__.__name__ == "true":
            return false()

        return Not(self.clause.nnf())

    def cnf(self):
        #assume NNF
        return And([Or([self])])

    def __unicode__(self):
        return u'\u00ac(' + unicode(self.clause) + u")"


class true:

    def evaluate(self, assignments={}):
        return true()

    def simplify(self):
        return self

    def deduplicate(self): return self

    def nnf(self):
        return self

    def cnf(self):
        #assume NNF
        return And([Or([self])])

    def setVariables(self, assignments={}):
        return true()

    def __unicode__(self):
        return u"\u22a4"


class false:

    def evaluate(self, assignments={}):
        return false()

    def simplify(self):
        return self

    def deduplicate(self): return self

    def nnf(self):
        return self

    def cnf(self):
        #assume NNF
        return And([Or([self])])

    def setVariables(self, assignments={}):
        return false()

    def __unicode__(self):
        return u"\u22a5"
