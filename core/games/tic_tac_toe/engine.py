# core/games/tic_tac_toe/engine.py
import random
from enum import Enum

class GameResult(Enum):
    ONGOING = 0
    DRAW = 1
    WIN = 2

class TicTacToeEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[" "]*3 for _ in range(3)]

    def available_moves(self):
        return [(i,j) for i in range(3) for j in range(3) if self.board[i][j]==" "]

    def make_move(self, r, c, s):
        if self.board[r][c]!=" ":
            return False
        self.board[r][c]=s
        return True

    def check_result(self, s):
        b=self.board
        lines = (
            b +
            list(zip(*b)) +
            [[b[i][i] for i in range(3)],
             [b[i][2-i] for i in range(3)]]
        )
        if any(all(cell==s for cell in line) for line in lines):
            return GameResult.WIN
        if not self.available_moves():
            return GameResult.DRAW
        return GameResult.ONGOING

    def ai_move(self, ai, human, level="easy"):
        if level=="easy":
            return random.choice(self.available_moves())
        if level=="medium":
            return self.block_or_win(ai, human)
        if level=="hard":
            return self.minimax_move(ai, human, depth=4)
        return self.minimax_move(ai, human, depth=6)

    def block_or_win(self, ai, human):
        for p in (ai, human):
            for r,c in self.available_moves():
                self.board[r][c]=p
                if self.check_result(p)==GameResult.WIN:
                    self.board[r][c]=" "
                    return (r,c)
                self.board[r][c]=" "
        return random.choice(self.available_moves())

    def minimax_move(self, ai, human, depth):
        def score(turn, d):
            if self.check_result(ai)==GameResult.WIN:
                return 10-d
            if self.check_result(human)==GameResult.WIN:
                return d-10
            if d==0 or not self.available_moves():
                return 0
            scores=[]
            for r,c in self.available_moves():
                self.board[r][c]=turn
                scores.append(score(human if turn==ai else ai, d-1))
                self.board[r][c]=" "
            return max(scores) if turn==ai else min(scores)

        best=-999
        move=None
        for r,c in self.available_moves():
            self.board[r][c]=ai
            s=score(human, depth)
            self.board[r][c]=" "
            if s>best:
                best=s
                move=(r,c)
        return move
