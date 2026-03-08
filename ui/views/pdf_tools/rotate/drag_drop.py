from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPalette

class DragDropMixin:
    """
    Mixin برای Drag & Drop روی QWidget.
    فقط فایل PDF پذیرفته می‌شود و یک callback هنگام Drop اجرا می‌شود.
    """

    def enable_drag_drop(self, callback):
        self._drag_drop_callback = callback
        self.setAcceptDrops(True)
        self._default_palette = self.palette()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.toLocalFile().lower().endswith(".pdf"):
                    event.acceptProposedAction()
                    # تغییر رنگ هنگام Hover
                    pal = self.palette()
                    pal.setColor(QPalette.Window, QColor("#e0f7fa"))
                    self.setPalette(pal)
                    self.setAutoFillBackground(True)
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        # بازگشت به رنگ اصلی
        self.setPalette(self._default_palette)

    def dropEvent(self, event):
        # Reset رنگ پس‌زمینه
        self.setPalette(self._default_palette)
        for url in event.mimeData().urls():
            file = url.toLocalFile()
            if file.lower().endswith(".pdf"):
                if hasattr(self, "_drag_drop_callback"):
                    self._drag_drop_callback(file)
                break
