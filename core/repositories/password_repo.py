from sqlalchemy import select
from core.models import Password


def create_password(session, user_id: int, site: str, login: str, encrypted_password: str) -> Password:
    password = Password(
        user_id=user_id,
        site=site,
        login=login,
        password=encrypted_password
    )
    session.add(password)
    session.flush()
    return password


def get_password_by_id(session, password_id: int) -> Password | None:
    stmt = select(Password).where(Password.id == password_id)
    return session.execute(stmt).scalars().first()


def get_passwords_by_user(session, user_id: int) -> list[Password]:
    stmt = select(Password).where(Password.user_id == user_id)
    return session.execute(stmt).scalars().all()


# Обновление пароля. Передаём именованные аргументы нового сайта, логина и пароля,
# со значением по умолчанию None, для удобного обновления
def update_password(session, password: Password, *, new_site: str | None = None,
                    new_login: str | None = None, new_encrypted_password: str | None = None
                    ) -> Password:
    if new_site is not None:
        password.site = new_site

    if new_login is not None:
        password.login = new_login

    if new_encrypted_password is not None:
        password.password = new_encrypted_password

    session.flush()
    return password


def delete_password(session, password: Password) -> None:
    session.delete(password)
    session.flush()
