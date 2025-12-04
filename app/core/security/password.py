from passlib.context import CryptContext

pwd = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Функция хэширование пароля чтобы мы могли безоасно хранить его в базе данных."""
    return pwd.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    """Функция проверки пароля по хэшу."""
    return pwd.verify(password, hashed)
