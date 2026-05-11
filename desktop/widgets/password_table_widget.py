from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QHeaderView,
    QFrame,
    QPushButton,
    QHBoxLayout,
    QLabel,
    QMenu,
    QApplication
)

from PySide6.QtCore import Qt, Signal

class PasswordTableWidget(QWidget):

    COL_CREATED = 0
    COL_SITE = 1
    COL_LOGIN = 2
    COL_PASSWORD = 3
    COL_CATEGORIES = 4
    COL_UPDATED = 5
    COL_MENU = 6
    COL_ID = 7

    edit_requested = Signal(int)
    delete_requested = Signal(int)
    history_requested = Signal(int)

    def __init__(self):
        super().__init__()

        self.build_ui()


    def build_ui(self):

        layout = QVBoxLayout()


        self.table = QTableWidget()

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels([
            "Created at",
            "Site",
            "Login",
            "Password",
            "Categories",
            "Updated at",
            "",
            "ID"
        ])

        self.table.setColumnHidden(self.COL_ID, True)

        self.table.setEditTriggers(
            QAbstractItemView.NoEditTriggers
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        self.table.verticalHeader().setVisible(False)

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.table.setFrameShape(QFrame.NoFrame)

        self.table.setFocusPolicy(Qt.NoFocus)

        self.table.cellDoubleClicked.connect(
            self.on_cell_double_clicked
        )

        layout.addWidget(self.table, stretch=1)

        self.setLayout(layout)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            self.COL_SITE,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            self.COL_LOGIN,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            self.COL_PASSWORD,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            self.COL_CATEGORIES,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            self.COL_UPDATED,
            QHeaderView.Stretch
        )

        header.setSectionResizeMode(
            self.COL_MENU,
            QHeaderView.ResizeToContents
        )

        self.table.setShowGrid(False)
        self.table.setAlternatingRowColors(True)

        self.table.setSortingEnabled(True)
        self.table.setSelectionMode(
            QAbstractItemView.SingleSelection
        )
        self.table.horizontalHeader().setSortIndicatorShown(False)
        self.table.horizontalHeader().setSectionsClickable(True)

    def load_data(self, passwords: list[dict]):
        self.table.setSortingEnabled(False)

        self.table.clearContents()

        self.table.setRowCount(len(passwords))

        for row, password_data in enumerate(passwords):

            password_widget = QWidget()

            password_layout = QHBoxLayout()

            password_layout.setContentsMargins(8, 0, 8, 0)
            password_layout.setSpacing(6)

            password_label = QLabel(
                "*" * len(password_data["password"])
            )

            password_label.setProperty(
                "real_password",
                password_data["password"]
            )

            show_button = QPushButton("👁")
            show_button.setFixedWidth(32)

            show_button.clicked.connect(
                lambda checked=False, lbl=password_label:
                self.toggle_password_label(lbl)
            )

            password_layout.addWidget(password_label, 1)
            password_layout.addWidget(show_button, 0)

            password_widget.setLayout(password_layout)

            menu_button = QPushButton("⋮")
            menu_button.setFixedWidth(32)

            menu = QMenu()

            copy_login_action = menu.addAction(
                "Копировать логин"
            )

            copy_password_action = menu.addAction(
                "Копировать пароль"
            )

            menu.addSeparator()

            history_action = menu.addAction(
                "История паролей"
            )

            history_action.triggered.connect(
                lambda checked=False, pid=password_data["id"]:
                self.history_requested.emit(pid)
            )

            menu.addSeparator()

            edit_action = menu.addAction(
                "Редактировать"
            )

            delete_action = menu.addAction(
                "Удалить"
            )

            copy_password_action.triggered.connect(
                lambda checked=False, p=password_data["password"]:
                QApplication.clipboard().setText(p)
            )

            copy_login_action.triggered.connect(
                lambda checked=False, l=password_data["login"]:
                QApplication.clipboard().setText(l)
            )

            edit_action.triggered.connect(
                lambda checked=False, pid=password_data["id"]:
                self.edit_requested.emit(pid)
            )

            delete_action.triggered.connect(
                lambda checked=False, pid=password_data["id"]:
                self.delete_requested.emit(pid)
            )

            menu_button.clicked.connect(
                lambda checked=False, m=menu, b=menu_button:
                m.exec(
                    b.mapToGlobal(
                        b.rect().bottomLeft()
                    )
                )
            )

            show_button.setFixedSize(28, 28)
            menu_button.setFixedSize(28, 28)

            show_button.setFlat(True)
            menu_button.setFlat(True)

            show_button.setCursor(Qt.PointingHandCursor)
            menu_button.setCursor(Qt.PointingHandCursor)

            show_button.setFocusPolicy(Qt.NoFocus)
            menu_button.setFocusPolicy(Qt.NoFocus)

            show_button.setObjectName("iconButton")
            menu_button.setObjectName("iconButton")

            password_layout.setContentsMargins(4, 0, 4, 0)

            self.table.setItem(
                row,
                self.COL_CREATED,
                QTableWidgetItem(
                    password_data["created_at"].strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )
            )

            self.table.setItem(
                row,
                self.COL_SITE,
                QTableWidgetItem(password_data["site"])
            )

            self.table.setItem(
                row,
                self.COL_LOGIN,
                QTableWidgetItem(password_data["login"])
            )

            self.table.setCellWidget(
                row,
                self.COL_PASSWORD,
                password_widget
            )

            self.table.setItem(
                row,
                self.COL_CATEGORIES,
                QTableWidgetItem(
                    ", ".join(password_data["categories"])
                )
            )

            self.table.setItem(
                row,
                self.COL_UPDATED,
                QTableWidgetItem(
                    password_data["updated_at"].strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )
            )

            self.table.setCellWidget(
                row,
                self.COL_MENU,
                menu_button
            )

            self.table.setItem(
                row,
                self.COL_ID,
                QTableWidgetItem(str(password_data["id"]))
            )

        self.table.setSortingEnabled(True)


    def get_selected_password_id(self) -> int | None:

        selected_row = self.table.currentRow()

        if selected_row == -1:
            return None

        password_id_item = self.table.item(
            selected_row,
            self.COL_ID
        )

        if not password_id_item:
            return None

        return int(password_id_item.text())

    def toggle_password_label(self, label):

        real_password = label.property(
            "real_password"
        )

        current = label.text()

        if current.startswith("*"):
            label.setText(real_password)

        else:
            label.setText(
                "*" * len(real_password)
            )

    def on_cell_double_clicked(self, row, column):

        password_id_item = self.table.item(
            row,
            self.COL_ID
        )

        password_id = int(
            password_id_item.text()
        )

        self.edit_requested.emit(password_id)