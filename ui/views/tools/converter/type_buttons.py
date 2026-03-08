import os
from PySide6.QtWidgets import QHBoxLayout, QPushButton
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

class TypeButtons:
    def __init__(self, parent, icon_dir, callback):
        self.parent = parent
        self.icon_dir = icon_dir
        self.callback = callback

        self.buttons = {}
        self.layouts = []

        self._create_buttons()

    def _type_btn(self, text, icon_name):
        btn = QPushButton(text)
        btn.setFixedWidth(100)
        btn.setIcon(QIcon(os.path.join(self.icon_dir, icon_name)))
        btn.setIconSize(QSize(20, 20))
        return btn

    def _create_buttons(self):
        top_layout = QHBoxLayout()
        top_layout.setAlignment(Qt.AlignHCenter)
        top_layout.setSpacing(10)

        for text, icon in [("Picture", "picture.png"), ("Audio", "audio.png"), ("Subtitle", "subtitle.png")]:
            btn = self._type_btn(text, icon)
            btn.clicked.connect(lambda checked=False, t=text: self.callback(t))
            top_layout.addWidget(btn)
            self.buttons[text] = btn

        self.layouts.append(top_layout)

        bottom_layout = QHBoxLayout()
        bottom_layout.setAlignment(Qt.AlignHCenter)
        bottom_layout.setSpacing(10)

        for text, icon in [("Document", "document.png"), ("Video", "video.png")]:
            btn = self._type_btn(text, icon)
            btn.clicked.connect(lambda checked=False, t=text: self.callback(t))
            bottom_layout.addWidget(btn)
            self.buttons[text] = btn

        self.layouts.append(bottom_layout)
