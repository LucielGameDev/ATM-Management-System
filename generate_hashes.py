from hashing_passwords import hash_password
from getpass import getpass

#Generate hashes for already stored customers, admins, and technicians:
while True:
    password = getpass("\nEnter the existing password (or type 'exit' to quit): ").strip()

    if password.lower() == "exit":
        print("Exiting hash generator...")
        break

    print("Replace the plain-text password with this hash:")
    print(hash_password(password))