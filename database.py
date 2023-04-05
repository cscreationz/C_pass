import psycopg2
from psycopg2 import sql
from encryption import encrypt_password, decrypt_password, encrypt_master_password, decrypt_master_password

class Database:
    def __init__(self, dbname, host, username, password):
        self.dbname = dbname
        self.host = host
        self.username = username
        self.password = password
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = psycopg2.connect(
            dbname=self.dbname,
            host=self.host,
            user=self.username,
            password=self.password
        )
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def insert(self, website, username, password, master_password):
        # Encrypt the password using the master password as the key
        encrypted_password, password_iv = encrypt_password(password, decrypt_master_password(master_password, master_password))

        # Construct the SQL query to insert the data into the table
        query = sql.SQL("INSERT INTO passwords (website, username, password, password_iv) VALUES ({}, {}, {}, {})").format(
            sql.Literal(website),
            sql.Literal(username),
            sql.Literal(encrypted_password),
            sql.Literal(password_iv)
        )

        # Execute the SQL query
        self.cursor.execute(query)
        self.connection.commit()

    def get_passwords(self, master_password):
        # Construct the SQL query to retrieve all rows from the table
        query = sql.SQL("SELECT website, username, password, password_iv FROM passwords")

        # Execute the SQL query and retrieve the rows
        self.cursor.execute(query)
        rows = self.cursor.fetchall()

        # Decrypt the passwords using the master password
        passwords = []
        for row in rows:
            website, username, encrypted_password, password_iv = row
            decrypted_password = decrypt_password(encrypted_password, password_iv, decrypt_master_password(master_password, master_password))
            passwords.append((website, username, decrypted_password))

        return passwords

    def update_password(self, website, new_password, master_password):
        # Encrypt the new password using the master password as the key
        encrypted_password, password_iv = encrypt_password(new_password, decrypt_master_password(master_password, master_password))

        # Construct the SQL query to update the password for the given website
        query = sql.SQL("UPDATE passwords SET password = {}, password_iv = {} WHERE website = {}").format(
            sql.Literal(encrypted_password),
            sql.Literal(password_iv),
            sql.Literal(website)
        )

        # Execute the SQL query
        self.cursor.execute(query)
        self.connection.commit()

    def delete_password(self, website):
        # Construct the SQL query to delete the row for the given website
        query = sql.SQL("DELETE FROM passwords WHERE website = {}").format(
            sql.Literal(website)
        )

        # Execute the SQL query
        self.cursor.execute(query)
        self.connection.commit()
