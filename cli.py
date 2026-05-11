from core.database import SessionLocal, engine, Base
import core.models

from core.services import user_service, password_service


def register(session):
    print("\n-- Регистрация --")

    username = input("Username: ")
    master_password = input("Master password: ")

    try:
        user_service.register_user(
            session,
            username=username,
            master_password=master_password
        )

        session.commit()
        print("Пользователь успешно зарегистрирован")

    except ValueError as e:
        session.rollback()
        print(e)

    except Exception as e:
        session.rollback()
        print(f"Unexpected error: {e}")


def login(session):
    print("\n-- Логин --")

    username = input("Username: ")
    master_password = input("Master password: ")

    result = user_service.login_user(
        session,
        username=username,
        master_password=master_password
    )

    if not result:
        print("Неверный username или master_password")
        return None, None

    user, key = result

    print(f"Добро пожаловать, {user.username}")

    return user, key


def password_menu(session, user, key):
    while True:
        print("\n-- Менеджер паролей --")
        print("1. Показать пароли")
        print("2. Добавить пароль")
        print("3. Открыть пароль")
        print("4. Поменять пароль")
        print("5. Удалить пароль")
        print("6. Выйти")

        choice = input("> ")

        # Показать все пароли
        if choice == "1":
            passwords = password_service.get_passwords(
                session,
                user.id,
                key
            )

            if not passwords:
                print("No passwords")
                continue

            for p in passwords:
                print(
                    f"ID: {p["id"]}"
                    f"Site: {p["site"]}"
                    f"Login: {p["login"]}"
                    f"Password: {"*" * len(p["password"])}"
                    f"Categories: {", ".join(p["categories"])}"
                )

        # Добавить пароль
        elif choice == "2":
            site = input("Site: ")
            login = input("Login: ")
            raw_password = input("Password: ")

            try:
                password_service.create_password(
                    session,
                    user_id=user.id,
                    site=site,
                    login=login,
                    raw_password=raw_password,
                    key=key
                )

                session.commit()
                print("Пароль добавлен")

            except Exception as e:
                session.rollback()
                print(f"Error: {e}")

        # Открыть пароль
        elif choice == "3":
            password_id = int(input("Password id: "))

            password_data = password_service.get_password(
                session,
                password_id,
                key
            )

            if not password_data:
                print("Пароль не найден")
                continue

            print("\n-- Пароль --")

            print(f"Site: {password_data['site']}")
            print(f"Login: {password_data['login']}")
            print(f"Password: {password_data['password']}")

            print("\n-- История --")

            if not password_data["history"]:
                print("Нет истории")

            else:
                for h in password_data["history"]:
                    print(
                        f"Old password: {h["old_password"]}"
                        f"Changed at: {h["changed_at"]}"
                    )

        # Изменить пароль
        elif choice == "4":
            password_id = int(input("Password id: "))
            new_password = input("Новый пароль: ")

            password_obj = password_service.password_repo.get_password_by_id(
                session,
                password_id
            )

            if not password_obj:
                print("Пароль не найден")
                continue

            try:
                password_service.change_password(
                    session,
                    password_obj,
                    new_password=new_password,
                    key=key
                )

                session.commit()
                print("Пароль обновлён")

            except Exception as e:
                session.rollback()
                print(f"Error: {e}")

        # Удалить пароль
        elif choice == "5":
            password_id = int(input("Password id: "))

            password_obj = password_service.password_repo.get_password_by_id(
                session,
                password_id
            )

            if not password_obj:
                print("Пароль не найден")
                continue

            try:
                password_service.delete_password(
                    session,
                    password_obj
                )

                session.commit()
                print("Пароль удалён")

            except Exception as e:
                session.rollback()
                print(f"Error: {e}")

        # Выход
        elif choice == "6":
            break

        else:
            print("Неверный выбор")


def main():
    Base.metadata.create_all(engine)

    session = SessionLocal()

    try:
        while True:
            print("\n-- Главное меню --")
            print("1. Регистрация")
            print("2. Логин")
            print("3. Выход")

            choice = input("> ")

            if choice == "1":
                register(session)

            elif choice == "2":
                user, key = login(session)

                if user:
                    password_menu(session, user, key)

            elif choice == "3":
                break

            else:
                print("Неверный выбор")

    finally:
        session.close()


if __name__ == "__main__":
    main()
