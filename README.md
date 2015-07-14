# My Elliptic Curve Chemistry Set

My Python code for experimenting with elliptic curves over finite fields, and elliptic curve cryptography.

This code is meant for experimentation and educational purposes, it is not meant to be used in real life scenarios.

## Experiments

- Short Weierstrass, Edwards, Twisted Edwards and Montgomery shapes.
- Addition, Doubling and Multiplication.
- Some support for Projective coordinates (or XY coordinates if X:Y:Z projective are missing).
- A half-assed generalization of EdDSA ruthlessly mangled from djb:s reference implementation.
- Convenient classes for Curve25519, Ed25519 and NIST P-256, P-384.
- An experimental and half-working, not-tested-at-all (because of lack of test vectors) implementation of Curve41417.
- A barely started implementation of converting curves in one shape to a different shape.
- A slow reference implementation of Elligator2.
- Point decompressing.
- Completely trivial code for arithmetic in GF(p).
- Some code for ECDH.
- Some code for ECDSA including breaking ECDSA in case it's misused.

## License

The Elliptic Curve Chemistry Set is written by Björn Edström in 2015. See LICENSE for details.
