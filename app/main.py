from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import sys
import os

from app.window import MainWindow


def resource_path(relative_path: str) -> str:
    """Resolve resource path for dev and PyInstaller"""
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)


def main():
    app = QApplication(sys.argv)

    # -------- Application identity (CRITICAL on Windows) --------
    app.setApplicationName("All in One")
    app.setOrganizationName("AllInOneStudio")

    icon_path = resource_path("ui/icons/logo.ico")
    app.setWindowIcon(QIcon(icon_path))
    # ------------------------------------------------------------

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
