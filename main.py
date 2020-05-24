import json
import os
import program_config
from cipher_pwd import cipher_pwd
from decipher_pwd import decipher_pwd
from register import register


def is_first_launch():
    if not os.path.exists("./passcoder/private") or not os.path.exists("./passcoder/public"):
        print("First launch. Creating program keypair for signatures. Please wait.")
        return program_config.init_passcoder()
    else:
        return program_config.get_private_key()


def greeting():
    with open("./passcoder/users.json", "r") as f:
        data = json.load(f)
    if len(data['users']) == 0:
        print("Welcome. It appears there is no registered user. Please type 'register' to register or 'help' to list all commands.")
    else:
        print("Welcome. Please type 'help' if you want to list all commands.")


def commands(signer):
    command = input().lower()
    if command in ['register', 'r']:
        register(signer)
    elif command in ['change-signature-key', 'csk', 'c']:
        program_config.change_passcoder()
    elif command in ['encrypt', 'e']:
        cipher_pwd()
    elif command in ['decrypt', 'd']:
        decipher_pwd()
    elif command in ['help', 'h']:
        print("'help'                        :      Return this message.")
        print("'register'                    :      Start the user registration process.")
        print("'change-signature-key', 'csk' :      Generate and switch key-pair for signature algorithm.")
        print("'encrypt'                     :      Encrypt the password.")
        print("'decrypt'                     :      Decrypt the password.")
    else:
        print("Unknown command.")
        print("'help'                        :      Return this message.")
        print("'register'                    :      Start the user registration process.")
        print("'change-signature-key', 'csk' :      Generate and switch key-pair for signature algorithm.")
        print("'encrypt'                     :      Encrypt the password.")
        print("'decrypt'                     :      Decrypt the password.")


if __name__ == '__main__':
    try:
        signer = is_first_launch()
        greeting()
        while True:
            commands(signer)
            print("\nAwaiting for further commands.")
    except KeyboardInterrupt:
        print()
        print("Terminating. Thank you for using this passcoder.")
