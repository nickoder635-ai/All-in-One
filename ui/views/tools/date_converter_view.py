from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel,
    QPushButton, QComboBox, QHBoxLayout,
    QSpinBox, QFrame, QSizePolicy, QApplication
)
from PySide6.QtCore import Qt
from datetime import date
import jdatetime
from hijri_converter import Gregorian, Hijri
import sys

# ---------- Helper: Check if Solar Hijri year is leap ----------
def is_jalali_leap(year):
    leap_years = [1, 5, 9, 13, 17, 22, 26, 30]
    return (year % 33) in leap_years

class DateConverterView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Date Converter")
        self.resize(400, 500)  # پنجره قابل resize

        # ---------- Main Layout ----------
        central_layout = QVBoxLayout(self)
        central_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        central_layout.setSpacing(14)

        # ---------- Title ----------
        self.title = QLabel("Date Converter")
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("font-size:22px;font-weight:bold;")
        self.title.setFixedSize(300, 40)
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        central_layout.addWidget(self.title, alignment=Qt.AlignHCenter)

        # ---------- Mode Buttons ----------
        button_layout = QHBoxLayout()
        button_layout.setSpacing(12)
        button_layout.setAlignment(Qt.AlignCenter)

        self.today_btn = QPushButton("Today's Date")
        self.today_btn.setFixedSize(150, 32)
        self.today_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.today_btn.clicked.connect(self.show_today)

        self.custom_btn = QPushButton("Custom Date")
        self.custom_btn.setFixedSize(150, 32)
        self.custom_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.custom_btn.clicked.connect(self.show_custom)

        button_layout.addWidget(self.today_btn)
        button_layout.addWidget(self.custom_btn)
        central_layout.addLayout(button_layout)

        # ---------- Today's Date Labels ----------
        self.today_frame = QFrame()
        self.today_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.today_layout = QVBoxLayout(self.today_frame)
        self.today_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.greg_label = QLabel()
        self.jalali_label = QLabel()
        self.hijri_label = QLabel()

        for lbl in [self.greg_label, self.jalali_label, self.hijri_label]:
            lbl.setAlignment(Qt.AlignCenter)
            lbl.setStyleSheet("font-size:16px;")
            lbl.setFixedSize(320, 50)
            lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.today_layout.addWidget(lbl)
            line = QFrame()
            line.setFrameShape(QFrame.HLine)
            line.setFrameShadow(QFrame.Sunken)
            line.setFixedWidth(320)
            line.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.today_layout.addWidget(line)

        central_layout.addWidget(self.today_frame)
        self.today_frame.hide()

        # ---------- Custom Date SpinBoxes ----------
        self.custom_frame = QFrame()
        self.custom_frame.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.custom_layout = QVBoxLayout(self.custom_frame)
        self.custom_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        lbl_from = QLabel("From calendar")
        lbl_from.setFixedSize(320, 25)
        lbl_from.setAlignment(Qt.AlignCenter)
        self.custom_layout.addWidget(lbl_from)

        self.from_combo = QComboBox()
        self.from_combo.setFixedSize(240, 30)
        self.from_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.custom_layout.addWidget(self.from_combo, alignment=Qt.AlignCenter)

        # SpinBoxes
        date_layout = QHBoxLayout()
        date_layout.setAlignment(Qt.AlignCenter)

        self.year = QSpinBox()
        self.year.setPrefix("Y: ")
        self.year.setRange(1, 9999)
        self.year.setFixedSize(75, 20)
        self.year.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.month = QSpinBox()
        self.month.setPrefix("M: ")
        self.month.setRange(1, 12)
        self.month.setFixedSize(75, 20)
        self.month.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.day = QSpinBox()
        self.day.setPrefix("D: ")
        self.day.setRange(1, 31)
        self.day.setFixedSize(75, 20)
        self.day.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        date_layout.addWidget(self.year)
        date_layout.addWidget(self.month)
        date_layout.addWidget(self.day)
        self.custom_layout.addLayout(date_layout)

        lbl_to = QLabel("To calendar")
        lbl_to.setFixedSize(320, 25)
        lbl_to.setAlignment(Qt.AlignCenter)
        self.custom_layout.addWidget(lbl_to)

        self.to_combo = QComboBox()
        self.to_combo.setFixedSize(240, 30)
        self.to_combo.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.custom_layout.addWidget(self.to_combo, alignment=Qt.AlignCenter)

        self.convert_btn = QPushButton("Convert")
        self.convert_btn.setFixedSize(240, 32)
        self.convert_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.convert_btn.clicked.connect(self.update_result_label)
        self.custom_layout.addWidget(self.convert_btn, alignment=Qt.AlignCenter)

        self.result_label = QLabel("—")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setStyleSheet("font-size:16px;")
        self.result_label.setFixedSize(320, 30)
        self.result_label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.custom_layout.addWidget(self.result_label, alignment=Qt.AlignCenter)

        central_layout.addWidget(self.custom_frame)
        self.custom_frame.hide()

        # ---------- Initialize Today ----------
        self.today = date.today()
        self.update_combo_dates()
        self.from_combo.currentIndexChanged.connect(self.sync_spinboxes_from_combo)
        self.to_combo.currentIndexChanged.connect(self.update_result_label)
        self.show_today()

    # ---------- Update ComboBox dates ----------
    def update_combo_dates(self):
        today = self.today
        j = jdatetime.date.fromgregorian(date=today)
        h = Gregorian(today.year, today.month, today.day).to_hijri()

        self.from_combo.clear()
        self.from_combo.addItem(f"Gregorian ({today.year}-{today.month:02}-{today.day:02})", "Gregorian")
        self.from_combo.addItem(f"Solar Hijri ({j.year}-{j.month:02}-{j.day:02})", "Solar Hijri")
        self.from_combo.addItem(f"Lunar Hijri ({h.year}-{h.month:02}-{h.day:02})", "Lunar Hijri")

        self.to_combo.clear()
        self.to_combo.addItem(f"Gregorian ({today.year}-{today.month:02}-{today.day:02})", "Gregorian")
        self.to_combo.addItem(f"Solar Hijri ({j.year}-{j.month:02}-{j.day:02})", "Solar Hijri")
        self.to_combo.addItem(f"Lunar Hijri ({h.year}-{h.month:02}-{h.day:02})", "Lunar Hijri")

        self.from_combo.setCurrentIndex(0)
        self.to_combo.setCurrentIndex(0)
        self.sync_spinboxes_from_combo()
    
    # ---------- Helper: Days in month ----------
    def days_in_month(self, year, month, calendar_type):
        if calendar_type == "Gregorian":
            if month == 2:
                return 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28
            return [31,28,31,30,31,30,31,31,30,31,30,31][month-1]
        elif calendar_type == "Solar Hijri":
            if month <= 6:
                return 31
            elif month <= 11:
                return 30
            else:  # Esfand
                return 30 if is_jalali_leap(year) else 29
        else:  # Lunar Hijri
            for day in (30, 29):
                try:
                    _ = Hijri(year, month, day).to_gregorian()
                    return day
                except ValueError:
                    continue
            return 29

    # ---------- Sync SpinBoxes from Combo ----------
    def sync_spinboxes_from_combo(self):
        data = self.from_combo.currentData()
        today = self.today

        if data == "Gregorian":
            self.year.setValue(today.year)
            self.month.setValue(today.month)
            self.month.setRange(1, 12)
            self.day.setRange(1, self.days_in_month(today.year, today.month, "Gregorian"))
            self.day.setValue(today.day)
        elif data == "Solar Hijri":
            j = jdatetime.date.fromgregorian(date=today)
            self.year.setValue(j.year)
            self.month.setValue(j.month)
            self.month.setRange(1, 12)
            self.day.setRange(1, self.days_in_month(j.year, j.month, "Solar Hijri"))
            self.day.setValue(j.day)
        else:  # Lunar Hijri
            h = Gregorian(today.year, today.month, today.day).to_hijri()
            self.year.setValue(h.year)
            self.month.setValue(h.month)
            self.month.setRange(1, 12)
            self.day.setRange(1, self.days_in_month(h.year, h.month, "Lunar Hijri"))
            self.day.setValue(h.day)

        self.update_result_label()

    # ---------- Show Today's Labels ----------
    def show_today(self):
        today = self.today
        j = jdatetime.date.fromgregorian(date=today)
        h = Gregorian(today.year, today.month, today.day).to_hijri()

        self.greg_label.setText(f"Gregorian Date:\n{today.year}-{today.month:02}-{today.day:02}")
        self.jalali_label.setText(f"Solar Hijri Date:\n{j.year}-{j.month:02}-{j.day:02}")
        self.hijri_label.setText(f"Lunar Hijri Date:\n{h.year}-{h.month:02}-{h.day:02}")

        self.today_frame.show()
        self.custom_frame.hide()
        self.update_combo_dates()

    def show_custom(self):
        self.today_frame.hide()
        self.custom_frame.show()

    # ---------- Convert / Update Result ----------
    def update_result_label(self):
        y, m, d = self.year.value(), self.month.value(), self.day.value()
        from_type = self.from_combo.currentData()
        to_type = self.to_combo.currentData()

        try:
            if from_type == "Gregorian":
                g_date = date(y, m, d)
            elif from_type == "Solar Hijri":
                j = jdatetime.date(y, m, d)
                g_date = j.togregorian()
            else:  # Lunar Hijri
                g_date = Hijri(y, m, d).to_gregorian()

            if to_type == "Gregorian":
                result = f"{g_date.year}-{g_date.month:02}-{g_date.day:02}"
            elif to_type == "Solar Hijri":
                j = jdatetime.date.fromgregorian(date=g_date)
                result = f"{j.year}-{j.month:02}-{j.day:02}"
            else:  # Hijri
                h = Gregorian(g_date.year, g_date.month, g_date.day).to_hijri()
                result = f"{h.year}-{h.month:02}-{h.day:02}"

            self.result_label.setText(result)

            # ---------- History ----------
            if hasattr(self, "history"):
                self.history.log_action(
                    action="convert_date",
                    input_file=f"{from_type} {y}-{m:02}-{d:02}",
                    output_file=result,
                    format_from=from_type,
                    format_to=to_type,
                    status="success"
                )

        except Exception:
            self.result_label.setText("❌ Invalid date")
            if hasattr(self, "history"):
                self.history.log_action(
                    action="convert_date",
                    input_file=f"{from_type} {y}-{m:02}-{d:02}",
                    output_file="Invalid",
                    format_from=from_type,
                    format_to=to_type,
                    status="failed"
                )

# ---------- Run ----------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DateConverterView()
    window.show()
    sys.exit(app.exec())
