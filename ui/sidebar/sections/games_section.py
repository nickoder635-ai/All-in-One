import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QObject, Signal
from pathlib import Path


class GamesSection(QObject):

    tic_tac_toe_clicked = Signal()
    chess_clicked = Signal()

    def __init__(self, parent_sidebar):
        super().__init__(parent_sidebar)

        self.sidebar = parent_sidebar
        self.icon_dir = Path(__file__).resolve().parent.parent.parent / "icons" / "sidebar"

        self._build()
        self._connect()

    def _build(self):
        choose_icon = QIcon(os.path.join(self.icon_dir, "games.png"))
        self.sidebar.games_btn = QPushButton("Games")
        self.sidebar._style_main_btn(self.sidebar.games_btn)
        self.sidebar.games_btn.setIcon(choose_icon)
        self.sidebar.layout.addWidget(self.sidebar.games_btn)

        self.sidebar.games_submenu = QWidget(self.sidebar)
        self.sidebar.games_submenu.setFixedWidth(180)
        self.sidebar.games_submenu.setStyleSheet("background: transparent;")

        self.sidebar.games_sub_layout = QVBoxLayout(self.sidebar.games_submenu)
        self.sidebar.games_sub_layout.setContentsMargins(15, 0, 0, 0)
        self.sidebar.games_sub_layout.setSpacing(0)

        self.sidebar.tic_tac_toe_btn = self._create_btn("tictactoe.png", "Tic Tac Toe")
        self.sidebar.chess_btn = self._create_btn("chess.png", "Chess")

        self.sidebar.games_buttons = [
            self.sidebar.tic_tac_toe_btn,
            self.sidebar.chess_btn,
        ]

        for btn in self.sidebar.games_buttons:
            self.sidebar._style_sub_btn(btn)
            btn.setMaximumHeight(0)
            self.sidebar.games_sub_layout.addWidget(btn)

        self.sidebar.layout.addWidget(self.sidebar.games_submenu)

    def _create_btn(self, icon_name, text):
        icon = QIcon(os.path.join(self.icon_dir, icon_name))
        btn = QPushButton(text)
        btn.setIcon(icon)
        return btn

    def _connect(self):
        self.sidebar.tic_tac_toe_btn.clicked.connect(self.tic_tac_toe_clicked.emit)
        self.sidebar.chess_btn.clicked.connect(self.chess_clicked.emit)