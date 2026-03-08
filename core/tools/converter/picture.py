# picture.py
from PIL import Image, ImageOps, ImageSequence, UnidentifiedImageError
import os

SUPPORTED_FORMATS = [
    "png", "jpg", "jpeg", "webp",
    "bmp", "tif", "tiff",
    "gif", "ico", "pdf"
]

FORMAT_MAP = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "bmp": "BMP",
    "tif": "TIFF",
    "tiff": "TIFF",
    "gif": "GIF",
    "ico": "ICO",
    "pdf": "PDF",
}


# ---------------- Core ----------------
def convert(input_path, output_path, fmt, quality=95):
    fmt = fmt.lower()

    if fmt not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported format: {fmt}")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File not found: {input_path}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        img = Image.open(input_path)
    except UnidentifiedImageError:
        raise ValueError("Invalid or corrupted image")

    img = ImageOps.exif_transpose(img)
    exif = img.info.get("exif")

    # ---------- Dispatch ----------
    if fmt in ("jpg", "jpeg"):
        _save_jpeg(img, output_path, quality, exif)
    elif fmt == "webp":
        _save_webp(img, output_path, quality)
    elif fmt == "gif":
        _save_gif(img, output_path)
    elif fmt == "ico":
        _save_ico(img, output_path)
    elif fmt == "pdf":
        _save_pdf(img, output_path)
    elif fmt in ("tif", "tiff"):
        _save_tiff(img, output_path, quality, exif)
    else:
        _save_simple(img, output_path, FORMAT_MAP[fmt])


# ---------------- Format Handlers ----------------

def _save_jpeg(img, path, quality, exif):
    # JPEG = بدون alpha، بدون palette
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")

    kwargs = {
        "quality": quality,
        "optimize": True
    }
    if exif:
        kwargs["exif"] = exif

    img.save(path, "JPEG", **kwargs)


def _save_webp(img, path, quality):
    # WEBP = alpha واقعی یا RGB تمیز
    if img.mode in ("P", "LA"):
        img = img.convert("RGBA")
    elif img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    img.save(
        path,
        "WEBP",
        quality=quality,
        method=6
    )


def _save_gif(img, path):
    frames = []
    duration = img.info.get("duration", 100)
    loop = img.info.get("loop", 0)

    for frame in ImageSequence.Iterator(img):
        frames.append(frame.convert("RGBA"))

    if len(frames) == 1:
        frames[0].save(path, "GIF")
    else:
        frames[0].save(
            path,
            "GIF",
            save_all=True,
            append_images=frames[1:],
            duration=duration,
            loop=loop,
            disposal=2
        )


def _save_ico(img, path):
    img = img.convert("RGBA")
    max_size = max(img.size)

    sizes = [(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
    sizes = [s for s in sizes if s[0] <= max_size]

    img.save(path, "ICO", sizes=sizes)


def _save_pdf(img, path):
    img.convert("RGB").save(path, "PDF")


def _save_tiff(img, path, quality, exif):
    if img.mode in ("RGBA", "LA", "P"):
        img = img.convert("RGB")

    kwargs = {"compression": "tiff_deflate"}
    if exif:
        kwargs["exif"] = exif

    img.save(path, "TIFF", **kwargs)


def _save_simple(img, path, fmt):
    if img.mode not in ("RGB", "RGBA", "L"):
        img = img.convert("RGB")
    img.save(path, fmt)
