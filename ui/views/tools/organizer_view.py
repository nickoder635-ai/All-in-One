from dataclasses import dataclass
from pathlib import Path
import shutil

from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QApplication
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon, QPixmap

from core.tools.organizer.logic import organize_files, clean_empty_dirs

ICON_DIR = Path(__file__).resolve().parent.parent.parent / "icons"

@dataclass
class OrganizerState:
    source_folder: str | None = None
    destination_folder: str | None = None
    use_custom_destination: bool = False
    is_running: bool = False

class OrganizerWorker(QThread):
    finished = Signal(list)
    error = Signal(str)

    def __init__(self, source: str, destination: str):
        super().__init__()
        self.source = source
        self.destination = destination

    def run(self):
        try:
            moved_files = organize_files(self.source, self.destination)
            self.finished.emit(moved_files)
        except Exception as e:
            self.error.emit(str(e))

class FileOrganizerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setUpdatesEnabled(False)

        self.state = OrganizerState()
        self.worker: OrganizerWorker | None = None
        self.moved_files: list[tuple[Path, Path]] = []
        self.undo_btn: QPushButton | None = None

        self.setWindowTitle("File Organizer")
        self.resize(420, 480)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignTop)
        self.layout.setSpacing(12)

        if parent and hasattr(parent, "hamburger") and parent.hamburger:
            self.layout.addSpacing(parent.hamburger.height())
        else:
            self.layout.addSpacing(10)

        self.title = QLabel("File Organizer")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.layout.addWidget(self.title)

        # Select Source Folder
        self.select_btn = QPushButton("Select Folder")
        self.select_btn.setFixedSize(200, 32)
        icon_path = ICON_DIR / "choose.png"
        if icon_path.exists():
            pix = QPixmap(str(icon_path)).scaled(16,16, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.select_btn.setIcon(QIcon(pix))
            self.select_btn.setIconSize(pix.size())
        self.select_btn.clicked.connect(self.select_source)
        self.layout.addWidget(self.select_btn, alignment=Qt.AlignHCenter)

        self.source_label = QLabel("")
        self.source_label.setWordWrap(True)
        self.source_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.source_label)

        # Toggle Custom Destination
        self.toggle_btn = QPushButton("Use Custom Destination: ❌")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setFixedSize(200, 32)
        self.toggle_btn.clicked.connect(self.toggle_destination)
        self.layout.addWidget(self.toggle_btn, alignment=Qt.AlignHCenter)

        # Destination Folder
        self.dest_btn = QPushButton("Select Destination Folder")
        self.dest_btn.setFixedSize(200, 32)
        self.dest_btn.setVisible(False)
        if icon_path.exists():
            self.dest_btn.setIcon(QIcon(str(icon_path)))
        self.dest_btn.clicked.connect(self.select_destination)
        self.layout.addWidget(self.dest_btn, alignment=Qt.AlignHCenter)

        self.dest_label = QLabel("")
        self.dest_label.setWordWrap(True)
        self.dest_label.setAlignment(Qt.AlignCenter)
        self.dest_label.setVisible(False)
        self.layout.addWidget(self.dest_label)

        # Organize Button
        self.organize_btn = QPushButton("Organize Files")
        self.organize_btn.setFixedSize(200, 32)
        self.organize_btn.clicked.connect(self.start_organize)
        self.layout.addWidget(self.organize_btn, alignment=Qt.AlignHCenter)

        # Status Label
        self.status = QLabel("")
        self.status.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status)

        self.update_ui()
        self.setUpdatesEnabled(True)

    # ---------- UI State ----------
    def update_ui(self):
        s = self.state
        idle = not s.is_running

        self.select_btn.setEnabled(idle)
        self.toggle_btn.setEnabled(idle and bool(s.source_folder))
        self.dest_btn.setEnabled(idle and s.use_custom_destination and bool(s.source_folder))
        self.organize_btn.setEnabled(
            idle and bool(s.source_folder) and
            (not s.use_custom_destination or bool(s.destination_folder))
        )

        self.source_label.setVisible(bool(s.source_folder))
        self.source_label.setText(s.source_folder or "")

        emoji = "✅" if s.use_custom_destination else "❌"
        self.toggle_btn.setText(f"Use Custom Destination: {emoji}")

        self.dest_btn.setVisible(s.use_custom_destination)
        self.dest_label.setVisible(s.use_custom_destination and bool(s.destination_folder))
        self.dest_label.setText(s.destination_folder or "")

        if self.undo_btn:
            self.undo_btn.setVisible(bool(self.moved_files))

    # ---------- Actions ----------
    def select_source(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder:
            return
        self.state.source_folder = folder
        self.state.destination_folder = None
        self.state.use_custom_destination = False
        self.toggle_btn.setChecked(False)
        self.status.clear()
        self.moved_files.clear()
        if self.undo_btn:
            self.undo_btn.setVisible(False)
        self.update_ui()

    def toggle_destination(self):
        self.state.use_custom_destination = self.toggle_btn.isChecked()
        self.update_ui()

    def select_destination(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.state.destination_folder = folder
            self.update_ui()

    def start_organize(self):
        s = self.state
        if s.use_custom_destination and not s.destination_folder:
            self.status.setText("❌ Select destination folder first")
            return

        destination = s.destination_folder if s.use_custom_destination else s.source_folder
        self.worker = OrganizerWorker(s.source_folder, destination)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self, moved_files: list[tuple[Path, Path]]):
        self.state.is_running = False
        self.moved_files = moved_files
        self.status.setText(f"✅ Done — {len(moved_files)} files")
        self.create_undo_button()
        self.update_ui()

        # 🔥 ثبت در history
        if hasattr(self, "history") and self.state.source_folder:
            destination = (
                self.state.destination_folder
                if self.state.use_custom_destination
                else self.state.source_folder
            )

            self.history.log_action(
                action="organize",
                input_file=self.state.source_folder,
                output_file=destination,
                format_from="folder",
                format_to="organized",
            status="success"
            )

    def on_error(self, message: str):
        self.state.is_running = False
        self.status.setText(f"❌ {message}")
        self.update_ui()

    # ---------- Undo ----------
    def create_undo_button(self):
        if self.undo_btn is None:
            self.undo_btn = QPushButton("↩️ Undo")
            self.undo_btn.setFixedSize(200, 32)
            self.undo_btn.clicked.connect(self.undo_organize)
            self.layout.addWidget(self.undo_btn, alignment=Qt.AlignHCenter)
        self.undo_btn.setVisible(bool(self.moved_files))

    def undo_organize(self):
        if not self.moved_files:
            return
        for src, dest in reversed(self.moved_files):
            if dest.exists():
                shutil.move(str(dest), str(src))
        target_folder = self.state.destination_folder if self.state.use_custom_destination else self.state.source_folder
        if target_folder:
            clean_empty_dirs(Path(target_folder))
        self.moved_files.clear()
        if self.undo_btn:
            self.undo_btn.setVisible(False)
        self.status.setText("↩️ Undo completed")
        self.update_ui()

    # ---------- Drag & Drop ----------
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        path = urls[0].toLocalFile()
        p = Path(path)
        if not p.is_dir():
            self.status.setText("❌ Please drop a folder, not a file")
            return

        if self.state.use_custom_destination:
            self.state.destination_folder = str(p)
        else:
            self.state.source_folder = str(p)
            self.state.destination_folder = None
            self.toggle_btn.setChecked(False)
            if self.undo_btn:
                self.undo_btn.setVisible(False)

        self.status.clear()
        self.update_ui()
