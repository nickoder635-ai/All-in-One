from PySide6.QtCore import QThread, Signal


class ConvertWorker(QThread):
    """
    Universal conversion worker.
    Works for Picture, Audio, Subtitle, Document, Video
    """

    finished = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        engine,
        input_path: str,
        output_path: str,
        fmt: str,
        **options
    ):
        super().__init__()
        self.engine = engine
        self.input_path = input_path
        self.output_path = output_path
        self.fmt = fmt
        self.options = options  # quality, bitrate, fps, etc.

    def run(self):
        try:
            if not self.engine or not hasattr(self.engine, "convert"):
                raise RuntimeError("Invalid conversion engine")

            self.engine.convert(
                self.input_path,
                self.output_path,
                fmt=self.fmt,
                **self.options
            )

            self.finished.emit("✅ Conversion completed successfully")

        except Exception as e:
            self.failed.emit(f"❌ Conversion failed: {str(e)}")
