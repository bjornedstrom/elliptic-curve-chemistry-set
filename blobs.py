# -*- coding: utf-8 -*-
# Copyright (C) 2015 Björn Edström <be@bjrn.se>

from pyasn1.codec.der import decoder, encoder
from pyasn1.type import univ, namedtype, tag

class X963(object):

    class ASN1_X9_63_Private_Key(univ.Sequence):
        componentType = namedtype.NamedTypes(
            namedtype.NamedType('flags', univ.BitString()),
            namedtype.NamedType('size', univ.Integer()),
            namedtype.NamedType('x', univ.Integer()), # public x
            namedtype.NamedType('y', univ.Integer()),
            namedtype.NamedType('k', univ.Integer()) # private key
            )

    class ASN1_X9_63_DSA_Signature(univ.Sequence):
        componentType = namedtype.NamedTypes(
            namedtype.NamedType('r', univ.Integer()),
            namedtype.NamedType('s', univ.Integer())
            )

    def decode_der_private_key(self, buf):
        obj, rest = decoder.decode(buf, asn1Spec=self.ASN1_X9_63_Private_Key())

        pub = (int(obj.getComponentByName('x')), int(obj.getComponentByName('y')))
        priv = int(obj.getComponentByName('k'))

        return pub, priv

    def encode_der_private_key(self, pub, priv, byte_size):
        obj = self.ASN1_X9_63_Private_Key()
        obj.setComponentByName('flags', (1,)) # private key
        obj.setComponentByName('size', byte_size)
        obj.setComponentByName('x', pub[0])
        obj.setComponentByName('y', pub[1])
        obj.setComponentByName('k', priv)

        return encoder.encode(obj)

    def decode_der_dsa_sig(self, buf):
        obj, rest = decoder.decode(buf, asn1Spec=self.ASN1_X9_63_DSA_Signature())

        sig = (int(obj.getComponentByName('r')), int(obj.getComponentByName('s')))

        return sig

    def encode_der_dsa_sig(self, sig):
        obj = self.ASN1_X9_63_DSA_Signature()
        obj.setComponentByName('r', sig[0])
        obj.setComponentByName('s', sig[1])

        return encoder.encode(obj)


x963 = X963()
