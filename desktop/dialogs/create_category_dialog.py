from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QLabel
)

from core.services import category_service


class CreateCategoryDialog(QDialog):

    def __init__(self, session):
        super().__init__()

        self.session = session

        self.setWindowTitle("Создание категории")
        self.resize(300, 120)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Новая категория")

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Название категории"
        )

        create_button = QPushButton(
            "Создать"
        )

        create_button.clicked.connect(
            self.on_create_clicked
        )

        layout.addWidget(title)
        layout.addWidget(self.name_input)
        layout.addWidget(create_button)

        self.setLayout(layout)

    def on_create_clicked(self):

        name = self.name_input.text()

        try:

            category_service.create_category(
                self.session,
                name
            )

            self.session.commit()

            self.accept()

        except ValueError as e:

            QMessageBox.warning(
                self,
                "Ошибка",
                str(e)
            )

        except Exception as e:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e)
            )