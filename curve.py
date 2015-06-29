# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

from field import Field
from numbertheory import sqrt_modp


class Curve(object):
    pass


class ShortWeierstrass(Curve):
    """The short Weierstrass equation y^2 = x^3 + ax + b, where 4a^3+27b^2 is nonzero in F_p, is an elliptic curve over F_p. Every elliptic curve over F_p can be converted to a short Weierstrass equation if p is larger than 3.
    """
    def __init__(self, a, b, field):
        self.a = a
        self.b = b
        self.gf = field

        if self.gf.add(4*a**3, 27*b**2) == 0:
            raise ValueError('singular')

    def neutral_point(self):
        return None

    def point_on_curve(self, P):
        if P is None: # infinity
            return True

        x, y = P
        return self.gf.normalize(y**2 - (x**3 + self.a*x + self.b)) == 0

    def neutral_point_projective(self):
        return (0, 1, 0)

    def affine_to_projective(self, P1):
        if P1 is None:
            return self.neutral_point_projective()
        x, y = P1
        return (x, y, 1)

    def projective_to_affine(self, P1):
        X, Y, Z = P1

        if P1 == self.neutral_point_projective():
            return None

        x = self.gf.div(X, Z)
        y = self.gf.div(Y, Z)

        return (x, y)

    def add_points_projective(self, P1, P2):
        X1, Y1, Z1 = P1
        X2, Y2, Z2 = P2

        if P1 == self.neutral_point_projective() and P2 == self.neutral_point_projective():
            return self.neutral_point_projective()

        elif P1 == self.neutral_point_projective():
            return P2

        elif P2 == self.neutral_point_projective():
            return P1

        # add-1998-cmo-2
        """
        Y1Z2 = Y1*Z2
        X1Z2 = X1*Z2
        Z1Z2 = Z1*Z2
        u = Y2*Z1-Y1Z2
        uu = u**2
        v = X2*Z1-X1Z2
        vv = v**2
        vvv = v*vv
        R = vv*X1Z2
        A = uu*Z1Z2-vvv-2*R
        X3 = v*A
        Y3 = u*(R-A)-vvv*Y1Z2
        Z3 = vvv*Z1Z2
        """

        # add-2007-bl
        U1 = X1*Z2
        U2 = X2*Z1
        S1 = Y1*Z2
        S2 = Y2*Z1
        ZZ = Z1*Z2
        T = U1+U2
        TT = T**2
        M = S1+S2
        R = TT-U1*U2+self.a*ZZ**2
        F = ZZ*M
        L = M*F
        LL = L**2
        G = (T+L)**2-TT-LL
        W = 2*R**2-G
        X3 = 2*F*W
        Y3 = R*(G-2*W)-2*LL
        Z3 = 4*F*F**2

        return (X3 % self.gf.p, Y3 % self.gf.p, Z3 % self.gf.p)

    def double_point_projective(self, P1):
        X1, Y1, Z1 = P1

        if P1 == self.neutral_point_projective():
            return self.neutral_point_projective()

        # dbl-2007-bl
        XX = X1**2
        ZZ = Z1**2
        w = self.a*ZZ+3*XX
        s = 2*Y1*Z1
        ss = s**2
        sss = s*ss
        R = Y1*s
        RR = R**2
        B = (X1+R)**2-XX-RR
        h = w**2-2*B
        X3 = h*s
        Y3 = w*(B-h)-2*RR
        Z3 = sss

        return (X3 % self.gf.p, Y3 % self.gf.p, Z3 % self.gf.p)

    def get_y(self, x):
        """Returns a list of the y-coordinates on the curve at given x."""

        yy = self.gf.normalize(x**3 + self.a*x + self.b)

        sqrs = sqrt_modp(yy, self.gf.p)

        result = []
        for y in sqrs:
            # TODO: check inverted point?
            if self.point_on_curve((x, y)):
                result.append((x, y))
        return result

    def add_points(self, P1, P2):
        if P1 is None and P2 is None:
            return None
        if P1 is None:
            return P2
        if P2 is None:
            return P1
        if P1 == self.invert_point(P2):
            return None

        x1, y1 = P1
        x2, y2 = P2

        x3 = self.gf.div((y2-y1)**2,(x2-x1)**2) - x1 - x2
        y3 = self.gf.div((2*x1+x2)*(y2-y1), x2-x1) - self.gf.div((y2-y1)**3, (x2-x1)**3)-y1

        return (self.gf.normalize(x3), self.gf.normalize(y3))

    def double_point(self, P):
        if P is None:
            return None

        x1, y1 = P

        x3 = self.gf.div((3*x1**2+self.a)**2,(2*y1)**2)-x1-x1
        y3 = self.gf.div((2*x1+x1)*(3*x1**2+self.a),(2*y1)) -\
             self.gf.div((3*x1**2+self.a)**3, (2*y1)**3)-y1

        return (self.gf.normalize(x3), self.gf.normalize(y3))

    def invert_point(self, P):
        x, y = P
        return (x, -y % self.gf.p)

    def __str__(self):
        return 'Weierstrass Curve y^2 = x^3 + %sx + %s over GF(%s)' % (
            self.a, self.b, self.gf.p)


class MontgomeryCurve(Curve):
    """
    By^2 = x^3 + Ax^2 + x
    """

    def __init__(self, a, b, field):
        self.a = a
        self.b = b
        self.gf = field

        if self.gf.mul(b, a**2 - 4) == 0:
            raise ValueError('invalid params')

    def neutral_point(self):
        return None

    def point_on_curve(self, P):
        """Returns True if the point P=(x,y) is on the curve."""

        if P is None:
            return True

        x, y = P

        return self.gf.normalize(self.b * y**2 - (
            x**3 + self.a*x**2 + x)) == 0

    def get_y(self, x):
        """Returns a list of the y-coordinates on the curve at given x."""

        Byy = self.gf.normalize(x**3 + self.a*x**2 + x)
        yy = self.gf.div(Byy, self.b)

        sqrs = sqrt_modp(yy, self.gf.p)

        result = []
        for y in sqrs:
            # TODO: check inverted point?
            if self.point_on_curve((x, y)):
                result.append((x, y))
        return result

    def get_x(self, y):
        # Hmm
        raise NotImplementedError('get_x')

    def affine_to_xy(self, P1):
        x, y = P1
        return (x, 1)

    def xy_to_affine(self, P1):
        X, Z = P1
        if Z == 0:
            return None

        x = self.gf.div(X, Z)
        y = max(self.get_y(x)) # XXX: which one to return?

        return (x, y)

    def double_point_xy(self, P1):
        X1, Z1 = P1

        X3 = (X1**2-Z1**2)**2
        Z3 = 4*X1*Z1*(X1**2+self.a*X1*Z1+Z1**2)

        return (X3 % self.gf.p, Z3 % self.gf.p)

    # XXX
    def diffadd_points_xy(self, P1, P2):
        X1, Z1 = P1
        X2, Z2 = P2
        X3, Z3 = P3

        # dadd-1987-m-3
        A = X2+Z2
        B = X2-Z2
        C = X3+Z3
        D = X3-Z3
        DA = D*A
        CB = C*B
        X5 = Z1*(DA+CB)**2
        Z5 = X1*(DA-CB)**2

        return (X5 % self.gf.p, Z5 % self.gf.p)

    def add_points(self, P1, P2):

        if P1 is None and P2 is None:
            return None
        if P1 is None:
            return P2
        if P2 is None:
            return P1
        if P1 == self.invert_point(P2):
            return None

        x1, y1 = P1
        x2, y2 = P2

        x3 = self.gf.div(self.b*(y2-y1)**2, (x2-x1)**2) - self.a - x1 - x2
        y3 = self.gf.div(
            (2*x1 + x2 + self.a)*(y2-y1), x2-x1) - self.gf.div(
                self.b*(y2-y1)**3, (x2-x1)**3) - y1

        res = (self.gf.normalize(x3), self.gf.normalize(y3))
        return res

    def double_point(self, P):
        if P is None:
            return None

        x1, y1 = P

        # ffs...
        x3 = self.gf.div(self.b*(3*x1**2+2*self.a*x1+1)**2, (2*self.b*y1)**2) - self.a - x1 - x1
        y3 = self.gf.div((2*x1+x1+self.a)*(3*x1**2+2*self.a*x1+1), (2*self.b*y1)) - self.gf.div(self.b*(3*x1**2+2*self.a*x1+1)**3, (2*self.b*y1)**3) - y1

        res = (self.gf.normalize(x3), self.gf.normalize(y3))
        return res

    def invert_point(self, P):
        x, y = P
        return (x, -y % self.gf.p)

    def to_short_weierstrass(self):
        """The Montgomery equation By^2 = x^3 + Ax^2 + x, where B(A^2-4) is nonzero in F_p, is an elliptic curve over F_p. Substituting x = Bu-A/3 and y = Bv produces the short Weierstrass equation v^2 = u^3 + au + b where a = (3-A^2)/(3B^2) and b = (2A^3-9A)/(27B^3). Montgomery curves were introduced by 1987 Montgomery. """

        a = self.gf.div(3 - self.a**2, 3*self.b**2)
        b = self.gf.div(2*self.a**3 - 9*self.a, 27*self.b**3)

        def montgomery_point_to_weierstrass_point(P):
            x, y = P

            a3 = self.gf.div(self.a, 3)
            x_ = self.gf.div(x + a3, self.b)
            y_ = self.gf.div(y, self.b)

            return (x_, y_)

        def weierstrass_point_to_montgomery_point(P):
            x_, y_ = P

            # TODO: any exception cases? I don't think so (no division by 0 at least)
            a3 = self.gf.div(self.a, 3)
            x_plus_a3 = self.gf.mul(x_, self.b)
            x = self.gf.sub(x_plus_a3, a3)
            y = self.gf.mul(y_, self.b)

            return (x, y)

        return ShortWeierstrass(a, b, self.gf), montgomery_point_to_weierstrass_point, weierstrass_point_to_montgomery_point

    def __str__(self):
        return 'Montgomery Curve %sy^2 = x^3 + %sx^2 + x over GF(%s)' % (
            self.b, self.a, self.gf.p)


# Sage Form: y^2 + a1*x*y + a3*y = x^3 + a2*x^2 + a4*x + a6
class EdwardsCurve(Curve):
    """The Edwards equation x^2 + y^2 = 1 + dx^2y^2, where d(1-d) is nonzero in F_p, is an elliptic curve over F_p. Substituting x = u/v and y = (u-1)/(u+1) produces the Montgomery equation Bv^2 = u^3 + Au^2 + u where A = 2(1+d)/(1-d) and B = 4/(1-d). Edwards curves were introduced by 2007 Edwards in the case that d is a 4th power. SafeCurves requires Edwards curves to be complete, i.e., for d to not be a square; complete Edwards curves were introduced by 2007 Bernstein–Lange.
    """

    def __init__(self, c, d, field):
        assert c == 1
        self.c = c
        self.d = d
        self.gf = field

        if self.gf.mul(d, 1-d) == 0:
            raise ValueError('invalid params')

        if sqrt_modp(d, self.gf.p):
            print 'WARNING: Edwards curve not complete'

    def neutral_point(self):
        return (0, self.c)

    def neutral_point_projective(self):
        return (0, self.c, 1)

    # XXX: This is a bit flaky...
    def get_x(self, y):
        result = []

        # HACK: Instead of brute forcing the square roots pick the right one directly.
        top = sqrt_modp((y**2 - self.c**2) % self.gf.p, self.gf.p) + sqrt_modp(-(y**2 - self.c**2) % self.gf.p, self.gf.p)
        bottom = sqrt_modp((self.c**2 * self.d * y**2 - 1) % self.gf.p, self.gf.p) + sqrt_modp(-(self.c**2 * self.d * y**2 - 1) % self.gf.p, self.gf.p)

        for t in top:
            for b in bottom:
                x = self.gf.div(t, b)

                if self.point_on_curve((x, y)):
                    result.append((x, y))
                if self.point_on_curve((-x % self.gf.p, y)):
                    result.append((-x % self.gf.p, y))

        return list(set(result))

    def point_on_curve(self, P):
        x, y = P

        return self.gf.normalize((x**2 + y**2) - self.c**2*(
            1 + self.d * x**2 * y**2)) == 0

    def affine_to_projective(self, P1):
        x, y = P1
        return (x, y, 1)

    def projective_to_affine(self, P1):
        X, Y, Z = P1

        x = self.gf.div(X, Z)
        y = self.gf.div(Y, Z)

        return (x, y)

    def double_point_projective(self, P1):
        # dbl-2007-bl-2

        X1, Y1, Z1 = P1

        R1 = X1
        R2 = Y1
        R3 = Z1
        R4 = R1+R2
        R3 = self.c*R3
        R1 = R1**2
        R2 = R2**2
        R3 = R3**2
        R4 = R4**2
        R3 = 2*R3
        R5 = R1+R2
        R2 = R1-R2
        R4 = R4-R5
        R3 = R5-R3
        R1 = R3*R4
        R3 = R3*R5
        R2 = R2*R5
        R1 = self.c*R1
        R2 = self.c*R2
        X3 = R1
        Y3 = R2
        Z3 = R3

        return (X3 % self.gf.p, Y3 % self.gf.p, Z3 % self.gf.p)

    def add_points_projective(self, P1, P2):
        # add-2007-bl-2

        X1, Y1, Z1 = P1
        X2, Y2, Z2 = P2

        R1 = X1
        R2 = Y1
        R3 = Z1
        R4 = X2
        R5 = Y2
        R6 = Z2
        R3 = R3*R6
        R7 = R1+R2
        R8 = R4+R5
        R1 = R1*R4
        R2 = R2*R5
        R7 = R7*R8
        R7 = R7-R1
        R7 = R7-R2
        R7 = R7*R3
        R8 = R1*R2
        R8 = self.d*R8
        R2 = R2-R1
        R2 = R2*R3
        R3 = R3**2
        R1 = R3-R8
        R3 = R3+R8
        R2 = R2*R3
        R3 = R3*R1
        R1 = R1*R7
        R3 = self.c*R3
        X3 = R1
        Y3 = R2
        Z3 = R3

        return (X3 % self.gf.p, Y3 % self.gf.p, Z3 % self.gf.p)

    def add_points(self, P1, P2):
        x1, y1 = P1
        x2, y2 = P2

        x3 = self.gf.div(x1*y2 + y1*x2,
                         self.c*(1 + self.d*x1*x2*y1*y2))

        y3 = self.gf.div(y1*y2 - x1*x2,
                         self.c*(1 - self.d*x1*x2*y1*y2))
        return (x3, y3)

    # XXX
    def double_point(self, P):
        return self.add_points(P, P)

    def invert_point(self, P):
        x, y = P
        return (-x % self.gf.p, y)

    # XXX
    def to_montgomery(self):
        a = self.gf.div(2*(1+self.d), 1-self.d)
        b = self.gf.div(4, 1-self.d)

        def edwards_point_to_montgomery_point(P):
            x, y = P

            x_ = self.gf.div(1 + y, 1 - y)
            y_ = self.gf.div(x_, x)

            return (x_, y_)

        def montgomery_point_to_edwards_point(P):
            x_, y_ = P

            if y_ == 0 or self.gf.add(x_, 1) == 0:
                raise ZeroDivisionError('invalid conversion')

            x = self.gf.div(x_, y_)
            y = self.gf.div(x_ - 1, x_ + 1)

            return (x, y)

        return MontgomeryCurve(a, b, self.gf), edwards_point_to_montgomery_point, montgomery_point_to_edwards_point

    def __str__(self):
        return 'Edwards Curve x^2 + y^2 = 1 + %sx^2y^2 over GF(%s)' % (
        self.d, self.gf.p)


class TwistedEdwardsCurve(Curve):
    """
    ax^2 + y^2 = 1 + dx^2y^2
    """
    def __init__(self, a, d, field):
        self.a = a
        self.d = d
        self.gf = field

    def neutral_point(self):
        # http://iacr.org/archive/asiacrypt2008/53500329/53500329.pdf
        return (0, 1)

    def neutral_point_projective(self):
        return (0, 1, 1)

    # XXX: This is a bit flaky...
    def get_x(self, y):
        # ax^2 + y^2 = 1 + dx^2y^2
        # x^2 (a - 2*y^2) = 1 - y^2

        result = []

        top = sqrt_modp(1 - y**2, self.gf.p)
        bottom = sqrt_modp(self.a - self.d * y**2, self.gf.p)
        for t in top:
            for b in bottom:
                x = self.gf.div(t, b)

                if self.point_on_curve((x, y)):
                    result.append((x, y))
                if self.point_on_curve((-x % self.gf.p, y)):
                    result.append((-x % self.gf.p, y))

        return list(set(result))

    def point_on_curve(self, P):
        x, y = P

        return self.gf.normalize((self.a * x**2 + y**2) - (
            1 + self.d * x**2 * y**2)) == 0

    def add_points_projective(self, P1, P2):
        X1, Y1, Z1 = P1
        X2, Y2, Z2 = P2

        """
        assert Z1 == Z2 == 1

        C = X1*X2
        D = Y1*Y2
        E = self.d*C*D
        X3 = (1-E)*((X1+Y1)*(X2+Y2)-C-D)
        Y3 = (1+E)*(D-self.a*C)
        Z3 = 1-E**2
        """

        # add-2008-bbjlp
        A = Z1*Z2
        B = A**2
        C = X1*X2
        D = Y1*Y2
        E = self.d*C*D
        F = B-E
        G = B+E
        X3 = A*F*((X1+Y1)*(X2+Y2)-C-D)
        Y3 = A*G*(D-self.a*C)
        Z3 = F*G

        return (X3 % self.gf.p, Y3 % self.gf.p, Z3 % self.gf.p)

    def double_point_projective(self, P1):
        X1, Y1, Z1 = P1

        """
        assert Z1 == 1

        B = (X1+Y1)**2
        C = X1**2
        D = Y1**2
        E = self.a*C
        F = E+D
        X3 = (B-C-D)*(F-2)
        Y3 = F*(E-D)
        Z3 = F**2-2*F
        """

        # dbl-2008-bbjlp

        B = (X1+Y1)**2
        C = X1**2
        D = Y1**2
        E = self.a*C
        F = E+D
        H = Z1**2
        J = F-2*H
        X3 = (B-C-D)*J
        Y3 = F*(E-D)
        Z3 = F*J

        return (X3 % self.gf.p, Y3 % self.gf.p, Z3 % self.gf.p)

    def affine_to_projective(self, P1):
        x, y = P1
        return (x, y, 1)

    def projective_to_affine(self, P1):
        X1, Y1, Z1 = P1

        x = self.gf.div(X1, Z1)
        y = self.gf.div(Y1, Z1)

        return (x, y)

    # Note similarity with Edwards curve
    def add_points(self, P1, P2):
        x1, y1 = P1
        x2, y2 = P2

        x3 = self.gf.div(x1*y2 + y1*x2,
                         1 + self.d*x1*x2*y1*y2)

        y3 = self.gf.div(y1*y2 - self.a*x1*x2,
                         1 - self.d*x1*x2*y1*y2)
        return (x3, y3)

    # XXX
    def double_point(self, P):
        return self.add_points(P, P)

    def invert_point(self, P):
        x, y = P
        return (-x % self.gf.p, y)

    def to_montgomery(self):
        A = self.gf.div(2*(self.a + self.d), self.a - self.d)
        B = self.gf.div(4, self.a - self.d)

        def map_affine_to(P):
            x, y = P
            if 1 - y == 0 or (1 - y)*x == 0:
                # XXX: is this correct?
                return None
            return (
                self.gf.div(1 + y, 1 - y),
                self.gf.div(1 + y, (1 - y)*x))

        def map_affine_from(P):
            if P is None:
                return None
            u, v = P
            # XXX: Handle exceptional cases
            if v == 0 or (u + 1) == 0:
                raise ZeroDivisionError('TODO')
            return (
                self.gf.div(u, v),
                self.gf.div(u - 1, u + 1))

        return MontgomeryCurve(A, B, self.gf), map_affine_to, map_affine_from


def montgomery_ladder(n, P, curve):
    R0 = curve.neutral_point()
    R1 = P

    # XXX
    bits = []
    while n:
        bits.insert(0, n & 1)
        n >>= 1

    for b in bits:
        if b & 1:
            R0 = curve.add_points(R0, R1)
            R1 = curve.double_point(R1)
        else:
            R1 = curve.add_points(R0, R1)
            R0 = curve.double_point(R0)

    return R0


def montgomery_ladder_projective(n, P, curve):
    R0 = curve.neutral_point_projective()
    R1 = P

    # XXX
    bits = []
    while n:
        bits.insert(0, n & 1)
        n >>= 1

    for b in bits:
        if b & 1:
            R0 = curve.add_points_projective(R0, R1)
            R1 = curve.double_point_projective(R1)
        else:
            R1 = curve.add_points_projective(R0, R1)
            R0 = curve.double_point_projective(R0)

    return R0
