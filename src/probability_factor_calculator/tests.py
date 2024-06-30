# tests.py
import unittest
from src.probability_calculator import calculate_total_probability

class TestProbabilityCalculator(unittest.TestCase):

    def test_case_1(self):
        # Case 1: X=3-W N=5-C C=2 W=1
        probability_factors = [("3-W", "5-C")]
        variables = {"C": 2, "W": 1}
        result = calculate_total_probability(probability_factors, variables)
        expected = 0.125  # expected result
        self.assertAlmostEqual(result, expected, places=3, msg="Case 1 failed")

    def test_case_2(self):
        # Case 2: X=1.5 N=3.6
        probability_factors = [("1.5", "3.6")]
        variables = {}
        result = calculate_total_probability(probability_factors, variables)
        expected = 0.23  # expected result
        self.assertAlmostEqual(result, expected, places=2, msg="Case 2 failed")

    def test_case_3(self):
        # Case 3: Combined probabilities with variables
        probability_factors = [("3-W", "5-C"), ("1.5", "3.6")]
        variables = {"C": 2, "W": 1}
        result = calculate_total_probability(probability_factors, variables)
        expected = 0.029  # expected result
        self.assertAlmostEqual(result, expected, places=3, msg="Case 3 failed")

if __name__ == '__main__':
    unittest.main()
