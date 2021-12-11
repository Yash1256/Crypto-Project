<center><h1> 5th Semester Final Term Cryptography Project </h1></center>

### Paper: https://drive.google.com/file/d/1mDYcgoQ8Esc7Ujn760j_IWJkaFnbqNtx/view

## Motivation of Paper:

As per the survey conducted by ITU in 2019, 53.6% of global populations are using the internet for their day to day work. That is why data transmission security is a major concern. There are a lot of cryptographic algorithms but encryption using ECC gives the improved security with smaller size.
This paper has presented the group security using ECC. Group security is using the m-gram selection. We want to reduce the time for the encryption and decryption using ECC taking the advantage of common grams. This paper will contrast the difference in processing time of the traditional ECC algorithm and the algorithm that is being implemented using common-gram technique. The fact that is being taken into advantage in this section is that the extended-common gram selection decreases the time for computation.

## Implementation:

In the Implementation Part of the Project we have done the complete ECC Encryption Decryption and ECCDSA Part but for the GFGS Part according to our understandace we have created the di-gram selection (Words of length 2) and shown the Encryption time difference between normal and diword hashing but the part in which GFGS Algorithm is implemeted over layers that part is not implemented.<br>
That part we will try to Implement in future.<br>
[Implementation of Our Part](https://gist.github.com/Yash1256/b7fda1082ecb6879914b79d6ba17799b)

## Contributors:

- Yash Shukla (@Yash1256)
- Himanshu Pal (@ContriverH)

For Running Purpose either use Jupyter notebook or import main.py file and use function accordingly

## Some Demo Codes are as follows

```
from main import *

# For making curve parameters (a,b,c,p)
C = CurveOverFp(0, 1, 1, 2833)

# For checking Point Lies on Curve
C.contains(Point(x,y))

# To Calculate Order of Point
C.order(Point(x,y))

# For generating key pair
key = generate_keypair(C, P, orderOfPoint)

# For Signing Message
sig = sign(msg, C, P, OrderOfPoint, key)

# For verifying message
verify(msg, C, P, OrderOfPoint, sig)

# For Generating G value
G = C.base_point(C.generate_points())

# For Primitive Roots
Pm = C.primitive_point(C.generate_points())

# For Making Keys (Public and Private)
k = C.random_generator()
nA = C.random_generator()
nB = C.random_generator()
PA = C.scalar_mult(nA, G)
PB = C.scalar_mult(nB, G)
UA = [ PA, nA, PB ]
UB = [ PB, nB, PA ]

# For Encryption
C.ecc_encrypt(G, Pm, k, plain_text, UA[2])

# For Decrption
C.ecc_decrypt(enc_text, UB[1])
```

### For any other doubt feel free to contact or take help from the Jupyter Implementation because things are sequentially defined over there.
