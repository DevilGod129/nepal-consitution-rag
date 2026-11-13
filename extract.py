import json
from pathlib import Path
from pypdf import PdfReader

BASE = Path(__file__).parent
PDF_PATH = BASE / "data" / "constitution.pdf"
OUT_PATH = BASE / "data" / "pages.json"


def extract_pages(pdf_path):
    reader = PdfReader(pdf_path)
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        pages.append({"pdf_page": page_number, "text": text})
    return pages


if __name__ == "__main__":
    pages = extract_pages(PDF_PATH)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    empty = sum(1 for p in pages if not p["text"].strip())
    print(f"Saved {len(pages)} pages to {OUT_PATH} ({empty} empty)")