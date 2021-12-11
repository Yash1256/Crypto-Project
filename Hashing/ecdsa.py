from Hashing.curve import *
from Hashing.numberTheory import *
from hashlib import sha256

'''
Use sha256 to hash a message, and return the hash value as an integer.
'''
def hash(message):
    return int(sha256(message.encode('utf-8')).hexdigest(), 16)

'''
Hash the message and return integer whose binary representation is the the L leftmost bits
of the hash value, where L is the bit length of n.
'''
def hash_and_truncate(message, n):
    h = hash(message)
    b = bin(h)[2:len(bin(n))]
    return int(b, 2)

'''
Generate a keypair using the point P of order n on the given curve. The private key is a
positive integer d smaller than n, and the public key is Q = dP.
'''
def generate_keypair(curve, P, n):
    sysrand = SystemRandom()
    d = sysrand.randrange(1, n)
    Q = curve.mult(P, d)
    print("Private key : d = " + str(d))
    print("Public key  : Q = " + str(Q))
    return (d, Q)

'''
Create a digital signature for the string message using a given curve with a distinguished
point P which generates a prime order subgroup of size n.
'''
def sign(message, curve, P, n, keypair):
    #Extract the private and public keys, and compute z by hashing the message.
    d, Q = keypair
    z = hash_and_truncate(message, n)
    #Choose a randomly selected secret point kP then compute r and s.
    r, s = 0, 0
    while r == 0 or s == 0:
        sysrand = SystemRandom()
        k = sysrand.randrange(1, n)
        R = curve.mult(P, k)
        r = R.x % n
        s = (mult_inv(k, n) * (z + r*d)) % n
    print('ECDSA sig: (Q, r, s) = (' + str(Q) + ', ' + str(r) + ', ' + str(s) + ')')
    return (Q, r, s)

'''
Verify the string message is authentic, given an ECDSA signature generated using a curve with
a distinguished point P that generates a prime order subgroup of size n.
'''
def verify(message, curve, P, n, sig):
    Q, r, s = sig
    #Confirm that Q is on the curve.
    if Q.is_infinite() or not curve.contains(Q):
        return False
    #Confirm that Q has order that divides n.
    if not curve.mult(Q,n).is_infinite():
        return False
    #Confirm that r and s are at least in the acceptable range.
    if r > n or s > n:
        return False
    #Compute z in the same manner used in the signing procedure,
    #and verify the message is authentic.
    z = hash_and_truncate(message, n)
    w = mult_inv(s, n) % n
    u_1, u_2 = z * w % n, r * w % n
    C_1, C_2 = curve.mult(P, u_1), curve.mult(Q, u_2)
    C = curve.add(C_1, C_2)
    return r % n == C.x % n