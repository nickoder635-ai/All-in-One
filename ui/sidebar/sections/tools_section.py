import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Signal
from pathlib import Path


class ToolsSection(QObject):

    converter_clicked = Signal()
    file_organizer_clicked = Signal()
    password_generator_clicked = Signal()
    date_converter_clicked = Signal()

    def __init__(self, parent_sidebar):
        super().__init__(parent_sidebar)

        self.sidebar = parent_sidebar
        self.icon_dir = Path(__file__).resolve().parent.parent.parent / "icons" / "sidebar"

        self._build()
        self._connect()

    def _build(self):
        choose_icon = QIcon(os.path.join(self.icon_dir, "tools.png"))
        self.sidebar.tools_btn = QPushButton("Tools")
        self.sidebar._style_main_btn(self.sidebar.tools_btn)
        self.sidebar.tools_btn.setIcon(choose_icon)
        self.sidebar.layout.addWidget(self.sidebar.tools_btn)

        self.sidebar.tools_submenu = QWidget(self.sidebar)
        self.sidebar.tools_submenu.setFixedWidth(180)
        self.sidebar.tools_submenu.setStyleSheet("background: transparent;")

        self.sidebar.tools_sub_layout = QVBoxLayout(self.sidebar.tools_submenu)
        self.sidebar.tools_sub_layout.setContentsMargins(15, 0, 0, 0)
        self.sidebar.tools_sub_layout.setSpacing(0)

        self.sidebar.converter_btn = self._create_btn("converter.png", "Converter")
        self.sidebar.file_organizer_btn = self._create_btn("organize.png", "File Organizer")
        self.sidebar.password_generator_btn = self._create_btn("passgen.png", "Password Generator")
        self.sidebar.date_converter_btn = self._create_btn("date.png", "Date Converter")

        self.sidebar.tools_buttons = [
            self.sidebar.converter_btn,
            self.sidebar.file_organizer_btn,
            self.sidebar.password_generator_btn,
            self.sidebar.date_converter_btn,
        ]

        for btn in self.sidebar.tools_buttons:
            self.sidebar._style_sub_btn(btn)
            btn.setMaximumHeight(0)
            self.sidebar.tools_sub_layout.addWidget(btn)

        self.sidebar.layout.addWidget(self.sidebar.tools_submenu)

    def _create_btn(self, icon_name, text):
        icon = QIcon(os.path.join(self.icon_dir, icon_name))
        btn = QPushButton(text)
        btn.setIcon(icon)
        return btn

    def _connect(self):
        self.sidebar.converter_btn.clicked.connect(self.converter_clicked.emit)
        self.sidebar.file_organizer_btn.clicked.connect(self.file_organizer_clicked.emit)
        self.sidebar.password_generator_btn.clicked.connect(self.password_generator_clicked.emit)
        self.sidebar.date_converter_btn.clicked.connect(self.date_converter_clicked.emit)