import os
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QHBoxLayout, QComboBox, QApplication
)
from PySide6.QtCore import Qt, Signal, QSize
from PySide6.QtGui import QIcon, QMovie

# فرض می‌کنیم این ماژول‌ها موجودند
from core.tools.converter import audio, picture, subtitle, document, video
from core.workers.convert_worker import ConvertWorker

from core.settings.settings import SettingsManager  # Settings مرکزی

from ui.views.tools.converter.type_buttons import TypeButtons
from ui.views.tools.converter.drag_drop import DragDropMixin

class ConverterView(DragDropMixin, QWidget):
    convert_requested = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumSize(350, 470)

        self.selected_file = None
        self.settings = SettingsManager()  # Settings مرکزی
        self.selected_file_type = None
        self.converter_directory = self.settings.get_path("converter")  # مسیر مرکزی
        self.worker = None

        self.engines = {
            "Picture": picture,
            "Audio": audio,
            "Subtitle": subtitle,
            "Document": document,
            "Video": video
        }

        self._setup_ui()
        self._init_ux()

    # ---------------- Settings ----------------
    def _save_settings(self):
        # مسیر converter رو ست کن و ذخیره کن
        self.settings.set_path("converter", self.converter_directory)

    # ---------------- UI ----------------
    def _setup_ui(self):
        icon_dir = Path(__file__).resolve().parent.parent.parent.parent / "icons" / "converter"

        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.main_layout.setSpacing(10)
        self.main_layout.addSpacing(10)

        # Title
        self.title = QLabel("Converter")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:24px;font-weight:bold;")
        self.main_layout.addWidget(self.title)

        # Info
        self.info = QLabel("Select Type")
        self.info.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.info)

        # Type Buttons
        self.type_buttons = TypeButtons(self, icon_dir, self._type_selected)
        for layout in self.type_buttons.layouts:
            self.main_layout.addLayout(layout)

        # Container
        self.container = QWidget()
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setAlignment(Qt.AlignHCenter)
        self.container_layout.setSpacing(8)
        self.main_layout.addWidget(self.container)

        # Choose File
        choose_icon = QIcon(os.path.join(icon_dir, "choose.png"))
        self.choose_file_button = QPushButton("Choose File")
        self.choose_file_button.setFixedSize(200, 32)
        self.choose_file_button.setIcon(choose_icon)
        self.choose_file_button.setIconSize(QSize(20, 20))
        self.choose_file_button.clicked.connect(self._choose_file)
        self.container_layout.addWidget(self.choose_file_button, alignment=Qt.AlignHCenter)

        # Selected Label
        self.selected_label = QLabel("")
        self.selected_label.setAlignment(Qt.AlignCenter)
        self.selected_label.setWordWrap(True)
        self.selected_label.setFixedWidth(300)
        self.container_layout.addWidget(self.selected_label, alignment=Qt.AlignHCenter)

        # Formats Button
        self.formats_button = QPushButton("Formats")
        formats_icon = QIcon(os.path.join(icon_dir, "add.png"))
        self.formats_button.setFixedSize(200, 32)
        self.formats_button.setIcon(formats_icon)
        self.formats_button.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.formats_button.clicked.connect(self._toggle_formats)
        self.container_layout.addWidget(self.formats_button, alignment=Qt.AlignHCenter)

        # Format Combo
        self.format_combo = QComboBox()
        self.format_combo.setFixedWidth(200)
        self.container_layout.addWidget(self.format_combo, alignment=Qt.AlignHCenter)

        # Output Label
        self.output_label = QLabel("")
        self.output_label.setAlignment(Qt.AlignCenter)
        self.output_label.setWordWrap(True)
        self.output_label.setFixedWidth(300)
        self.container_layout.addWidget(self.output_label, alignment=Qt.AlignHCenter)

        # Output Button
        self.output_button = QPushButton("Select Output Folder")
        output_icon = QIcon(os.path.join(icon_dir, "output.png"))
        self.output_button.setFixedSize(200, 32)
        self.output_button.setIcon(output_icon)
        self.output_button.setIconSize(QSize(20, 20))
        self.output_button.clicked.connect(self._select_converter_directory)
        self.container_layout.addWidget(self.output_button, alignment=Qt.AlignHCenter)

        # Start Conversion
        self.start_button = QPushButton("Start Conversion")
        self.start_button.setFixedSize(200, 32)
        self.start_button.clicked.connect(self._start_conversion)
        self.container_layout.addWidget(self.start_button, alignment=Qt.AlignHCenter)

        # Conversion Label + GIF
        self.conversion_widget = QWidget()
        self.conversion_layout = QHBoxLayout(self.conversion_widget)
        self.conversion_layout.setContentsMargins(0, 0, 0, 0)
        self.conversion_layout.setSpacing(6)
        self.conversion_layout.setAlignment(Qt.AlignHCenter)

        self.loading_label = QLabel()
        self.loading_label.setFixedSize(24, 24)
        self.loading_label.hide()
        self.conversion_layout.addWidget(self.loading_label)

        # GIF
        loading_gif_path = os.path.join(icon_dir, "loading.gif")
        self.loading_movie = QMovie(loading_gif_path)
        self.loading_movie.setScaledSize(QSize(24, 24))
        self.loading_label.setMovie(self.loading_movie)

        self.conversion_label = QLabel()
        self.conversion_label.setWordWrap(False)
        self.conversion_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.conversion_layout.addWidget(self.conversion_label)
        self.container_layout.addWidget(self.conversion_widget, alignment=Qt.AlignHCenter)

        # Change Output
        self.change_output_button = QPushButton("Change Output Folder")
        output_icon = QIcon(os.path.join(icon_dir, "change.png"))
        self.change_output_button.setFixedSize(200, 32)
        self.change_output_button.setIcon(output_icon)
        self.change_output_button.setIconSize(QSize(20, 20))
        self.change_output_button.clicked.connect(self._select_converter_directory)
        self.container_layout.addWidget(self.change_output_button, alignment=Qt.AlignHCenter)

    # ---------------- UX ----------------
    def _init_ux(self):
        for w in [
            self.choose_file_button, self.selected_label, self.formats_button,
            self.format_combo, self.output_label, self.output_button,
            self.start_button, self.conversion_label, self.change_output_button
        ]:
            w.hide()

    # ---------------- Type Selection ----------------
    def _type_selected(self, file_type):
        self.selected_file_type = file_type
        self.info.setText("Select File")
        self.selected_file = None
        self.selected_label.setText("")
        self.selected_label.hide()
        self.conversion_label.hide()
        self._load_formats()
        self.choose_file_button.show()
        self.formats_button.show()
        self.format_combo.hide()

        if self.converter_directory:
            self.output_label.setText(f"Output: {self.converter_directory}")
            self.output_label.show()
            self.output_button.hide()
            self.start_button.show()
            self.change_output_button.show()
        else:
            self.output_label.hide()
            self.output_button.show()
            self.start_button.hide()
            self.change_output_button.hide()

        # Highlight
        for b in self.type_buttons.buttons.values():
            b.setStyleSheet("")
        if file_type in self.type_buttons.buttons:
            self.type_buttons.buttons[file_type].setStyleSheet("background:#cce5ff;")

    # ---------------- Load Formats ----------------
    def _load_formats(self):
        self.format_combo.clear()
        self.format_combo.addItem("Select Format")
        self.format_combo.model().item(0).setEnabled(False)
        engine = self.engines.get(self.selected_file_type)
        if not engine:
            return
        if self.selected_file_type == "Document":
            formats = getattr(engine, "SUPPORTED_OUTPUT", [])
        else:
            formats = getattr(engine, "SUPPORTED_FORMATS", [])
        for f in formats:
            self.format_combo.addItem(f.upper())
        if self.format_combo.count() > 1:
            self.format_combo.setCurrentIndex(0)

    # ---------------- Toggle Formats ----------------
    def _toggle_formats(self):
        self.format_combo.setVisible(not self.format_combo.isVisible())

    # ---------------- Choose File ----------------
    def _choose_file(self):
        if not self.selected_file_type:
            return
        engine = self.engines.get(self.selected_file_type)
        if not engine:
            return
        if self.selected_file_type == "Document":
            filt = "Supported Files (" + " ".join(f"*.{f}" for f in getattr(engine, "SUPPORTED_INPUT", [])) + ")"
        else:
            filt = "Supported Files (" + " ".join(f"*.{f}" for f in getattr(engine, "SUPPORTED_FORMATS", [])) + ")"
        file, _ = QFileDialog.getOpenFileName(self, "Select File", "", filt)
        if file:
            self._file_selected(file)

    def _file_selected(self, file_path):
        self.selected_file = file_path
        self.selected_label.setText(f"Selected: {os.path.basename(file_path)}")
        self.selected_label.show()
        self.conversion_label.hide()

    # ---------------- Output ----------------
    def _select_converter_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Folder", self.converter_directory or "")
        if directory:
            self.converter_directory = directory
            self.output_label.setText(f"Output: {directory}")
            self.output_label.show()
            self.output_button.hide()
            self.start_button.show()
            self.change_output_button.show()
            self._save_settings()

    # ---------------- Conversion ----------------
    def _start_conversion(self):
        self.conversion_label.hide()

        if not self.selected_file or not self.selected_file_type:
            self._conversion_failed("❌ Please select a file and type first")
            return

        selected_format = self.format_combo.currentText()
        if selected_format == "Select Format":
            self._conversion_failed("❌ Please select format")
            return

        engine = self.engines.get(self.selected_file_type)
        if not engine or not hasattr(engine, "convert"):
            self._conversion_failed("❌ Conversion engine not available")
            return

        type_folder = os.path.join(self.converter_directory, self.selected_file_type)
        os.makedirs(type_folder, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(self.selected_file))[0]
        out_file = os.path.join(type_folder, f"{base_name}.{selected_format.lower()}")

        options = {}
        if self.selected_file_type == "Picture":
            options["quality"] = 95
        elif self.selected_file_type == "Audio":
            options["bitrate"] = "320k"

        self.start_button.setEnabled(False)
        self.conversion_label.setText(f"Converting {self.selected_file_type.lower()}...")
        self.conversion_label.show()
        self.loading_label.show()
        self.loading_movie.start()

        self.worker = ConvertWorker(
            engine=engine,
            input_path=self.selected_file,
            output_path=out_file,
            fmt=selected_format.lower(),
            **options
        )
        self.worker.finished.connect(self._conversion_done)
        self.worker.failed.connect(self._conversion_failed)
        self.worker.start()

    def _conversion_done(self, message):
        self.loading_movie.stop()
        self.loading_label.hide()
        self.start_button.setEnabled(True)
        self.conversion_label.setText(message)
        self.conversion_label.show()

        # اگر history از MainWindow پاس داده شده باشد
        if hasattr(self, "history") and self.selected_file and self.selected_file_type:

            input_file = self.selected_file

            selected_format = self.format_combo.currentText().lower()
            base_name = os.path.splitext(os.path.basename(input_file))[0]

            output_file = os.path.join(
                self.converter_directory,
                self.selected_file_type,
                f"{base_name}.{selected_format}"
            )

            self.history.log_action(
                action="convert",
                input_file=input_file,
                output_file=output_file,
                format_from=os.path.splitext(input_file)[1].replace(".", ""),
                format_to=selected_format,
                status="success"
            )
            
    def _conversion_failed(self, message):
        self.loading_movie.stop()
        self.loading_label.hide()
        self.start_button.setEnabled(True)
        self.conversion_label.setText(message)
        self.conversion_label.show()

# ---------------- Run ----------------
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    w = ConverterView()
    w.show()
    sys.exit(app.exec())
