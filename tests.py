try:
    import unittest2 as unittest
except ImportError:
    import unittest

from decimal import Decimal

import ralc


class TestRalc(unittest.TestCase):

    def test_abs_decimal(self):
        self.assertRaises(ValueError, ralc.abs_decimal, '-10.00')
        self.assertRaises(ValueError, ralc.abs_decimal, '-10.00', False)
        self.assertRaises(ValueError, ralc.abs_decimal, Decimal())
        self.assertEqual(str(ralc.abs_decimal(Decimal(), False)), '0.00')
        self.assertEqual(str(ralc.abs_decimal(20)), '20.00')
        self.assertEqual(str(ralc.abs_decimal('25.50')), '25.50')
        self.assertEqual(str(ralc.abs_decimal(25.50)), '25.50')

    def test_calc(self):
        self.assertEqual(ralc.calc('10', '20'), Decimal('200.00'))
        self.assertEqual(ralc.calc('10', '20.50'), Decimal('205.00'))
        self.assertEqual(ralc.calc('10:30', '20'), Decimal('210.00'))
        self.assertEqual(ralc.calc('10:30:45', '25.50'), Decimal('268.26'))

        self.assertEqual(ralc.calc(10, '20'), Decimal('200.00'))
        self.assertEqual(ralc.calc('10:00', 20.5), Decimal('205.00'))
        self.assertEqual(ralc.calc(10.5, 20), Decimal('210.00'))
        self.assertEqual(ralc.calc('10:30:45', Decimal('25.5')),
                         Decimal('268.26'))

    def test_main(self):
        self.assertRaises(SystemExit, ralc.main, 'Invalid', '20')
        self.assertRaises(SystemExit, ralc.main, '10', 'Invalid')
        self.assertFalse(ralc.main('10', '20'))

    def test_validate_hours(self):
        self.assertEqual(ralc.validate_hours(10), Decimal('10.00'))
        self.assertEqual(ralc.validate_hours(10.5), Decimal('10.50'))
        self.assertEqual(ralc.validate_hours('120:40'), Decimal('120.67'))
        self.assertEqual(ralc.validate_hours('10:55:30'), Decimal('10.93'))


if __name__ == '__main__':
    unittest.main()
