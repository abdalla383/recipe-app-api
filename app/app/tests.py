"""
Sample tests
"""
from django.test import SimpleTestCase
from app import calc


# Defining the test class:
class CalcTests(SimpleTestCase):
    """Test the calc module"""

    def test_add_numbers(self):
        """Test adding number together"""
        res = calc.add(5, 6)  # ✅ space after comma
        self.assertEqual(res, 11)  # ✅ space after comma

    def test_subtract_numbers(self):
        """Test subtracting numbers"""
        res = calc.subtract(10, 15)
        self.assertEqual(res, -5)
