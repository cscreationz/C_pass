import psycopg2
import hashlib

# Connect to the PostgreSQL database
conn = psycopg2.connect(database="password_manager", user="postgres", password="password", host="localhost", port="5432")
cur = conn.cursor()

# Load the SQL commands from a file
with open("blah.sql", "r") as f:
    cur.execute(f.read())
    conn.commit()

# Function to hash a password using SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to add a password to the database
def add_password(website, username, password):
    cur.execute("INSERT INTO passwords (website, username, password) VALUES (%s, %s, %s)", (website, username, hash_password(password)))
    conn.commit()
    print("Password added successfully.")

# Function to retrieve a password from the database
def get_password(website):
    cur.execute("SELECT password FROM passwords WHERE website=%s", (website,))
    result = cur.fetchone()
    if result is not None:
        return result[0]
    else:
        return None

# Function to check if a master password is correct
def check_master_password(master_password):
    return hash_password(master_password) == "insert the hashed master password here"

# Main function to prompt the user for input
def main():
    # Prompt the user for the master password
    master_password = input("Enter the master password: ")
    if not check_master_password(master_password):
        print("Invalid master password.")
        return

    # Prompt the user for the action they want to perform
    while True:
        print("Select an action:")
        print("1. Add a password")
        print("2. Get a password")
        print("3. Quit")
        action = input("> ")
        if action == "1":
            website = input("Enter the website: ")
            username = input("Enter the username: ")
            password = input("Enter the password: ")
            add_password(website, username, password)
        elif action == "2":
            website = input("Enter the website: ")
            password = get_password(website)
            if password is not None:
                print(f"The password for {website} is {password}.")
            else:
                print(f"No password found for {website}.")
        elif action == "3":
            break
        else:
            print("Invalid action.")

# Call the main function
if __name__ == "__main__":
    main()

# Close the database connection
conn.close()
