from Hashing.numberTheory import *
from fractions import Fraction
from random import SystemRandom, randrange
import random

class Point(object):
    #Construct a point with two given coordindates.
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.inf = False

    #Construct the point at infinity.
    @classmethod
    def atInfinity(cls):
        P = cls(0, 0)
        P.inf = True
        return P

    #The secp256k1 generator.
    @classmethod
    def secp256k1(cls):
        return cls(55066263022277343669578718895168534326250603453777594175500187360389116729240,
                   32670510020758816978083085130507043184471273380659243275938904335757337482424)

    def __str__(self):
        if self.inf:
            return 'Inf'
        else:
            return '(' + str(self.x) + ',' + str(self.y) + ')'

    def __eq__(self,other):
        if self.inf:
            return other.inf
        elif other.inf:
            return self.inf
        else:
            return self.x == other.x and self.y == other.y

    def is_infinite(self):
        return self.inf

class Curve(object):
    #Set attributes of a general Weierstrass cubic y^2 = x^3 + ax^2 + bx + c over any field.
    def __init__(self, a, b, c, char, exp):
        self.a, self.b, self.c = a, b, c
        self.char, self.exp = char, exp
        print(self)

    def __str__(self):
        #Cases for 0, 1, -1, and general coefficients in the x^2 term.
        if self.a == 0:
            aTerm = ''
        elif self.a == 1:
            aTerm = ' + x^2'
        elif self.a == -1:
            aTerm = ' - x^2'
        elif self.a < 0:
            aTerm = " - " + str(-self.a) + 'x^2'
        else:
            aTerm = " + " + str(self.a) + 'x^2'
        #Cases for 0, 1, -1, and general coefficients in the x term.
        if self.b == 0:
            bTerm = ''
        elif self.b == 1:
            bTerm = ' + x'
        elif self.b == -1:
            bTerm = ' - x'
        elif self.b < 0:
            bTerm = " - " + str(-self.b) + 'x'
        else:
            bTerm = " + " + str(self.b) + 'x'
        #Cases for 0, 1, -1, and general coefficients in the constant term.
        if self.c == 0:
            cTerm = ''
        elif self.c < 0:
            cTerm = " - " + str(-self.c)
        else:
            cTerm = " + " + str(self.c)
        #Write out the nicely formatted Weierstrass equation.
        self.eq = 'y^2 = x^3' + aTerm + bTerm + cTerm
        #Print prettily.
        if self.char == 0:
            return self.eq + ' over Q'
        elif self.exp == 1:
            return self.eq + ' over ' + 'F_' + str(self.char)
        else:
            return self.eq + ' over ' + 'F_' + str(self.char) + '^' + str(self.exp)

    #Compute the discriminant.
    def discriminant(self):
        a, b, c = self.a, self.b, self.c
        return -4*a*a*a*c + a*a*b*b + 18*a*b*c - 4*b*b*b - 27*c*c

    #Compute the order of a point on the curve.
    def order(self, P):
        Q = P
        orderP = 1
        #Add P to Q repeatedly until obtaining the identity (point at infinity).
        while not Q.is_infinite():
            Q = self.add(P,Q)
            orderP += 1
        return orderP

    #List all multiples of a point on the curve.
    def generate(self, P):
        Q = P
        orbit = [str(Point.atInfinity())]
        #Repeatedly add P to Q, appending each (pretty printed) result.
        while not Q.is_infinite():
            orbit.append(str(Q))
            Q = self.add(P,Q)
        return orbit

    #Double a point on the curve.
    def double(self, P):
        return self.add(P,P)

    #Add P to itself k times.
    def mult(self, P, k):
        if P.is_infinite():
            return P
        elif k == 0:
            return Point.atInfinity()
        elif k < 0:
            return self.mult(self.invert(P), -k)
        else:
            #Convert k to a bitstring and use peasant multiplication to compute the product quickly.
            b = bin(k)[2:]
            return self.repeat_additions(P, b, 1)

    #Add efficiently by repeatedly doubling the given point, and adding the result to a running
    #total when, after the ith doubling, the ith digit in the bitstring b is a one.
    def repeat_additions(self, P, b, n):
        if b == '0':
            return Point.atInfinity()
        elif b == '1':
            return P
        elif b[-1] == '0':
            return self.repeat_additions(self.double(P), b[:-1], n+1)
        elif b[-1] == '1':
            return self.add(P, self.repeat_additions(self.double(P), b[:-1], n+1))

    #Returns a pretty printed list of points.
    def show_points(self):
        return [str(P) for P in self.get_points()]

class CurveOverFp(Curve):
    def __init__(self, a, b, c, p):
        Curve.__init__(self, a, b, c, p, 1)

    def contains(self, P):
        if P.is_infinite():
            return True
        else:
            return (P.y*P.y) % self.char == (P.x*P.x*P.x + self.a*P.x*P.x + self.b*P.x + self.c) % self.char

    def get_points(self):
        # Start with the point at infinity.
        points = [Point.atInfinity()]

        # Just brute force the rest.
        for x in range(self.char):
                for y in range(self.char):
                    P = Point(x,y)
                    if (y*y) % self.char == (x*x*x + self.a*x*x + self.b*x + self.c) % self.char:
                        points.append(P)
        return points

    def invert(self, P):
        if P.is_infinite():
            return P
        else:
            return Point(P.x, -P.y % self.char)

    def add(self, P_1, P_2):
        # Adding points over Fp and can be done in exactly the same way as adding over Q,
        # but with of the all arithmetic now happening in Fp.
        y_diff = (P_2.y - P_1.y) % self.char
        x_diff = (P_2.x - P_1.x) % self.char
        if P_1.is_infinite():
            return P_2
        elif P_2.is_infinite():
            return P_1
        elif x_diff == 0 and y_diff != 0:
            return Point.atInfinity()
        elif x_diff == 0 and y_diff == 0:
            if P_1.y == 0:
                return Point.atInfinity()
            else:
                ld = ((3*P_1.x*P_1.x + 2*self.a*P_1.x + self.b) * mult_inv(2*P_1.y, self.char)) % self.char
        else:
            ld = (y_diff * mult_inv(x_diff, self.char)) % self.char
        nu = (P_1.y - ld*P_1.x) % self.char
        x = (ld*ld - self.a - P_1.x - P_2.x) % self.char
        y = (-ld*x - nu) % self.char
        return Point(x,y)
    
    def generate_points(self):
        points = []
        finite_field = [i for i in range(self.char)]
        x = 0
        while(x < self.char):
            y = ( pow(x, 3) + self.b*x + self.c ) % self.char
            if mod_sqrt(y, self.char) != 0 and y in finite_field:
                points.append(Point(x, mod_sqrt(y, self.char)))
                points.append(Point(x, -mod_sqrt(y, self.char) % self.char))
            x = x + 1
        return points
    
    def base_point(self, curve_points):
        if curve_points[0].y > curve_points[1].y:
            return Point(curve_points[1].x,curve_points[1].y)
        else:
            return Point(curve_points[0].x,curve_points[0].y)
    
    def primitive_point(self,curve_points):
        point = random.choice(curve_points)
        return Point(point.x,point.y)
    
    def random_generator(self):
        return random.randint(0, self.char - 1)
    
    def scalar_mult(self,k, P):
        return Curve.mult(self,P,k)
    
    def ecc_encrypt(self,G, Pm, k, text, Pb):
        encrypted_text = []
        print_encrypted_text = []
        Pml_text = []
        for char in text:
            Pml = self.scalar_mult(ord(char), Pm)
            Pml_text.append((Pml.x,Pml.y))
            kPb = self.scalar_mult(k, Pb)
            Pml_kPb = []
            Pml_kPb = self.add(Pml, kPb)
            kG = self.scalar_mult(k, G)
            encrypted_text.append([Point(kG.x,kG.y), Point(Pml_kPb.x,Pml_kPb.y)])
            print_encrypted_text.append([(kG.x,kG.y), (Pml_kPb.x,Pml_kPb.y)])
        # print("The plaintext on the curve is represented as the following list\n", Pml_text)
        # print("\nThe encrypted plaintext on the curve is represented as the following list\n", print_encrypted_text)
        return encrypted_text
    
    def ecc_decrypt(self, encrypted_text, nb):
        decrypted_text = []
        for enc_msg in encrypted_text:
            kG = enc_msg[0]
            Pml_kPb = enc_msg[1]
            nbkG = self.scalar_mult(nb, kG)
            Pml = self.add(Pml_kPb, self.invert(nbkG))
            decrypted_text.append((Pml.x,Pml.y))
        # print("\nThe decrypted ciphertext on the curve is represented as the following list\n", decrypted_text)