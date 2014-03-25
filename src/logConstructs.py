#!/usr/bin/env python


class Var:

    def __init__(self, name):
        self.name = name

    def value(self, assignments):
        return assignments[self.name]

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

    def value(self, assignments):
        return reduce(lambda x, y: x or y,
                      map(lambda x: x.value(assignments), self.clause))

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
                return And(map(lambda x: Or(complement+[x]), newclause[i].clause)).cnf()

        #return cnf
        return And([Or(newclause)])

    def __unicode__(self):
        return "(" + u" \u2228 ".join(map(unicode, self.clause)) + u")"


class And:

    def __init__(self, l):
        self.clause = l

    def value(self, assignments):
        return reduce(lambda x, y: x and y, map(lambda x: x.value(assignments),
                                                self.clause))

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

        return ret

    def deduplicate(self):
        self.clause = map(lambda x: x.deduplicate(), self.clause)

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

    #should not be used
    def value(self, assignments):
        return not self.clause.value(assignments)

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
    def value(self, assignments):
        return True

    def evaluate(self, assignments={}):
        return true()

    def simplify(self):
        return self

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
    def value(self, assignments):
        return False

    def evaluate(self, assignments={}):
        return false()

    def simplify(self):
        return self

    def nnf(self):
        return self

    def cnf(self):
        #assume NNF
        return And([Or([self])])

    def setVariables(self, assignments={}):
        return false()

    def __unicode__(self):
        return u"\u22a5"


def main():
    # first task
    expr1 = Not(And([Var("p"), Var("q")]))
    expr2 = Or([Not(Var("p")), Not(Var("q"))])

    print unicode(expr1)
    print unicode(expr2)

    # second task
    for p in (False, True):
        for q in (False, True):
            print expr1.value({"p": p, "q": q}), " == ",
            expr2.value({"p": p, "q": q})

    # third task
    print unicode(expr1.simplify())
    print unicode(expr2.simplify())

    # examples

    expr = Or([false(), Var("p")])
    print unicode(expr) + " => " + unicode(expr.simplify())
    expr = And([true(), Var("p")])
    print unicode(expr) + " => " + unicode(expr.simplify())
    expr = Not(false())
    print unicode(expr) + " => " + unicode(expr.simplify())

    # test cases
    def pretty(expr):
        print unicode(expr) + " => " + unicode(expr.simplify())

    def test(expr, varlist, assignments={}):
        if len(varlist) == 0:
            print ""
            pretty(expr)
            print `assignments` + " -> " + `expr.value(assignments)`
            return

        for i in [False, True]:
            assignments[varlist[0]] = i
            test(expr, varlist[1:], assignments)

    expr = Or([
        Var("p"),
        And([
            Var("q"),
            Var("p")
            ])
    ])

    test(expr,  ["p", "q"])
    print "================================================="
    print "CNF"
    print "================================================="
    expr = Or([
        Var("p"),
        And([
            Var("q"),
            Var("p")
            ])
    ])
    expr2 = Var("p")
    expr3 = Or([Var("p"), Var("q")])
    expr4 = Or([And([Var("p"), Var("q")]), Var("h"), And([Var("g"), Var("k")])])
    expr5 = true()
    expr6 = false()
    expr7 = And([Var("p"), Var("q")])

    print "Expression: " + unicode(expr2)
    print "Expression (CNF): "+ unicode(expr2.cnf())
    print "Expression: " + unicode(expr5)
    print "Expression (CNF): "+ unicode(expr5.cnf())
    print "Expression: " + unicode(expr6)
    print "Expression (CNF): "+ unicode(expr6.cnf())
    print "Expression: " + unicode(expr3)
    print "Expression (CNF): "+ unicode(expr3.cnf())
    print "Expression: " + unicode(expr7)
    print "Expression (CNF): "+ unicode(expr7.cnf())
    print "Expression: " + unicode(expr)
    print "Expression (CNF): "+ unicode(expr.cnf())
    print "Expression: " + unicode(expr4)
    print "Expression (CNF): "+ unicode(expr4.cnf())
    print "================================================="

    print "================================================="
    print "Test function."
    print "================================================="
    expr = And([
        Or([
            Not(Var("p")),
            Var("q")
        ]),
        Var("p")
    ])
    test(expr, ["p", "q"])
    print "================================================="
    print "================================================="
    print "Testing setVariables method."
    print "================================================="
    print "Testing setVariables method - proper copy."
    print "================================================="
    newexpr = expr.setVariables()
    newexpr2 = expr.setVariables({"p": False})

    print "Expression: " + unicode(expr)
    print "Expression (setVariables-empty): " + unicode(newexpr)
    print "Expression (setVariables- p->False): " + unicode(newexpr2)

    print "================================================="
    print "Testing setVariables method - independent copy."
    print "================================================="

    newexpr1 = expr.setVariables({"p": False})
    newexpr2 = expr.setVariables({"p": True})
    newexpr3 = expr.setVariables({"z": True})

    print "Expression: " + unicode(expr)
    print "Expression (p->False): " + unicode(newexpr1)
    print "Expression (p->True): " + unicode(newexpr2)
    print "Expression (z->True): " + unicode(newexpr3)

    print "================================================="
    print "================================================="
    print "Testing simplify method."
    print "================================================="
    print "Expression: " + unicode(expr)
    print "Expression (p -> False): " + unicode(expr.evaluate({"p": False}))
    print "Expression (p -> True): " + unicode(expr.evaluate({"p": True}))
    print "================================================="

if __name__ == '__main__':
    main()
