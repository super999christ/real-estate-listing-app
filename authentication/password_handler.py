from passlib.context import CryptContext


password_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str):
    """function for hashing a plain string password."""
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    """
    function for comparing plain password with
    its hashed version for authentication purposes.
    """
    return password_context.verify(plain_password, hashed_password)
