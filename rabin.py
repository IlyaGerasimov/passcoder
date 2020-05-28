import random
import math
import base64
from prime import get_prime_big_p_1
from calc import pow
import customtypes
import sys


def simple_factor(a):
    factor = {}
    for prime in [2, 3, 5, 7, 11]:
        while a % prime == 0:
            if prime not in factor:
                factor[prime] = 1
            else:
                factor[prime] += 1
            a = a // prime
    return factor


def legendre(a, p):
    if a % p == 0:
        return 0
    if a > p:
        a = a % p
    if a == 1:
        return 1
    if a == 2:
        if p % 8 == 1 or p % 8 == 7:
            return 1
        return -1
    if a == p - 1:
        if p % 4 == 1:
            return 1
        return -1
    res = 1
    factor = simple_factor(a)
    if sum(value for value in factor.values()) > 1:
        for q, step in factor.items():
            if step % 2 == 1:
                res = res * legendre(q, p)
        return res
    else:
        if (p - 1) % 2 == 0 or (a - 1) % 2 == 0:
            return legendre(p, a)
        else:
            return (-1) * legendre(p, a)
    #return pow(a, (p - 1) // 2, p)


def square_solve(a, p):
    if a == 1:
        return a
    if p % 4 == 3:
        return pow(a, (p+1) // 4, p)
    s = p - 1
    m = 0
    while s % 2 == 0:
        m += 1
        s = s // 2
    b = 2
    while legendre(b, p) != -1:
        b += 1
    b = pow(b, s, p)
    t_1 = pow(a, s, p)
    if m == 1:
        j_res = 0
    else:
        r_1 = b
        t = list([t_1])
        r = list([r_1])
        if m > 2:
            for i in range(1, m - 1):
                t_1 = pow(t_1, 2, p)
                t.append(t_1)
                r_1 = pow(r_1, 2, p)
                r.append(r_1)
        eps = t[m-2]
        j = [0 if eps == 1 else 1]
        if m == 2:
            j_res = j[0]
        else:
            for i in range(m - 3, -1, -1):
                eps = t[i]
                for k in range(i + 1, m - 1):
                    eps = eps*pow(r[k], j[k - i - 1], p) % p
                j.append(0 if eps == 1 else 1)
            j_res = 0
            for i in range(m - 2, -1, -1):
                j_res = (j_res * 2 + j[i]) % (p - 1)
    x = (pow(b, j_res, p) * pow(a, (s + 1) // 2, p)) % p
    return x


def reverse(a, b):
    n = b
    res = 1
    prev = 0
    i = 0
    while a != 1:
        temp = res
        res = res * (b // a) + prev
        prev = temp
        a_1 = b%a
        b = a
        a = a_1
        i += 1
    return res if i % 2 == 0 else -res+n


def big_p_1_check(p, q):
    if p % 4 != 3 or q % 4 != 3:
        return False
    return True


class Rabin:

    def __init__(self, k, p=None, q=None, n=None):
        if p and q:
            p = customtypes.type_int(p, True)
            q = customtypes.type_int(q, True)
            self.p = p
            self.q = q
            self.n = self.p * self.q
            if math.log2(self.n) < 2 * k:
                print("Warning: specified module is too small.")
        elif n:
            n = customtypes.type_int(n, True)
            self.p = None
            self.q = None
            self.n = n
            if math.log2(self.n) < 2 * k:
                print("Warning: specified module is too small.")
        else:
            self.p = get_prime_big_p_1(k)
            self.q = get_prime_big_p_1(k + 2)
            while not big_p_1_check(self.p, self.q):
                self.p = get_prime_big_p_1(k)
                self.q = get_prime_big_p_1(k + 2)
            self.n = self.p * self.q

    def encrypt(self, m):
        m = customtypes.type_int(m) % self.n
        return base64.b32encode(customtypes.type_bytes((m ** 2) % self.n))

    def decrypt(self, c):
        if self.p is None:
            exit("Cannot decrypt, no private key.")
        c = customtypes.type_int(c, True) % self.n
        m_1 = square_solve(c, self.p)
        m_2 = square_solve(c, self.q)
        print(m_1, m_2)
        m_plus = (m_1 * self.q * reverse(self.q % self.p, self.p) + m_2 * self.p * reverse(self.p % self.q, self.q)) % self.n
        m_minus = (m_1 * self.q * reverse(self.q % self.p, self.p) - m_2 * self.p * reverse(self.p % self.q, self.q)) % self.n
        res = [m_plus, m_minus, (-m_plus) % self.n, (-m_minus) % self.n]
        i = 0
        while i < len(res):
            try:
                res[i] = customtypes.type_bytes(res[i]).decode("ascii")
                i += 1
            except UnicodeDecodeError:
                res.pop(i)
        return res
