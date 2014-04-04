#!/usr/bin/env python
import unittest
import sys
sys.path.append("..")
from sat import SAT_solver
from logConstructs import *
from graphColoring import graph_coloring
from sudoku import sudoku


class TestSAT(unittest.TestCase):

    def test_true(self):
        solver = SAT_solver()
        self.assertTrue(solver.solve(true())[0])

    def test_false(self):
        solver = SAT_solver()
        self.assertFalse(solver.solve(false())[0])

    def test_variable(self):
        solver = SAT_solver()
        formula = Var("A")
        result = solver.solve(formula)
        self.assertTrue(result[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(result[1]).__class__.__name__)

    def test_variableNegation(self):
        solver = SAT_solver()
        formula = Not(Var("A"))
        result = solver.solve(formula)
        self.assertTrue(result[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(result[1]).__class__.__name__)

    def test_And(self):
        solver = SAT_solver()
        formula = And([Var("A"), Var("B")])
        result = solver.solve(formula)
        self.assertTrue(result[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(result[1]).__class__.__name__)

    def test_Or(self):
        solver = SAT_solver()
        formula = Or([Var("A"), Var("B")])
        result = solver.solve(formula)
        self.assertTrue(result[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(result[1]).__class__.__name__)

    def test_contradiction(self):
        solver = SAT_solver()
        formula = And([Var("A"), Not(Var("A"))])
        result = solver.solve(formula)
        self.assertFalse(result[0])

    def test_completeGraphTwoCollors(self):
        solver = SAT_solver()

        graph = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]
        colors = 2
        formula = graph_coloring(graph, colors)[0]
        solution = solver.solve(formula)
        self.assertFalse(solution[0])

    def test_completeGraphThreeCollors(self):
        solver = SAT_solver()

        graph = [
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1],
        ]

        colors = 3
        formula = graph_coloring(graph, colors)[0]
        solution = solver.solve(formula)
        self.assertTrue(solution[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(solution[1]).__class__.__name__)

    def test_EvenCicleGraphTwoCollors(self):
        solver = SAT_solver()

        graph = [
            [0, 1, 0, 1],
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 1, 0],
        ]

        colors = 2
        formula = graph_coloring(graph, colors)[0]
        solution = solver.solve(formula)
        self.assertTrue(solution[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(solution[1]).__class__.__name__)

    def test_OddCicleGraphTwoCollors(self):
        solver = SAT_solver()

        graph = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0],
        ]

        colors = 2
        formula = graph_coloring(graph, colors)[0]
        solution = solver.solve(formula)
        self.assertFalse(solution[0])


    def test_CustomGraphOneTwoCollors(self):
        solver = SAT_solver()
        graph=[
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0]
        ]

        colors = 2
        formula = graph_coloring(graph, colors)[0]
        solution = solver.solve(formula)
        self.assertFalse(solution[0])

    def test_CustomGraphOneThreeCollors(self):
        solver = SAT_solver()
        graph=[
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0]
        ]

        colors = 3
        formula = graph_coloring(graph, colors)[0]
        solution = solver.solve(formula)
        self.assertFalse(solution[0])

    def test_CustomGraphOneFourCollors(self):
        solver = SAT_solver()
        graph=[
            [0, 1, 1, 1, 1],
            [1, 0, 1, 1, 0],
            [1, 1, 0, 1, 0],
            [1, 1, 1, 0, 1],
            [1, 0, 0, 1, 0]
        ]

        colors = 4
        formula = graph_coloring(graph, colors)[0]
        solution = solver.solve(formula)
        self.assertTrue(solution[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(solution[1]).__class__.__name__)

    def test_SudokuCustom(self):

        solver = SAT_solver()
        board=[[4, 8, None, 1, 6, None, None, None, 7],
         [1, None, 7, 4, None, 3, 6, None, None],
         [3, None, None, 5, None, None, 4, 2, None],
         [None, 9, None, None, 3, 2, 7, None, 4],
         [None, None, None, None, None, None, None, None, None],
         [2, None, 4, 8, 1, None, None, 6, None],
         [None, 4, 1, None, None, 8, None, None, 6],
         [None, None, 6, 7, None, 1, 9, None, 3],
         [7, None, None, None, 9, 6, None, 4, None]]

        formula = sudoku(board)[0]
        solution = solver.solve(formula)

        self.assertTrue(solution[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(solution[1]).__class__.__name__)

    @unittest.expectedFailure
    def test_SudokuEasy(self):

        solver = SAT_solver()
        board=[[None, None, None, 4, None, None, None, 5, None],
         [None, None, None, None, 1, None, 3, 6, None],
         [None, None, 8, None, None, 6, 9, 4, 7],
         [1, None, 2, None, None, None, None, 9, 5],
         [None, 9, None, 2, None, 1, None, None, None],
         [None, None, None, 5, 9, 3, None, None, None],
         [4, None, None, None, None, None, 1, 7, 9],
         [7, 2, None, 1, None, None, None, None, None],
         [None, 8, None, None, None, 9, None, 2, None]]

        formula = sudoku(board)[0]
        solution = solver.solve(formula)

        self.assertTrue(solution[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(solution[1]).__class__.__name__)

    @unittest.expectedFailure
    def test_SudokuMedium(self):

        solver = SAT_solver()
        board=[[None, None, 9, None, 6, 4, None, None, 1],
         [None, None, None, None, 5, None, None, None, None],
         [4, 6, None, 1, None, 7, None, None, 8],
         [None, None, None, None, None, None, None, 9, None],
         [None, None, None, None, 3, None, None, 1, None],
         [3, None, None, None, None, None, None, 4, None],
         [None, 4, 8, None, None, None, 2, None, None],
         [2, None, 7, None, 4, 5, None, 8, 6],
         [5, None, None, None, None, None, None, None, None]]

        formula = sudoku(board)[0]
        solution = solver.solve(formula)

        self.assertTrue(solution[0])
        self.assertEqual("true", formula.nnf().cnf().evaluate(solution[1]).__class__.__name__)


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSAT)
    unittest.TextTestRunner(verbosity=2).run(suite)
