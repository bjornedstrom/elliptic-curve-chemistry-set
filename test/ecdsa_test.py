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
            'msg': "abc",
            'sig': (hex2int("""CB28E099 9B9C7715 FD0A80D8 E47A7707 9716CBBF 917DD72E 97566EA1 C066957C"""),
                    hex2int("""86FA3BB4 E26CAD5B F90B7F81 899256CE 7594BB1E A0C89212 748BFF3B 3D5B0315""")),
            'k': hex2int("""9E56F509 196784D9 63D1C0A4 01510EE7 ADA3DCC5 DEE04B15 4BF61AF1 D5A6DECE"""),
            },

        # https://www.nsa.gov/ia/_files/ecdsa.pdf
        'key2w': {
            'public': (
                hex2int("8101ece4 7464a6ea d70cf69a 6e2bd3d8 8691a326 2d22cba4 f7635eaf f26680a8"),
                hex2int("d8a12ba6 1d599235 f67d9cb4 d58f1783 d3ca43e7 8f0a5aba a6240799 36c0c3a9")),
            'private': hex2int("70a12c2d b16845ed 56ff68cf c21a472b 3f04d7d6 851bf634 9f2d7d5b 3452b38a"),
            },
        'msg2': {
            'msg': "This is only a test message. It is 48 bytes long",
            'sig': (hex2int("7214bc96 47160bbd 39ff2f80 533f5dc6 ddd70ddf 86bb8156 61e805d5 d4e6f27c"),
                    hex2int("7d1ff961 980f961b daa3233b 6209f401 3317d3e3 f9e14935 92dbeaa1 af2bc367")),
            'k': hex2int("580ec00d 85643433 4cef3f71 ecaed496 5b12ae37 fa47055b 1965c7b1 34ee45d0"),
            },

        'key3w': {
            'public': (
                hex2int("1fbac8ee bd0cbf35 640b39ef e0808dd7 74debff2 0a2a329e 91713baf 7d7f3c3e 81546d88 3730bee7 e48678f8 57b02ca0"),
                hex2int("eb213103 bd68ce34 3365a8a4 c3d4555f a385f533 0203bdd7 6ffad1f3 affb9575 1c132007 e1b24035 3cb0a4cf 1693bdf9")),
            'private': hex2int("c838b852 53ef8dc7 394fa580 8a518398 1c7deef5 a69ba8f4 f2117ffe a39cfcd9 0e95f6cb c854abac ab701d50 c1f3cf24"),
            },
        'msg3': {
            'msg': "This is only a test message. It is 48 bytes long",
            'sig': (hex2int("a0c27ec8 93092dea 1e1bd2cc fed3cf94 5c8134ed 0c9f8131 1a0f4a05 942db8db ed8dd59f 267471d5 462aa14f e72de856"),
                    hex2int("20ab3f45 b74f10b6 e11f96a2 c8eb694d 206b9dda 86d3c7e3 31c26b22 c987b753 77265776 67adadf1 68ebbe80 3794a402")),
            'k': hex2int("dc6b4403 6989a196 e39d1cda c000812f 4bdd8b2d b41bb33a f5137258 5ebd1db6 3f0ce827 5aa1fd45 e2d2a735 f8749359"),
            },
    }

    def test_1(self):
        curve_obj = asymmetric.ECC_NISTP256()
        priv = util.be2int(self.TEST_VECTORS['key1w']['private'])
        pub = tuple(map(util.be2int, self.TEST_VECTORS['key1w']['public']))
        hash_func = lambda m: util.be2int(hashlib.sha256(m).digest())
        hash_bits = 256
        msg = self.TEST_VECTORS['msg1']['msg']
        k = util.be2int(self.TEST_VECTORS['msg1']['k'])
        reference_sig = tuple(map(util.be2int, self.TEST_VECTORS['msg1']['sig']))

        self._test_ecdsa(curve_obj, priv, pub, hash_func, hash_bits, msg, k, reference_sig)

    def test_2(self):
        curve_obj = asymmetric.ECC_NISTP256()
        priv = util.be2int(self.TEST_VECTORS['key2w']['private'])
        pub = tuple(map(util.be2int, self.TEST_VECTORS['key2w']['public']))
        hash_func = lambda m: util.be2int(hashlib.sha256(m).digest())
        hash_bits = 256
        msg = self.TEST_VECTORS['msg2']['msg']
        k = util.be2int(self.TEST_VECTORS['msg2']['k'])
        reference_sig = tuple(map(util.be2int, self.TEST_VECTORS['msg2']['sig']))

        self._test_ecdsa(curve_obj, priv, pub, hash_func, hash_bits, msg, k, reference_sig)

    def test_3(self):
        curve_obj = asymmetric.ECC_NISTP384()
        priv = util.be2int(self.TEST_VECTORS['key3w']['private'])
        pub = tuple(map(util.be2int, self.TEST_VECTORS['key3w']['public']))
        hash_func = lambda m: util.be2int(hashlib.sha384(m).digest())
        hash_bits = 384
        msg = self.TEST_VECTORS['msg3']['msg']
        k = util.be2int(self.TEST_VECTORS['msg3']['k'])
        reference_sig = tuple(map(util.be2int, self.TEST_VECTORS['msg3']['sig']))

        self._test_ecdsa(curve_obj, priv, pub, hash_func, hash_bits, msg, k, reference_sig)

    def _test_ecdsa(self, curve_obj, priv, pub, hash_func, hash_bits, msg, k, reference_sig):
        self.assertEquals(pub, curve_obj.derive_public_key(priv))

        sig = ecdsa.ecdsa_sign(curve_obj,
                               hash_func,
                               hash_bits,
                               priv,
                               msg,
                               k)

        self.assertEquals(reference_sig, sig)

        # verify
        self.assertTrue(
            ecdsa.ecdsa_verify(curve_obj,
                               hash_func,
                               hash_bits,
                               pub,
                               msg,
                               reference_sig))

        self.assertTrue(not
            ecdsa.ecdsa_verify(curve_obj,
                               hash_func,
                               hash_bits,
                               pub,
                               'abcdef',
                               reference_sig))


if __name__ == '__main__':
    unittest.main()
