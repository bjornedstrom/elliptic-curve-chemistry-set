# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import unittest

import asymmetric
import reference_ed25519 as ref_ed
#import re
import curve as curvemod

def arr2str(arr):
    return ''.join(map(chr, arr))


# https://github.com/Yawning/libelligator/blob/master/src/tests/kat.cc
class Curve25519KeyTest(unittest.TestCase):
    def setUp(self):
        self.curve25519 = asymmetric.ECC_Curve25519()

    def test_vector_1(self):
        VALID = True
        PUB = [0x4b, 0x97, 0x97, 0xd0, 0x98, 0x5a, 0xf7, 0x42, 0x9b, 0xc3, 0x55, 0xd9, 0x4, 0x81, 0xcf, 0xc7, 0xcc, 0x14, 0x54, 0x5c, 0xa5, 0xe6, 0x7c, 0x84, 0xcb, 0x1b, 0x4a, 0x4c, 0x4d, 0xa1, 0xda, 0x33]
        REPR = [0xbc, 0x13, 0x1a, 0x67, 0xb, 0x92, 0x2, 0x65, 0x8f, 0x2f, 0x79, 0xa, 0x7e, 0x4, 0x71, 0xd0, 0xe, 0x67, 0x90, 0xdb, 0x4d, 0x59, 0x8, 0xd2, 0x54, 0x4e, 0x5f, 0xbb, 0x8d, 0xa, 0x89, 0x78]
        PRIV = [0x10, 0x3d, 0xba, 0xb8, 0x6f, 0x99, 0xee, 0xdb, 0xec, 0xa, 0xd6, 0x8f, 0xa9, 0x20, 0x3d, 0x5f, 0xd4, 0xf5, 0xe0, 0xdc, 0x48, 0xbc, 0xaf, 0x6c, 0x98, 0x50, 0xd0, 0x1a, 0x12, 0x9f, 0x28, 0x5c]

        self._test_with_vector(PUB, REPR, PRIV, VALID)

    def test_vector_2(self):
        VALID = True
        PUB = [0xf1, 0x8, 0x6d, 0x75, 0xb3, 0x59, 0x5c, 0xe7, 0x3c, 0x41, 0xa8, 0x11, 0xbf, 0x1a, 0x10, 0xb1, 0xba, 0x1a, 0x75, 0xe4, 0xff, 0xd4, 0x98, 0x6c, 0x37, 0x98, 0xe3, 0x54, 0xf3, 0x24, 0x6b, 0x50]
        REPR = [0x6, 0x13, 0x6a, 0x4f, 0x20, 0x93, 0x37, 0x12, 0x4f, 0x4d, 0x92, 0x31, 0xc8, 0x34, 0xe9, 0xa0, 0x94, 0x8f, 0x89, 0x6d, 0xc9, 0x1c, 0x85, 0x5b, 0x32, 0x80, 0xd3, 0xd1, 0x4f, 0x42, 0xe8, 0x4e]
        PRIV = [0x68, 0x4f, 0x96, 0xdf, 0xde, 0xa0, 0x57, 0xf5, 0xb2, 0x3f, 0xf6, 0x29, 0x52, 0xb3, 0x34, 0x95, 0xb0, 0x7b, 0xa3, 0xd5, 0x4, 0xac, 0x79, 0x1d, 0xf, 0x3c, 0x87, 0x52, 0x3a, 0xa7, 0x3f, 0x6d]

        self._test_with_vector(PUB, REPR, PRIV, VALID)

    def test_vector_3(self):
        VALID = True
        PUB = [0x49, 0x76, 0xe, 0x1, 0x60, 0x24, 0x44, 0x48, 0x48, 0xc7, 0x9d, 0xc1, 0x81, 0x4, 0x6d, 0xc, 0x3a, 0x48, 0x8e, 0xf8, 0x67, 0xbd, 0xf9, 0xd1, 0x6f, 0x8c, 0x8f, 0xe4, 0x9b, 0x7b, 0x7f, 0x66]
        REPR = [0xb7, 0xdd, 0x0, 0x28, 0x3, 0xe0, 0x9f, 0x93, 0x52, 0x5d, 0xf6, 0x49, 0xa3, 0x9, 0xbf, 0x29, 0x16, 0x71, 0xfd, 0x82, 0x52, 0x23, 0xf2, 0x96, 0x2, 0xee, 0x97, 0x20, 0xc1, 0xd7, 0xa6, 0x3b]
        PRIV = [0x8, 0x69, 0x14, 0xc7, 0xc7, 0xe8, 0x33, 0x79, 0x27, 0xf4, 0xa7, 0x1c, 0xda, 0x21, 0x25, 0x41, 0x9a, 0xe7, 0xe1, 0x83, 0x90, 0x52, 0x1f, 0xaf, 0x14, 0x3d, 0x5a, 0x2, 0xbc, 0x2e, 0x9c, 0x55]

        self._test_with_vector(PUB, REPR, PRIV, VALID)

    def test_vector_6(self):
        VALID = True
        PUB = [0x1e, 0x92, 0x62, 0xd, 0xc3, 0x9f, 0xf1, 0x28, 0x86, 0x40, 0x80, 0xb1, 0xfd, 0x37, 0xb9, 0x91, 0xac, 0xcc, 0xbf, 0x3d, 0x2e, 0x48, 0x67, 0xd2, 0xed, 0xf1, 0x75, 0xa6, 0x58, 0x10, 0x6d, 0x55]
        REPR = [0x5a, 0x25, 0x9d, 0x71, 0x1f, 0xec, 0xb2, 0x6d, 0xe7, 0x8, 0x4f, 0x8d, 0x80, 0x15, 0x4e, 0xec, 0x8c, 0xa3, 0xde, 0xd5, 0xde, 0x3f, 0xb6, 0x2f, 0x38, 0xc8, 0x6b, 0xf5, 0xf6, 0x84, 0x6e, 0x26]
        PRIV = [0x28, 0x4f, 0x7, 0xcf, 0x45, 0xc0, 0x56, 0x74, 0xc6, 0xa7, 0xce, 0xa4, 0x8e, 0xf1, 0x83, 0xb7, 0xb5, 0x22, 0x3c, 0xff, 0xe9, 0x2e, 0xa7, 0xcb, 0x78, 0xa2, 0x3, 0x1a, 0x47, 0x54, 0xc, 0x6d]

        self._test_with_vector(PUB, REPR, PRIV, VALID)

    def test_vector_9(self):
        VALID = True
        PUB = [0x64, 0x27, 0xe0, 0x5, 0x13, 0xab, 0x7a, 0x81, 0x46, 0xd5, 0x8e, 0xbc, 0x28, 0x25, 0xf4, 0x66, 0xe3, 0x1c, 0x12, 0xbf, 0x97, 0x25, 0x99, 0x20, 0x37, 0x27, 0xd6, 0x1e, 0x9b, 0x6a, 0x6e, 0x7d]
        REPR = [0x5f, 0x9e, 0x2, 0x23, 0x7c, 0xa4, 0xfc, 0xc2, 0xc1, 0x8c, 0xc8, 0x91, 0x53, 0xdb, 0xa7, 0x5c, 0xca, 0x58, 0xea, 0x12, 0x60, 0x41, 0x3f, 0x36, 0xe, 0xe7, 0x7d, 0x78, 0x1d, 0x72, 0xa9, 0x33]
        PRIV = [0x80, 0x5a, 0x8f, 0xba, 0x73, 0x45, 0x30, 0xc8, 0xf0, 0xb7, 0x64, 0x6a, 0xae, 0x73, 0x6f, 0x54, 0x65, 0x22, 0x5, 0xe8, 0x7, 0xd6, 0xab, 0x83, 0xc2, 0xe6, 0x79, 0x5e, 0x9a, 0x73, 0x22, 0x78]

        self._test_with_vector(PUB, REPR, PRIV, VALID)

    def _test_with_vector(self, PUB, REPR, PRIV, VALID):
        Repr = ref_ed.decodeint(''.join(map(chr, REPR)))
        X = ref_ed.decodeint(''.join(map(chr, PUB)))
        Priv = ref_ed.decodeint(''.join(map(chr, PRIV)))
        Pub = curvemod.montgomery_ladder(Priv, self.curve25519.base_point, self.curve25519.curve)

        self.assertEquals(arr2str(PRIV), self.curve25519.canonical_binary_form_private(Priv))
        self.assertEquals(arr2str(PUB), self.curve25519.canonical_binary_form_public(Pub))

        self.assertEquals(Priv, self.curve25519.binary_to_private(arr2str(PRIV)))
        #self.assertEquals(Pub, self.curve25519.non_canonical_binary_to_public(arr2str(PUB)))


if __name__ == '__main__':
    unittest.main()
