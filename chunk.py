import json
from pathlib import Path

BASE = Path(__file__).parent
IN_PATH = BASE / "data" / "pages_clean.json"
OUT_PATH = BASE / "data" / "chunks.json"

CHUNK_SIZE = 800  # characters (about 200 tokens)
OVERLAP = 150     # each chunk repeats ~150 characters of the previous one


def chunk_page(text, size=CHUNK_SIZE, overlap=OVERLAP):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))      # never go past the page

        # not at the end of the page -> don't cut a word in half
        if end < len(text):
            space = text.rfind(" ", start, end)
            if space > start:                   # -1 (not found) is ignored
                end = space

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        if end >= len(text):                    # reached the end -> done
            break
        start = max(end - overlap, start + 1)   # always move forward
    return chunks


if __name__ == "__main__":
    with open(IN_PATH, encoding="utf-8") as f:
        pages = json.load(f)

    print("page 3 chunk lengths:", [len(c) for c in chunk_page(pages[2]["text"])])

    records = []
    for page in pages:
        for i, chunk in enumerate(chunk_page(page["text"])):
            records.append({
                "chunk_id": f"p{page['pdf_page']}_c{i}",
                "page": page["pdf_page"],
                "text": chunk,
            })

    # --- tests ---
    text_by_page = {p["pdf_page"]: p["text"] for p in pages}
    ids = [r["chunk_id"] for r in records]
    assert len(set(ids)) == len(ids), "duplicate chunk ids"
    assert {r["page"] for r in records} == set(text_by_page), "a page has no chunks"
    for r in records:
        assert r["text"] and len(r["text"]) <= CHUNK_SIZE, r["chunk_id"]
        assert r["text"] in text_by_page[r["page"]], r["chunk_id"]

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    lengths = [len(r["text"]) for r in records]
    print(f"Saved {len(records)} chunks to {OUT_PATH}")
    print(f"min={min(lengths)} avg={sum(lengths)//len(lengths)} max={max(lengths)}")