# ui/footer/footer.py
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt

class Footer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.footer_height = 20
        self.offset = 5
        self.setFixedHeight(self.footer_height)

        # برچسب
        self.label = QLabel(
            "Version: 2.0.1 | Author: Mahdi Haqiqat | Powered by Python",
            self
        )
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: gray; font-size: 10pt;")
        self.label.setFixedHeight(self.footer_height)

        # خط جداکننده بالای footer
        self.line = QWidget(self)
        self.line.setStyleSheet("background-color: #cccccc;")
        self.line.setFixedHeight(1)

        self.update_position()

    def resizeEvent(self, event):
        self.update_position()
        super().resizeEvent(event)

    def update_position(self):
        """Footer همیشه پایین صفحه و عرض کامل parent را داشته باشد"""
        if not self.parent():
            return

        parent_width = self.parent().width()
        parent_height = self.parent().height()

        self.setGeometry(0, parent_height - self.footer_height - self.offset,
                         parent_width, self.footer_height)
        self.label.setGeometry(0, 0, parent_width, self.footer_height)
        self.line.setGeometry(0, 0, parent_width, 1)
