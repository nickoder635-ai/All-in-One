import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Signal
from pathlib import Path


class AIAgentsSection(QObject):

    researcher_clicked = Signal()

    def __init__(self, parent_sidebar):
        super().__init__(parent_sidebar)

        self.sidebar = parent_sidebar
        self.icon_dir = Path(__file__).resolve().parent.parent.parent / "icons" / "sidebar"

        self._build()
        self._connect()

    def _build(self):
        choose_icon = QIcon(os.path.join(self.icon_dir, "agents.png"))
        self.sidebar.ai_agents_btn = QPushButton("AI agents")
        self.sidebar._style_main_btn(self.sidebar.ai_agents_btn)
        self.sidebar.ai_agents_btn.setIcon(choose_icon)
        self.sidebar.layout.addWidget(self.sidebar.ai_agents_btn)

        self.sidebar.ai_agents_submenu = QWidget(self.sidebar)
        self.sidebar.ai_agents_submenu.setFixedWidth(180)
        self.sidebar.ai_agents_submenu.setStyleSheet("background: transparent;")

        self.sidebar.ai_agents_sub_layout = QVBoxLayout(self.sidebar.ai_agents_submenu)
        self.sidebar.ai_agents_sub_layout.setContentsMargins(15, 0, 0, 0)
        self.sidebar.ai_agents_sub_layout.setSpacing(0)

        self.sidebar.researcher_btn = self._create_btn("research.png", "Researcher")

        self.sidebar.ai_agents_buttons = [
            self.sidebar.researcher_btn,
        ]

        for btn in self.sidebar.ai_agents_buttons:
            self.sidebar._style_sub_btn(btn)
            btn.setMaximumHeight(0)
            self.sidebar.ai_agents_sub_layout.addWidget(btn)

        self.sidebar.layout.addWidget(self.sidebar.ai_agents_submenu)

    def _create_btn(self, icon_name, text):
        icon = QIcon(os.path.join(self.icon_dir, icon_name))
        btn = QPushButton(text)
        btn.setIcon(icon)
        return btn

    def _connect(self):
        self.sidebar.researcher_btn.clicked.connect(self.researcher_clicked.emit)