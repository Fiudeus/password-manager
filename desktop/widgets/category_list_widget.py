from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QPushButton,
    QLabel,
    QMenu,
    QInputDialog,
    QListWidgetItem,
)
from PySide6.QtCore import Signal, Qt


class CategoryListWidget(QWidget):

    category_selected = Signal(object)
    create_category_requested = Signal()
    delete_requested = Signal(int)
    rename_requested = Signal(int, str)

    def __init__(self):
        super().__init__()

        self.build_ui()

    def build_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Категории")

        self.category_list = QListWidget()

        self.category_list.currentTextChanged.connect(
            self.on_category_changed
        )

        self.add_button = QPushButton(
            "Создать категорию"
        )

        self.add_button.clicked.connect(
            self.create_category_requested.emit
        )

        self.category_list.setSpacing(4)

        self.category_list.setFocusPolicy(Qt.NoFocus)

        self.category_list.setContextMenuPolicy(
            Qt.CustomContextMenu
        )

        self.category_list.customContextMenuRequested.connect(
            self.open_context_menu
        )

        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        layout.addWidget(title)
        layout.addWidget(self.category_list)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def on_category_changed(self, text):

        if text == "Все пароли":
            self.category_selected.emit(None)

        else:
            self.category_selected.emit(text)

    def load_categories(self, categories):

        self.category_list.clear()

        all_item = QListWidgetItem("Все пароли")
        all_item.setData(Qt.UserRole, None)

        self.category_list.addItem(all_item)

        for category in categories:
            item = QListWidgetItem(category.name)

            item.setData(
                Qt.UserRole,
                category.id
            )

            self.category_list.addItem(item)

    def open_context_menu(self, position):

        item = self.category_list.itemAt(position)

        if not item:
            return

        category_name = item.text()

        if category_name == "Все пароли":
            return

        category_id = item.data(Qt.UserRole)

        menu = QMenu(self)

        rename_action = menu.addAction(
            "Переименовать"
        )

        delete_action = menu.addAction(
            "Удалить"
        )

        action = menu.exec(
            self.category_list.viewport().mapToGlobal(position)
        )

        if action == delete_action:

            self.delete_requested.emit(
                category_id
            )

        elif action == rename_action:

            new_name, ok = QInputDialog.getText(
                self,
                "Переименование",
                "Новое название:",
                text=category_name
            )

            if ok and new_name.strip():
                self.rename_requested.emit(
                    category_id,
                    new_name.strip()
                )