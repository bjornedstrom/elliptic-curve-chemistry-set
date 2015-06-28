# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import numbertheory

class Field(object):
    def __init__(self, p):
        self.p = p

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def mul_inv(self, n):
        return numbertheory.inverse_of(n, self.p)

    def div(self, a, b):
        return self.mul(a, self.mul_inv(b))

    def normalize(self, n):
        return n % self.p
