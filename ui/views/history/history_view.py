import sys
import sqlite3
from pathlib import Path
from datetime import datetime

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QScrollArea, QSizePolicy, QFrame,
    QPushButton, QMessageBox, QSpacerItem
)
from PySide6.QtCore import Qt

DB_FILE = Path("history.db")

def human_action(action):
    mapping = {
        "convert": "Convert",
        "organize": "Organization",
        "generate_password": "Password Generate",
        "convert_date": "Date Convert",
        "rotate_pdf": "Rotate",
        "merge_pdfs": "Merge",
        "delete_pages": "Delete Pages",
        "protect": "Protect"
    }
    
    return mapping.get(action, action.capitalize())

class HistoryView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("History")
        self.resize(350, 500)

        # ---------- Main Layout ----------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.layout.setSpacing(10)

        # ---------- Title ----------
        title = QLabel("History")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addWidget(title)

        # ---------- Database ----------
        self.conn = sqlite3.connect(DB_FILE)
        self.create_table()

        # ---------- Scroll Area ----------
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFixedSize(320, 370)  # Fixed size scroll area
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_layout.setSpacing(10)  # فاصله بین کارت‌ها
        self.scroll.setWidget(self.scroll_content)
        self.layout.addWidget(self.scroll)

        # ---------- Delete Button ----------
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.setFixedSize(200, 32)
        self.delete_btn.setEnabled(False)
        self.delete_btn.clicked.connect(self.delete_selected)
        self.layout.addWidget(self.delete_btn, alignment=Qt.AlignCenter)

        # ---------- Selection ----------
        self.selected_card = None
        self.selected_card_id = None
        self.cards = []

        # ---------- Load History ----------
        self.load_history()

    def create_table(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                action TEXT NOT NULL,
                input_file TEXT NOT NULL,
                output_file TEXT NOT NULL,
                format_from TEXT NOT NULL,
                format_to TEXT NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def log_action(self, action, input_file, output_file, format_from, format_to, status="success"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor = self.conn.execute('''
            INSERT INTO history (timestamp, action, input_file, output_file, format_from, format_to, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (timestamp, action, input_file, output_file, format_from, format_to, status))
        self.conn.commit()
        record_id = cursor.lastrowid
        self.add_card(record_id, input_file, action, timestamp, format_from, format_to)

    def get_history(self):
        cursor = self.conn.execute('''
            SELECT id, input_file, action, timestamp, format_from, format_to FROM history ORDER BY id DESC
        ''')
        return cursor.fetchall()

    def load_history(self):
        self.cards.clear()
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for rec in self.get_history():
            self.add_card(*rec)

        self.scroll_layout.addSpacerItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def add_card(self, record_id, input_file, action, timestamp, fmt_from, fmt_to):
        card = QFrame()
        card.setFixedSize(290, 120)  # ارتفاع بلندتر و طول مناسب
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            background-color: #f9f9f9; 
            border-radius: 8px; 
            padding: 8px;
            border: 1px solid #ccc;
        """)
        layout = QVBoxLayout(card)
        layout.setSpacing(10)  # فاصله بیشتر بین label ها
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        # ---------- File Name ----------
        file_label = QLabel(f"📄 {Path(input_file).name}")
        file_label.setWordWrap(True)
        file_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        file_label.setStyleSheet("font-size:12px; font-weight:bold;")
        file_label.setFixedHeight(30)
        layout.addWidget(file_label)

        # ---------- Action ----------
        action_label = QLabel(f"⚡ {human_action(action)} = {fmt_from.upper()} to {fmt_to.upper()}")
        action_label.setWordWrap(True)
        action_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        action_label.setStyleSheet("font-size:10px;")
        action_label.setFixedHeight(30)
        layout.addWidget(action_label)

        # ---------- Timestamp ----------
        time_label = QLabel(f"⏰ {timestamp}")
        time_label.setWordWrap(True)
        time_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        time_label.setStyleSheet("font-size:10px; color: gray;")
        time_label.setFixedHeight(30)
        layout.addWidget(time_label)

        # ---------- Click Selection ----------
        def on_click(event):
            if self.selected_card:
                self.selected_card.setStyleSheet("""
                    background-color: #f9f9f9; 
                    border-radius: 8px; 
                    padding: 8px;
                    border: 1px solid #ccc;
                """)
            self.selected_card = card
            self.selected_card_id = record_id
            card.setStyleSheet("""
                background-color: #a0c4ff;
                border-radius: 8px;
                padding: 8px;
                border: 2px solid #3b82f6;
            """)
            self.delete_btn.setEnabled(True)

        card.mousePressEvent = on_click
        self.scroll_layout.addWidget(card)
        self.cards.append((record_id, card))

    def delete_selected(self):
        if not self.selected_card:
            return
        reply = QMessageBox.question(self, "Confirm Delete", "Are you sure you want to delete this record?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.conn.execute('DELETE FROM history WHERE id=?', (self.selected_card_id,))
            self.conn.commit()
            self.load_history()
            self.selected_card = None
            self.selected_card_id = None
            self.delete_btn.setEnabled(False)
