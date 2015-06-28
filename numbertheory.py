# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>


def legendre_symbol(n, p):
    ls = pow(n, (p - 1) / 2, p)
    if ls == p - 1:
        return -1
    return ls


def tonelli_shanks(n, p):
    # https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm#The_algorithm

    # Step 1
    q, s = p - 1, 0
    while q % 2 == 0:
        s += 1
        q //= 2

    # Step 2
    z = 1
    while legendre_symbol(z, p) != -1:
        z += 1
    c = pow(z, q, p)

    # Step 3
    x = pow(n, (q + 1)/2, p)
    t = pow(n, q, p)
    m = s
    while t != 1:
        # Find the lowest i such that t^(2^i) = 1
        i, e = 0, 2
        for i in xrange(1, m):
            if pow(t, e, p) == 1:
                break
            e *= 2

        # Update next value to iterate
        b = pow(c, 2**(m - i - 1), p)
        x = (x * b) % p
        t = (t * b * b) % p
        c = (b * b) % p
        m = i

    return [x, p-x]


def sqrt_modp(n, p):
    """Calculate the square root x**2 = n (mod p).
    """

    n %= p

    if n == 0:
        return [0]

    if p == 2:
        return [n]

    if legendre_symbol(n, p) != 1:
        return []

    # Common case #1
    if p % 4 == 3:
        x = pow(n, (p + 1)/4, p)
        return [x, p-x]

    # Common case #2
    if p % 8 == 5:
        if n == pow(n, (p + 3)/4, p):
            x = pow(n, (p + 3)/8, p)
            return [x, p-x]

        s = pow(n, (p + 3)/8, p)
        x = (tonelli_shanks(p - 1, p)[0] * s) % p
        return [x, p-x]

    # Shouldn't end up here very often.
    return tonelli_shanks(n, p)


def extended_euclid(a, b):
    s_, s = 0, 1
    t_, t = 1, 0
    r_, r = b, a

    while r_ != 0:
        q = r // r_
        r, r_ = r_, r - q * r_
        s, s_ = s_, s - q * s_
        t, t_ = t_, s - q * t_

    return r, s, t


def inverse_of(n, p):
    """m such that (n * m) % p == 1."""

    gcd, x, y = extended_euclid(n, p)
    assert (n * x + p * y) % p == gcd

    if gcd != 1:
        raise ValueError('no inverse')
    else:
        return x % p
