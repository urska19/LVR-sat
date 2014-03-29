#!/usr/bin/env python
import unittest
import sys
sys.path.append("..")
from logConstructs import *


class TestCNF_Basic(unittest.TestCase):

    def test_true(self):

        expr1 = true()
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 1)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 1)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "true")

    def test_notTrue(self):

        expr1 = Not(true())
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 1)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 1)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "Not")
        self.assertEquals(cnfexpr1.clause[0].clause[0].clause.__class__.__name__, "true")

    def test_false(self):

        expr1 = false()
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 1)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 1)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "false")

    def test_notTrue(self):

        expr1 = Not(false())
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 1)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 1)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "Not")
        self.assertEquals(cnfexpr1.clause[0].clause[0].clause.__class__.__name__, "false")

    def test_variable(self):

        expr1 = Var("p")
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 1)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 1)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "Var")
        self.assertEqual(cnfexpr1.clause[0].clause[0].name, "p")

    def test_notVariable(self):

        expr1 = Not(Var("p"))
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 1)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 1)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "Not")
        self.assertEquals(cnfexpr1.clause[0].clause[0].clause.__class__.__name__, "Var")
        self.assertEqual(cnfexpr1.clause[0].clause[0].clause.name, "p")

    def test_basicAnd(self):

        expr1 = And([Var("p"), Var("q")])
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 2)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEquals(cnfexpr1.clause[1].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 1)
        self.assertEqual(len(cnfexpr1.clause[1].clause), 1)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "Var")
        self.assertEquals(cnfexpr1.clause[1].clause[0].__class__.__name__, "Var")
        self.assertEqual(cnfexpr1.clause[0].clause[0].name, "p")
        self.assertEqual(cnfexpr1.clause[1].clause[0].name, "q")

    def test_basicOr(self):

        expr1 = Or([Var("p"), Var("q")])
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 1)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 2)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "Var")
        self.assertEquals(cnfexpr1.clause[0].clause[1].__class__.__name__, "Var")
        self.assertEqual(cnfexpr1.clause[0].clause[0].name, "p")
        self.assertEqual(cnfexpr1.clause[0].clause[1].name, "q")

    def test_basicDistribution(self):

        expr1 = Or([Var("p"), And([Var("q"), Var("k")])])
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 2)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[0].clause), 2)
        self.assertEquals(cnfexpr1.clause[1].__class__.__name__, "Or")
        self.assertEqual(len(cnfexpr1.clause[1].clause), 2)
        self.assertEquals(cnfexpr1.clause[0].clause[0].__class__.__name__, "Var")
        self.assertEquals(cnfexpr1.clause[0].clause[1].__class__.__name__, "Var")
        self.assertEquals(cnfexpr1.clause[1].clause[0].__class__.__name__, "Var")
        self.assertEquals(cnfexpr1.clause[1].clause[1].__class__.__name__, "Var")

        self.assertTrue(cnfexpr1.clause[0].clause[0].name == "p" or
                cnfexpr1.clause[0].clause[1].name == "p")

        self.assertTrue(cnfexpr1.clause[1].clause[0].name == "p" or
                cnfexpr1.clause[1].clause[1].name == "p")

        if(cnfexpr1.clause[0].clause[0].name == "p"):
            cnfexpr1.clause[0].clause = [cnfexpr1.clause[0].clause[1]]
        else:
            cnfexpr1.clause[0].clause = [cnfexpr1.clause[0].clause[0]]

        if(cnfexpr1.clause[1].clause[0].name == "p"):
            cnfexpr1.clause[1].clause = [cnfexpr1.clause[1].clause[1]]
        else:
            cnfexpr1.clause[1].clause = [cnfexpr1.clause[1].clause[0]]

        self.assertTrue(cnfexpr1.clause[0].clause[0].name == "q" or
                cnfexpr1.clause[1].clause[0].name == "q")

        self.assertTrue(cnfexpr1.clause[1].clause[0].name == "k" or
                cnfexpr1.clause[0].clause[0].name == "k")

    def test_basicDistributionTwoAnds(self):

        expr1 = Or([And([Var("p"), Var("q")]), Var("h"), And([Var("g"), Var("k")])])
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 4)

        sol = [set(["p", "g", "h"]),
                set(["p", "k", "h"]),
                set(["g", "q", "h"]),
                set(["q", "k", "h"])]

        res = []
        for o in cnfexpr1.clause:
            self.assertEqual(len(o.clause), 3)

            cur = []
            for v in o.clause:
                self.assertEqual(v.__class__.__name__, "Var")
                cur.append(v.name)

            res.append(set(cur))

        for s in sol:
            self.assertTrue(s == res[0] or s == res[1] or s == res[2] or
                    s == res[3])

    def test_basicDistributionWithDeduplicate(self):

        expr1 = Or([Var("p"), And([Var("q"), Var("p")])])
        cnfexpr1 = expr1.cnf()

        self.assertEquals(cnfexpr1.__class__.__name__, "And")
        self.assertEqual(len(cnfexpr1.clause), 2)
        self.assertEquals(cnfexpr1.clause[0].__class__.__name__, "Or")
        self.assertEquals(cnfexpr1.clause[1].__class__.__name__, "Or")

        one = cnfexpr1.clause[0]
        two = cnfexpr1.clause[1]

        if(len(one.clause) != 1):
            tmp = one
            one = two
            two = tmp

        self.assertTrue(len(one.clause) == 1)
        self.assertTrue(len(two.clause) == 2)

        self.assertEquals(one.clause[0].__class__.__name__, "Var")
        self.assertEquals(two.clause[0].__class__.__name__, "Var")
        self.assertEquals(two.clause[1].__class__.__name__, "Var")

        self.assertEqual(one.clause[0].name, "p")

        self.assertTrue(two.clause[0].name == "p" or two.clause[1].name == "p")
        self.assertTrue(two.clause[0].name == "q" or two.clause[1].name == "q")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCNF_Basic)
    unittest.TextTestRunner(verbosity=2).run(suite)
