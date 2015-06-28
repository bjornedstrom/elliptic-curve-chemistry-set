# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>


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
