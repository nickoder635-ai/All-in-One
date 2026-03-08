# core/workers/api_worker.py
from PySide6.QtCore import QObject, Signal, QThread
from core.ai_agents.researcher.agent import validate_api_key
import os

class APIWorker(QThread):
    finished = Signal(bool)          # True if valid
    error = Signal(str)

    def __init__(self, api_key, summarizer="", translator=""):
        super().__init__()
        self.api_key = api_key
        self.summarizer = summarizer
        self.translator = translator

    def run(self):
        try:
            valid = validate_api_key(self.api_key, self.summarizer, self.translator)
            self.finished.emit(valid)
        except Exception as e:
            self.error.emit(str(e))