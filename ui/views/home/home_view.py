from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QFont
from ui.animations.home_animation import HomeAnimation

class HomeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------------- Layout ----------------
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(5)
        self.layout.setAlignment(Qt.AlignCenter)

        # ---------------- Labels ----------------
        self.label1 = QLabel("")
        self.label2 = QLabel("")
        font = QFont("Segoe UI", 24, QFont.Bold)  # فونت، سایز و bold
        for lbl in (self.label1, self.label2):
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setFont(font)
            self.layout.addWidget(lbl)

        # ---------------- Animation ----------------
        # HomeAnimation منطق typewriter و cursor blink را مدیریت می‌کند
        self.animation = HomeAnimation(self)

    # ---------------- Timer برای بخش بعدی ----------------
    def start_next_part_timer(self):
        QTimer.singleShot(500, self.animation.next_part)
