import random
import math
from calc import pow

def is_prime(p, k):
    if p%2 == 0 or p%3 == 0 or p%5 == 0 or p%7 == 0 or p%11 == 0:
        return False
    p_1 = p - 1
    s = 0
    t = 0
    while p_1 % 2 == 0:
        s += 1
        p_1 = p_1 // 2
    t = p_1
    a_set = set()
    for i in range(k):
        a = random.randint(2, p - 2)
        while a in a_set:
            a = random.randint(2, p - 2)
        a_set.add(a)
        if not miller_rabin(p, t, s, a):
            return False
    return True


def miller_rabin(p, t, s, a):
    x = pow(a, t, p)
    if x == 1 or x == p-1:
        return True
    for i in range(s-1):
        x = x*x % p
        if x == 1:
            return False
        elif x == p-1:
            return True
        return False


def get_prime(k):
    p = (1<<(k-1))+int(random.getrandbits(k-2)<<1)+1
    while not is_prime(p, k):
        p = (1 << (k - 1)) + int(random.getrandbits(k - 2) << 1) + 1
    return p


def get_prime_big_p_1(k):
    p_1 = get_prime(k // 2 + 1)
    p_2 = get_prime(k // 2 + 1)
    while not is_prime(2 * p_1 * p_2 + 1, k):
        p_1 = get_prime(k // 2 + 1)
        p_2 = get_prime(k // 2 + 1)
    return 2 * p_1 * p_2 + 1
