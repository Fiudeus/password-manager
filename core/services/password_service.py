from core.models import Password
from core.repositories import password_repo, history_repo, category_repo
from core.services.security.crypto import encrypt_password, decrypt_password


def create_password(session, *, user_id: int, site: str, login: str, raw_password: str, key: bytes):
    encrypted = encrypt_password(raw_password, key)

    return password_repo.create_password(
        session,
        user_id=user_id,
        site=site,
        login=login,
        encrypted_password=encrypted
    )


def get_passwords(session, user_id: int, key: bytes):
    passwords = password_repo.get_passwords_by_user(session, user_id)

    result = []

    for p in passwords:
        decrypted = decrypt_password(p.password, key)

        result.append({
            "id": p.id,
            "site": p.site,
            "login": p.login,
            "password": decrypted,
            "categories": [c.name for c in p.categories]
        })

    return result


def get_password(session, password_id: int, key: bytes):
    p = password_repo.get_password_by_id(session, password_id)
    if not p:
        return None
    history = history_repo.get_history_by_password_id(session, p.id)

    return {
        "id": p.id,
        "site": p.site,
        "login": p.login,
        "password": decrypt_password(p.password, key),
        "history": [
            {
                "old_password": decrypt_password(h.old_password, key),
                "changed_at": h.changed_at
            }
            for h in history
        ]
    }


# Старый пароль сохраняем в историю до обновления
def change_password(session, password_obj: Password, *, new_password: str, key: bytes):
    history_repo.create_history(
        session,
        password_obj.id,
        password_obj.password
    )

    encrypted = encrypt_password(new_password, key)

    password_repo.update_password(
        session,
        password_obj,
        new_encrypted_password=encrypted
    )


def update_password_data(session, password_obj: Password, *,
    new_site: str | None = None,
    new_login: str | None = None
):
    return password_repo.update_password(
        session,
        password_obj,
        new_site=new_site,
        new_login=new_login
    )


def delete_password(session, password_obj: Password):
    return password_repo.delete_password(session, password_obj)


# Создаём категорию, если её ещё нет, после добавляем её к паролю
def add_category(session, password_obj, category_name: str):
    category = category_repo.get_category_by_name(session, category_name)

    if not category:
        category = category_repo.create_category(session, category_name)

    if category not in password_obj.categories:
        password_obj.categories.append(category)

    session.flush()


def remove_category(session, password_obj, category_name: str):
    category = category_repo.get_category_by_name(session, category_name)

    if category and category in password_obj.categories:
        password_obj.categories.remove(category)

    session.flush()