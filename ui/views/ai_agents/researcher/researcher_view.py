import os
from pathlib import Path
from dotenv import load_dotenv, set_key
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout, QComboBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from core.settings.settings import SettingsManager
from core.workers.research_worker import ResearchWorker
from core.workers.api_set_worker import APIWorker
from core.ai_agents.researcher.agent import validate_api_key, run_research

ENV_PATH = Path(".env")

if not ENV_PATH.exists():
    ENV_PATH.touch()
    set_key(ENV_PATH, "OLLAMA_API_KEY", "")
    set_key(ENV_PATH, "OLLAMA_GPT_MODEL", "gpt-oss:20b-cloud")
    set_key(ENV_PATH, "OLLAMA_MINIMAX_MODEL", "minimax-m2.5:cloud")
    
load_dotenv(ENV_PATH)

class ResearcherView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        load_dotenv()
        self.settings = SettingsManager()

        self.setWindowTitle("AI Researcher")
        self.resize(380, 560)

        icon_dir = Path(__file__).resolve().parent.parent.parent.parent / "icons" / "researcher"

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(14)
        self.layout.setContentsMargins(20, 20, 20, 20)

        # Title
        self.title = QLabel("AI Researcher")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addLayout(self.centered(self.title))

        # API Widgets
        self.api_instruction_label = QLabel("Enter your Ollama API Key")
        self.api_instruction_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.api_instruction_label)

        # API Input
        self.api_input = QLineEdit()
        self.api_input.setPlaceholderText("Enter API Key")
        self.api_input.setFixedWidth(200)
        self.api_input.setEchoMode(QLineEdit.Password)
        self.layout.addLayout(self.centered(self.api_input))
        
        # Instruction Label
        self.instruction_label = QLabel(
            '<b>How to get Ollama API Key:</b><br>'
            'Go to: <a href="https://ollama.com/">https://ollama.com/</a><br>'
            'Sign up or Sign in<br>'
            'Next go to Settings &gt; Keys<br>'
            'Click on Add API Key<br>'
            'Write a name<br>'
            'Click on Generate API Key<br>'
            'Copy the API KEY <br>'
            '(The full API Key is visible just once)'
        )
        self.instruction_label.setAlignment(Qt.AlignLeft)
        self.instruction_label.setWordWrap(True)
        self.instruction_label.setAlignment(Qt.AlignCenter)
        self.instruction_label.setTextInteractionFlags(Qt.TextBrowserInteraction)  # فعال کردن تعامل
        self.instruction_label.setOpenExternalLinks(True)  # لینک‌ها مرورگر باز شوند
        self.instruction_label.hide()
        self.layout.addWidget(self.instruction_label)

        # Set API Button 
        choose_icon = QIcon(os.path.join(icon_dir, "api.png"))
        self.set_api_btn = QPushButton("Set API")
        self.set_api_btn.setFixedSize(200, 32)
        self.set_api_btn.setIcon(choose_icon)
        self.set_api_btn.clicked.connect(self.set_api)
        self.layout.addLayout(self.centered(self.set_api_btn))

        # API Status
        self.api_status = QLabel("")
        self.api_status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.api_status)

        # Main Widgets
        self.step_label = QLabel("Write a Topic")
        self.step_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.step_label)
        
        self.topic_input = QLineEdit()
        self.topic_input.setPlaceholderText("Enter Topic")
        self.topic_input.setFixedWidth(200)
        self.topic_input.hide()
        self.layout.addLayout(self.centered(self.topic_input))

        # Language List
        self.language_combo = QComboBox()
        self.language_combo.addItems([
            "English", "Persian", "French",
            "German", "Arabic", "Spanish", "Italian",
            "Turkish"
        ])
        self.language_combo.setFixedWidth(200)
        self.language_combo.hide()
        self.layout.addLayout(self.centered(self.language_combo))

        # Format List
        self.format_combo = QComboBox()
        self.format_combo.addItems(["txt", "md", "docx", "pdf"])
        self.format_combo.setFixedWidth(200)
        self.format_combo.hide()
        self.layout.addLayout(self.centered(self.format_combo))

        # Output Label
        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setWordWrap(True)
        self.output_label.hide()
        self.layout.addWidget(self.output_label)

        # Select Output Button
        choose_icon = QIcon(os.path.join(icon_dir, "output.png"))
        self.select_output_btn = QPushButton("Select Output Folder")
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.select_output_btn.setFixedSize(200, 32)
        self.select_output_btn.setIcon(choose_icon)
        self.select_output_btn.hide()
        self.layout.addLayout(self.centered(self.select_output_btn))

        # Research Button
        choose_icon = QIcon(os.path.join(icon_dir, "research.png"))
        self.research_btn = QPushButton("Start Research")
        self.research_btn.clicked.connect(self.research_action)
        self.research_btn.setFixedSize(200, 32)
        self.research_btn.setIcon(choose_icon)
        self.research_btn.hide()
        self.layout.addLayout(self.centered(self.research_btn))
        
        # Status Label
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        self.layout.addWidget(self.status_label)

        
        # Change Output Button
        choose_icon = QIcon(os.path.join(icon_dir, "change.png"))
        self.change_btn = QPushButton("Change Output Folder")
        self.change_btn.setFixedSize(200, 32)
        self.change_btn.setIcon(choose_icon)
        self.change_btn.clicked.connect(self.select_output_folder)
        self.change_btn.hide()
        self.layout.addLayout(self.centered(self.change_btn))

        # Auto-check API
        self.auto_check_api()

    def centered(self, widget):
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(widget)
        layout.addStretch()
        return layout
        
    # API LOGIC
    def auto_check_api(self):
        api_key = os.getenv("OLLAMA_API_KEY")
        if not api_key:
            self.show_api_screen()  # فقط وقتی اصلاً API نداریم
        else:
            # مسیر خروجی بررسی شود
            output_dir = self.settings.get_path("researcher_directory")
            if not output_dir or not os.path.exists(output_dir):
                # مسیر قبلی وجود ندارد → کاربر باید مسیر را انتخاب کند
                self.show_main_screen(select_output_needed=True)
            else:
                # مسیر موجود است → فقط Change Output فعال باشد
                self.show_main_screen(select_output_needed=False)
    
    def set_api(self):
        api_key = self.api_input.text().strip()
        summarizer = os.getenv("OLLAMA_GPT_MODEL", "")
        translator = os.getenv("OLLAMA_MINIMAX_MODEL", "")

        if not api_key:
            self.api_status.setText("Enter API key ❌")
            return

        # Disable button while checking
        self.set_api_btn.setEnabled(False)
        self.api_status.setText("Checking API... ⏳")

        # Worker
        self.api_worker = APIWorker(api_key, summarizer, translator)
        self.api_worker.finished.connect(self.on_api_checked)
        self.api_worker.error.connect(self.on_api_error)
        self.api_worker.start()

    def on_api_checked(self, is_valid):
        self.set_api_btn.setEnabled(True)
        if is_valid:
            set_key(ENV_PATH, "OLLAMA_API_KEY", self.api_input.text().strip())
            load_dotenv(ENV_PATH, override=True)  # ← این خط باعث می‌شه Worker همان لحظه مقدار درست را ببیند
            
            self.api_status.setText("API Valid ✅")

            # بررسی مسیر خروجی
            output_dir = self.settings.get_path("researcher_directory")
            select_needed = not output_dir or not os.path.exists(output_dir)

            self.show_main_screen(select_output_needed=select_needed)
        else:
            self.api_status.setText("Invalid API ❌")

    def on_api_error(self, error_msg):
        self.set_api_btn.setEnabled(True)
        self.api_status.setText(f"Error ❌: {error_msg}")
    
    # MAIN ACTIONS
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.settings.set_path("researcher_directory", folder)
            self.output_label.setText(f"Output: {folder}")
            self.output_label.show()
            self.select_output_btn.hide()
            self.change_btn.show()

    def research_action(self):
        topic = self.topic_input.text().strip()
        language = self.language_combo.currentText().lower()
        filetype = self.format_combo.currentText().lower()
        output_dir = self.settings.get_path("researcher_directory")
        api_key = os.getenv("OLLAMA_API_KEY")

        if not topic:
            self.status_label.setText("Enter topic ❌")
            return
        if not output_dir:
            self.status_label.setText("Select output folder ❌")
            return

        self.research_btn.setEnabled(False)

        # Worker
        self.worker = ResearchWorker(
            topic=topic,
            api_key=api_key,
            target_language=language,
            output_format=filetype,
            output_dir=output_dir
        )

        # Status مرحله‌ای
        self.worker.progress.connect(lambda msg: self.status_label.setText(msg))
        # وقتی کامل شد
        self.worker.finished.connect(self.on_research_finished)
        # وقتی خطا داشت
        self.worker.error.connect(self.on_research_error)
        # وقتی API مشکل داشت
        self.worker.api_invalid.connect(self.show_api_screen)

        self.worker.start()
        self.research_btn.setEnabled(False)

    def on_research_finished(self, filepath):
        self.status_label.setText(f"✅ Research Saved to: {Path(filepath).name}")
        self.research_btn.setEnabled(True)

    def on_research_error(self, error_msg):
        self.status_label.setText(f"❌ {error_msg}")
        self.research_btn.setEnabled(True)
    
    # ================= UI STATE =================
    def show_api_screen(self):
        self.api_instruction_label.show()
        self.api_input.show()
        self.instruction_label.show()
        self.set_api_btn.show()
        self.api_status.show()

        self.step_label.hide()
        self.topic_input.hide()
        self.language_combo.hide()
        self.format_combo.hide()
        self.output_label.hide()
        self.select_output_btn.hide()
        self.research_btn.hide()
        self.status_label.hide()

    def show_main_screen(self, select_output_needed=True):
        self.api_instruction_label.hide()
        self.api_input.hide()
        self.instruction_label.hide()
        self.set_api_btn.hide()
        self.api_status.hide()

        self.step_label.show()
        self.topic_input.show()
        self.language_combo.show()
        self.format_combo.show()
        self.research_btn.show()
        self.status_label.show()

        if select_output_needed:
            self.output_label.hide()
            self.select_output_btn.show()
            self.change_btn.hide()
        else:
            # مسیر قبلی موجود است
            output_dir = self.settings.get_path("researcher_directory")
            self.output_label.setText(f"Output: {output_dir}")
            self.output_label.show()
            self.select_output_btn.hide()
            self.change_btn.show()