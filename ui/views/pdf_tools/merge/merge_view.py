import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QLineEdit, QHBoxLayout, QApplication, QListWidget, QListWidgetItem
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QTimer
from core.settings.settings import SettingsManager
from core.pdf_tools.merge.merge import PDFMergerEngine

class MergeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = SettingsManager()
        self.files = []
        self.engine = PDFMergerEngine()
        
        self.setWindowTitle("Merge PDFs")
        self.resize(350, 470)
        self.setAcceptDrops(True)
        
        icon_dir = Path(__file__).resolve().parent.parent.parent.parent / "icons" / "merge"
        self.icon_dir = icon_dir

        # ---------- Main Layout ----------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(14)
        self.layout.setContentsMargins(20, 15, 20, 20)

        # ---------- Title ----------
        self.title = QLabel("Merge PDFs")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addLayout(self.centered(self.title))

        # ---------- Step Label ----------
        self.step_label = QLabel("Select PDF files")
        self.step_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.step_label)

        # ---------- Select Files Button ----------
        choose_icon = QIcon(os.path.join(icon_dir, "pdf.png"))
        self.select_btn = QPushButton("Select PDFs")
        self.select_btn.setFixedSize(200, 32)
        self.select_btn.setIcon(choose_icon)
        self.select_btn.clicked.connect(self.select_files)
        self.layout.addLayout(self.centered(self.select_btn))

        # ---------- List of Selected Files ----------
        self.file_list_widget = QListWidget()
        self.file_list_widget.hide()
        self.layout.addWidget(self.file_list_widget)
        
        # ---------- Reorder Buttons ----------
        self.up_btn = QPushButton("↑")
        self.up_btn.setFixedSize(32, 32)
        self.up_btn.clicked.connect(lambda: self.move_item(-1))

        self.down_btn = QPushButton("↓")
        self.down_btn.setFixedSize(32, 32)
        self.down_btn.clicked.connect(lambda: self.move_item(1))

        btn_layout = QHBoxLayout()
        btn_layout.addStretch(1)
        btn_layout.addWidget(self.up_btn)
        btn_layout.addWidget(self.down_btn)
        btn_layout.addStretch(1)
        self.layout.addLayout(btn_layout)
        
        # ---------- Hide reorder buttons initially ----------
        self.up_btn.hide()
        self.down_btn.hide()

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

        # ---------- Merge Button ----------
        choose_icon = QIcon(os.path.join(icon_dir, "merge.png"))
        self.merge_btn = QPushButton("Merge PDFs")
        self.merge_btn.setFixedSize(200, 32)
        self.merge_btn.setIcon(choose_icon)
        self.merge_btn.clicked.connect(self.merge_action)
        self.merge_btn.hide()
        self.layout.addLayout(self.centered(self.merge_btn))

        # ---------- Status Label ----------
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()
        self.layout.addWidget(self.status_label)

    # ---------- Center Helper ----------
    def centered(self, widget):
        layout = QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(widget)
        layout.addStretch(1)
        return layout

    # ---------- Select Multiple Files ----------
    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDFs", "", "PDF Files (*.pdf)"
        )
        if files:
            self.handle_files(files)

    # ---------- Handle Selected Files ----------
    def handle_files(self, files: list[str]):
        self.files = files
        self.file_list_widget.clear()
        for f in files:
            item = QListWidgetItem(os.path.basename(f))
            self.file_list_widget.addItem(item)
        self.file_list_widget.show()
        self.up_btn.show()
        self.down_btn.show()
        self.step_label.setText(f"{len(files)} file(s) selected")
        self.merge_btn.show()

        stored_path = self.settings.get_path("merge_directory")
        if stored_path:
            self.output_label.setText(f"Output: {stored_path}")
            self.output_label.show()
            self.select_output_btn.hide()  # مسیر خروجی هست => دیگه نیازی به انتخاب نیست
            # Change button میاد زیر label
            if not hasattr(self, "change_btn"):
                choose_icon = QIcon(os.path.join(self.icon_dir, "change.png"))
                self.change_btn = QPushButton("Change Output Folder")
                self.change_btn.setFixedSize(200, 32)
                self.change_btn.setIcon(choose_icon)
                self.change_btn.clicked.connect(self.select_output_folder)
                self.layout.addLayout(self.centered(self.change_btn))
            self.change_btn.show()
        else:
            self.output_label.hide()
            self.select_output_btn.show()
            if hasattr(self, "change_btn"):
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
        files = []
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            if file.lower().endswith(".pdf"):
                files.append(file)
        if files:
            self.handle_files(files)

    # ---------- Select Output Folder ----------
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.settings.set_path("merge_directory", folder)
            self.output_label.setText(f"Output: {folder}")
            self.output_label.show()

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
        
    # ---------- Up/Down ---------------   
    def move_item(self, direction):
        current_row = self.file_list_widget.currentRow()
        if current_row == -1:
            return  # هیچ آیتمی انتخاب نشده

        new_row = current_row + direction
        if new_row < 0 or new_row >= self.file_list_widget.count():
            return  # نمی‌توان به بالا یا پایین رفت

        # تبادل آیتم‌ها
        current_item = self.file_list_widget.takeItem(current_row)
        self.file_list_widget.insertItem(new_row, current_item)
        self.file_list_widget.setCurrentRow(new_row)

        # highlight بصری
        current_item.setBackground(Qt.yellow)
        QApplication.processEvents()
        # کمی delay ساده برای اینکه highlight حس بشه
        QTimer.singleShot(300, lambda: current_item.setBackground(Qt.white))

        # بروزرسانی لیست فایل‌ها
        self.files.insert(new_row, self.files.pop(current_row))

    # ---------- Merge Action ----------
    def merge_action(self):
        if not self.files:
            self.show_status("No files selected ❌", error=True)
            return

        folder = self.settings.get_path("merge_directory")
        if not folder:
            self.show_status("Please select an output folder ❌", error=True)
            return

        self.merge_btn.setDisabled(True)
        self.show_status("Merging PDFs...", error=False)
        QApplication.processEvents()

        try:
            output_path = self.generate_unique_filename("Merged PDF", folder)
            self.engine.merge_pdfs(self.files, output_path)
            self.show_status("Merged successfully ✅")

            # ---------- History Logging ----------
            if hasattr(self, "history"):
                self.history.log_action(
                    action="merge",
                    input_file=[os.path.basename(f) for f in self.files] if self.files else ["None"],
                    output_file=output_path,
                    format_from="PDF",
                    format_to="PDF merged",
                    status="success"
                )

        except Exception as e:
            self.show_status(f"Error: {e} ❌", error=True)
            if hasattr(self, "history"):
                self.history.log_action(
                    action="merge",
                    input_file=[os.path.basename(f) for f in self.files] if self.files else ["None"],
                    output_file="failed",
                    format_from="PDF",
                    format_to="PDF merged",
                    status="failed"
                )

        finally:
            self.merge_btn.setDisabled(False)