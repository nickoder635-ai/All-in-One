# file: ui/views/games/chess_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QComboBox, QRadioButton, QButtonGroup,
    QDialog, QMessageBox
)
from PySide6.QtCore import Qt, QTimer
import chess
import random

THEMES = {
    "Classic": {"light":"#f0d9b5", "dark":"#b58863", "highlight":"#90ee90"},
    "Dark": {"light":"#eeeeee", "dark":"#444444", "highlight":"#90ee90"}
}

PLAYER = 0
AI = 1

UNICODE_PIECES = {
    'P':'♙', 'R':'♖', 'N':'♘', 'B':'♗', 'Q':'♕', 'K':'♔',
    'p':'♟', 'r':'♜', 'n':'♞', 'b':'♝', 'q':'♛', 'k':'♚'
}

class ChessView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chess")
        self.resize(350, 500)
        self.board_size = 275
        self.board = chess.Board()
        self.current_theme = "Classic"
        self.buttons = [[None]*8 for _ in range(8)]
        self.selected_square = None
        self.highlighted_squares = []

        # ---------- Main Layout ----------
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(10)

        self.layout.addSpacing(16)  # فاصله بالای title
        self.title = QLabel("Chess")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addWidget(self.title)
        self.layout.addSpacing(16)  # فاصله پایین title

        # ---------- Theme selector ----------
        theme_layout = QHBoxLayout()
        theme_layout.setAlignment(Qt.AlignCenter)
        theme_layout.addWidget(QLabel("Theme:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(THEMES.keys())
        self.theme_combo.setCurrentText(self.current_theme)
        theme_layout.addWidget(self.theme_combo)
        self.layout.addLayout(theme_layout)

        # ---------- Difficulty selector ----------
        diff_layout = QHBoxLayout()
        diff_layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(diff_layout)
        self.level_group = QButtonGroup()
        for lvl in ["easy","medium","hard"]:
            rb = QRadioButton(lvl.capitalize())
            self.level_group.addButton(rb)
            diff_layout.addWidget(rb)
        self.level_group.buttons()[0].setChecked(True)

        # ---------- Board container ----------
        self.board_container = QWidget()
        self.board_container_layout = QVBoxLayout(self.board_container)
        self.board_container_layout.setAlignment(Qt.AlignCenter)
        self.board_container_layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.board_container, stretch=1)

        # ---------- Chess Board ----------
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(0)
        self.grid_layout.setAlignment(Qt.AlignCenter)
        self.board_container_layout.addLayout(self.grid_layout)

        btn_size = self.board_size // 8
        for r in range(8):
            for c in range(8):
                btn = QPushButton(" ")
                btn.setMinimumSize(btn_size, btn_size)
                btn.setMaximumSize(btn_size, btn_size)
                btn.clicked.connect(lambda _, x=r, y=c: self.player_click(x,y))
                self.grid_layout.addWidget(btn,r,c)
                self.buttons[r][c] = btn

        # ---------- Connect Signals ----------
        self.theme_combo.currentTextChanged.connect(lambda t: [self.change_theme(t), self.reset_game()])
        for rb in self.level_group.buttons():
            rb.toggled.connect(self.reset_game)

        # ---------- Initialize Board ----------
        self.update_board()

    # ---------- Helpers ----------
    def square_color(self, r, c):
        if (r,c) in self.highlighted_squares:
            return THEMES[self.current_theme]["highlight"]
        light = THEMES[self.current_theme]["light"]
        dark = THEMES[self.current_theme]["dark"]
        return light if (r+c)%2==0 else dark

    def update_board(self):
        for r in range(8):
            for c in range(8):
                btn = self.buttons[r][c]
                if btn is None:
                    continue
                sq_index = chess.square(c, 7-r)
                piece = self.board.piece_at(sq_index)
                text = UNICODE_PIECES[piece.symbol()] if piece else " "
                btn.setText(text)
                btn.setStyleSheet(
                    f"background-color:{self.square_color(r,c)}; font-size:{self.board_size//8 - 4}px;"
                )
        self.highlighted_squares = []

    def highlight_moves(self, sq_index):
        self.highlighted_squares = []
        for move in self.board.legal_moves:
            if move.from_square == sq_index:
                r = 7 - chess.square_rank(move.to_square)
                c = chess.square_file(move.to_square)
                self.highlighted_squares.append((r,c))
        self.update_board()

    # ---------- Gameplay ----------
    def player_click(self, r, c):
        sq_index = chess.square(c, 7-r)
        piece = self.board.piece_at(sq_index)

        if self.selected_square is None:
            if piece and piece.color == chess.WHITE:
                self.selected_square = sq_index
                self.highlight_moves(sq_index)
        else:
            move = chess.Move(self.selected_square, sq_index)
            if move in self.board.legal_moves:
                if self.board.piece_at(self.selected_square).piece_type == chess.PAWN and chess.square_rank(sq_index) == 7:
                    self.show_pawn_promotion(move)
                else:
                    self.animate_move(move, callback=self.post_player_move)
            self.selected_square = None
            self.highlighted_squares = []
            self.update_board()

    def show_pawn_promotion(self, move):
        dialog = QDialog(self)
        dialog.setModal(True)
        dialog.setWindowFlags(Qt.FramelessWindowHint)
        dialog.setStyleSheet("background-color: rgba(0,0,0,150);")
        dialog.resize(self.board_size, self.board_size)
        layout = QHBoxLayout(dialog)
        layout.setAlignment(Qt.AlignCenter)
        for piece_type, symbol in [(chess.QUEEN,'♕'), (chess.ROOK,'♖'), (chess.BISHOP,'♗'), (chess.KNIGHT,'♘')]:
            btn = QPushButton(symbol)
            btn.setStyleSheet("font-size:32px; background-color:white;")
            btn.clicked.connect(lambda _, pt=piece_type: self.finish_pawn_promotion(move, pt, dialog))
            layout.addWidget(btn)
        dialog.exec()

    def finish_pawn_promotion(self, move, piece_type, dialog):
        move.promotion = piece_type
        dialog.accept()
        self.animate_move(move, callback=self.post_player_move)

    def post_player_move(self):
        if self.board.is_checkmate():
            QMessageBox.information(self, "Game Over", "Checkmate! You win!")
            self.disable_board()
            return
        elif self.board.is_check():
            self.highlight_king(chess.BLACK)
        QTimer.singleShot(300, self.ai_move)

    def highlight_king(self, color):
        for r in range(8):
            for c in range(8):
                sq_idx = chess.square(c, 7-r)
                p = self.board.piece_at(sq_idx)
                if p and p.piece_type == chess.KING and p.color == color:
                    self.buttons[r][c].setStyleSheet(
                        f"background-color:#FF6347; font-size:{self.board_size//8 - 4}px;"
                    )

    def ai_move(self):
        if self.board.is_game_over():
            return
        level = next((b.text().lower() for b in self.level_group.buttons() if b.isChecked()), "easy")
        move = self.get_ai_move(level)
        if move:
            self.animate_move(move, callback=self.post_ai_move)

    def post_ai_move(self):
        if self.board.is_checkmate():
            QMessageBox.information(self, "Game Over", "Checkmate! AI wins!")
            self.disable_board()
            return
        elif self.board.is_check():
            self.highlight_king(chess.WHITE)

    def disable_board(self):
        for row in self.buttons:
            for btn in row:
                if btn:
                    btn.setEnabled(False)

    # ---------- AI ----------
    def get_ai_move(self, level):
        moves = list(self.board.legal_moves)
        if not moves:
            return None
        if level == "easy":
            return random.choice(moves)
        elif level == "medium":
            # ساده‌ترین الگوریتم که چک‌میت را نمی‌گذارد
            for m in moves:
                self.board.push(m)
                if self.board.is_checkmate():
                    self.board.pop()
                    return m
                self.board.pop()
            return random.choice(moves)
        elif level == "hard":
            return self.minimax_move(depth=3)
        return random.choice(moves)

    def minimax_move(self, depth):
        best_score = -float("inf")
        best_move = None
        for move in self.board.legal_moves:
            self.board.push(move)
            score = -self.minimax(depth-1, False)
            self.board.pop()
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, depth, is_maximizing):
        if depth == 0 or self.board.is_game_over():
            return self.evaluate_board()
        max_eval = -float("inf")
        for move in self.board.legal_moves:
            self.board.push(move)
            eval = -self.minimax(depth-1, not is_maximizing)
            self.board.pop()
            max_eval = max(max_eval, eval)
        return max_eval

    def evaluate_board(self):
        piece_values = {chess.PAWN:1, chess.KNIGHT:3, chess.BISHOP:3, chess.ROOK:5, chess.QUEEN:9, chess.KING:1000}
        eval = 0
        for sq in chess.SQUARES:
            piece = self.board.piece_at(sq)
            if piece:
                val = piece_values[piece.piece_type]
                eval += val if piece.color == chess.BLACK else -val
        return eval

    # ---------- Animation ----------
    def animate_move(self, move, callback=None):
        from_square = move.from_square
        to_square = move.to_square
        from_r, from_c = 7 - chess.square_rank(from_square), chess.square_file(from_square)
        to_r, to_c = 7 - chess.square_rank(to_square), chess.square_file(to_square)
        piece = self.board.piece_at(from_square)
        if not piece:
            if callback: callback()
            return
        self.buttons[from_r][from_c].setText(" ")
        QTimer.singleShot(150, lambda: self.finish_move(move, callback))

    def finish_move(self, move, callback=None):
        self.board.push(move)
        self.update_board()
        if callback: callback()

    # ---------- Theme ----------
    def change_theme(self,text):
        self.current_theme = text
        self.update_board()

    # ---------- Reset Game ----------
    def reset_game(self):
        self.board.reset()
        self.selected_square = None
        self.highlighted_squares = []
        self.update_board()