import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Signal
from pathlib import Path


class PdfToolsSection(QObject):

    rotate_clicked = Signal()
    delete_pages_clicked = Signal()
    merge_clicked = Signal()
    split_clicked = Signal()
    protect_clicked = Signal()
    unlock_clicked = Signal()

    def __init__(self, parent_sidebar):
        super().__init__(parent_sidebar)
        self.sidebar = parent_sidebar
        self.icon_dir = Path(__file__).resolve().parent.parent.parent / "icons" / "sidebar"

        self._build()
        self._connect()

    def _build(self):
        icon = QIcon(os.path.join(self.icon_dir, "pdf.png"))
        self.sidebar.pdf_tools_btn = QPushButton("PDF Tools")
        self.sidebar._style_main_btn(self.sidebar.pdf_tools_btn)
        self.sidebar.pdf_tools_btn.setIcon(icon)
        self.sidebar.layout.addWidget(self.sidebar.pdf_tools_btn)

        self.sidebar.pdf_tools_submenu = QWidget(self.sidebar)
        self.sidebar.pdf_tools_submenu.setFixedWidth(180)
        self.sidebar.pdf_tools_submenu.setStyleSheet("background: transparent;")

        self.sidebar.pdf_tools_sub_layout = QVBoxLayout(self.sidebar.pdf_tools_submenu)
        self.sidebar.pdf_tools_sub_layout.setContentsMargins(15, 0, 0, 0)
        self.sidebar.pdf_tools_sub_layout.setSpacing(0)

        self.sidebar.rotate_btn = self._create_btn("rotate.png", "Rotate")
        self.sidebar.delete_pages_btn = self._create_btn("delete.png", "Delete Pages")
        self.sidebar.merge_btn = self._create_btn("merge.png", "Merge")
        self.sidebar.split_btn = self._create_btn("split.png", "Split")
        self.sidebar.protect_btn = self._create_btn("protect.png", "Protect")
        self.sidebar.unlock_btn = self._create_btn("unlock.png", "Unlock")

        self.sidebar.pdf_tools_buttons = [
            self.sidebar.rotate_btn,
            self.sidebar.delete_pages_btn,
            self.sidebar.merge_btn,
            self.sidebar.split_btn,
            self.sidebar.protect_btn,
            self.sidebar.unlock_btn,
        ]

        for btn in self.sidebar.pdf_tools_buttons:
            self.sidebar._style_sub_btn(btn)
            btn.setMaximumHeight(0)
            self.sidebar.pdf_tools_sub_layout.addWidget(btn)

        self.sidebar.layout.addWidget(self.sidebar.pdf_tools_submenu)

    def _create_btn(self, icon_name, text):
        icon = QIcon(os.path.join(self.icon_dir, icon_name))
        btn = QPushButton(text)
        btn.setIcon(icon)
        return btn

    def _connect(self):
        self.sidebar.rotate_btn.clicked.connect(self.rotate_clicked.emit)
        self.sidebar.delete_pages_btn.clicked.connect(self.delete_pages_clicked.emit)
        self.sidebar.merge_btn.clicked.connect(self.merge_clicked.emit)
        self.sidebar.split_btn.clicked.connect(self.split_clicked.emit)
        self.sidebar.protect_btn.clicked.connect(self.protect_clicked.emit)
        self.sidebar.unlock_btn.clicked.connect(self.unlock_clicked.emit)