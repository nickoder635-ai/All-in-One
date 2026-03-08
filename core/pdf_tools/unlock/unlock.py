from pathlib import Path
from typing import Optional
from pypdf import PdfReader, PdfWriter


class PDFUnlockError(Exception):
    """Raised when PDF cannot be unlocked."""
    pass


def unlock_pdf(
    input_path: str | Path,
    output_path: str | Path,
    password: Optional[str] = None,
) -> Path:
    """
    Unlock a password-protected PDF.

    Args:
        input_path: Path to encrypted PDF.
        output_path: Path where unlocked PDF will be saved.
        password: User password (if required).

    Returns:
        Path to unlocked PDF.

    Raises:
        PDFUnlockError: If unlocking fails.
        FileNotFoundError: If input file does not exist.
    """

    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    reader = PdfReader(str(input_path))

    if not reader.is_encrypted:
        # Already unlocked → just copy content
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path

    # If encrypted
    if password is None:
        raise PDFUnlockError("PDF is encrypted and no password was provided.")

    try:
        result = reader.decrypt(password)
        if result == 0:
            raise PDFUnlockError("Invalid password.")

        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)

        with open(output_path, "wb") as f:
            writer.write(f)

        return output_path

    except Exception as e:
        raise PDFUnlockError(f"Failed to unlock PDF: {e}") from e