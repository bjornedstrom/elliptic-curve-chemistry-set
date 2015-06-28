# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import random

import field
import curve


def randint(a, b):
    # XXX: This is not cryptographically secure.
    return random.randint(a, b)


class ECCBase(object):
    curve = None
    order = None
    base_point = None

    def generate_private_key(self, seed):
        return randint(1, self.order - 1)

    def generate_key_pair(self, seed):
        private = self.generate_private_key(seed)
        public = curve.montgomery_ladder(private, self.base_point)

        return (public, private)


class ECC_Curve25519(ECCBase):
    curve = curve.MontgomeryCurve(486662, 1, field.Field(2**255 - 19))
    order = 2**252 + 27742317777372353535851937790883648493L
    base_point = (9L, 14781619447589544791020593568409986887264606134616475288964881837755586237401L)

    def generate_private_key(self, seed):
        return 2**254 + 8 * randint(0, 2**251 - 1)


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


class ECC_Curve41417(ECCBase):
    curve = curve.EdwardsCurve(1, 3617, field.Field(2**414 - 17))
    order = 2**411 - 33364140863755142520810177694098385178984727200411208589594759
    base_point = (17319886477121189177719202498822615443556957307604340815256226171904769976866975908866528699294134494857887698432266169206165, 34)

    def generate_private_key(self, seed):
        # As Curve25519 this one has a cofactor of 8.
        return 2**413 + 8 * randint(0, 2**410 - 1)
