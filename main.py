import argparse
from database import Database
from encryption import encrypt_password, decrypt_password, encrypt_master_password, decrypt_master_password

# Initialize database connection
db = Database()

# Define command-line interface
parser = argparse.ArgumentParser(description='Password manager')
parser.add_argument('command', choices=['add', 'view', 'update', 'delete'], help='Command to execute')
parser.add_argument('--website', help='Website name')
parser.add_argument('--username', help='Username')
parser.add_argument('--password', help='Password')
parser.add_argument('--new-password', help='New password')

# Get master password from user
master_password = input('Enter master password: ')

# Encrypt master password
master_password_key = b'secret_key_for_master_password'
encrypted_master_password, master_password_iv = encrypt_master_password(master_password.encode(), master_password_key)

# Parse command-line arguments and execute command
args = parser.parse_args()
if args.command == 'add':
    # Encrypt password
    password_key = b'secret_key_for_passwords'
    encrypted_password, password_iv = encrypt_password(args.password.encode(), password_key)

    # Insert password into database
    db.insert(args.website, args.username, encrypted_password, password_iv, encrypted_master_password, master_password_iv)

elif args.command == 'view':
    # Get all passwords from database
    passwords = db.get_passwords(encrypted_master_password, master_password_iv)

    # Print passwords to console
    for website, username, encrypted_password, password_iv in passwords:
        password = decrypt_password(encrypted_password, password_iv, password_key)
        print(f'Website: {website}, Username: {username}, Password: {password}')

elif args.command == 'update':
    # Encrypt new password
    new_encrypted_password, new_password_iv = encrypt_password(args.new_password.encode(), password_key)

    # Update password in database
    db.update_password(args.website, new_encrypted_password, new_password_iv, encrypted_master_password, master_password_iv)

elif args.command == 'delete':
    # Delete password from database
    db.delete_password(args.website, encrypted_master_password, master_password_iv)

# Close database connection
db.close()
