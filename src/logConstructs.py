#!/usr/bin/env python

'''Logicni elementi za Boolove formule.'''


class Var:
    '''Razred za spremenljivke.'''
    def __init__(self, name):
        self.name = name

    def evaluate(self, assignments={}):
        '''Funkcija, ki vraca vrednost spremenljivke.'''
        return (self.setVariables(assignments))

    def setVariables(self, assignments={}):
        '''Vrne true(), false() ali kopijo sebe.'''

        if(self.name in assignments):
            if(assignments[self.name]):
                return true()
            else:
                return false()

        return Var(self.name)

    def simplify(self):
        '''Poenostavitev.'''
        return self

    def nnf(self):
        '''Negacijska normalna oblika.'''
        return self

    def cnf(self):
        '''Konjuktivna normalna oblika.

           Formula mora biti v negacijski normalni obliki.'''
        return And([Or([self])])

    def __unicode__(self):
        return unicode(self.name)


class Or:
    '''Razred za disjunkcijo.'''
    def __init__(self, l):
        self.clause = l

    def evaluate(self, assignments={}):
        '''Funkcija, ki delno evaluira formulo in jo poenostavi.'''
        return (self.setVariables(assignments)).simplify()

    def setVariables(self, assignments={}):
        '''Funkcija, ki delno evaluira formulo.'''
        return Or(map(lambda x: x.setVariables(assignments), self.clause))

    def simplify(self):
        '''Poenostavitev.'''
        if len(self.clause) == 0:
            return false()

        ret = Or(map(lambda x: x.simplify(), self.clause))

        #odstrani neresnice
        ret.clause = filter(lambda x: x.__class__.__name__ != "false",
                            ret.clause)

        #absorpcija (A or True = True)
        if "true" in map(lambda x: x.__class__.__name__, ret.clause):
            return true()

        #identiteta za disjunkcijo
        if len(ret.clause) == 0:
            return false()

        return ret

    def deduplicate(self):
        '''Funkcija, ki odstrani podvojene literale.'''
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
        '''Negacijska normalna oblika.'''
        return Or(map(lambda x: x.nnf(), self.clause))

    def cnf(self):
        '''Konjuktivna normalna oblika.

           Formula mora biti v negacijski normalni obliki.'''
         
        #=================================================
        #PSEUDOCODE
        #=================================================
        #remove all nested or classes
        #apply distribution if there are and classes
        #if there are no and classes only thing which remains are literals
            #return and(or(literals))
        #remove nested ors
        #=================================================

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


        #uporabi distributivni zakon
        for i in xrange(len(newclause)):
            if newclause[i].__class__.__name__ == "And":
                complement = newclause[:i] + newclause[i+1:]
                return And(map(lambda x: Or(complement+[x]).deduplicate(), newclause[i].clause)).cnf()

        #vrni formulo v konjuktivni normalni obliki
        return And([Or(newclause).deduplicate()])

    def __unicode__(self):
        return "(" + u" \u2228 ".join(map(unicode, self.clause)) + u")"


class And:
    '''Razred za konjunkcijo.'''
    def __init__(self, l):
        self.clause = l

    def evaluate(self, assignments={}):
        '''Funkcija, ki delno evaluira formulo in jo poenostavi.'''
        return (self.setVariables(assignments)).simplify()

    def setVariables(self, assignments={}):
        '''Funkcija, ki delno evaluira formulo.'''
        return And(map(lambda x: x.setVariables(assignments), self.clause))

    def simplify(self):
        '''Poenostavitev.'''
        if len(self.clause) == 0:
            return true()

        ret = And(map(lambda x: x.simplify(), self.clause))

        #odstrani resnice
        ret.clause = filter(lambda x: x.__class__.__name__ != "true",
                            ret.clause)

        #absorpcija (A and False = False)
        if "false" in map(lambda x: x.__class__.__name__, ret.clause):
            return false()

        #identiteta za konjunkcijo
        if len(ret.clause) == 0:
            return true()

        return ret

    def deduplicate(self):
        '''Funkcija, ki odstrani podvojene literale.'''
        self.clause = map(lambda x: x.deduplicate(), self.clause)
        return self

    def nnf(self):
        '''Negacijska normalna oblika.'''
        return And(map(lambda x: x.nnf(), self.clause))

    def cnf(self):
        '''Konjuktivna normalna oblika.

           Formula mora biti v negacijski normalni obliki.'''
 
        #=================================================
        #PSEUDOCODE
        #=================================================
        #propagate cnf
        #remove all nested ands
        #only thing which remains are or classes - return And(ors)
        #=================================================

        #pretvori stavke v konjuktivno normalno obliko
        newselfclauses = map(lambda x: x.cnf(), self.clause)

        #odstrani vgnezdene konjunkcije
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

        #vrni formulo v konjuktivni normalni obliki
        return And(newclause)

    def __unicode__(self):
        return u"(" + u" \u2227 ".join(map(unicode, self.clause)) + u")"


class Not:
    '''Razred za negacijo.'''
    def __init__(self, l):
        self.clause = l

    def evaluate(self, assignments={}):
        '''Funkcija, ki delno evaluira formulo in jo poenostavi.'''
        return (self.setVariables(assignments)).simplify()

    def setVariables(self, assignments={}):
        '''Funkcija, ki delno evaluira formulo.'''
        return Not(self.clause.setVariables(assignments))

    def simplify(self):
        '''Poenostavitev.'''
        formula = self.clause.simplify()
        name = formula.__class__.__name__

        if name == "false":
            return true()
        elif name == "true":
            return false()
        else:
            return Not(formula)

    def deduplicate(self): 
        return self

    def nnf(self):
        '''Negacijska normalna oblika.'''

        #DeMorganov zakon
        if self.clause.__class__.__name__ == "And":
            return Or(map(lambda x: Not(x), self.clause.clause)).nnf()

        #DeMorganov zakon
        if self.clause.__class__.__name__ == "Or":
            return And(map(lambda x: Not(x), self.clause.clause)).nnf()

        #dvojna negacija
        if self.clause.__class__.__name__ == "Not":
            return self.clause.clause.nnf()

        #neresnica postane resnica
        if self.clause.__class__.__name__ == "false":
            return true()

        #resnica postane neresnica
        if self.clause.__class__.__name__ == "true":
            return false()

        return Not(self.clause.nnf())

    def cnf(self):
        '''Konjuktivna normalna oblika.

        Formula mora biti v negacijski normalni obliki.'''
        return And([Or([self])])

    def __unicode__(self):
        return u'\u00ac(' + unicode(self.clause) + u")"


class true:

    '''Razred za resnico.'''

    def evaluate(self, assignments={}):
        return true()

    def simplify(self):
        return self

    def deduplicate(self): return self

    def nnf(self):
        return self

    def cnf(self):
        return And([Or([self])])

    def setVariables(self, assignments={}):
        return true()

    def __unicode__(self):
        return u"\u22a4"


class false:

    '''Razred za neresnico.'''

    def evaluate(self, assignments={}):
        return false()

    def simplify(self):
        return self

    def deduplicate(self): return self

    def nnf(self):
        return self

    def cnf(self):
        return And([Or([self])])

    def setVariables(self, assignments={}):
        return false()

    def __unicode__(self):
        return u"\u22a5"
