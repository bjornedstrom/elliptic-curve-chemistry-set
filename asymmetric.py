# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import random

import field
import curve
import util
import ecdh
import util


class ECCBase(object):
    curve = None
    order = None
    base_point = None

    def generate_private_key(self, seed):
        return util.randint(1, self.order - 1)

    def derive_public_key(self, private):
        return curve.mul(private, self.base_point, self.curve)

    def generate_key_pair(self, seed):
        private = self.generate_private_key(seed)
        public = curve.mul(private, self.base_point, self.curve)

        return (public, private)

    def canonical_binary_form_private(self, private):
        raise NotImplementedError()

    def canonical_binary_form_public(self, public):
        raise NotImplementedError()

    def binary_to_private(self, private_bin):
        raise NotImplementedError()

    def binary_to_public(self, public_bin):
        raise NotImplementedError()


class ECC_Curve25519(ECCBase):
    curve = curve.MontgomeryCurve(486662, 1, field.Field(2**255 - 19))
    order = 2**252 + 27742317777372353535851937790883648493L
    base_point = (9L, 14781619447589544791020593568409986887264606134616475288964881837755586237401L)

    def generate_private_key(self, seed):
        return 2**254 + 8 * util.randint(0, 2**251 - 1)

    def canonical_binary_form_private(self, private):
        return util.int2le(private, 32)

    def canonical_binary_form_public(self, public):
        return util.int2le(public[0], 32)

    def binary_to_private(self, private_bin):
        return util.le2int(private_bin)

    def binary_to_public(self, public_bin):
        raise NotImplementedError('AFAIK there is no canonical way to recover y from x')

    def non_canonical_binary_to_public(self, public_bin):
        x = util.le2int(public_bin)
        P1, P2 = self.curve.get_y(x)

        """
        print
        print P1[1] <= (self.curve.gf.p - 1)/2
        print P1
        print P2
        #print (P1[0] % 2, P1[1] % 2)
        #print (P2[0] % 2, P2[1] % 2)
        print

        # XXX
        q = self.curve.gf.p
        I = pow(2, (q-1)/4, q)
        yy = x**3 + self.curve.a*x**2 + x
        y = pow(yy, (q+3)/8, q)
        if (y*y - yy) % q != 0:
            y = (y*I) % q
        if y % 2 != 0:
            y = q-y

        #print (x, y)
        #print

        return max(P1, P2)"""

        return P1 # XXX

    def ecdh(self, my_private, other_public):
        # Curve25519 only cares about the x affine coordinate.
        return ecdh.ecdh(self, my_private, other_public)[0]



class ECC_Ed25519(ECC_Curve25519):
    curve = curve.TwistedEdwardsCurve(
        -1,
         field.Field(2**255 - 19).div(-121665, 121666),
         field.Field(2**255 - 19))
    base_point = (15112221349535400772501151409588531511454012693041857206046113283949847762202L, 46316835694926478169428394003475163141307993866256225615783033603165251855960L)


class ECC_NISTP256(ECCBase):
    curve = curve.ShortWeierstrass(-3, 41058363725152142129326129780047268409114441015993725554835256314039467401291L, field.Field(2**256 - 2**224 + 2**192 + 2**96 - 1))
    base_point = (48439561293906451759052585252797914202762949526041747995844080717082404635286L, 36134250956749795798585127919587881956611106672985015071877198253568414405109L)
    order = 2**256 - 2**224 + 2**192 - 89188191075325690597107910205041859247


class ECC_NISTP384(ECCBase):
    curve = curve.ShortWeierstrass(-3, 27580193559959705877849011840389048093056905856361568521428707301988689241309860865136260764883745107765439761230575, field.Field(2**384 - 2**128 - 2**96 + 2**32 - 1))
    base_point = (26247035095799689268623156744566981891852923491109213387815615900925518854738050089022388053975719786650872476732087, 8325710961489029985546751289520108179287853048861315594709205902480503199884419224438643760392947333078086511627871)
    order = 2**384 - 1388124618062372383947042015309946732620727252194336364173


class ECC_Curve41417(ECCBase):
    curve = curve.EdwardsCurve(1, 3617, field.Field(2**414 - 17))
    order = 2**411 - 33364140863755142520810177694098385178984727200411208589594759
    base_point = (17319886477121189177719202498822615443556957307604340815256226171904769976866975908866528699294134494857887698432266169206165, 34)

    def generate_private_key(self, seed):
        # As Curve25519 this one has a cofactor of 8.
        return 2**413 + 8 * util.randint(0, 2**410 - 1)
