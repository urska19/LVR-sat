#!/usr/bin/env python
import unittest
import test_cnf_basic
import test_simplify_basic
import test_sat

if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromModule(test_cnf_basic)
    suite2 = unittest.TestLoader().loadTestsFromModule(test_simplify_basic)
    suite3 = unittest.TestLoader().loadTestsFromModule(test_sat)

    alltests = unittest.TestSuite([suite1, suite2, suite3])

    unittest.TextTestRunner(verbosity=2).run(alltests)
