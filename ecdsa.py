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


def ecdsa_verify(curve_obj, hash_int, hash_num_bits, public_key, message, signature):
    # Verify
    if public_key == curve_obj.base_point or \
            curve_obj.curve.invert_point(public_key) == curve_obj.base_point: # XXX: Check inverted too?
        return False

    if not curve_obj.curve.point_on_curve(public_key):
        return False

    if not curve.montgomery_ladder(curve_obj.order, public_key, curve_obj.curve) == curve_obj.curve.neutral_point():
        return False

    (r, s) = signature

    if not 1 <= r <= curve_obj.order - 1:
        return False

    if not 1 <= s <= curve_obj.order - 1:
        return False

    e = hash_int(message)
    L_n = util.count_bits(curve_obj.order)
    z = e >> max(hash_num_bits - L_n, 0)

    # Verify
    w = numbertheory.inverse_of(s, curve_obj.order) % curve_obj.order
    u_1 = (z * w) % curve_obj.order
    u_2 = (r * w) % curve_obj.order

    (x1, y1) = curve_obj.curve.add_points(
        curve.montgomery_ladder(u_1, curve_obj.base_point, curve_obj.curve),
        curve.montgomery_ladder(u_2, public_key, curve_obj.curve)
        )

    return (r % curve_obj.order) == x1
