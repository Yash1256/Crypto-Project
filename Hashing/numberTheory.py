def divisors(n):
    divs = [0]
    for i in range(1, abs(n) + 1):
        if n % i == 0:
            divs.append(i)
            divs.append(-i)
    return divs

#Extended Euclidean algorithm.
def euclid(sml, big):
    if sml == 0:
        return (big, 0, 1)
    else:
        g, y, x = euclid(big % sml, sml)
        return (g, x - (big//sml)*y, y)

def mult_inv(a, n):
    g, x, y = euclid(a, n)
    if g != 1:
        raise ValueError('multiplicative inverse does not exist')
    else:
        return x % n

def mod_sqrt(a, P):
    def leg_symb(a, P):
        leg_sym = pow(a, (P - 1) // 2, P)
        return -1 if leg_sym == P - 1 else leg_sym
    if leg_symb(a, P) != 1:
        return 0
    elif a == 0:
        return 0
    elif P == 2:
        return P
    elif P % 4 == 3:
        return pow(a, (P + 1) // 4, P)
    i, h = [P-1, 0]
    while i % 2 == 0:
        i //= 2
        h += 1
    n = 2
    while leg_symb(n, P) != -1:
        n += 1
    x = pow(a, (i + 1) // 2, P)
    b, g, r = [pow(a, i, P), pow(n, i, P), h]
    while True:
        u,v = [b,0]
        for v in range(r):
            if u == 1:
                break
            u = pow(u, 2, P)
        if v == 0:
            return x
        gs = pow(g, 2 ** (r - v - 1), P)
        g = (gs * gs) % P
        x = (x * gs) % P
        b = (b * g) % P
        r = v
