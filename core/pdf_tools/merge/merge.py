# core/pdf_tools/merge/merge.py
import pikepdf
from pathlib import Path

class PDFMergerEngine:
    def __init__(self):
        pass

    def merge_pdfs(self, files: list[str], output_path: str):
        if not files:
            raise ValueError("هیچ فایلی برای ادغام انتخاب نشده است!")

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        merged_pdf = pikepdf.Pdf.new()

        for f in files:
            try:
                src_pdf = pikepdf.Pdf.open(f)
                merged_pdf.pages.extend(src_pdf.pages)
                src_pdf.close()
            except Exception as e:
                print(f"Error with {f}: {e}")

        merged_pdf.save(output_path)
        merged_pdf.close()
        return output_path
