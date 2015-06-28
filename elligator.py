# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import curve
import numbertheory


class Elligator2(object):
    """
    "Elligator 2" works for any odd prime and any curve of the form
    y^2=x^3+Ax^2+Bx with nonzero AB(A^2-4B). This includes all
    Montgomery curves y^2=x^3+Ax^2+x except for one curve
    y^2=x^3+x. It also includes, after conversion, all Edwards curves
    x^2+y^2=1+dx^2y^2 except for one curve x^2+y^2=1-x^2y^2. More
    generally, it includes all curves with points of order 2, except
    for j-invariant 1728.
    """

    def __init__(self, curve_obj):
        self.curve = curve_obj

        # A defined non-square
        if self.curve.gf.p % 4 == 3:
            self.u = -1
        elif self.curve.gf.p % 8 == 5:
            self.u = 2
        else:
            raise NotImplementedError('uh oh, I dont know what to do with this field!')

        if isinstance(self.curve, curve.MontgomeryCurve):
            if self.curve.b != 1:
                raise NotImplementedError('for now only montgomery curves with B==1 are supported')
        else:
            raise NotImplementedError('for now Elligator2 is only implemented for MontgomeryCurve')

    """
    def abs(self, a):
        if a <= (self.curve.gf.p - 1) / 2:
            return a
        return (-a) % self.curve.gf.p

    def sqrt_test(self, a):
        b = pow(a, (self.curve.gf.p + 3) / 8, self.curve.gf.p)
        if b**2 == a:
            return self.abs(b)
        return self.abs(self.curve.gf.mul(19681161376707505956807079304988542015446066515923890162744021073123829784752L, b))
    """

    def map_point_to_random(self, P):
        x, y = P

        sqrt = lambda a: numbertheory.sqrt_modp(a, self.curve.gf.p)
        div = self.curve.gf.div

        if y <= ((self.curve.gf.p - 1) / 2):
            r = sqrt(div(-x, (x + self.curve.a)*self.u))
        else:
            r = sqrt(div(-(x + self.curve.a), x*self.u))

        # XXX: First
        return r[0]

    def map_random_to_point(self, r):
        sqrt = lambda a: numbertheory.sqrt_modp(a, self.curve.gf.p)
        div = self.curve.gf.div
        sub = self.curve.gf.sub
        mul = self.curve.gf.mul

        v = div(-self.curve.a, 1 + self.u*r**2)
        epsilon = numbertheory.legendre_symbol(v**3 + self.curve.a*v**2 + self.curve.b*v, self.curve.gf.p)
        x = sub(epsilon*v, div((1 - epsilon)*self.curve.a, 2))
        y = mul(-epsilon, sqrt(x**3 + self.curve.a*x**2 + self.curve.b*x)[0]) # XXX: First

        return (x, y)
