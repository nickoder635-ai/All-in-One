# video.py
import os
import sys
import subprocess
from pathlib import Path

# ---------------- Supported Formats ----------------
SUPPORTED_FORMATS = [
    "mp4", "mkv", "mov", "avi", "webm",
    "flv", "mpeg", "mpg", "ts", "wmv", "m4v", "3gp"
]

# ---------------- FFmpeg Utils ----------------

def get_ffmpeg_path():
    """
    exe -> PyInstaller
    dev -> project path
    """
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "ffmpeg", "bin", "ffmpeg.exe")

    return os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            "..", "..", "..",
            "ffmpeg", "bin", "ffmpeg.exe"
        )
    )


def check_ffmpeg_once():
    ffmpeg = get_ffmpeg_path()

    if not os.path.isfile(ffmpeg):
        raise RuntimeError("ffmpeg not found")

    CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    try:
        subprocess.run(
            [ffmpeg, "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=CREATE_NO_WINDOW,
            check=True
        )
    except Exception:
        raise RuntimeError("ffmpeg not working")

    return ffmpeg


FFMPEG_PATH = check_ffmpeg_once()

# ---------------- Main Convert ----------------

def convert(input_path, output_path, fmt=None):
    """
    fmt فقط برای سازگاری با UI است
    """

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError("Input video not found")

    ext = input_path.suffix.lower().replace(".", "")
    if ext not in SUPPORTED_FORMATS:
        raise ValueError("Unsupported video format")

    os.makedirs(output_path.parent, exist_ok=True)

    # ⚠️ تنظیمات کم‌فشار مخصوص سیستم بدون GPU
    cmd = [
        FFMPEG_PATH,

        "-y",
        "-hide_banner",
        "-loglevel", "error",

        "-i", str(input_path),

        # ⚡ CPU SAFE SETTINGS
        "-c:v", "libx264",
        "-preset", "ultrafast",   # مهم‌ترین عامل سرعت
        "-crf", "28",             # کیفیت مناسب بدون فشار
        "-threads", "1",          # جلوگیری از داغ شدن

        "-c:a", "copy",           # صدا بدون تبدیل (خیلی مهم)

        str(output_path)
    ]

    CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    subprocess.run(
        cmd,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=CREATE_NO_WINDOW,
        check=True
    )
