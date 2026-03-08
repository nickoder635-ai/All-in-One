from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QHBoxLayout
)
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
import os
from core.settings.settings import SettingsManager  # Settings مرکزی
from core.pdf_tools.rotate.rotate import rotate_pdf  # تابع rotate اصلی PDF

class RotateView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # ---------------- Settings ----------------
        self.settings = SettingsManager()  # Settings مرکزی
        self.rotate_directory = self.settings.get_path("rotate")  # مسیر rotate
        self.file_path = None
        self.rotation = None

        # ---------------- Window ----------------
        self.setWindowTitle("Rotate")
        self.resize(350, 470)
        self.setAcceptDrops(True)

        icon_dir = Path(__file__).resolve().parent.parent.parent.parent / "icons" / "rotate"

        # ---------------- Layout ----------------
        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(14)
        self.layout.setContentsMargins(20, 15, 20, 20)

        # Title
        self.title = QLabel("Rotate")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addLayout(self.center_widget(self.title))

        # Step Label
        self.step_label = QLabel("Select PDF")
        self.step_label.setAlignment(Qt.AlignCenter)
        self.step_label.setStyleSheet("font-size:14px;")
        self.layout.addWidget(self.step_label)

        # Select PDF Button
        choose_icon = QIcon(os.path.join(icon_dir, "pdf"))
        self.select_btn = QPushButton("Select PDF")
        self.select_btn.setIcon(choose_icon)
        self.select_btn.setFixedSize(200, 32)
        self.select_btn.clicked.connect(self.select_file)
        self.layout.addLayout(self.center_widget(self.select_btn))

        # Selected Label
        self.selected_label = QLabel("")
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.selected_label.setWordWrap(True)
        self.selected_label.hide()
        self.layout.addWidget(self.selected_label)

        # Rotation Buttons
        self.rotation_layout = QHBoxLayout()
        self.rotation_layout.addStretch()
        self.rotation_buttons = {}
        for angle in (90, 180, 270):
            btn = QPushButton()
            btn.setIcon(QIcon(str(icon_dir / f"{angle}.png")))
            btn.setIconSize(QSize(35, 35))
            btn.clicked.connect(lambda checked, a=angle: self.set_rotation(a))
            btn.hide()
            self.rotation_layout.addWidget(btn)
            self.rotation_buttons[angle] = btn
        self.rotation_layout.addStretch()
        self.layout.addLayout(self.rotation_layout)

        # ---------------- Output Label ----------------
        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setWordWrap(True)
        self.output_label.hide()  # اول مخفی
        self.layout.addWidget(self.output_label)  # بالای rotate_btn

        # ---------------- Select Output Button ----------------
        choose_icon = QIcon(os.path.join(icon_dir, "output"))
        self.select_output_btn = QPushButton("Select Output Folder")
        self.select_output_btn.setFixedSize(200, 32)
        self.select_output_btn.setIcon(choose_icon)
        self.select_output_btn.clicked.connect(self.select_output_folder)
        self.select_output_btn.hide()  # اول مخفی
        self.layout.addLayout(self.center_widget(self.select_output_btn))  # بالای rotate_btn

        # ---------------- Rotate Button ----------------
        rotate_icon = QIcon(os.path.join(icon_dir, "rotate.png"))
        self.rotate_btn = QPushButton("Rotate PDF")
        self.rotate_btn.setFixedSize(200, 32)
        self.rotate_btn.setIcon(rotate_icon)
        self.rotate_btn.clicked.connect(self.rotate_file)
        self.rotate_btn.hide()
        self.layout.addLayout(self.center_widget(self.rotate_btn))

        # ---------------- Status Label ----------------
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setWordWrap(True)
        self.status_label.hide()  # اول مخفی
        self.layout.addWidget(self.status_label)  # بین rotate_btn و change_output_btn

        # ---------------- Change Output Button ----------------
        choose_icon = QIcon(os.path.join(icon_dir, "change"))
        self.change_output_btn = QPushButton("Change Output Folder")
        self.change_output_btn.setFixedSize(200, 32)
        self.change_output_btn.setIcon(choose_icon)
        self.change_output_btn.clicked.connect(self.select_output_folder)
        self.change_output_btn.hide()  # اول مخفی
        self.layout.addLayout(self.center_widget(self.change_output_btn))  # زیر status_label

    # ---------------- Center Helper ----------------
    def center_widget(self, widget):
        layout = QHBoxLayout()
        layout.addStretch()
        layout.addWidget(widget)
        layout.addStretch()
        return layout

    # ---------------- Update Output UI ----------------
    def _update_output_ui(self):
        if self.rotate_directory:
            self.output_label.setText(f"Output: {self.rotate_directory}")
            self.output_label.show()
            self.select_output_btn.hide()
            self.change_output_btn.show()
        else:
            self.output_label.hide()
            self.select_output_btn.show()
            self.change_output_btn.hide()

    # ---------------- File Handling ----------------
    def handle_file(self, file):
        self.file_path = file
        self.step_label.setText("Select Degree")
        self.selected_label.setText(f"Selected: {os.path.basename(file)}")
        self.selected_label.show()

        for btn in self.rotation_buttons.values():
            btn.show()
        self.rotate_btn.show()

        self._update_output_ui()  # بعد از انتخاب فایل، output_label و دکمه‌ها نمایش داده شوند

        self.status_label.hide()
        self.status_label.setText("")

    def select_file(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select PDF", "", "PDF Files (*.pdf)")
        if file:
            self.handle_file(file)

    # ---------------- Drag & Drop ----------------
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

    # ---------------- Output Folder ----------------
    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.rotate_directory = folder
            self.settings.set_path("rotate", folder)  # ذخیره در JSON مرکزی
            self._update_output_ui()

    # ---------------- Rotation ----------------
    def set_rotation(self, angle):
        self.rotation = angle
        self.status_label.setText(f"Rotation selected: {angle}° 🔄")
        self.status_label.show()

    # ---------------- Unique Filename ----------------
    def generate_unique_filename(self, base_name, folder):
        name = f"{base_name}.pdf"
        path = os.path.join(folder, name)
        counter = 1
        while os.path.exists(path):
            name = f"{base_name} ({counter}).pdf"
            path = os.path.join(folder, name)
            counter += 1
        return path

    # ---------------- Rotate ----------------
    def rotate_file(self):
        if not self.file_path:
            self.status_label.setText("Please select a file ❌")
            self.status_label.show()
            return

        if not self.rotation:
            self.status_label.setText("Please select a rotation angle ⚠️")
            self.status_label.show()
            return

        if not self.rotate_directory:
            self.select_output_folder()
            if not self.rotate_directory:
                return

        try:
            folder = self.rotate_directory
            original_name = Path(self.file_path).stem
            base_name = f"{original_name} {self.rotation}° rotated"
            output_path = self.generate_unique_filename(base_name, folder)

            rotate_pdf(self.file_path, output_path, self.rotation)

            self.status_label.setText("Rotate completed successfully ✅")
            self.status_label.show()

            # ---------- History ----------
            if hasattr(self, "history"):
                self.history.log_action(
                    action="rotate_pdf",
                    input_file=self.file_path,
                    output_file=output_path,
                    format_from="PDF",
                    format_to=f"PDF {self.rotation}° rotated",
                    status="success"
                )

        except Exception as e:
            self.status_label.setText(f"Error: {e} ❌")
            self.status_label.show()
            if hasattr(self, "history"):
                self.history.log_action(
                    action="rotate_pdf",
                    input_file=self.file_path if self.file_path else "None",
                    output_file="failed",
                    format_from="PDF",
                    format_to=f"{self.rotation}° rotated" if self.rotation else "None",
                    status="failed"
                )