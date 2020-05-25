def pow(x, y, n=None):
    if n:
        if y == 0:
            return 1
        if y == 1:
            return x % n
        res = 1
        while y:
            if y & 1 == 1:
                res = res * x % n
            x = x * x % n
            y = y // 2
    else:
        if y == 0:
            return 1
        if y == 1:
            return x
        res = 1
        while y:
            if y & 1 == 1:
                res = res * x
            x = x * x
            y = y // 2
    return res
