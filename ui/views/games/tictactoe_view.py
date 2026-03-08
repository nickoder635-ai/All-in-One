# file: ui/views/games/tictactoe_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QRadioButton, QButtonGroup
)
from PySide6.QtCore import Qt, QTimer
from core.games.tic_tac_toe.engine import TicTacToeEngine, GameResult
import random

THEMES = {
    "Classic": {"board":"#f0f0f0","X":"#FFD700","O":"#FF6347"},
    "Dark":    {"board":"#2b2b2b","X":"#1E90FF","O":"#FFA500"}
}

PLAYER = 0
AI = 1

class TicTacToeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------- Window ----------
        self.setWindowTitle("Tic Tac Toe")
        self.resize(450, 350)

        # ---------- Engine ----------
        self.engine = TicTacToeEngine()
        self.current_turn = PLAYER
        self.next_start_after_draw = PLAYER
        self.player_symbol = "X"
        self.ai_symbol = "O"
        self.current_theme = "Classic"
        self.buttons = [[None]*3 for _ in range(3)]

        # ---------- Layout اصلی ----------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # وسط چین عرضی + بالای پنجره
        self.layout.setSpacing(12)
        self.layout.setContentsMargins(0,0,0,0)

        # ---------- spacer بالای layout برای hamburger ----------
        if parent and hasattr(parent, "hamburger") and parent.hamburger:
            self.layout.addSpacing(parent.hamburger.height())
        else:
            self.layout.addSpacing(16)

        # ---------- Container داخلی ----------
        self.container = QWidget()
        container_layout = QVBoxLayout(self.container)
        container_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # وسط چین عرضی + بالای container
        container_layout.setSpacing(10)
        container_layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.container)

        # ---------- Title ----------
        self.title = QLabel("Tic Tac Toe")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        container_layout.addWidget(self.title)
        container_layout.addSpacing(10)

        # ---------- Difficulty selector ----------
        diff_layout = QHBoxLayout()
        diff_layout.setAlignment(Qt.AlignCenter)
        container_layout.addLayout(diff_layout)
        self.level_group = QButtonGroup()
        for lvl in ["easy","medium","hard","professional"]:
            rb = QRadioButton(lvl.capitalize())
            rb.toggled.connect(self.prepare_board)
            self.level_group.addButton(rb)
            diff_layout.addWidget(rb)
        self.level_group.buttons()[0].setChecked(True)

        # ---------- Theme selector ----------
        theme_layout = QHBoxLayout()
        theme_layout.setAlignment(Qt.AlignCenter)
        container_layout.addLayout(theme_layout)
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(THEMES.keys())
        self.theme_combo.setCurrentText(self.current_theme)
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        theme_layout.addWidget(self.theme_combo)

        # ---------- Board ----------
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.grid_layout.setAlignment(Qt.AlignCenter)
        container_layout.addLayout(self.grid_layout)

        btn_size = 70
        for r in range(3):
            for c in range(3):
                btn = QPushButton(" ")
                btn.setMinimumSize(btn_size, btn_size)
                btn.setMaximumSize(btn_size, btn_size)
                btn.clicked.connect(lambda _, x=r, y=c: self.player_move(x,y))
                self.grid_layout.addWidget(btn,r,c)
                self.buttons[r][c] = btn

        # ---------- Symbol selection ----------
        sym_layout = QHBoxLayout()
        sym_layout.setAlignment(Qt.AlignCenter)
        container_layout.addLayout(sym_layout)
        sym_layout.addWidget(QLabel("Symbol:"))
        btn_x = QPushButton("X")
        btn_x.clicked.connect(lambda: self.choose_symbol("X"))
        btn_o = QPushButton("O")
        btn_o.clicked.connect(lambda: self.choose_symbol("O"))
        sym_layout.addWidget(btn_x)
        sym_layout.addWidget(btn_o)

        # ---------- Prepare board ----------
        self.prepare_board()

        # Store container_layout for later
        self.container_layout = container_layout

    # ---------- Helper ----------
    def get_button_style(self, symbol=" ", empty=False):
        if empty or symbol==" ":
            color = THEMES[self.current_theme]["board"]
        else:
            color = THEMES[self.current_theme][symbol]
        return f"background-color:{color}; font-size:18px; font-weight:bold;"

    # ---------- Gameplay ----------
    def choose_symbol(self,s):
        self.player_symbol = s
        self.ai_symbol = "O" if s=="X" else "X"
        self.prepare_board()

    def prepare_board(self):
        self.engine.reset()
        for i in range(3):
            for j in range(3):
                btn = self.buttons[i][j]
                if btn:
                    btn.setText(" ")
                    btn.setStyleSheet(self.get_button_style(empty=True))
                    btn.setEnabled(True)
        self.current_turn = PLAYER if self.next_start_after_draw==PLAYER else AI
        if self.current_turn == AI:
            delay = random.randint(100,200)
            QTimer.singleShot(delay, self.ai_move)

    def change_theme(self,text):
        self.current_theme = text
        self.update_board_colors()

    def update_board_colors(self):
        for r in range(3):
            for c in range(3):
                sym = self.engine.board[r][c]
                btn = self.buttons[r][c]
                if btn:
                    empty = sym==" "
                    btn.setStyleSheet(self.get_button_style(sym, empty))

    def player_move(self,r,c):
        if self.engine.board[r][c]!=" " or self.current_turn!=PLAYER:
            return
        self.engine.make_move(r,c,self.player_symbol)
        self.update_button(r,c,self.player_symbol)
        if self.check_end(self.player_symbol): return
        self.current_turn = AI
        delay = random.randint(100,200)
        QTimer.singleShot(delay, self.ai_move)

    def ai_move(self):
        if not self.engine.available_moves(): return
        level = next((b.text().lower() for b in self.level_group.buttons() if b.isChecked()), "easy")
        move = self.engine.ai_move(self.ai_symbol, self.player_symbol, level)
        if not move: return
        r,c = move
        self.engine.make_move(r,c,self.ai_symbol)
        self.update_button(r,c,self.ai_symbol)
        if self.check_end(self.ai_symbol): return
        self.current_turn = PLAYER

    def update_button(self,r,c,symbol):
        btn = self.buttons[r][c]
        if btn:
            btn.setText(symbol)
            btn.setStyleSheet(self.get_button_style(symbol))

    def check_end(self,symbol):
        result = self.engine.check_result(symbol)
        if result in [GameResult.WIN, GameResult.DRAW]:
            for i in range(3):
                for j in range(3):
                    btn = self.buttons[i][j]
                    if btn:
                        btn.setEnabled(False)
            if result == GameResult.WIN:
                color = "#90EE90" if symbol==self.player_symbol else "#FF6347"
                for i in range(3):
                    for j in range(3):
                        if self.engine.board[i][j]!=" ":
                            self.buttons[i][j].setStyleSheet(f"background-color:{color}; font-size:18px; font-weight:bold;")
            elif result == GameResult.DRAW:
                for i in range(3):
                    for j in range(3):
                        if self.engine.board[i][j]!=" ":
                            self.buttons[i][j].setStyleSheet("background-color:#FFFF99; font-size:18px; font-weight:bold;")
            self.next_start_after_draw = PLAYER if symbol==self.player_symbol else AI
            QTimer.singleShot(600, self.prepare_board)
            return True
        return False
