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
            return true()

        ret = Or(map(lambda x: x.simplify(), self.clause))

        ret.clause = filter(lambda x: x.__class__.__name__ != "false",
                            ret.clause)

        if "true" in map(lambda x: x.__class__.__name__, ret.clause):
            return true()

        return ret

    def nnf(self):
        return Or(map(lambda x: x.nnf(), self.clause))

    def cnf(self):

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

    def nnf(self):
        return And(map(lambda x: x.nnf(), self.clause))

    def cnf(self):
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
        #return And([self])
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
        #return And([self])
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
        #return And([self])
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
    print "CNF: "+unicode(expr.cnf())

    expr = And([
        Or([
            Not(Var("p")),
            Var("q")
        ]),
        Var("p")
    ])

    test(expr, ["p", "q"])

    print "Testing setVariables method."
    print "Testing setVariables method - proper copy."
    newexpr = expr.setVariables()

    print unicode(expr)
    print unicode(newexpr)

    print "Testing setVariables method - independent copy."
    newexpr1 = expr.setVariables({"p": False})
    newexpr2 = expr.setVariables({"p": True})
    print unicode(newexpr1)
    print unicode(newexpr1.simplify())
    print unicode(newexpr2)
    print unicode(newexpr2.simplify())

    print "Testing simplify method."
    print unicode(expr.evaluate({"p": False}))
    print unicode(expr.evaluate({"p": True}))

if __name__ == '__main__':
    main()
