# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import unittest

from numbertheory import sqrt_modp, inverse_of


class NumbertheoryTest(unittest.TestCase):
    def _test_square_roots(self, p):
        all_squares = set()
        not_squares = set(range(1, p))
        for x in xrange(1, p):
            all_squares.add((x, pow(x, 2, p)))

        for x, xx in all_squares:
            self.assertTrue(x in sqrt_modp(xx, p))

            if xx in not_squares:
                not_squares.remove(xx)

        for x in not_squares:
            self.assertEquals([], sqrt_modp(x, p))

    def test_square_roots_3_mod_4(self):
        p = 7919
        assert p % 4 == 3
        self._test_square_roots(p)

    def test_square_roots_5_mod_8(self):
        p = 7901
        assert p % 8 == 5
        self._test_square_roots(p)

    def test_other_square_roots(self):
        p = 7873
        assert p % 4 == 1 and p % 8 == 1
        self._test_square_roots(p)

    def test_inverse(self):
        p = 7873

        for n in range(1, 3000):

            all_valid = set()
            for m in range(p):
                if (n * m) % p == 1:
                    all_valid.add(m)
                    break

            self.assertTrue(inverse_of(n, p) in all_valid)


if __name__ == '__main__':
    unittest.main()
