from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox
)

from core.services import password_service


class AddPasswordDialog(QDialog):

    def __init__(self, session, user, key):
        super().__init__()

        self.session = session
        self.user = user
        self.key = key

        self.setWindowTitle("Добавить пароль")
        self.resize(400, 250)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Новый пароль")

        self.site_input = QLineEdit()
        self.site_input.setPlaceholderText("Сайт")

        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")

        self.password_input.setEchoMode(QLineEdit.Password)

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        save_button.clicked.connect(self.on_save_clicked)
        cancel_button.clicked.connect(self.reject)

        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        layout.addWidget(title)
        layout.addWidget(self.site_input)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def on_save_clicked(self):

        site = self.site_input.text()
        login = self.login_input.text()
        password = self.password_input.text()

        if not site:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите сайт"
            )
            return

        if not password:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите пароль"
            )
            return

        try:

            password_service.create_password(
                self.session,
                user_id=self.user.id,
                site=site,
                login=login,
                raw_password=password,
                key=self.key
            )

            self.session.commit()

            self.accept()

        except Exception as e:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e)
            )