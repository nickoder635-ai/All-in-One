# audio.py
import os
import sys
import subprocess

SUPPORTED_FORMATS = [
    "mp3", "wav", "ogg", "opus", "flac", "m4a", "aiff",
    "mp2", "ac3", "tta", "wma", "caf",
]

# فلگ مخصوص ویندوز برای ناپدید کردن CMD
CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0


def get_ffmpeg_path():
    """
    مسیر ffmpeg.exe:
    - exe (PyInstaller) -> sys._MEIPASS
    - run.py -> مسیر محلی پروژه
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
    """
    فقط یک بار در کل برنامه صدا زده می‌شود
    """
    ffmpeg_path = get_ffmpeg_path()

    if not os.path.isfile(ffmpeg_path):
        raise RuntimeError(f"ffmpeg not found at {ffmpeg_path}")

    try:
        subprocess.run(
            [ffmpeg_path, "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
            creationflags=CREATE_NO_WINDOW
        )
    except Exception:
        raise RuntimeError("ffmpeg is not working properly")

    return ffmpeg_path


# مسیر ffmpeg کش می‌شود (نه هر بار اجرا)
FFMPEG_PATH = check_ffmpeg_once()


def convert(input_path: str, output_path: str, fmt: str, bitrate: str | None = None):
    fmt = fmt.lower()

    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported audio format: {fmt}")

    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Input audio file not found: {input_path}")

    input_ext = os.path.splitext(input_path)[1].lower().lstrip(".")
    if input_ext not in SUPPORTED_FORMATS:
        raise ValueError(f"Invalid input audio type: .{input_ext}")

    if not output_path.lower().endswith(f".{fmt}"):
        output_path = os.path.splitext(output_path)[0] + f".{fmt}"

    cmd = [
        FFMPEG_PATH,
        "-y",
        "-i", input_path
    ]

    # codecهای lossy
    if fmt in ("mp3", "ogg", "m4a", "opus"):
        codec_map = {
            "mp3": "libmp3lame",
            "ogg": "libvorbis",
            "m4a": "aac",
            "opus": "libopus",
        }
        cmd += ["-codec:a", codec_map[fmt]]

        if bitrate:
            cmd += ["-b:a", bitrate]

    cmd.append(output_path)

    result = subprocess.run(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        creationflags=CREATE_NO_WINDOW
    )

    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed:\n{result.stderr}")

    return output_path
