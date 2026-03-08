import os
from PySide6.QtWidgets import QMainWindow, QWidget, QPushButton
from PySide6.QtCore import Qt, QPropertyAnimation, QPoint, QAbstractAnimation
from PySide6.QtGui import QIcon, QPixmap

from ui.views.home.home_view import HomeView

from ui.sidebar.sidebar import Sidebar

from ui.animations.sidebar_animation import SidebarAnimation

from ui.footer.footer import Footer

from ui.views.tools.converter.converter_view import ConverterView
from ui.views.tools.organizer_view import FileOrganizerView
from ui.views.tools.password_view import PasswordGeneratorView
from ui.views.tools.date_converter_view import DateConverterView

from ui.views.games.tictactoe_view import TicTacToeView
from ui.views.games.chess_view import ChessView

from ui.views.pdf_tools.rotate.rotate_view import RotateView
from ui.views.pdf_tools.delete_pages.delete_pages_view import DeletePagesView
from ui.views.pdf_tools.merge.merge_view import MergeView
from ui.views.pdf_tools.split.split_view import SplitView
from ui.views.pdf_tools.protect.protect_view import ProtectView
from ui.views.pdf_tools.unlock.unlock_view import UnlockView

from ui.views.ai_agents.researcher.researcher_view import ResearcherView

from ui.views.history.history_view import HistoryView

from core.settings.signals import AppSignals

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "ui/icons/logo.ico")
        )
        
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("All in One")
        self.resize(350, 500)
        self.setMinimumSize(350, 500)
        self.sidebar_width = 180
        self.sidebar_open = False

        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        # ---------------- Hamburger ----------------
        self.hamburger = QPushButton("☰", self.central)
        self.hamburger.setFixedSize(40, 40)
        self.hamburger.move(10, 10)
        self.hamburger.clicked.connect(self.toggle_sidebar)
        self.hamburger.setStyleSheet("""
            QPushButton {
                font-size: 20px;
                border: none;
                background: transparent;
            }
            QPushButton:hover {
                background: #eaeaea;
                border-radius: 6px;
            }
        """)

        # ---------------- Sidebar ----------------
        self.sidebar = Sidebar(self.central)
        self.signals = AppSignals()
        self.signals.connect_sidebar(self.sidebar, self.show_view_by_key)
        self.sidebar.move(-self.sidebar_width, 0)
        self.sidebar_anim = SidebarAnimation(self.sidebar)
        
        # ---------------- Footer ----------------
        self.footer = Footer(self.central)
        self.footer.lower()

        # ---------------- Separator ----------------
        self.separator = QWidget(self.central)
        self.separator.setStyleSheet("background-color: #cccccc;")

        # ---------------- Sidebar animation ----------------
        self.anim = QPropertyAnimation(self.sidebar, b"pos", self)
        self.anim.setDuration(250)
        self.anim.valueChanged.connect(self.on_anim_value_changed)

        # ---------------- Content Container ----------------
        self.view_container = QWidget(self.central)
        self.content = HomeView(self.view_container)

        self.update_layout()
        
        # ---------------- History ---------------------------
        self.history_view = HistoryView()

    # ---------------- Sidebar toggle ----------------
    def toggle_sidebar(self):
        if self.anim.state() == QAbstractAnimation.Running:
            self.anim.stop()

        end_pos = QPoint(0, 0) if not self.sidebar_open else QPoint(-self.sidebar_width, 0)
        self.anim.setStartValue(self.sidebar.pos())
        self.anim.setEndValue(end_pos)
        self.anim.start()

        self.sidebar_open = not self.sidebar_open
        self.footer.lower()

    def on_anim_value_changed(self, value):
        self.separator.setGeometry(
            value.x() + self.sidebar_width,
            0,
            1,
            self.height()
        )

    # ---------------- Show any view ----------------
    def show_view(self, view_class):
        if self.sidebar_open:
            self.toggle_sidebar()

        if self.content:
            if isinstance(self.content, HistoryView):
                self.content.hide()
            else:
                self.content.deleteLater()
            self.content = None

        if view_class == ConverterView:
            self.content = ConverterView(self.view_container)
            self.content.history = self.history_view

        elif view_class == FileOrganizerView:
            self.content = FileOrganizerView(self.view_container)
            self.content.history = self.history_view

        elif view_class == PasswordGeneratorView:
            self.content = PasswordGeneratorView(self.view_container)
            self.content.history = self.history_view
            
        elif view_class == DateConverterView:
            self.content = DateConverterView(self.view_container)
            self.content.history = self.history_view

        elif view_class == RotateView:
            self.content = RotateView(self.view_container)
            self.content.history = self.history_view
        
        elif view_class == DeletePagesView:
            self.content = DeletePagesView(self.view_container)
            self.content.history = self.history_view
        
        elif view_class == MergeView:
            self.content = MergeView(self.view_container)
            self.content.history = self.history_view
            
        elif view_class == SplitView:
            self.content = SplitView(self.view_container)
            self.content.history = self.history_view
        
        elif view_class == ProtectView:
            self.content = ProtectView(self.view_container)
            self.content.history = self.history_view
            
        elif view_class == UnlockView:
            self.content = UnlockView(self.view_container)
            self.content.history = self.history_view
            
        elif view_class == HistoryView:
            self.content = self.history_view
            self.content.setParent(self.view_container)

        else:
            self.content = view_class(self.view_container)

        self.content.setGeometry(
            0, 0,
            self.view_container.width(),
            self.view_container.height()
        )
        self.content.show()
        
    def show_view_by_key(self, key):
        mapping = {
            "converter": ConverterView,
            "organizer": FileOrganizerView,
            "password": PasswordGeneratorView,
            "date": DateConverterView,
            "tictactoe": TicTacToeView,
            "chess": ChessView,
            "rotate": RotateView,
            "delete_pages": DeletePagesView,
            "merge": MergeView,
            "split": SplitView,
            "protect": ProtectView,
            "unlock": UnlockView,
            "researcher": ResearcherView,
            "history": HistoryView,
        }

        view_class = mapping.get(key)
        if view_class:
            self.show_view(view_class)
        
    # ---------------- Layout / Resize ----------------
    def update_layout(self):
        w = self.width()
        h = self.height()

        top_offset = 0
        bottom_offset = self.footer.height()

        self.view_container.setGeometry(0, top_offset, w, h - top_offset - bottom_offset)
        if self.content:
            self.content.setGeometry(0, 0, self.view_container.width(), self.view_container.height())

        self.sidebar.setGeometry(self.sidebar.pos().x(), 0, self.sidebar_width, h)
        self.separator.setGeometry(self.sidebar.pos().x() + self.sidebar_width, 0, 1, h)
        self.footer.update_position()

    # ---------------- ShowEvent ----------------
    def showEvent(self, event):
        super().showEvent(event)
        self.sidebar.raise_()
        self.separator.raise_()
        self.hamburger.raise_()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_layout()
