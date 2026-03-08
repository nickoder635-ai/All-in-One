class SidebarConnections:

    @staticmethod
    def connect(sidebar):

        # -------- Tools --------
        sidebar.converter_btn.clicked.connect(
            sidebar.tools_section.converter_clicked.emit
        )
        sidebar.file_organizer_btn.clicked.connect(
            sidebar.tools_section.file_organizer_clicked.emit
        )
        sidebar.password_generator_btn.clicked.connect(
            sidebar.tools_section.password_generator_clicked.emit
        )
        sidebar.date_converter_btn.clicked.connect(
            sidebar.tools_section.date_converter_clicked.emit
        )

        # -------- Games --------
        sidebar.tic_tac_toe_btn.clicked.connect(
            sidebar.games_section.tic_tac_toe_clicked.emit
        )
        sidebar.chess_btn.clicked.connect(
            sidebar.games_section.chess_clicked.emit
        )

        # -------- PDF --------
        sidebar.rotate_btn.clicked.connect(
            sidebar.pdf_tools_section.rotate_clicked.emit
        )
        sidebar.delete_pages_btn.clicked.connect(
            sidebar.pdf_tools_section.delete_pages_clicked.emit
        )
        sidebar.merge_btn.clicked.connect(
            sidebar.pdf_tools_section.merge_clicked.emit
        )
        sidebar.split_btn.clicked.connect(
            sidebar.pdf_tools_section.split_clicked.emit
        )
        sidebar.protect_btn.clicked.connect(
            sidebar.pdf_tools_section.protect_clicked.emit
        )
        sidebar.unlock_btn.clicked.connect(
            sidebar.pdf_tools_section.unlock_clicked.emit
        )
        
        # -------- Ai Agents ------
        sidebar.researcher_btn.clicked.connect(
            sidebar.ai_agents_section.researcher_clicked.emit
        )
        
        # -------- History --------
        sidebar.history_btn.clicked.connect(
            sidebar.history_section.history_clicked.emit
        )