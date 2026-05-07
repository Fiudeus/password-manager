from sqlalchemy import select
from core.models import User


# Добавление пользователя (первый вход в приложение)
def create_user(session, username: str, master_password_hash: str, salt: str) -> User:
    user = User(username=username, master_password=master_password_hash, salt=salt)
    session.add(user)
    session.flush()
    return user


# Получение пользователя по username, в service используется для получения мастер-пароля и аутентификации
def get_user_by_username(session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return session.execute(stmt).scalars().first()


def get_user_by_id(session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return session.execute(stmt).scalars().first()