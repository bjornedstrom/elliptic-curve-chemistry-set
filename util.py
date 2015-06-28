# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

import random


def le2int(buf):
    """little endian buffer to integer."""
    integer = 0
    shift = 0
    for byte in buf:
        integer |= ord(byte) << shift
        shift += 8
    return integer


def be2int(buf):
    """big endian buffer to integer."""
    integer = 0
    for byte in buf:
        integer <<= 8
        integer |= ord(byte)
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


def int2be(integer, pad):
    """integer to big endian buffer."""
    buf = []
    while integer:
        buf.insert(0, chr(integer & 0xff))
        integer >>= 8
        pad -= 1
    while pad > 0:
        buf.insert(0, '\x00')
        pad -= 1
    if not buf:
        return '\x00' # XXX
    return ''.join(buf)


def randint(a, b):
    # XXX: This is not cryptographically secure.
    return random.randint(a, b)


def count_bits(n):
    cnt = 0
    while n:
        n >>= 1
        cnt += 1
    return cnt
