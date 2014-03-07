#!/usr/bin/env python


class Var:

    def __init__(self, name):
        self.name = name

    def value(self, assignments):
        return assignments[self.name]

    def simplify(self):
        return self

    def __unicode__(self):
        return unicode(self.name)


class Or:

    def __init__(self, l):
        self.clause = l

    def value(self, assignments):
        return reduce(lambda x, y: x or y,
                      map(lambda x: x.value(assignments), self.clause))

    def simplify(self):
        if len(self.clause) == 0:
            return true()

        ret = Or(map(lambda x: x.simplify(), self.clause))

        ret.clause = filter(lambda x: x.__class__.__name__ != "false",
                            ret.clause)

        if "true" in map(lambda x: x.__class__.__name__, ret.clause):
            return true()

        return ret

    def __unicode__(self):
        return "(" + u" \u2228 ".join(map(unicode, self.clause)) + u")"


class And:

    def __init__(self, l):
        self.clause = l

    def value(self, assignments):
        return reduce(lambda x, y: x and y, map(lambda x: x.value(assignments),
                                                self.clause))

    def simplify(self):

        if len(self.clause) == 0:
            return true()

        ret = And(map(lambda x: x.simplify(), self.clause))

        ret.clause = filter(lambda x: x.__class__.__name__ != "true",
                            ret.clause)

        if "false" in map(lambda x: x.__class__.__name__, ret.clause):
            return false()

        return ret

    def __unicode__(self):
        return u"(" + u" \u2227 ".join(map(unicode, self.clause)) + u")"


class Not:
    def __init__(self, l):
        self.clause = l

    def value(self, assignments):
        return not self.clause.value(assignments)

    def simplify(self):
        if self.clause.__class__.__name__ == "And":
            return Or(map(lambda x: Not(x), self.clause.clause)).simplify()

        if self.clause.__class__.__name__ == "Or":
            return And(map(lambda x: Not(x), self.clause.clause)).simplify()

        if self.clause.__class__.__name__ == "Not":
            return self.clause.clause.simplify()

        if self.clause.__class__.__name__ == "false":
            return true()

        if self.clause.__class__.__name__ == "true":
            return false()

        return Not(self.clause.simplify())

    def __unicode__(self):
        return u'\u00ac(' + unicode(self.clause) + u")"


class true:
    def value(self, assignments):
        return True

    def simplify(self):
        return self

    def __unicode__(self):
        return u"\u22a4"


class false:
    def value(self, assignments):
        return False

    def simplify(self):
        return self

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

    expr = And([
        Or([
            Not(Var("p")),
            Var("q")
        ]),
        Var("p")
    ])

    test(expr, ["p", "q"])

if __name__ == '__main__':
    main()
