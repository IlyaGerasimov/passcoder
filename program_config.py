import base64
import os
import customtypes
from rsa import RSASign
from rabin import Rabin
import hashlib


def init_passcoder():
    cipher = RSASign(512)
    with open("./passcoder/private", 'wb') as f:
        f.write(b'-----BEGIN RSA PRIVATE KEY-----' +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.p)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.q)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.e)) +
                bytes(os.linesep, "ascii") +
                b'-----END RSA PRIVATE KEY-----'
                )
    with open("./passcoder/public", "wb") as f:
        f.write(b'-----BEGIN RSA PUBLIC KEY-----' +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.e)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.n)) +
                bytes(os.linesep, "ascii") +
                b'-----END RSA PUBLIC KEY-----'
                )
    return cipher


def get_private_key():
    with open("./passcoder/private", "r") as f:
        title = f.readline().strip('\n')
        if title != '-----BEGIN RSA PRIVATE KEY-----':
            exit("Wrong file format")
        p = f.readline().strip('\n')
        q = f.readline().strip('\n')
        e = f.readline().strip('\n')
        title = f.readline().strip('\n')
        if title != '-----END RSA PRIVATE KEY-----':
            exit("Wrong file format")
        return RSASign(512, p=p, q=q, e=e)


def get_public_key():
    with open("./passcoder/public", "r") as f:
        title = f.readline().strip('\n')
        if title != '-----BEGIN RSA PUBLIC KEY-----':
            exit("Wrong file format")
        e = f.readline().strip('\n')
        n = f.readline().strip('\n')
        title = f.readline().strip('\n')
        if title != '-----END RSA PUBLIC KEY-----':
            exit("Wrong file format")
        return RSASign(512, e=e, n=n)


def get_public_rabin(f):
    # f with "r" mode
    title = f.readline().strip('\n')
    if title != '-----BEGIN RABIN PUBLIC KEY-----':
        return None, None
    n = f.readline().strip('\n')
    sig = f.readline().strip('\n')
    title = f.readline().strip('\n')
    if title != '-----END RABIN PUBLIC KEY-----':
        return None, None
    return n, sig


def get_private_rabin(f, hash):
    # f with "r" mode
    title = f.readline().strip('\n')
    if title != '-----BEGIN RABIN PRIVATE KEY-----':
        return "Wrong format."
    h_check = f.readline().strip('\n')
    if h_check != hash:
        return "No access."
    p = f.readline().strip('\n')
    q = f.readline().strip('\n')
    title = f.readline().strip('\n')
    if title != '-----END RABIN PRIVATE KEY-----':
        return "Wrong format."
    return Rabin(512, p=p, q=q)


def change_passcoder():
    source = input("Please specify the directory of Rabin public keys in order to resign them: ")
    p = int(input("Please specify the first prime: "))
    q = int(input("Please specify the second prime: "))
    e = int(input("Please specify the cipher exponent: "))
    curr_cipher = get_private_key()
    cipher = RSASign(512, p, q, e)
    print("Updating specified signatures:")
    directory = os.fsencode(source)
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        with open(source + ("/" if source[-1] != '/' else "") + filename, 'r') as f:
            n, sig = get_public_rabin(f)
            if n is None or sig is None:
                continue
        if curr_cipher.verify(n, sig):
            tmp, sig = cipher.sign(n)
            with open(source + ("/" if source[-1] != '/' else "") + filename, 'wb') as f:
                f.write(b'-----BEGIN RABIN PUBLIC KEY-----' +
                        bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.n)) +
                        bytes(os.linesep, "ascii") + sig + bytes(os.linesep, "ascii") +
                        b'-----END RABIN PUBLIC KEY-----')
        else:
            print("{}: Invalid signature".format(filename))
    with open("./passcoder/private", 'wb') as f:
        f.write(b'-----BEGIN RSA PRIVATE KEY-----' +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.p)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.q)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.e)) +
                bytes(os.linesep, "ascii") +
                b'-----END RSA PRIVATE KEY-----'
                )
    with open("./passcoder/public", "wb") as f:
        f.write(b'-----BEGIN RSA PUBLIC KEY-----' +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.e)) +
                bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.n)) +
                bytes(os.linesep, "ascii") +
                b'-----END RSA PUBLIC KEY-----'
                )
    print("Program signature has changed.")
    return 0