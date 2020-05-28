import getpass
import json
import hashlib
import pathlib
import base64
import os
import customtypes
from program_config import get_private_rabin


def decipher_pwd():
    h = hashlib.sha256()
    log = input("Please specify your login: ")
    passw = getpass.getpass("Please type your system password: ")
    with open("./passcoder/users.json", "r") as f:
        data = json.load(f)
    user_credentials = next((user for user in data['users'] if user['login'] == log), None)
    while user_credentials is None:
        log = input("Invalid credentials. Please specify your login: ")
        passw = getpass.getpass("Please type your system password: ")
        user_credentials = next((user for user in data['users'] if user['login'] == log), None)
    h.update(bytes(passw, 'utf-8') + b'hello')
    while str(base64.b32encode(h.digest()), "ascii") != user_credentials['pwd']:
        passw = getpass.getpass("Wrong system password. Please try again: ")
        h.update(bytes(passw, 'utf-8') + b'hello')
    p = input("Please specify path to the private key: ")
    p = pathlib.Path(p)
    while not p.exists():
        p = input("Cannot find such file. Please try again: ")
        p = pathlib.Path(p)
    with p.open("r") as f:
        cipher = get_private_rabin(f, str(base64.b32encode(h.digest()),  "ascii"))
    if type(cipher) == str:
        exit(cipher)
    passw = input("Please specify the encrypted password you want to decrypt: ")
    while '|' not in passw:
        passw = input("Wrong format. Please try again: ")
    passw, n = passw.split('|', 1)
    if customtypes.type_int(n, True) != cipher.n:
        exit("Ciphertext cannot be decrypted with this key.")
    print("\nPerforming operation..")
    decr = cipher.decrypt(passw)
    print("Done. Here is list of possible passwords:")
    print()
    for elem in decr:
        print(elem)
        print()
    print()
    answer = input("\nDo you want to save it? ").lower()
    if answer in ['yes', 'y', 'да', 'д']:
        index = sum([len(files) for r, d, files in os.walk("./decrypted_pwds")])
        with open('./decrypted_pwds/pwd{}'.format(index), "w") as f:
            for elem in decr:
                f.write(elem)
                f.write(os.linesep)
        print("Done. The path is './decrypted_pwds/pwd{}'".format(index))
    return decr