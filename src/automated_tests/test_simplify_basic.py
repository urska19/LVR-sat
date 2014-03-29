#!/usr/bin/env python
import unittest
import sys
sys.path.append("..")
from logConstructs import *


class TestSimplifyBasic(unittest.TestCase):

    def test_true(self):
        e = true()
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "true")

    def test_notTrue(self):
        e = Not(true())
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "false")

    def test_false(self):
        e = false()
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "false")

    def test_notFalse(self):
        e = Not(false())
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "true")

    def test_variable(self):
        e = Var("p")
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "Var")
        self.assertEqual(se.name, "p")

    def test_notVariable(self):
        e = Not(Var("p"))
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "Not")
        self.assertEqual(se.clause.__class__.__name__, "Var")
        self.assertEqual(se.clause.name, "p")

    def test_emptyOr(self):
        e = Or([])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "false")

    def test_emptyAnd(self):
        e = And([])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "true")

    def test_and_with_true_element(self):
        e = And([true()])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "true")

    def test_and_with_false_element(self):
        e = And([false()])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "false")

    def test_and_with_true_and_false_element(self):
        e = And([true(), false()])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "false")

    def test_or_with_true_element(self):
        e = Or([true()])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "true")

    def test_or_with_false_element(self):
        e = Or([false()])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "false")

    def test_or_with_true_and_false_element(self):
        e = Or([true(), false()])
        se = e.simplify()
        self.assertEqual(se.__class__.__name__, "true")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSimplifyBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)
