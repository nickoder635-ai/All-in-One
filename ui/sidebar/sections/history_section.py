import os
from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Signal
from pathlib import Path


class HistorySection(QObject):

    history_clicked = Signal()

    def __init__(self, parent_sidebar):
        super().__init__(parent_sidebar)
        self.sidebar = parent_sidebar
        self.icon_dir = Path(__file__).resolve().parent.parent.parent / "icons" / "sidebar"

        self._build()
        self._connect()

    def _build(self):
        icon = QIcon(os.path.join(self.icon_dir, "history.png"))
        self.sidebar.history_btn = QPushButton("History")
        self.sidebar._style_main_btn(self.sidebar.history_btn)
        self.sidebar.history_btn.setIcon(icon)
        self.sidebar.layout.addWidget(self.sidebar.history_btn)

    def _connect(self):
        self.sidebar.history_btn.clicked.connect(
            self.history_clicked.emit
        )