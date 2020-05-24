import base64


def type_int(m, is_base=False):
    if type(m) is int:
        return m
    if is_base:
        m = base64.b32decode(m)
    if type(m) == str:
        m = m.encode('utf-8')
        m = m.hex()
    else:
        m = m.hex()
    return int(m, 16)


def type_bytes(m, is_base=False):
    if type(m) is int:
        if ((m.bit_length() + 3) // 4) % 2 == 1:
            return bytes.fromhex('0' + hex(m).split('x')[1])
        else:
            return bytes.fromhex(hex(m).split('x')[1])
    if is_base:
        m = base64.b32decode(m)
    if type(m) is bytes:
        return m
    elif type(m) is str:
        return bytes(m, 'ascii')
    return m