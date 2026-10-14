import hashlib
import secrets
import hmac

#Take a password and return a hashed version of it using PBKDF2 with SHA-256 and a random salt:
def hash_password(password):
    
    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        600_000
    ).hex()

    return f"{salt}${password_hash}"

#Verify a password against a stored hashed password:
def verify_password(password, stored_password):

    try:
        salt, stored_hash = stored_password.split("$", 1)
    except ValueError:
        return False

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        600_000
    ).hex()

    return hmac.compare_digest(password_hash, stored_hash)
