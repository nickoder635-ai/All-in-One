from PyPDF2 import PdfReader, PdfWriter

def rotate_pdf(input_path: str, output_path: str, rotation: int = 90):
    """
    Rotate all pages in a PDF file.
    rotation: 90, 180, 270
    """
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(rotation)  # rotate_clockwise(rotation)
        writer.add_page(page)

    with open(output_path, "wb") as f:
        writer.write(f)

    return output_path
