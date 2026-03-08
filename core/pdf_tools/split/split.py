# core/pdf_tools/split/split.py
import os
from pathlib import Path
import pikepdf

class PDFSplitEngine:
    """
    Engine برای تقسیم PDF به صفحات جداگانه
    یا بازه‌ای از صفحات دلخواه
    """

    def __init__(self):
        pass

    def split_pdf(self, file_path: str, output_dir: str, pages: list[int] | None = None, merge_into_one: bool = False):
        file_path = Path(file_path)
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        pdf = pikepdf.Pdf.open(file_path)
        output_files = []

        pages_to_use = pages if pages else list(range(1, len(pdf.pages)+1))  # همه صفحات اگر None بود

        if merge_into_one:
            new_pdf = pikepdf.Pdf.new()
            for page_num in pages_to_use:
                new_pdf.pages.append(pdf.pages[page_num - 1])

            output_file = output_dir / f"{file_path.stem}_extracted.pdf"
            counter = 1
            while output_file.exists():
                output_file = output_dir / f"{file_path.stem}_extracted({counter}).pdf"
                counter += 1

            new_pdf.save(output_file)
            new_pdf.close()
            output_files.append(str(output_file))
        else:
            for page_num in pages_to_use:
                new_pdf = pikepdf.Pdf.new()
                new_pdf.pages.append(pdf.pages[page_num - 1])

                output_file = output_dir / f"{file_path.stem}_page_{page_num}.pdf"
                counter = 1
                while output_file.exists():
                    output_file = output_dir / f"{file_path.stem}_page_{page_num}({counter}).pdf"
                    counter += 1

                new_pdf.save(output_file)
                new_pdf.close()
                output_files.append(str(output_file))

        pdf.close()
        return output_files