from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QHBoxLayout,
    QMessageBox,
    QLabel
)

from core.services import password_service

class EditPasswordDialog(QDialog):

    def __init__(
        self,
        session,
        password_obj,
        key
    ):
        super().__init__()

        self.session = session
        self.password_obj = password_obj
        self.key = key

        self.setWindowTitle("Редактирование пароля")
        self.resize(400, 250)

        self.build_ui()

    def build_ui(self):
        layout = QVBoxLayout()

        title = QLabel("Редактировать пароль")

        self.site_input = QLineEdit()
        self.site_input.setText(
            self.password_obj.site
        )

        self.login_input = QLineEdit()
        self.login_input.setText(
            self.password_obj.login or ""
        )

        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Новый пароль"
        )

        self.password_input.setEchoMode(
            QLineEdit.Password
        )

        self.categories_input = QLineEdit()

        self.categories_input.setPlaceholderText(
            "Категории через запятую"
        )

        current_categories = [
            category.name
            for category in self.password_obj.categories
        ]

        self.categories_input.setText(
            ", ".join(current_categories)
        )

        save_button = QPushButton("Сохранить")
        cancel_button = QPushButton("Отмена")

        save_button.clicked.connect(
            self.on_save_clicked
        )

        cancel_button.clicked.connect(
            self.reject
        )

        buttons_layout = QHBoxLayout()

        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(cancel_button)

        layout.addWidget(title)
        layout.addWidget(self.site_input)
        layout.addWidget(self.login_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.categories_input)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def on_save_clicked(self):

        site = self.site_input.text()
        login = self.login_input.text()
        new_password = self.password_input.text()

        categories_text = self.categories_input.text()

        category_names = [
            category.strip()
            for category in categories_text.split(",")
            if category.strip()
        ]

        if not site:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Введите сайт"
            )
            return

        try:

            password_service.update_password_data(
                self.session,
                self.password_obj,
                new_site=site,
                new_login=login
            )

            password_service.sync_password_categories(
                self.session,
                self.password_obj,
                category_names
            )

            if new_password:
                password_service.change_password(
                    self.session,
                    self.password_obj,
                    new_password=new_password,
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