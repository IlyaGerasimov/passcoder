from prime import get_prime_big_p_1
import random
import math
import base64
import hashlib
import customtypes
from calc import pow


def reverse(a, b):
    n = b
    res = 1
    prev = 0
    i = 0
    while a != 1:
        temp = res
        res = res * (b // a) + prev
        prev = temp
        a_1 = b % a
        b = a
        a = a_1
        i += 1
    return res if i % 2 == 0 else -res+n


def get_secure_prime_p_1(k):
    p = get_prime_big_p_1(k)
    q = get_prime_big_p_1(k + 2)
    while math.gcd(p - 1, q - 1) != 2:
        p = get_prime_big_p_1(k)
        q = get_prime_big_p_1(k + 2)
    return p, q


def get_secure_e_d(p, q):
    p_calc = int(math.sqrt(p))
    q_calc = int(math.sqrt(q))
    bound = p_calc * q_calc
    phi_n = (p - 1) * (q - 1)
    e = random.randint(65536, int(bound / 4))
    while math.gcd(e, phi_n) != 1:
        e = random.randint(65536, int(bound / 4))
    d = reverse(e, phi_n)
    while d < 0.2 * (p_calc * q_calc) or d == e:
        e = random.randint(65536, int(bound / 4))
        while math.gcd(e, phi_n) != 1:
            e = random.randint(65536, int(bound / 4))
        d = reverse(e, phi_n)
    return e, d


class RSASign:

    def __init__(self, k, p=None, q=None, e=None, n=None):
        if p and q:
            p = customtypes.type_int(p, True)
            q = customtypes.type_int(q, True)
            if p < k or q < k:
                print("Warning: Specified prime numbers are too short for RSA signature.")
            self.p = p
            self.q = q
        elif e and n:
            e = customtypes.type_int(e, True)
            n = customtypes.type_int(n, True)
            self.p = None
            self.q = None
            if math.log2(n) < 2 * k:
                print("Warning: Specified module is too small")
            self.n = n
            if e < 65536:
                print("Warning: Specified encryption exponent is too small.")
            self.e = e
            return
        else:
            self.p, self.q = get_secure_prime_p_1(k)
        if e:
            p_calc = int(math.sqrt(self.p))
            q_calc = int(math.sqrt(self.q))
            e = customtypes.type_int(e, True)
            if math.gcd(e, (p - 1)*(q - 1)) != 1:
                exit("Cannot use such parameters for RSA signature.")
            if e < 65536:
                print("Warning: Specified encryption exponent is too small.")
            self.e = e
            self.d = reverse(self.e, (self.p - 1) * (self.q - 1))
            if self.d < 0.2 * ((p_calc * q_calc) ** 0.2):
                print("Warning: Decryption exponent is too small.")
        else:
            self.e, self.d = get_secure_e_d(self.p, self.q)
        self.n = self.p * self.q
        self.__phi = (self.p - 1) * (self.q - 1)

    def sign(self, m):
        if self.d is None:
            exit("Cannot sign.")
        m = customtypes.type_bytes(m, True)
        h = hashlib.sha512()
        h.update(m)
        h_int = customtypes.type_int(h.digest())
        c = pow(h_int, self.d, self.n)
        c = base64.b32encode(customtypes.type_bytes(c, False))
        return m, c

    def verify(self, m, c):
        m = customtypes.type_bytes(m, True)
        h = hashlib.sha512()
        h.update(m)
        h_int = customtypes.type_int(h.digest())
        c = customtypes.type_int(c, True)
        res = pow(c, self.e, self.n)
        if res == h_int:
            return True
        return False
