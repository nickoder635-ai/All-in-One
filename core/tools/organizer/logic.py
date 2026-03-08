from pathlib import Path
import shutil

FILE_MAP = {
    "PDFs": ["pdf"],
    "Documents": ["docx", "doc", "md", "odt", "rtf"],
    "Spreadsheets": ["xls", "xlsx", "csv", "ods"],
    "Presentations": ["ppt", "pptx", "key"],
    "Images": ["png", "jpg", "jpeg", "gif", "bmp", "webp", "tif", "tiff", "ico", "svg"],
    "Videos": ["mp4", "mkv", "avi", "mov", "flv", "wmv", "webm", "m4v"],
    "Audio": ["mp3", "wav", "ogg", "opus", "flac", "m4a", "aiff", "mp2", "ac3", "tta", "wma", "caf", "aac", "alac"],
    "Subtitles": ["srt", "vtt", "ass", "ssa", "sub", "sbv", "mpl", "dfxp", "ttml"],
    "Archives": ["zip", "rar", "7z", "tar", "gz", "bz2", "tar.gz", "tar.bz2"],
    "Executables": ["exe", "msi", "bat", "sh", "app"],
    "Code": ["py", "js", "java", "cpp", "c", "cs", "html", "css", "php", "ts", "rb", "go", "ipynb", "pyc"],
    "Data": ["json", "xml", "yaml", "yml", "sql", "db", "mdb", "sqlite"],
    "Fonts": ["ttf", "otf", "woff", "woff2"],
    "Others": []
}

def get_full_suffix(file_path: Path) -> str:
    return ''.join(s.lstrip('.') for s in file_path.suffixes).lower()

def generate_unique_path(dest_dir: Path, filename: str) -> Path:
    dest_path = dest_dir / filename
    if not dest_path.exists():
        return dest_path
    base = dest_path.stem
    suffix = dest_path.suffix
    counter = 1
    while True:
        new_name = f"{base}_copy{counter}{suffix}"
        new_path = dest_dir / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def clean_empty_dirs(folder: Path, allowed_folders=None):
    allowed_folders = allowed_folders or FILE_MAP.keys()
    for sub in folder.iterdir():
        if sub.is_dir() and sub.name in allowed_folders:
            clean_empty_dirs(sub, allowed_folders)
            if not any(sub.iterdir()):
                sub.rmdir()

def organize_files(source_folder: str, destination_root: str = None) -> list[tuple[Path, Path]]:
    """
    مرتب سازی فایل‌ها و برگرداندن لیست فایل‌های جابجا شده
    [(original_path, new_path), ...]
    """
    source_folder = Path(source_folder)
    if not source_folder.exists() or not source_folder.is_dir():
        raise ValueError("Source folder معتبر نیست")

    destination_root = Path(destination_root) if destination_root else source_folder
    destination_root.mkdir(parents=True, exist_ok=True)

    for folder in FILE_MAP.keys():
        (destination_root / folder).mkdir(exist_ok=True)

    moved_files: list[tuple[Path, Path]] = []

    for file_path in source_folder.iterdir():
        if not file_path.is_file():
            continue

        full_ext = get_full_suffix(file_path)
        moved = False

        for folder, extensions in FILE_MAP.items():
            if full_ext in extensions:
                dest_path = generate_unique_path(destination_root / folder, file_path.name)
                shutil.move(str(file_path), str(dest_path))
                moved_files.append((file_path, dest_path))
                moved = True
                break

        if not moved:
            dest_path = generate_unique_path(destination_root / "Others", file_path.name)
            shutil.move(str(file_path), str(dest_path))
            moved_files.append((file_path, dest_path))

    clean_empty_dirs(destination_root, allowed_folders=FILE_MAP.keys())
    return moved_files
