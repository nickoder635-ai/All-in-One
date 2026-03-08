import os
from pathlib import Path
from tempfile import NamedTemporaryFile
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout, QApplication
)
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt
from core.settings.settings import SettingsManager
from core.pdf_tools.unlock.unlock import unlock_pdf

class UnlockView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = SettingsManager()
        self.file_path = None
        
        self.setWindowTitle("Unlock PDFs")
        self.resize(350, 470)
        self.setAcceptDrops(True)
        
        icon_dir = Path(__file__).resolve().parent.parent.parent.parent / "icons" / "unlock"
        self.icon_dir = icon_dir

        # ---------- Main Layout ------------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(14)
        self.layout.setContentsMargins(20, 15, 20, 20)
        
        # ---------- Title ----------
        self.title = QLabel("Unlock PDFs")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addLayout(self.centered(self.title))

        # ---------- Step Label ----------
        self.step_label = QLabel("Select PDF")
        self.step_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.step_label)

        # ---------- Select File Button ----------
        choose_icon = QIcon(os.path.join(icon_dir, "pdf.png"))
        self.select_btn = QPushButton("Select PDF")
        self.select_btn.setFixedSize(200, 32)
        self.select_btn.setIcon(choose_icon)
        self.select_btn.clicked.connect(self.select_file)
        self.layout.addLayout(self.centered(self.select_btn))

        # ---------- Selected Label ----------
        self.selected_label = QLabel("")
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.selected_label.setWordWrap(True)
        self.selected_label.hide()
        self.layout.addWidget(self.selected_label)

        # ---------- Password Input ----------
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password to Unlock")
        self.password_input.setFixedWidth(200)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.hide()
        self.layout.addLayout(self.centered(self.password_input))
        self.add_password_toggle(self.password_input)

        # ---------- Output Label ----------
        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setWordWrap(True)
        self.output_label.hide()
        self.layout.addWidget(self.output_label)

        # ---------- Select Output Buttons ----------
        choose_icon = QIcon(os.path.join(icon_dir, "output.png"))
        self.select_output_btn = QPushButton("Select Output Folder")
        self.select_output_btn.setFixedSize(200, 32)
        self.select_output_btn.setIcon(choose_icon)
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.select_output_btn.hide()
        self.layout.addLayout(self.centered(self.select_output_btn))

        # ---------- Unlock Button ----------
        choose_icon = QIcon(os.path.join(icon_dir, "unlock.png"))
        self.unlock_btn = QPushButton("Unlock PDF")
        self.unlock_btn.setFixedSize(200, 32)
        self.unlock_btn.setIcon(choose_icon)
        self.unlock_btn.clicked.connect(self.unlock_action)
        self.unlock_btn.hide()
        self.layout.addLayout(self.centered(self.unlock_btn))

        # ---------- Status Label ----------
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        self.layout.addWidget(self.status_label)

        # ---------- Change Output Buttons ----------
        choose_icon = QIcon(os.path.join(icon_dir, "change.png"))
        self.change_btn = QPushButton("Change Output Folder")
        self.change_btn.setFixedSize(200, 32)
        self.change_btn.setIcon(choose_icon)
        self.change_btn.clicked.connect(self.select_output_folder)
        self.change_btn.hide()
        self.layout.addLayout(self.centered(self.change_btn))
        
    # ---------- Center Helper ----------
    def centered(self, widget):
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(widget)
        layout.addStretch(1)
        return layout
    
    # ---------- Eye Section ------------
    def add_password_toggle(self, line_edit):
        eye_open_icon = QIcon(os.path.join(self.icon_dir, "eye_open.png"))
        eye_close_icon = QIcon(os.path.join(self.icon_dir, "eye_close.png"))

        action = QAction(eye_open_icon, "", self)
        action.setCheckable(True)

        def toggle_visibility():
            if action.isChecked():
                line_edit.setEchoMode(QLineEdit.Normal)
                action.setIcon(eye_close_icon)
            else:
                line_edit.setEchoMode(QLineEdit.Password)
                action.setIcon(eye_open_icon)

        action.triggered.connect(toggle_visibility)
        line_edit.addAction(action, QLineEdit.TrailingPosition)
        
    # ---------- Handle File ----------
    def handle_file(self, file):
        try:
            self.file_path = file
        except Exception as e:
            self.show_status(f"Error reading PDF: {e}", error=True)
            return

        # Reset all labels/widgets
        self.password_input.hide()
        self.output_label.hide()
        self.select_output_btn.hide()
        self.change_btn.hide()

        self.selected_label.setText(f"Selected: {os.path.basename(file)}")
        self.selected_label.show()
            
        stored_path = self.settings.get_path("unlock_directory")
        if stored_path:
            self.output_label.setText(f"Output: {stored_path}")
            self.output_label.show()
            self.change_btn.show()
        else:
            self.select_output_btn.show()
            self.change_btn.hide()
            
        self.password_input.show()
        self.unlock_btn.show()
        
        self.step_label.setText("Enter Password")

    # ---------- Select File ----------
    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select PDF", "", "PDF Files (*.pdf)"
        )
        if file:
            self.handle_file(file)

    # ---------- Drag & Drop ----------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".pdf"):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            if file.lower().endswith(".pdf"):
                self.handle_file(file)
                break

    # ---------- Select Output Folder ----------
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.settings.set_path("unlock_directory", folder)
            self.output_label.setText(f"Output: {folder}")
            self.output_label.show()
            self.select_output_btn.hide()
            self.change_btn.show()

    # ---------- Unique Name ----------
    def generate_unique_filename(self, base_name, folder):
        name = f"{base_name}.pdf"
        path = os.path.join(folder, name)
        counter = 1
        while os.path.exists(path):
            name = f"{base_name} ({counter}).pdf"
            path = os.path.join(folder, name)
            counter += 1
        return path
    
    # ---------- Show Status ----------
    def show_status(self, message, error=False):
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color:red;" if error else "color:green;")
        self.status_label.show()
        
    # ---------- Protect Action ----------
    def unlock_action(self):
        if not self.file_path:
            self.show_status("Please select a file ❌", error=True)
            return

        password = self.password_input.text().strip()

        if not password:
            self.show_status("Enter password ⚠️", error=True)
            return

        folder = self.settings.get_path("unlock_directory")
    
        if not folder:
            self.show_status("Please select an output folder first ❌", error=True)
            return

        self.unlock_btn.setDisabled(True)
        self.show_status("Unlocking...", error=False)
        QApplication.processEvents()

        try:
            original_name = Path(self.file_path).stem
            base_name = f"{original_name} unlocked"
            output_path = self.generate_unique_filename(base_name, folder)

            # ---------- Unlock PDF ----------
            unlock_pdf(self.file_path, output_path, password)

            self.show_status("Unlocked successfully ✅")
            self.change_btn.show()

            # ---------- History Logging ----------
            if hasattr(self, "history"):
                self.history.log_action(
                    action="unlock",
                    input_file=os.path.basename(self.file_path) if self.file_path else "None",
                    output_file=output_path,
                    format_from="PDF",
                    format_to="PDF protected",
                    status="success"
                )

        except Exception as e:
            self.show_status(f"Error: {e} ❌", error=True)
            if hasattr(self, "history"):
                self.history.log_action(
                    action="unlock",
                    input_file=os.path.basename(self.file_path) if self.file_path else "None",
                    output_file="failed",
                    format_from="PDF",
                    format_to="PDF protected",
                    status="failed"
                )

        finally:
            self.unlock_btn.setDisabled(False)