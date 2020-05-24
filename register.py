from rabin import Rabin
import customtypes
import base64
import os
import getpass
import hashlib
import json


def register(rsa):
    log = input("Please specify your login: ")
    with open("./passcoder/users.json", "r") as f:
        data = json.load(f)
    user = next((user for user in data['users'] if user['login'] == log), None)
    while user is not None:
        log = input("Such login already exists. Please use another login: ")
        user = next((user for user in data['users'] if user['login'] == log), None)
    passw = getpass.getpass("Please create your system password: ")
    h = hashlib.sha256()
    h.update(bytes(passw, 'utf-8') + b'hello')
    passw = getpass.getpass("Please type the created system password again: ")
    h_check = hashlib.sha256()
    h_check.update(bytes(passw, 'utf-8') + b'hello')
    while h.digest() != h_check.digest():
        passw = getpass.getpass("There is a mismatch. Please create your system password again: ")
        h = hashlib.sha256()
        h.update(bytes(passw, 'utf-8'))
        passw = getpass.getpass("Please type the created system password again: ")
        h_check = hashlib.sha256()
        h_check.update(bytes(passw, 'utf-8'))
    data['users'].append({
        'login': log,
        'pwd': str(base64.b32encode(h.digest()), "ascii")
    })
    with open("./passcoder/users.json", "w") as f:
        json.dump(data, f)
    print("\nGenerating your keypair.")
    cipher = Rabin(256)
    print("Done.")
    print("\nSigning the public key.")
    temp, signature = rsa.sign(cipher.n)
    print("Done.")
    is_file = input("\nDo you want to save your keypair as file? ").lower()
    if is_file in ['yes', 'y', 'да', 'д']:
        with open('./user/rabin_private', 'wb') as f:
            f.write(b'-----BEGIN RABIN PRIVATE KEY-----' +
                    bytes(os.linesep, "ascii") + base64.b32encode(h.digest()) +
                    bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.p)) +
                    bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.q)) +
                    bytes(os.linesep, "ascii") +
                    b'-----END RABIN PRIVATE KEY-----')
        with open('./user/rabin_public', 'wb') as f:
            f.write(b'-----BEGIN RABIN PUBLIC KEY-----' +
                    bytes(os.linesep, "ascii") + base64.b32encode(customtypes.type_bytes(cipher.n)) +
                    bytes(os.linesep, "ascii") + signature + bytes(os.linesep, "ascii") +
                    b'-----END RABIN PUBLIC KEY-----')
        print("Done. The files are stored as './user/rabin_private' and './user/rabin_public'. Please save them in private space and delete.")
    print("\nHere is your private key. Please copy and save it in private place:\n")
    print("-----BEGIN RABIN PRIVATE KEY-----")
    print(str(base64.b32encode(h.digest()), "ascii"))
    print(str(base64.b32encode(customtypes.type_bytes(cipher.p)), "ascii"))
    print(str(base64.b32encode(customtypes.type_bytes(cipher.q)), "ascii"))
    print("-----END RABIN PRIVATE KEY-----")
    print("\nHere is your public key. Please copy and save it:\n")
    print("-----BEGIN RABIN PUBLIC KEY-----")
    print(str(base64.b32encode(customtypes.type_bytes(cipher.n)), "ascii"))
    print(str(signature, "ascii"))
    print("-----END RABIN PUBLIC KEY-----")
    return 0
