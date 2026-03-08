import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QHBoxLayout, QLineEdit, QApplication
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt

from core.settings.settings import SettingsManager
from core.pdf_tools.delete_pages.delete_pages import (
    get_total_pages,
    parse_pages,
    validate_pages,
    delete_pages
)


class DeletePagesView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.settings = SettingsManager()
        self.file_path = None
        self.total_pages = 0

        self.setWindowTitle("Delete Pages")
        self.resize(350, 470)
        self.setAcceptDrops(True)
        
        icon_dir = Path(__file__).resolve().parent.parent.parent.parent / "icons" / "delete_pages"

        # ---------- Main Layout ----------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(14)
        self.layout.setContentsMargins(20, 15, 20, 20)

        # ---------- Title ----------
        self.title = QLabel("Delete Pages")
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

        # ---------- Pages Input ----------
        self.pages_input = QLineEdit()
        self.pages_input.setPlaceholderText("Enter the page number to delete")
        self.pages_input.setFixedWidth(200)
        self.pages_input.hide()
        self.pages_input.textChanged.connect(self.limit_pages_input)
        self.layout.addLayout(self.centered(self.pages_input))

        # ---------- Instruction ----------
        self.instruction_label = QLabel(
            "If you want to delete a single page: 1\n"
            "For a range of pages: 1-2\n"
            "For multiple single pages: 1,3\n"
            "Combine both: 1,3-5"
        )
        self.instruction_label.setAlignment(Qt.AlignLeft)
        self.instruction_label.setWordWrap(True)
        self.instruction_label.hide()
        self.layout.addWidget(self.instruction_label)

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

        # ---------- Delete Button ----------
        choose_icon = QIcon(os.path.join(icon_dir, "delete.png"))
        self.delete_btn = QPushButton("Delete Pages")
        self.delete_btn.setFixedSize(200, 32)
        self.delete_btn.setIcon(choose_icon)
        self.delete_btn.clicked.connect(self.delete_action)
        self.delete_btn.hide()
        self.layout.addLayout(self.centered(self.delete_btn))

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

    # ---------- Handle File ----------
    def handle_file(self, file):
        try:
            self.file_path = file
            self.total_pages = get_total_pages(file)
        except Exception as e:
            self.show_status(f"Error reading PDF: {e}", error=True)
            return

        self.step_label.setText("Enter Pages to Delete")
        self.selected_label.setText(
            f"Selected: {os.path.basename(file)}\nTotal Pages: {self.total_pages}"
        )
        self.selected_label.show()
        self.pages_input.show()
        self.instruction_label.show()
        self.delete_btn.show()
        self.status_label.show()
        self.output_label.hide()

        # نمایش تعداد صفحات در status_label
        self.show_status(f"Total Pages: {self.total_pages}")

        stored_path = self.settings.get_path("delete_pages_directory")
        if stored_path:
            self.output_label.setText(f"Output: {stored_path}")
            self.output_label.show()
            self.change_btn.show()
            self.select_output_btn.hide()
        else:
            self.select_output_btn.show()
            self.change_btn.hide()

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
            self.settings.set_path("delete_pages_directory", folder)
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

    # ---------- Limit Pages Input ----------
    def limit_pages_input(self, text):
        if not self.total_pages:
            return

        cursor_pos = self.pages_input.cursorPosition()

        # حذف separator انتهایی
        if text.endswith(',') or text.endswith('-'):
            text = text[:-1]

        new_text = ""
        num_buffer = ""
        last_char = ""

        for ch in text:
            if ch.isdigit():
                num_buffer += ch

                if int(num_buffer) > self.total_pages:
                    num_buffer = ""
            elif ch in [',', '-']:
                # جلوگیری از تکرار غیرمجاز علامت
                if last_char == ch:
                    continue

                if num_buffer:
                    new_text += num_buffer
                    num_buffer = ""

                new_text += ch
            last_char = ch

        if num_buffer:
            new_text += num_buffer

        # اگر متن تغییر کرد، بروزرسانی input
        if new_text != text:
            self.pages_input.blockSignals(True)
            self.pages_input.setText(new_text)
            self.pages_input.setCursorPosition(min(cursor_pos, len(new_text)))
            self.pages_input.blockSignals(False)

    # ---------- Delete Pages ----------
    def delete_action(self):
        if not self.file_path:
            self.show_status("Please select a file ❌", error=True)
            return

        text = self.pages_input.text().strip()
        if not text:
            self.show_status("Enter pages to delete ⚠️", error=True)
            return

        try:
            pages = parse_pages(text)
        except Exception:
            self.show_status("Invalid input ❌", error=True)
            return

        if not validate_pages(pages, self.total_pages):
            self.show_status(f"Pages must be between 1 and {self.total_pages} ⚠️", error=True)
            return

        folder = self.settings.get_path("delete_pages_directory")
        if not folder:
            self.show_status("Please select an output folder first ❌", error=True)
            return

        self.delete_btn.setDisabled(True)
        self.show_status("Deleting...", error=False)
        QApplication.processEvents()

        try:
            original_name = Path(self.file_path).stem
            base_name = f"{original_name} pages deleted"
            output_path = self.generate_unique_filename(base_name, folder)

            delete_pages(self.file_path, output_path, pages)

            self.show_status("Pages deleted successfully ✅")
            self.change_btn.show()

            # ---------- History Logging ----------
            if hasattr(self, "history"):
                self.history.log_action(
                    action="delete_pages",
                    input_file=os.path.basename(self.file_path),
                    output_file=output_path,
                    format_from="PDF",
                    format_to=f"PDF with pages {text} deleted",
                    status="success"
                )

        except Exception as e:
            self.show_status(f"Error: {e} ❌", error=True)
            if hasattr(self, "history"):
                self.history.log_action(
                    action="delete_pages",
                    input_file=os.path.basename(self.file_path) if self.file_path else "None",
                    output_file="failed",
                    format_from="PDF",
                    format_to=f"PDF with pages {text} deleted",
                    status="failed"
                )

        finally:
            self.delete_btn.setDisabled(False)