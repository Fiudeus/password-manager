import sys
from pathlib import Path
from PySide6.QtWidgets import QApplication
from desktop.windows.login_window import LoginWindow
from core.database import SessionLocal, Base, engine


Base.metadata.create_all(engine)

session = SessionLocal()

app = QApplication(sys.argv)
window = LoginWindow(session)

BASE_DIR = Path(__file__).resolve().parent
style_path = BASE_DIR / "desktop" / "styles" / "app.qss"

with open(style_path, "r") as file:
    app.setStyleSheet(
        file.read()
    )

window.show()

sys.exit(app.exec())
