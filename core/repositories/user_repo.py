from sqlalchemy import select
from core.models import User


# Добавление пользователя (первый вход в приложение)
def create_user(session, username: str, master_password_hash: str) -> User:
    user = User(username=username, master_password=master_password_hash)
    session.add(user)
    session.flush()
    return user


# Получение пользователя по username, в service используется для получения мастер-пароля и аутентификации
def get_user_by_username(session, username: str) -> User | None:
    stmt = select(User).where(User.username == username)
    return session.execute(stmt).scalars().first()


# Получение пользователя по id
def get_user_by_id(session, user_id: int) -> User | None:
    stmt = select(User).where(User.id == user_id)
    return session.execute(stmt).scalars().first()


# Обновление мастер-пароля
def update_master_password(session, user: User, new_hash: str) -> User:
    user.master_password = new_hash
    session.flush()
    return user