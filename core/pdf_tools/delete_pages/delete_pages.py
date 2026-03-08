from pypdf import PdfReader, PdfWriter

def get_total_pages(file_path: str) -> int:
    reader = PdfReader(file_path)
    return len(reader.pages)

def parse_pages(text: str) -> list[int]:
    pages = set()

    parts = text.split(",")

    for part in parts:
        part = part.strip()

        if "-" in part:
            start, end = part.split("-")
            start = int(start)
            end = int(end)

            for i in range(start, end + 1):
                pages.add(i)
        else:
            pages.add(int(part))

    return sorted(pages)

def validate_pages(pages: list[int], total_pages: int) -> bool:
    for p in pages:
        if p < 1 or p > total_pages:
            return False
    return True

def delete_pages(input_path: str, output_path: str, pages_to_delete: list[int]):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    delete_set = set(pages_to_delete)

    for i in range(len(reader.pages)):
        if (i + 1) not in delete_set:
            writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)
