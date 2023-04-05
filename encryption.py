from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib

def generate_key(password):
    # Generate a 256-bit key using the SHA-256 hash function
    key = hashlib.sha256(password.encode()).digest()
    return key

def encrypt_master_password(password, key):
    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)

    # Create an AES cipher object with CBC mode and PKCS7 padding
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the password to a multiple of 16 bytes
    padded_password = password + b'\0' * (AES.block_size - len(password) % AES.block_size)

    # Encrypt the padded password using AES-CBC mode
    ciphertext = cipher.encrypt(padded_password)

    # Return the encrypted password and IV
    return ciphertext, iv

def decrypt_master_password(encrypted_password, iv, key):
    # Create an AES cipher object with CBC mode and PKCS7 padding
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the password using AES-CBC mode
    decrypted_password = cipher.decrypt(encrypted_password)

    # Remove padding from the decrypted password
    password = decrypted_password.rstrip(b'\0')

    # Return the decrypted password
    return password

def encrypt_password(password, key):
    cipher = AES.new(key, AES.MODE_CBC)
    cipher_text = cipher.encrypt(pad(password.encode(), AES.block_size))
    iv = cipher.iv
    return cipher_text, iv

def decrypt_password(cipher_text, iv, key):
    cipher = AES.new(key, AES.MODE_CBC, iv=iv)
    plain_text = unpad(cipher.decrypt(cipher_text), AES.block_size)
    return plain_text.decode()
