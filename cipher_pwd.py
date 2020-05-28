import pathlib
import getpass
import hashlib
import customtypes
import base64
import os
from program_config import get_public_rabin, get_public_key
from rabin import Rabin


def cipher_pwd():
    signer = get_public_key()
    if signer == "Wrong file format":
        exit("Cannot find program public key.")
    p = input("Please specify path to the public key: ")
    p = pathlib.Path(p)
    while not p.exists():
        p = input("Cannot find such file. Please try again: ")
        p = pathlib.Path(p)
    with p.open('r') as f:
        n, sig = get_public_rabin(f)
    if n is None:
        exit("Wrong file format.")
    if not signer.verify(n, sig):
        exit("Invalid public key signature.")
    cipher = Rabin(512, n=n)
    passw = getpass.getpass("Please create your password: ")
    h = hashlib.sha256()
    h.update(bytes(passw, 'utf-8'))
    passw = getpass.getpass("Please type the created password again: ")
    h_check = hashlib.sha256()
    h_check.update(bytes(passw, 'utf-8'))
    while h.digest() != h_check.digest():
        passw = getpass.getpass("There is a mismatch. Please create your password again: ")
        h = hashlib.sha256()
        h.update(bytes(passw, 'utf-8'))
        passw = getpass.getpass("Please type the created password again: ")
        h_check = hashlib.sha256()
        h_check.update(bytes(passw, 'utf-8'))
    while len(bytes(passw, 'utf-8')) >= 32:
        passw = getpass.getpass("The password is too long. Please create another password: ")
        h = hashlib.sha256()
        h.update(bytes(passw, 'utf-8'))
        passw = getpass.getpass("Please type the created password again: ")
        h_check = hashlib.sha256()
        h_check.update(bytes(passw, 'utf-8'))
        while h.digest() != h_check.digest():
            passw = getpass.getpass("There is a mismatch. Please create your password again: ")
            h = hashlib.sha256()
            h.update(bytes(passw, 'utf-8'))
            passw = getpass.getpass("Please type the created password again: ")
            h_check = hashlib.sha256()
            h_check.update(bytes(passw, 'utf-8'))
    print("\nPerforming operation..")
    res = str(cipher.encrypt(passw), "ascii")
    print("Done. Here is your encrypted password:")
    print()
    print(res + '|' + str(base64.b32encode(customtypes.type_bytes(cipher.n)), "ascii"))
    print()
    answer = input("\nDo you want to save it? ").lower()
    if answer in ['yes', 'y', 'да', 'д']:
        index = sum([len(files) for r, d, files in os.walk("./encrypted_pwds")])
        with open('./encrypted_pwds/pwd{}'.format(index), "w") as f:
            f.write(res)
        print("Done. The path is './encrypted_pwds/pwd{}'".format(index))
    return res