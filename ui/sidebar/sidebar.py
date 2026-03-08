# Sidebar
import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from pathlib import Path

from ui.sidebar.sections.tools_section import ToolsSection
from ui.sidebar.sections.games_section import GamesSection
from ui.sidebar.sections.pdf_tools_section import PdfToolsSection
from ui.sidebar.sections.ai_agents_section import AIAgentsSection
from ui.sidebar.sections.history_section import HistorySection

from core.settings.sidebar_connections import SidebarConnections

class Sidebar(QWidget):   
    # --------- History Signal ---------
    history_clicked = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setFixedWidth(180)
        self.setStyleSheet("#Sidebar { background-color: #f2f2f2; }")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 60, 20, 20)
        self.layout.setSpacing(0)
        icon_dir = Path(__file__).resolve().parent.parent / "icons" / "sidebar"
        
        self.tools_section = ToolsSection(self)
        self.games_section = GamesSection(self)
        self.pdf_tools_section = PdfToolsSection(self)
        self.ai_agents_section = AIAgentsSection(self)
        self.history_section = HistorySection(self)
        self.layout.addStretch()  # فقط یکبار، آخر layout
        
        # ================= STATES =================
        self.tools_open = False
        self.games_open = False
        self.pdf_tools_open = False
        self.ai_agents_open = False
        
        SidebarConnections.connect(self)

    def _style_main_btn(self, btn):
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 14px;
                text-align: left;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
                border-radius: 6px;
            }
        """)

    def _style_sub_btn(self, btn):
        btn.setCursor(Qt.PointingHandCursor)
        btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                border: none;
                font-size: 13px;
                text-align: left;
                padding: 4px 6px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
                border-radius: 4px;
            }
        """)
