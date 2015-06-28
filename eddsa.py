# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import hashlib
import random

from field import Field
from curve import TwistedEdwardsCurve, EdwardsCurve


def le2int(buf):
    """little endian buffer to integer."""
    integer = 0
    shift = 0
    for byte in buf:
        integer |= ord(byte) << shift
        shift += 8
    return integer

def int2le(integer, pad):
    """integer to little endian buffer."""
    buf = []
    while integer:
        buf.append(chr(integer & 0xff))
        integer >>= 8
        pad -= 1
    while pad > 0:
        buf.append('\x00')
        pad -= 1
    if not buf:
        return '\x00'
    return ''.join(buf)

class Ed25519(object):

    L = 2**252 + 27742317777372353535851937790883648493
    b = 256

    def __init__(self):
        field = Field(2**255 - 19)
        ed25519 = TwistedEdwardsCurve(-1, field.div(-121665, 121666), field)

        base_point = (15112221349535400772501151409588531511454012693041857206046113283949847762202L,
                      46316835694926478169428394003475163141307993866256225615783033603165251855960L)

        self.curve = ed25519
        self.bp = base_point

    def encodeint(self, y):
        return int2le(y, self.b/8)

    def encodepoint(self, P):
        x, y = P

        print 'encodepoint', P

        new = self.encodeint(((x & 1) << (self.b - 1)) + y)

        #return self.encodeint(y + (x & 1))

        bits = [(y >> i) & 1 for i in range(self.b - 1)] + [x & 1]
        ref = ''.join([chr(sum([bits[i * 8 + j] << j for j in range(8)])) for i in range(self.b/8)])

        assert new == ref
        return new

    def bit(self, h, i):
        return (ord(h[i/8]) >> (i%8)) & 1

    def H(self, m):
        return hashlib.sha512(m).digest()

    def publickey(self, sk):
        h = hashlib.sha512(sk).digest()
        a = 2**(self.b-2) + sum(2**i * self.bit(h,i) for i in range(3,self.b-2))

        #a_new = 2**(self.b-2) + self.Hint(sk) & (2**(self.b-2) - 1)
        #a_new -= (a_new & 0b111)

        a_new = h[:32]
        a_new = map(ord, a_new)
        a_new[0] &= 248
        a_new[31] &= 127
        a_new[31] |= 64
        a_new = le2int(''.join(map(chr,a_new)))

        assert a == a_new

        a = a_new

        A = montgomery_ladder(a, self.bp, self.curve)
        return self.encodepoint(A)

    def generate_key_pair_from_seed(self, sk):
        h = hashlib.sha512(sk).digest()
        priv = h[0:32]
        priv = map(ord, priv)
        priv[0] &= 248
        priv[31] &= 127
        priv[31] |= 64
        priv = le2int(''.join(map(chr,priv)))

        pub = montgomery_ladder(priv, self.bp, self.curve)
        return (pub, priv)

    def generate_random_k_from_seed(self, sk):
        return hashlib.sha512(sk).digest()[32:]

    def Hint(self,m):
        return le2int(self.H(m))
        #h = self.H(m)
        #return sum(2**i * self.bit(h,i) for i in range(2*self.b))

    def signature(self,m,sk,pk):
        # a = private key
        h = self.H(sk)
        a = 2**(self.b-2) + sum(2**i * self.bit(h,i) for i in range(3,self.b-2))

        # r = "k" || m
        r = self.Hint(''.join([h[i] for i in range(self.b/8,self.b/4)]) + m)
        #R = scalarmult(B,r)
        R = montgomery_ladder(r, self.bp, self.curve)
        S = (r + self.Hint(self.encodepoint(R) + pk + m) * a) % self.L
        return self.encodepoint(R) + self.encodeint(S)

    def sign(self, M, k, A, a):
        """above:

        r = HASH(k || M)
        R = rG
        S = (r + HASH(R || A || M) * a)
        sig = R || S
        """

        print ['sign', M, k, A, a]

        r = self.Hint(k + M)
        R = montgomery_ladder(r, self.bp, self.curve)
        S = (r + self.Hint(self.encodepoint(R) + self.encodepoint(A) + M) * a) % self.L

        return self.encodepoint(R) + self.encodeint(S)

    def decodeint(self,s):
        return le2int(s)

    def decodepoint(self,s):
        y = sum(2**i * self.bit(s,i) for i in range(0,self.b-1))
        #x = xrecover(y)
        #if x & 1 != bit(s,b-1): x = q-x
        #P = [x,y]

        #print '!!! y', [y]

        xs = self.curve.get_x(y) #[0][0]

        #print 'xs', xs
        
        x = xs[0][0]
        if x & 1 != self.bit(s,self.b-1):
            x = self.curve.gf.p - x
        P = (x,y)

        if not self.curve.point_on_curve(P): raise Exception("decoding point that is not on curve")
        return P

    def checkvalid(self,s,m,pk):
        print 'checkvalid',[s,m,pk]
        print 'length s', len(s), 'pk', len(pk)
        if len(s) != self.b/4: raise Exception("signature length is wrong")
        if len(pk) != self.b/8: raise Exception("public-key length is wrong")
        R = self.decodepoint(s[0:self.b/8])
        A = self.decodepoint(pk)
        S = self.decodeint(s[self.b/8:self.b/4])
        h = self.Hint(self.encodepoint(R) + pk + m)
        #if scalarmult(B,S) != edwards(R,scalarmult(A,h)):
        if montgomery_ladder(S, self.bp, self.curve) != self.curve.add_points(R, montgomery_ladder(h, A, self.curve)):
            raise Exception("signature does not pass verification")

class Ed41417(Ed25519):

    L = 2**411 - 33364140863755142520810177694098385178984727200411208589594759
    b = 416

    def __init__(self):
        field = Field(2**414 - 17)
        ed41417 = EdwardsCurve(1, 3617, field)

        self.curve = ed41417
        self.bp = (17319886477121189177719202498822615443556957307604340815256226171904769976866975908866528699294134494857887698432266169206165, 34)

    def generate_key_pair_from_seed(self, sk):
        h = hashlib.sha512(sk).digest()
        priv = h[0:52]
        priv = map(ord, priv)
        priv[0] &= 248
        priv[51] &= 127
        priv[51] |= 64
        priv = le2int(''.join(map(chr,priv)))

        pub = montgomery_ladder(priv, self.bp, self.curve)
        return (pub, priv)

    def generate_random_k_from_seed(self, sk):
        return hashlib.sha512('seed' + sk).digest()[:52]
