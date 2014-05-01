#!/usr/bin/env python
import unittest
import test_cnf_basic
import test_simplify_basic
import test_sat
import test_sat_mt
import test_sat_flat

if __name__ == "__main__":
    suite1 = unittest.TestLoader().loadTestsFromModule(test_cnf_basic)
    suite2 = unittest.TestLoader().loadTestsFromModule(test_simplify_basic)
    suite3 = unittest.TestLoader().loadTestsFromModule(test_sat)
    suite4 = unittest.TestLoader().loadTestsFromModule(test_sat_mt)
    suite5 = unittest.TestLoader().loadTestsFromModule(test_sat_flat)

    alltests = unittest.TestSuite([suite1, suite2, suite3, suite4, suite5])

    unittest.TextTestRunner(verbosity=2).run(alltests)
