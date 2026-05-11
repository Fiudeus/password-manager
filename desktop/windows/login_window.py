from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)
from core.services import user_service
from desktop.windows.main_window import MainWindow

class LoginWindow(QWidget):

    def __init__(self, session):
        super().__init__()

        self.session = session

        self.setWindowTitle("Password Manager")
        self.resize(400, 250)

        self.build_ui()


    def build_ui(self):

        title_label = QLabel("Авторизация")

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")


        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)


        login_button = QPushButton("Войти")
        login_button.clicked.connect(self.on_login_clicked)

        register_button = QPushButton("Регистрация")
        register_button.clicked.connect(self.on_register_clicked)


        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(login_button)
        buttons_layout.addWidget(register_button)


        main_layout = QVBoxLayout()

        main_layout.addWidget(title_label)
        main_layout.addWidget(self.login_input)
        main_layout.addWidget(self.password_input)
        main_layout.addLayout(buttons_layout)

        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)


        self.setLayout(main_layout)

    def on_login_clicked(self):
        username = self.login_input.text()
        password = self.password_input.text()

        result = user_service.login_user(
            self.session,
            username=username,
            master_password=password
        )

        if not result:
            QMessageBox.warning(
                self,
                "Ошибка входа",
                "Неверный логин или пароль"
            )
            return

        user, key = result

        self.user = user
        self.key = key

        self.main_window = MainWindow(
            self.session,
            self.user,
            self.key
        )

        self.main_window.show()

        self.close()

    def on_register_clicked(self):

        username = self.login_input.text()
        password = self.password_input.text()

        if not username:
            QMessageBox.warning(
                self,
                "Ошибка регистрации",
                "Введите имя пользователя"
            )
            return

        if not password:
            QMessageBox.warning(
                self,
                "Ошибка регистрации",
                "Введите пароль"
            )
            return

        try:

            user_service.register_user(
                session=self.session,
                username=username,
                master_password=password
            )

            self.session.commit()

            QMessageBox.information(
                self,
                "Успешная регистрация",
                "Пользователь успешно создан"
            )

            result = user_service.login_user(
                self.session,
                username=username,
                master_password=password
            )

            user, key = result

            self.user = user
            self.key = key

            self.main_window = MainWindow(
                self.session,
                self.user,
                self.key
            )

            self.main_window.show()

            self.close()

        except ValueError as e:

            self.session.rollback()

            QMessageBox.warning(
                self,
                "Ошибка регистрации",
                str(e)
            )

        except Exception as e:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Критическая ошибка",
                str(e)
            )
