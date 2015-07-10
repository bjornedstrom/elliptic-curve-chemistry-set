# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import curve


def ecdh(curve_obj, my_private, other_public):
    """Derive the shared secret in ECDH."""

    # here curve_obj is from asymmetric.ECCBase
    return curve.mul(my_private, other_public, curve_obj.curve)
