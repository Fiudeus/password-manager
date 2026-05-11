from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
)


class PasswordHistoryDialog(QDialog):

    def __init__(self, history_data, site):
        super().__init__()

        self.history_data = history_data
        self.site = site

        self.setWindowTitle(
            "История паролей"
        )

        self.resize(500, 400)

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel(
            f"История изменений: {self.site}"
        )

        history_list = QListWidget()

        if not self.history_data:

            history_list.addItem(
                "История пуста"
            )

        else:

            for item in self.history_data:

                history_list.addItem(
                    (
                        f"Пароль: {item['old_password']} | "
                        f"Изменён: {item['changed_at']}"
                    )
                )

        close_button = QPushButton(
            "Закрыть"
        )

        close_button.clicked.connect(
            self.accept
        )

        layout.addWidget(title)
        layout.addWidget(history_list)
        layout.addWidget(close_button)

        self.setLayout(layout)