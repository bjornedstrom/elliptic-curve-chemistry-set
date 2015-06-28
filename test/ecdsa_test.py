# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import unittest
import hashlib

import asymmetric
import ecdsa
import util


def hex2int(h):
    return (h.replace(' ', '').replace('\n', '')).decode('hex')


class ECDSATest(unittest.TestCase):
    # http://www.ietf.org/rfc/rfc4754.txt
    TEST_VECTORS = {
        'key1w': {
            'public': (
                hex2int("2442A5CC 0ECD015F A3CA31DC 8E2BBC70 BF42D60C BCA20085 E0822CB0 4235E970"),
                hex2int("6FC98BD7 E50211A4 A27102FA 3549DF79 EBCB4BF2 46B80945 CDDFE7D5 09BBFD7D")),
            'private': hex2int("""DC51D386 6A15BACD E33D96F9 92FCA99D A7E6EF09 34E70975 59C27F16 14C88A7F"""),
            },
        'msg1': {
            'msg': hex2int("""BA7816BF 8F01CFEA 414140DE 5DAE2223 B00361A3 96177A9C B410FF61 F20015AD"""),
            'sig': (hex2int("""CB28E099 9B9C7715 FD0A80D8 E47A7707 9716CBBF 917DD72E 97566EA1 C066957C"""),
                    hex2int("""86FA3BB4 E26CAD5B F90B7F81 899256CE 7594BB1E A0C89212 748BFF3B 3D5B0315""")),
            'k': hex2int("""9E56F509 196784D9 63D1C0A4 01510EE7 ADA3DCC5 DEE04B15 4BF61AF1 D5A6DECE"""),
            }
    }

    def test_1(self):
        self.curve = asymmetric.ECC_NISTP256()

        priv = util.be2int(self.TEST_VECTORS['key1w']['private'])
        #print [priv]
        #print [self.curve.derive_public_key(priv)]

        pub = tuple(map(util.be2int, self.TEST_VECTORS['key1w']['public']))
        #print [pub]

        self.assertEquals(pub, self.curve.derive_public_key(priv))

        sig = ecdsa.ecdsa_sign(self.curve,
                               lambda m: util.be2int(hashlib.sha256(m).digest()),
                               256,
                               priv,
                               'abc',
                               util.be2int(self.TEST_VECTORS['msg1']['k']))

        #print [sig]
        reference_sig = tuple(map(util.be2int, self.TEST_VECTORS['msg1']['sig']))

        self.assertEquals(reference_sig, sig)

        # verify
        self.assertTrue(
            ecdsa.ecdsa_verify(self.curve,
                               lambda m: util.be2int(hashlib.sha256(m).digest()),
                               256,
                               pub,
                               'abc',
                               sig))

        self.assertTrue(not
            ecdsa.ecdsa_verify(self.curve,
                               lambda m: util.be2int(hashlib.sha256(m).digest()),
                               256,
                               pub,
                               'abcdef',
                               sig))


if __name__ == '__main__':
    unittest.main()
