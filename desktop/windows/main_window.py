from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFrame,
    QMessageBox,
    QLineEdit,
)
from desktop.widgets.password_table_widget import PasswordTableWidget
from desktop.widgets.category_list_widget import CategoryListWidget
from desktop.widgets.stats_widget import StatsWidget
from desktop.dialogs.add_password_dialog import AddPasswordDialog
from desktop.dialogs.edit_password_dialog import EditPasswordDialog
from desktop.dialogs.create_category_dialog import CreateCategoryDialog
from desktop.dialogs.password_history_dialog import PasswordHistoryDialog
from core.services import password_service, category_service


class MainWindow(QMainWindow):

    def __init__(self, session, user, key):
        super().__init__()

        self.session = session
        self.user = user
        self.key = key

        self.search_query = ""
        self.current_category = None

        self.setWindowTitle("Password Manager")
        self.resize(1200, 700)

        self.build_ui()

    def build_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(central_widget)

        # Главный horizontal layout
        main_layout = QHBoxLayout()

        # ===== LEFT SIDEBAR =====

        self.category_widget = CategoryListWidget()

        self.category_widget.create_category_requested.connect(
            self.open_create_category_dialog
        )

        self.category_widget.delete_requested.connect(
            self.delete_category
        )

        self.category_widget.rename_requested.connect(
            self.rename_category
        )

        # ===== CENTER CONTENT =====

        center_widget = QFrame()

        center_layout = QVBoxLayout()

        top_bar = QHBoxLayout()

        title = QLabel("Пароли")

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Поиск по сайту или логину"
        )

        self.search_input.textChanged.connect(
            self.on_search_changed
        )

        delete_password_btn = QPushButton("Удалить")

        delete_password_btn.clicked.connect(
            self.on_delete_password_clicked
        )

        add_password_btn = QPushButton("Добавить пароль")

        add_password_btn.clicked.connect(
            self.open_add_password_dialog
        )

        add_password_btn.setObjectName(
            "primaryButton"
        )

        top_bar.addWidget(title)

        top_bar.addStretch()

        top_bar.addWidget(self.search_input)
        top_bar.addWidget(delete_password_btn)
        top_bar.addWidget(add_password_btn)

        self.password_table = PasswordTableWidget()

        center_layout.addLayout(top_bar)
        center_layout.addWidget(self.password_table, stretch=1)

        center_widget.setLayout(center_layout)

        self.password_table.delete_requested.connect(
            self.delete_password_by_id
        )

        # ===== RIGHT STATS PANEL =====

        self.stats_widget = StatsWidget()

        # ===== ADD TO MAIN LAYOUT =====

        main_layout.addWidget(self.category_widget, 1)
        main_layout.addWidget(center_widget, 4)
        main_layout.addWidget(self.stats_widget, 1)

        central_widget.setLayout(main_layout)

        self.category_widget.category_selected.connect(
            self.on_category_selected
        )

        self.load_categories()
        self.load_passwords()

        self.password_table.edit_requested.connect(
            self.open_edit_dialog
        )

        self.password_table.history_requested.connect(
            self.open_password_history
        )

    def load_passwords(self):

        passwords = password_service.get_passwords(
            self.session,
            self.user.id,
            self.key
        )

        if self.search_query:
            query = self.search_query.lower()

            passwords = [
                p for p in passwords
                if (
                        query in p["site"].lower()
                        or
                        query in p["login"].lower()
                )
            ]

        if self.current_category:
            passwords = [
                p for p in passwords
                if self.current_category in p["categories"]
            ]

        self.password_table.load_data(passwords)
        self.stats_widget.update_stats(passwords)

    def open_add_password_dialog(self):
        dialog = AddPasswordDialog(
            self.session,
            self.user,
            self.key
        )

        result = dialog.exec()

        if result:
            self.load_passwords()

    def open_edit_dialog(self, password_id):

        password_obj = (
            password_service
            .get_password_by_id(
                self.session,
                password_id
            )
        )

        if not password_obj:
            return

        dialog = EditPasswordDialog(
            self.session,
            password_obj,
            self.key
        )

        result = dialog.exec()

        if result:
            self.load_passwords()

    def on_delete_password_clicked(self):

        password_id = self.password_table.get_selected_password_id()

        if password_id is None:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Выберите пароль"
            )

            return

        reply = QMessageBox.question(
            self,
            "Удаление",
            "Удалить пароль?"
        )

        if reply != QMessageBox.Yes:
            return

        try:

            password_service.delete_password_by_id(
                self.session,
                password_id
            )

            self.session.commit()

            self.load_passwords()

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

    def delete_password_by_id(self, password_id):

        reply = QMessageBox.question(
            self,
            "Удаление",
            "Удалить пароль?"
        )

        if reply != QMessageBox.Yes:
            return

        try:

            password_service.delete_password_by_id(
                self.session,
                password_id
            )

            self.session.commit()

            self.load_passwords()

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

    def on_search_changed(self, text):

        self.search_query = text

        self.load_passwords()

    def on_category_selected(self, category_name):

        self.current_category = category_name

        self.load_passwords()

    def open_create_category_dialog(self):

        dialog = CreateCategoryDialog(
            self.session
        )

        result = dialog.exec()

        if result:
            self.load_categories()

    def load_categories(self):

        categories = category_service.get_all_categories(
            self.session
        )

        self.category_widget.load_categories(
            categories
        )

    def delete_category(self, category_name):

        reply = QMessageBox.question(
            self,
            "Удаление категории",
            f"Удалить категорию '{category_name}'?"
        )

        if reply != QMessageBox.Yes:
            return

        try:

            category_service.delete_category(
                self.session,
                category_name
            )

            self.session.commit()

            self.load_categories()
            self.load_passwords()

        except Exception as e:

            self.session.rollback()

            QMessageBox.critical(
                self,
                "Ошибка",
                str(e)
            )

    def rename_category(self, old_name, new_name):

        try:

            category_service.rename_category(
                self.session,
                old_name,
                new_name
            )

            self.session.commit()

            self.load_categories()
            self.load_passwords()

        except ValueError as e:

            self.session.rollback()

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

    def open_password_history(self, password_id):

        password_data = password_service.get_password(
            self.session,
            password_id,
            self.key
        )

        if not password_data:
            return

        dialog = PasswordHistoryDialog(
            password_data["history"],
            password_data["site"]
        )

        dialog.exec()