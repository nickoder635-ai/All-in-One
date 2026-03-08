import os
import time
from PySide6.QtCore import QThread, Signal
from core.ai_agents.researcher.agent import run_research

class ResearchWorker(QThread):
    progress = Signal(str)      # برای نمایش پیام‌های مرحله‌ای
    finished = Signal(str)      # مسیر فایل خروجی وقتی تمام شد
    error = Signal(str)         # خطاها
    api_invalid = Signal()      # وقتی API مشکل داره

    def __init__(self, topic: str, api_key: str, target_language: str,
                 output_format: str, output_dir: str,
                 summarizer_model: str = None, translator_model: str = None):
        super().__init__()
        self.topic = topic
        self.api_key = api_key
        self.target_language = target_language
        self.output_format = output_format
        self.output_dir = output_dir
        self.summarizer_model = summarizer_model or os.getenv("OLLAMA_GPT_MODEL", "")
        self.translator_model = translator_model or os.getenv("OLLAMA_MINIMAX_MODEL", "")

    def run(self):
        try:
            from core.ai_agents.researcher.agent import Client, DDGS, arabic_reshaper, get_display, Document, SimpleDocTemplate, Paragraph, Spacer, ParagraphStyle, pdfmetrics, TTFont, A4
            import logging

            client = Client(
                host="https://ollama.com",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )

            # ---------- SEARCH ----------
            self.progress.emit(f"🔍 Searching for '{self.topic}'...")
            results = []
            import io
            from contextlib import redirect_stdout, redirect_stderr

            f = io.StringIO()  # برای گرفتن خروجی stdout
            e = io.StringIO()  # برای گرفتن خروجی stderr

            try:
                with redirect_stdout(f), redirect_stderr(e):
                    with DDGS() as ddgs:
                        for r in ddgs.text(self.topic, max_results=3):
                            results.append(f"Title: {r['title']}\nURL: {r['href']}\nSnippet: {r['body']}\n")
            except Exception as ex:
                self.error.emit(f"Search Error: {str(ex)}")
                return

            search_text = "\n\n".join(results)
            self.progress.emit("✅ Search completed")
            time.sleep(1.5)

            # ---------- SUMMARIZE ----------
            self.progress.emit("🧩 Summarizing results...")
            try:
                response = client.chat(
                    model=self.summarizer_model,
                    messages=[
                        {"role": "system", "content": "Summarize clearly as continuous prose."},
                        {"role": "user", "content": search_text}
                    ]
                )
                summary = response["message"]["content"]
            except Exception as e:
                if "401" in str(e):
                    self.api_invalid.emit()
                self.error.emit(f"Summarize Error: {str(e)}")
                return

            self.progress.emit("✅ Summarization completed")
            time.sleep(1.5)

            # ---------- TRANSLATE ----------
            translated = summary
            if self.target_language.lower() != "english":
                lang_display = self.target_language.capitalize()
                self.progress.emit(f"🌐 Translating to {lang_display}...")
                try:
                    response = client.chat(
                        model=self.translator_model,
                        messages=[
                            {"role": "system", "content": f"Translate to fluent {lang_display}."},
                            {"role": "user", "content": summary}
                        ]
                    )
                    translated = response["message"]["content"]
                except Exception as e:
                    if "401" in str(e):
                        self.api_invalid.emit()
                    self.error.emit(f"Translate Error: {str(e)}")
                    return
                self.progress.emit("✅ Translate Completed")

            # ---------- WRITE FILE ----------
            safe_topic = "".join(c if c.isalnum() or c in " _-" else "_" for c in self.topic)
            filename = f"{safe_topic}.{self.output_format}"
            filepath = os.path.join(self.output_dir, filename)

            try:
                if self.output_format in ("txt", "md"):
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(translated)
                elif self.output_format == "docx":
                    doc = Document()
                    doc.add_paragraph(translated)
                    doc.save(filepath)
                elif self.output_format == "pdf":
                    font_path = "DejaVuSans.ttf"
                    if not os.path.exists(font_path):
                        raise Exception("DejaVuSans.ttf required in project root for PDF output.")
                    pdfmetrics.registerFont(TTFont("DejaVu", font_path))
                    doc = SimpleDocTemplate(filepath, pagesize=A4)
                    elements = []
                    style = ParagraphStyle(
                        "Custom",
                        parent=getSampleStyleSheet()["Normal"],
                        fontName="DejaVu",
                        fontSize=12
                    )
                    for line in translated.split("\n"):
                        if self.target_language.lower() in ("persian", "arabic", "turkish"):
                            line = get_display(arabic_reshaper.reshape(line))
                        elements.append(Paragraph(line, style))
                        elements.append(Spacer(1, 8))
                    doc.build(elements)
                else:
                    raise ValueError("Unsupported format.")
            except Exception as e:
                self.error.emit(f"File Write Error: {str(e)}")
                return

            self.progress.emit(f"💾 Research Saved to: {filename}")
            self.finished.emit(filepath)

        except Exception as e:
            self.error.emit(f"Unexpected Error: {str(e)}")