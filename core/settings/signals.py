from PySide6.QtCore import QObject

class AppSignals(QObject):
    def __init__(self):
        super().__init__()

    def connect_sidebar(self, sidebar, show_view_callback):

        # ---------------- Tools ----------------
        sidebar.tools_section.converter_clicked.connect(
            lambda: show_view_callback("converter")
        )
        sidebar.tools_section.file_organizer_clicked.connect(
            lambda: show_view_callback("organizer")
        )
        sidebar.tools_section.password_generator_clicked.connect(
            lambda: show_view_callback("password")
        )
        sidebar.tools_section.date_converter_clicked.connect(
            lambda: show_view_callback("date")
        )

        # ---------------- Games ----------------
        sidebar.games_section.tic_tac_toe_clicked.connect(
            lambda: show_view_callback("tictactoe")
        )
        sidebar.games_section.chess_clicked.connect(
            lambda: show_view_callback("chess")
        )

        # ---------------- PDF ----------------
        sidebar.pdf_tools_section.rotate_clicked.connect(
            lambda: show_view_callback("rotate")
        )
        sidebar.pdf_tools_section.delete_pages_clicked.connect(
            lambda: show_view_callback("delete_pages")
        )
        sidebar.pdf_tools_section.merge_clicked.connect(
            lambda: show_view_callback("merge")
        )
        sidebar.pdf_tools_section.split_clicked.connect(
            lambda: show_view_callback("split")
        )
        sidebar.pdf_tools_section.protect_clicked.connect(
            lambda: show_view_callback("protect")
        )
        sidebar.pdf_tools_section.unlock_clicked.connect(
            lambda: show_view_callback("unlock")
        )
        
        # ---------------- Ai Agents --------------
        sidebar.ai_agents_section.researcher_clicked.connect(
            lambda: show_view_callback("researcher")
        )

        # ---------------- History ----------------
        sidebar.history_section.history_clicked.connect(
            lambda: show_view_callback("history")
        )