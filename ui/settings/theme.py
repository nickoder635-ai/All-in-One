# ui/settings/theme.py
from PySide6.QtWidgets import QApplication

LIGHT_THEME = """..."""  # تم روشن
DARK_THEME = """..."""   # تم تاریک

class ThemeManager:
    current_theme = "light"

    @staticmethod
    def apply_theme(app: QApplication, theme_name: str):
        if theme_name == "light":
            app.setStyleSheet(LIGHT_THEME)
            ThemeManager.current_theme = "light"
        elif theme_name == "dark":
            app.setStyleSheet(DARK_THEME)
            ThemeManager.current_theme = "dark"

    @staticmethod
    def toggle_theme(app: QApplication):
        if ThemeManager.current_theme == "light":
            ThemeManager.apply_theme(app, "dark")
        else:
            ThemeManager.apply_theme(app, "light")
