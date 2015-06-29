# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import unittest

import util


class UtilTest(unittest.TestCase):
    def test_little_endian_conv(self):
        self.assertEquals(0, util.le2int('\x00'))
        self.assertEquals(1, util.le2int('\x01'))
        self.assertEquals(0xaaff, util.le2int('\xff\xaa'))
        self.assertEquals(0xaabbcc, util.le2int('\xcc\xbb\xaa'))

        self.assertEquals('\x00', util.int2le(0, 1))
        self.assertEquals('\x00\x00', util.int2le(0, 2))
        self.assertEquals('\x01', util.int2le(1, 1))
        self.assertEquals('\x01\x00', util.int2le(1, 2))
        self.assertEquals('\xff\xaa\x00\x00', util.int2le(0xaaff, 4))

        self.assertEquals('\xdd\xcc\xbb\xaa', util.int2le(0xaabbccdd, 4))

        self.assertRaises(ValueError, util.int2le, 0xaabbccdd, 2)

    def test_big_endian_conv(self):
        self.assertEquals(0, util.be2int('\x00'))
        self.assertEquals(1, util.be2int('\x01'))
        self.assertEquals(0xffaa, util.be2int('\xff\xaa'))
        self.assertEquals(0xccbbaa, util.be2int('\xcc\xbb\xaa'))

        self.assertEquals('\x00', util.int2be(0, 1))
        self.assertEquals('\x00\x00', util.int2be(0, 2))
        self.assertEquals('\x01', util.int2be(1, 1))
        self.assertEquals('\x00\x01', util.int2be(1, 2))
        self.assertEquals('\x00\x00\xaa\xff', util.int2be(0xaaff, 4))

        self.assertEquals('\xdd\xcc\xbb\xaa', util.int2be(0xddccbbaa, 4))

        self.assertRaises(ValueError, util.int2be, 0xaabbccdd, 2)

    def test_count_bits(self):
        self.assertEquals(0, util.count_bits(0b0))
        self.assertEquals(1, util.count_bits(0b1))
        self.assertEquals(2, util.count_bits(0b10))
        self.assertEquals(2, util.count_bits(0b11))
        self.assertEquals(3, util.count_bits(0b100))
        self.assertEquals(3, util.count_bits(0b101))
        self.assertEquals(3, util.count_bits(0b111))
        self.assertEquals(4, util.count_bits(0b1000))
        self.assertEquals(599, util.count_bits(2**599 - 1))
        self.assertEquals(600, util.count_bits(2**599))

    def test_random_correct_range(self):
        for i in xrange(10000):
            r = util.randint(1, 6)
            self.assertTrue(r in [1, 2, 3, 4, 5, 6])


if __name__ == '__main__':
    unittest.main()
