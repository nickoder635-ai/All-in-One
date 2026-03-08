# drag_drop.py
import os

class DragDropMixin:
    """Mixin for handling drag & drop files in ConverterView."""

    def dragEnterEvent(self, event):
        """Called when something is dragged over the widget."""
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                file_path = url.toLocalFile()
                if os.path.isfile(file_path) and self._detect_type(file_path):
                    event.acceptProposedAction()
                    return
        event.ignore()  # اگر فایل پشتیبانی نشد

    def dropEvent(self, event):
        """Called when something is dropped onto the widget."""
        urls = event.mimeData().urls()
        for url in urls:
            file_path = url.toLocalFile()
            if not os.path.isfile(file_path):
                continue

            new_type = self._detect_type(file_path)
            if not new_type:
                continue

            # اگر نوع فایل تغییر کرده، دکمه مربوطه رو انتخاب کن
            if getattr(self, "selected_file_type", None) != new_type:
                if hasattr(self, "_type_selected"):
                    self._type_selected(new_type)

            # انتخاب فایل
            if hasattr(self, "_file_selected"):
                self._file_selected(file_path)

            event.acceptProposedAction()
            return  # فقط اولین فایل معتبر رو بگیر

    def _detect_type(self, file_path):
        """Detect file type based on extension and engines dict."""
        ext = os.path.splitext(file_path)[1][1:].lower()  # بدون نقطه
        engines = getattr(self, "engines", {})
        for type_name, engine in engines.items():
            if not engine:
                continue
            supported_exts = []
            if type_name == "Document":
                supported_exts = getattr(engine, "SUPPORTED_INPUT", [])
            else:
                supported_exts = getattr(engine, "SUPPORTED_FORMATS", [])
            if ext in supported_exts:
                return type_name
        return None
