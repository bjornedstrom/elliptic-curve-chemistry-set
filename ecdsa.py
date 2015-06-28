# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import asymmetric
import curve
import util
import numbertheory


def ecdsa_sign(curve_obj, hash_int, hash_num_bits, private_key, message, k=None):
    if k is None:
        k = util.randint(1, curve_obj.order - 1)

    e = hash_int(message)
    L_n = util.count_bits(curve_obj.order)
    z = e >> max(hash_num_bits - L_n, 0)

    while True:
        (x1, y1) = curve.montgomery_ladder(k, curve_obj.base_point, curve_obj.curve)
        r = x1 % curve_obj.order
        if r == 0:
            continue

        # XXX?
        k_neg = numbertheory.inverse_of(k, curve_obj.order)

        #s = curve_obj.curve.gf.div(z + r*private_key, k) % curve_obj.order
        s = (k_neg * (z + r * private_key)) % curve_obj.order
        if s == 0:
            continue

        break

    return (r, s)
