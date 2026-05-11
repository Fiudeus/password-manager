import sys
from PySide6.QtWidgets import QApplication
from desktop.windows.login_window import LoginWindow
from core.database import SessionLocal, Base, engine


Base.metadata.create_all(engine)

session = SessionLocal()

app = QApplication(sys.argv)

window = LoginWindow(session)

with open(
    "desktop/styles/app.qss",
    "r"
) as file:

    app.setStyleSheet(
        file.read()
    )

window.show()

sys.exit(app.exec())
