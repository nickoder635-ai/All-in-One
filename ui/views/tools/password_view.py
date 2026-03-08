from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QApplication, QSpinBox, QSlider, QSizePolicy, QFrame
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from core.tools.password.generator import PasswordGenerator
import sys

ICON_DIR = Path(__file__).resolve().parent.parent.parent / "icons"

class PasswordGeneratorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Password Generator")
        self.resize(350, 500)

        # ---------- Main Layout ----------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.layout.setSpacing(12)

        if parent and hasattr(parent, "hamburger") and parent.hamburger:
            self.layout.addSpacing(parent.hamburger.height())
        else:
            self.layout.addSpacing(10)

        # ---------- Title ----------
        title = QLabel("Password Generator")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addWidget(title, alignment=Qt.AlignHCenter)

        # ---------- Password Card ----------
        self.password_card = QFrame()
        self.password_card.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 10px;
                background-color: #f7f7f7;
            }
        """)
        self.password_card.setFixedWidth(300)
        self.password_card.setMinimumHeight(100)
        card_layout = QVBoxLayout(self.password_card)
        card_layout.setContentsMargins(10,10,10,10)
        card_layout.setSpacing(8)

        # Password display
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setAlignment(Qt.AlignCenter)
        self.password_display.setFixedHeight(35)
        self.password_display.setStyleSheet("""
            QLineEdit {
                font-size: 12px;
                border: 1px solid #bbb;
                border-radius: 10px;
                padding: 5px;
                background-color: #fff;
            }
        """)
        self.password_display.addAction(
            QIcon(str(ICON_DIR / "copy.png")),
            QLineEdit.TrailingPosition
        )
        self.password_display.actions()[0].triggered.connect(self.copy_password)
        card_layout.addWidget(self.password_display)

        # Strength label
        self.strength_label = QLabel("Strength: -")
        self.strength_label.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(self.strength_label)

        self.layout.addWidget(self.password_card, alignment=Qt.AlignHCenter)

        # ---------- Length Section ----------
        length_box = QVBoxLayout()
        length_box.setAlignment(Qt.AlignHCenter)
        length_label = QLabel("Length")
        length_label.setAlignment(Qt.AlignCenter)

        slider_row = QHBoxLayout()
        slider_row.setAlignment(Qt.AlignCenter)

        self.length_slider = QSlider(Qt.Horizontal)
        self.length_slider.setRange(1,50)
        self.length_slider.setValue(12)
        self.length_slider.setFixedWidth(200)

        self.length_spin = QSpinBox()
        self.length_spin.setRange(1,50)
        self.length_spin.setValue(12)
        self.length_spin.setAlignment(Qt.AlignCenter)
        self.length_spin.setFixedWidth(60)

        slider_row.addWidget(self.length_slider)
        slider_row.addWidget(self.length_spin)
        length_box.addWidget(length_label)
        length_box.addLayout(slider_row)
        self.layout.addLayout(length_box)

        self.length_slider.valueChanged.connect(self.length_spin.setValue)
        self.length_spin.valueChanged.connect(self.length_slider.setValue)

        # ---------- Options (Toggle Buttons) ----------
        self.lower_btn = QPushButton("a - z")
        self.upper_btn = QPushButton("A - Z")
        self.number_btn = QPushButton("0 - 9")
        self.symbol_btn = QPushButton("#$%")
        self.no_repeat_btn = QPushButton("No Repeat")

        for btn in (self.lower_btn, self.upper_btn, self.number_btn, self.symbol_btn, self.no_repeat_btn):
            btn.setCheckable(True)
            btn.setChecked(True)
            btn.setFixedWidth(80)
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #aaa;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:checked {
                    background-color: #2d5bd4;
                    color: white;
                }
            """)

        options_layout = QVBoxLayout()
        options_layout.setAlignment(Qt.AlignHCenter)

        # Row 1: Uppercase | Lowercase
        row1 = QHBoxLayout()
        row1.addStretch()
        row1.addWidget(self.upper_btn)
        row1.addSpacing(30)
        row1.addWidget(self.lower_btn)
        row1.addStretch()

        # Row 2: Number | Symbol
        row2 = QHBoxLayout()
        row2.addStretch()
        row2.addWidget(self.number_btn)
        row2.addSpacing(30)
        row2.addWidget(self.symbol_btn)
        row2.addStretch()

        # Row 3: No Repeat (وسط)
        row3 = QHBoxLayout()
        row3.addStretch()
        row3.addWidget(self.no_repeat_btn)
        row3.addStretch()

        options_layout.addLayout(row1)
        options_layout.addLayout(row2)
        options_layout.addLayout(row3)
        self.layout.addLayout(options_layout)

        # ---------- Generate ----------
        self.generate_btn = QPushButton("Generate Password")
        self.generate_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.generate_btn.setFixedSize(200, 32)
        self.layout.addWidget(self.generate_btn, alignment=Qt.AlignHCenter)
        self.generate_btn.clicked.connect(self.generate_password)

        # ---------- Signals ----------
        for btn in (self.lower_btn, self.upper_btn, self.number_btn, self.symbol_btn, self.no_repeat_btn):
            btn.toggled.connect(self.update_strength)

        self.length_slider.valueChanged.connect(self.update_strength)
        self.update_strength()

    # ---------- Logic ----------
    def generate_password(self):
        engine = PasswordGenerator(
            lower=self.lower_btn.isChecked(),
            upper=self.upper_btn.isChecked(),
            numbers=self.number_btn.isChecked(),
            symbols=self.symbol_btn.isChecked(),
            no_repeat=self.no_repeat_btn.isChecked()
        )
        pw = engine.generate(self.length_slider.value())
        self.password_display.setText(pw)
        if hasattr(self, "history"):
            self.history.log_action(
                action="generate_password",
                input_file="length=" + str(self.length_slider.value()),
                output_file="generated_password",
                format_from="options",
                format_to="text",
                status="success"
            )
        self.update_strength()

    def update_strength(self):
        length = self.length_slider.value()
        variety = sum([
            self.lower_btn.isChecked(),
            self.upper_btn.isChecked(),
            self.number_btn.isChecked(),
            self.symbol_btn.isChecked()
        ])
        if variety == 0:
            self.generate_btn.setEnabled(False)
            self.strength_label.setText("Strength: -")
            return
        self.generate_btn.setEnabled(True)

        # Strength ranges
        if length <= 5:
            text, color = "Very Weak", "red"
        elif length <= 8:
            text, color = "Weak", "orange"
        elif length <= 10:
            text, color = "Good", "#DAA520"
        elif length <= 14:
            text, color = "Strong", "green"
        else:
            text, color = "Very Strong", "darkgreen"

        self.strength_label.setText(f"Strength: {text}")
        self.strength_label.setStyleSheet(f"color:{color}; font-weight:bold;")

    def copy_password(self):
        if self.password_display.text():
            QApplication.clipboard().setText(self.password_display.text())
            self.strength_label.setText("Copied ✔")
            self.strength_label.setStyleSheet("font-weight:bold;")

# ---------- RUN ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = PasswordGeneratorView()
    w.show()
    sys.exit(app.exec())
