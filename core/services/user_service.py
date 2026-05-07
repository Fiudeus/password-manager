from core.repositories import user_repo
from core.services.security.crypto import generate_key, generate_salt
from core.services.security.hashing import hash_password, verify_password


def register_user(session, username: str, master_password: str):
    existing = user_repo.get_user_by_username(session, username)
    if existing:
        raise ValueError("User already exists")

    hashed = hash_password(master_password)
    salt = generate_salt()

    user = user_repo.create_user(
        session,
        username=username,
        master_password_hash=hashed,
        salt=salt.hex()
    )

    return user


def login_user(session, username: str, master_password: str):
    user = user_repo.get_user_by_username(session, username)

    if not user:
        return None

    if not verify_password(master_password, user.master_password):
        return None

    salt = bytes.fromhex(user.salt)
    key = generate_key(master_password, salt)

    return user, key