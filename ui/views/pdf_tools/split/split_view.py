import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout, QApplication, QCheckBox
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from core.settings.settings import SettingsManager
from core.pdf_tools.split.split import PDFSplitEngine

class SplitView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = SettingsManager()
        self.file_path = None
        self.engine = PDFSplitEngine()
        
        self.setWindowTitle("Split PDF")
        self.resize(350, 470)
        self.setAcceptDrops(True)
        
        icon_dir = Path(__file__).resolve().parent.parent.parent.parent / "icons" / "split"
        self.icon_dir = icon_dir

        # ---------- Main Layout ----------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(14)
        self.layout.setContentsMargins(20, 15, 20, 20)

        # ---------- Title ----------
        self.title = QLabel("Split PDF")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addLayout(self.centered(self.title))

        # ---------- Step Label ----------
        self.step_label = QLabel("Select a PDF")
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

        # ---------- Pages Input ----------
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Enter pages (e.g., 1,3-5)")
        self.pages_input.setFixedWidth(200)
        self.pages_input.hide()
        self.layout.addLayout(self.centered(self.pages_input))
        
        # ---------- Merge extracted pages into one ----------
        self.merge_checkbox = QCheckBox("Merge extracted pages into one PDF file")
        self.merge_checkbox.setFixedWidth(300)
        self.merge_checkbox.hide()  # قبل از انتخاب فایل مخفی
        self.layout.addLayout(self.centered(self.merge_checkbox))

        # ---------- Output Folder ----------
        choose_icon = QIcon(os.path.join(icon_dir, "output.png"))
        self.select_output_btn = QPushButton("Select Output Folder")
        self.select_output_btn.setFixedSize(200, 32)
        self.select_output_btn.setIcon(choose_icon)
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.select_output_btn.hide()
        self.layout.addLayout(self.centered(self.select_output_btn))

        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setWordWrap(True)
        self.output_label.hide()
        self.layout.addWidget(self.output_label)

        # ---------- Split Button ----------
        choose_icon = QIcon(os.path.join(icon_dir, "split.png"))
        self.split_btn = QPushButton("Split PDF")
        self.split_btn.setFixedSize(200, 32)
        self.split_btn.setIcon(choose_icon)
        self.split_btn.clicked.connect(self.split_action)
        self.split_btn.hide()
        self.layout.addLayout(self.centered(self.split_btn))

        # ---------- Status Label ----------
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        self.layout.addWidget(self.status_label)
        
        # ---------- Change Output Folder ----------
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

    # ---------- Select File ----------
    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(
            self, "Select PDF", "", "PDF Files (*.pdf)"
        )
        if file:
            self.handle_file(file)

    def handle_file(self, file):
        self.file_path = file
        self.selected_label.setText(f"Selected: {os.path.basename(file)}")
        self.selected_label.show()

        self.pages_input.show()
        self.merge_checkbox.show()
        self.split_btn.show()

        stored_path = self.settings.get_path("split_directory")
        if stored_path:
            self.output_label.setText(f"Output: {stored_path}")
            self.output_label.show()
            self.select_output_btn.hide()
            self.change_btn.show()  # نمایش change
        else:
            self.output_label.hide()
            self.select_output_btn.show()
            self.change_btn.hide()

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
            self.settings.set_path("split_directory", folder)
            self.output_label.setText(f"Output: {folder}")
            self.output_label.show()
            self.select_output_btn.hide()
            self.change_btn.show()  # نمایش change بعد از انتخاب

    # ---------- Parse Pages ----------
    def parse_pages(self, text: str):
        pages = set()
        parts = text.split(',')
        for part in parts:
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                try:
                    start, end = int(start), int(end)
                    pages.update(range(start, end + 1))
                except:
                    continue
            else:
                try:
                    pages.add(int(part))
                except:
                    continue
        return sorted(pages)

    # ---------- Generate Unique Filename ----------
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

    # ---------- Split Action ----------
    def split_action(self):
        if not self.file_path:
            self.show_status("Please select a file ❌", error=True)
            return

        folder = self.settings.get_path("split_directory")
        if not folder:
            self.show_status("Please select an output folder ❌", error=True)
            return

        pages_text = self.pages_input.text().strip()
    
        # ---------- همیشه تعریف کن ----------
        pages_to_extract = self.parse_pages(pages_text) if pages_text else []

        self.split_btn.setDisabled(True)
        self.show_status("Splitting PDF...", error=False)
        QApplication.processEvents()

        try:
            if self.merge_checkbox.isChecked():
                # Merge all extracted pages into one PDF
                output_path = self.generate_unique_filename(f"{Path(self.file_path).stem}_extracted", folder)
                self.engine.split_pdf(self.file_path, folder, pages_to_extract, merge_into_one=True)
                output_files = [output_path]  # فقط یک فایل خروجی
            else:
                # Split each page separately
                output_files = self.engine.split_pdf(self.file_path, folder, pages_to_extract)

            # ---------- Convert lists to strings for sqlite ----------
            input_files_str = os.path.basename(self.file_path)
            output_files_str = ', '.join([str(Path(f).name) for f in output_files])

            # ---------- History Logging ----------
            if hasattr(self, "history"):
                self.history.log_action(
                    action="split",
                    input_file=input_files_str,
                    output_file=output_files_str,
                    format_from="PDF",
                    format_to="PDF split",
                    status="success"
                )

            self.show_status("Split successfully ✅")

        except Exception as e:
            self.show_status(f"Error: {e} ❌", error=True)
            if hasattr(self, "history"):
                self.history.log_action(
                    action="split",
                    input_file=os.path.basename(self.file_path),
                    output_file="failed",
                    format_from="PDF",
                    format_to="PDF split",
                    status="failed"
                )

        finally:
            self.split_btn.setDisabled(False)   