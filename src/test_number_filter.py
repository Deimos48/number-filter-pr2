"""Модульные тесты для number_filter.py."""

import unittest
import number_filter as nf


class NumberFilterTests(unittest.TestCase):
    def test_is_prime_typical_values(self):
        for number in (2, 3, 5, 7, 11, 97):
            with self.subTest(number=number):
                self.assertTrue(nf.is_prime(number))
        for number in (4, 6, 8, 9, 10, 25, 100):
            with self.subTest(number=number):
                self.assertFalse(nf.is_prime(number))

    def test_is_prime_boundaries(self):
        for number in (-10, -1, 0, 1):
            with self.subTest(number=number):
                self.assertFalse(nf.is_prime(number))
        self.assertTrue(nf.is_prime(2))

    def test_is_prime_rejects_non_integer(self):
        for value in (True, False, 2.0, "7", None, [], {}):
            with self.subTest(value=value), self.assertRaises(TypeError):
                nf.is_prime(value)

    def test_filter_primes(self):
        self.assertEqual(nf.filter_primes([1, 2, 3, 4, 5, 9, 11]), [2, 3, 5, 11])
        self.assertEqual(nf.filter_primes((-3, 0, 1, 2)), [2])
        self.assertEqual(nf.filter_primes([]), [])

    def test_split_even_odd(self):
        even, odd = nf.split_even_odd([-3, -2, -1, 0, 1, 2, 3, 4])
        self.assertEqual(even, [-2, 0, 2, 4])
        self.assertEqual(odd, [-3, -1, 1, 3])

    def test_split_even_odd_empty(self):
        self.assertEqual(nf.split_even_odd([]), ([], []))

    def test_fibonacci_boundaries(self):
        self.assertEqual(nf.fibonacci_up_to(0), [0])
        self.assertEqual(nf.fibonacci_up_to(1), [0, 1, 1])
        self.assertEqual(nf.fibonacci_up_to(2), [0, 1, 1, 2])

    def test_fibonacci_typical(self):
        self.assertEqual(nf.fibonacci_up_to(10), [0, 1, 1, 2, 3, 5, 8])
        self.assertEqual(nf.fibonacci_up_to(21), [0, 1, 1, 2, 3, 5, 8, 13, 21])

    def test_fibonacci_rejects_negative(self):
        for limit in (-1, -10):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                nf.fibonacci_up_to(limit)

    def test_fibonacci_rejects_non_integer(self):
        for value in (True, 5.0, "5", None):
            with self.subTest(value=value), self.assertRaises(TypeError):
                nf.fibonacci_up_to(value)

    def test_filter_divisible(self):
        self.assertEqual(nf.filter_divisible([0, 1, 2, 3, 4, 5, 6], 2), [0, 2, 4, 6])
        self.assertEqual(nf.filter_divisible([-9, -6, -3, 0, 3, 6, 9], 3), [-9, -6, -3, 0, 3, 6, 9])
        self.assertEqual(nf.filter_divisible([1, 2, 3], 5), [])

    def test_filter_divisible_negative_divisor(self):
        self.assertEqual(nf.filter_divisible([-6, -3, 0, 3, 6, 7], -3), [-6, -3, 0, 3, 6])

    def test_filter_divisible_rejects_zero(self):
        with self.assertRaises(ValueError):
            nf.filter_divisible([1, 2, 3], 0)

    def test_sequence_functions_reject_invalid_container(self):
        for function, args in (
            (nf.filter_primes, ("123",)),
            (nf.split_even_odd, ({1, 2, 3},)),
            (nf.filter_divisible, (123, 2)),
        ):
            with self.subTest(function=function.__name__), self.assertRaises(TypeError):
                function(*args)

    def test_sequence_functions_reject_non_integer_elements(self):
        for function, args in (
            (nf.filter_primes, ([1, 2.0, 3],)),
            (nf.split_even_odd, ([1, True, 3],)),
            (nf.filter_divisible, ([1, "2", 3], 2)),
        ):
            with self.subTest(function=function.__name__), self.assertRaises(TypeError):
                function(*args)

    def test_filter_divisible_rejects_non_integer_divisor(self):
        for divisor in (True, 2.0, "2", None):
            with self.subTest(divisor=divisor), self.assertRaises(TypeError):
                nf.filter_divisible([1, 2, 3], divisor)


if __name__ == "__main__":
    unittest.main()
