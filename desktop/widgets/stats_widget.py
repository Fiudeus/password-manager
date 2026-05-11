from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFrame
)


class StatsCard(QFrame):

    def __init__(self, title: str, value: str):
        super().__init__()

        self.setObjectName("statsCard")

        layout = QVBoxLayout()

        self.title = QLabel(title)
        self.value = QLabel(value)

        self.title.setObjectName("statsTitle")
        self.value.setObjectName("statsValue")

        layout.addWidget(self.title)
        layout.addWidget(self.value)

        self.setLayout(layout)


class StatsWidget(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.total = StatsCard("Всего паролей", "0")
        self.sites = StatsCard("Уникальные сайты", "0")
        self.updated = StatsCard("Последнее обновление", "-")

        self.categories = StatsCard("Категории", "—")

        layout.addWidget(self.total)
        layout.addWidget(self.sites)
        layout.addWidget(self.updated)
        layout.addWidget(self.categories)

        layout.addStretch()

        self.setLayout(layout)

    def update_stats(self, passwords):

        self.total.value.setText(str(len(passwords)))

        self.sites.value.setText(
            str(len({p["site"] for p in passwords}))
        )

        updates = [p["updated_at"] for p in passwords if p["updated_at"]]

        self.updated.value.setText(
            str(max(updates)) if updates else "-"
        )

        categories = {}

        for p in passwords:
            for c in p["categories"]:
                categories[c] = categories.get(c, 0) + 1

        self.categories.value.setText(
            "\n".join(
                f"{k}: {v}"
                for k, v in categories.items()
            ) or "-"
        )