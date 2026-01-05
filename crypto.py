from cryptography.fernet import Fernet

def encrypt_password(p):
    key = Fernet.generate_key()
    f = Fernet(key)
    return key.decode(), f.encrypt(p.encode()).decode()
