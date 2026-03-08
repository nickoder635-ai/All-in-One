from PySide6.QtCore import QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup

class SidebarAnimation:
    def __init__(self, sidebar):
        self.sidebar = sidebar

        # متصل کردن دکمه‌ها به Animation
        self.sidebar.tools_btn.clicked.connect(self.toggle_tools)
        self.sidebar.games_btn.clicked.connect(self.toggle_games)
        self.sidebar.pdf_tools_btn.clicked.connect(self.toggle_pdf_tools)
        self.sidebar.ai_agents_btn.clicked.connect(self.toggle_ai_agents)
        
        # اگه بخوای روی selection هم collapse بشه:
        for btn in self.sidebar.tools_buttons:
            btn.clicked.connect(self.collapse_tools)
        for btn in self.sidebar.games_buttons:
            btn.clicked.connect(self.collapse_games)
        for btn in self.sidebar.pdf_tools_buttons:
            btn.clicked.connect(self.collapse_pdf_tools)
        for btn in self.sidebar.ai_agents_buttons:
            btn.clicked.connect(self.collapse_ai_agents)
        
    def toggle_tools(self):
        # اگه games بازه، اول اون رو ببند
        if self.sidebar.games_open:
            self.collapse_games()
        if self.sidebar.pdf_tools_open:
            self.collapse_pdf_tools()
        if self.sidebar.ai_agents_open:
            self.collapse_ai_agents()

        duration = 250
        seq = QSequentialAnimationGroup(self.sidebar)
        buttons = self.sidebar.tools_buttons if not self.sidebar.tools_open else reversed(self.sidebar.tools_buttons)
        for btn in buttons:
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(duration)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            if self.sidebar.tools_open:
                anim.setStartValue(btn.sizeHint().height())
                anim.setEndValue(0)
            else:
                anim.setStartValue(0)
                anim.setEndValue(btn.sizeHint().height())
            seq.addAnimation(anim)
        self.sidebar.tools_open = not self.sidebar.tools_open
        seq.start()

    def toggle_games(self):
        # اگه games بازه، اول اون رو ببند
        if self.sidebar.tools_open:
            self.collapse_tools()
        if self.sidebar.pdf_tools_open:
            self.collapse_pdf_tools()
        if self.sidebar.ai_agents_open:
            self.collapse_ai_agents()

        duration = 250
        seq = QSequentialAnimationGroup(self.sidebar)
        buttons = self.sidebar.games_buttons if not self.sidebar.games_open else reversed(self.sidebar.games_buttons)
        for btn in buttons:
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(duration)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            if self.sidebar.games_open:
                anim.setStartValue(btn.sizeHint().height())
                anim.setEndValue(0)
            else:
                anim.setStartValue(0)
                anim.setEndValue(btn.sizeHint().height())
            seq.addAnimation(anim)
        self.sidebar.games_open = not self.sidebar.games_open
        seq.start()

    def toggle_pdf_tools(self):
        # اگه games بازه، اول اون رو ببند
        if self.sidebar.tools_open:
            self.collapse_tools()
        if self.sidebar.games_open:
            self.collapse_games()
        if self.sidebar.ai_agents_open:
            self.collapse_ai_agents()
            
        duration = 250
        seq = QSequentialAnimationGroup(self.sidebar)
        buttons = self.sidebar.pdf_tools_buttons if not self.sidebar.pdf_tools_open else reversed(self.sidebar.pdf_tools_buttons)
        for btn in buttons:
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(duration)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            if self.sidebar.pdf_tools_open:
                anim.setStartValue(btn.sizeHint().height())
                anim.setEndValue(0)
            else:
                anim.setStartValue(0)
                anim.setEndValue(btn.sizeHint().height())
            seq.addAnimation(anim)
        self.sidebar.pdf_tools_open = not self.sidebar.pdf_tools_open
        seq.start()

    def toggle_ai_agents(self):
        # اگه games بازه، اول اون رو ببند
        if self.sidebar.tools_open:
            self.collapse_tools()
        if self.sidebar.games_open:
            self.collapse_games()
        if self.sidebar.pdf_tools_open:
            self.collapse_pdf_tools()
            
        duration = 250
        seq = QSequentialAnimationGroup(self.sidebar)
        buttons = self.sidebar.ai_agents_buttons if not self.sidebar.ai_agents_open else reversed(self.sidebar.ai_agents_buttons)
        for btn in buttons:
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(duration)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            if self.sidebar.ai_agents_open:
                anim.setStartValue(btn.sizeHint().height())
                anim.setEndValue(0)
            else:
                anim.setStartValue(0)
                anim.setEndValue(btn.sizeHint().height())
            seq.addAnimation(anim)
        self.sidebar.ai_agents_open = not self.sidebar.ai_agents_open
        seq.start()    

    # Collapse functions برای selection
    def collapse_tools(self):
        if not self.sidebar.tools_open:
            return
        seq = QSequentialAnimationGroup(self.sidebar)
        for btn in reversed(self.sidebar.tools_buttons):
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setStartValue(btn.sizeHint().height())
            anim.setEndValue(0)
            seq.addAnimation(anim)
        self.sidebar.tools_open = False
        seq.start()

    def collapse_games(self):
        if not self.sidebar.games_open:
            return
        seq = QSequentialAnimationGroup(self.sidebar)
        for btn in reversed(self.sidebar.games_buttons):
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setStartValue(btn.sizeHint().height())
            anim.setEndValue(0)
            seq.addAnimation(anim)
        self.sidebar.games_open = False
        seq.start()

    def collapse_pdf_tools(self):
        if not self.sidebar.pdf_tools_open:
            return
        seq = QSequentialAnimationGroup(self.sidebar)
        for btn in reversed(self.sidebar.pdf_tools_buttons):
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setStartValue(btn.sizeHint().height())
            anim.setEndValue(0)
            seq.addAnimation(anim)
        self.sidebar.pdf_tools_open = False
        seq.start()

    def collapse_ai_agents(self):
        if not self.sidebar.ai_agents_open:
            return
        seq = QSequentialAnimationGroup(self.sidebar)
        for btn in reversed(self.sidebar.ai_agents_buttons):
            anim = QPropertyAnimation(btn, b"maximumHeight")
            anim.setDuration(200)
            anim.setEasingCurve(QEasingCurve.OutCubic)
            anim.setStartValue(btn.sizeHint().height())
            anim.setEndValue(0)
            seq.addAnimation(anim)
        self.sidebar.ai_agents_open = False
        seq.start()
