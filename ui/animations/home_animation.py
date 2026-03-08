from PySide6.QtCore import QTimer
from ui.stop.stop_manager import StopManager

class HomeAnimation:
    def __init__(self, home_view):
        self.home_view = home_view

        # متن کامل و فعلی
        self.full_text = ["Welcome to", "All\nin One"]
        self.current_text = ["", ""]
        self.part_index = 0
        self.char_index = 0

        # cursor blink
        self.cursor_visible = True
        self.cursor_timer = QTimer()
        self.cursor_timer.timeout.connect(self.blink_cursor)
        self.cursor_timer.start(500)

        # typewriter timer
        self.type_timer = QTimer()
        self.type_timer.timeout.connect(self.type_step)
        self.type_timer.start(100)

    # -------------------------
    # تایپ مرحله‌ای
    # -------------------------
    def type_step(self):
        try:
            if self.part_index >= len(self.full_text):
                self.type_timer.stop()
                return

            part = self.full_text[self.part_index]

            if self.char_index < len(part):
                self.current_text[self.part_index] += part[self.char_index]
                self.char_index += 1
                self.update_label()
            else:
                self.type_timer.stop()
                self.home_view.start_next_part_timer()
        except RuntimeError:
            # ویجت حذف شده → ایمن توقف
            StopManager.stop_animation(self)

    def next_part(self):
        self.part_index += 1
        self.char_index = 0
        self.update_label()
        self.type_timer.start(100)

    # -------------------------
    # بروزرسانی labels
    # -------------------------
    def update_label(self):
        try:
            cursor = "|" if self.cursor_visible else " "
            if self.part_index < len(self.full_text):
                self.home_view.label1.setText(
                    self.current_text[0] + (cursor if self.part_index == 0 else "")
                )
                self.home_view.label2.setText(
                    self.current_text[1] + (cursor if self.part_index == 1 else "")
                )
            else:
                self.home_view.label1.setText(self.current_text[0])
                self.home_view.label2.setText(self.current_text[1] + cursor)
        except RuntimeError:
            # QLabel حذف شده → ایمن توقف
            StopManager.stop_animation(self)

    # -------------------------
    # چشمک زدن cursor
    # -------------------------
    def blink_cursor(self):
        self.cursor_visible = not self.cursor_visible
        try:
            self.update_label()
        except RuntimeError:
            StopManager.stop_animation(self)

    # -------------------------
    # توقف کامل انیمیشن
    # -------------------------
    def stop(self):
        StopManager.safe_stop(self.cursor_timer)
        StopManager.safe_stop(self.type_timer)
