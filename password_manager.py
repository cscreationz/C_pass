import hashlib
import getpass
import database
import encryption

# Prompt the user for the master password
key = hashlib.sha256(getpass.getpass("Enter the key: ").encode()).digest()
master_password = getpass.getpass("Enter the master password: ")

# Check if the master password is correct
master_password_hash, master_password_iv = database.get_master_password()
if master_password_hash is not None and encryption.decrypt_master_password(master_password_hash, master_password_iv, key) != master_password:
    print("Invalid master password.")
    exit()

