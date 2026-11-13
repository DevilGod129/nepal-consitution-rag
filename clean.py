import json
import re
from pathlib import Path

BASE = Path(__file__).parent
IN_PATH = BASE / "data" / "pages.json"
OUT_PATH = BASE / "data" / "pages_clean.json"

# step 4: (bad, good) pairs -- a space before punctuation
PUNCT_FIXES = [
    (" :", ":"),
    (" ,", ","),
    (" ;", ";"),
    (" 's", "'s"),
]

# step 5: known damaged spots (include neighbour words so we never
# touch correct text like the "itutional" inside "constitutional")
GLITCH_FIXES = {
    "republic an": "republican",
    "cit xizen": "citizen",
    "Right totutional remedies": "Right to constitutional remedies",
    "obtain itutional remedies": "obtain constitutional remedies",
}


def clean_text(text):
    # step 1: remove the "(N)" page header at the very start
    text = re.sub(r"^\s*\(\d+\)\s*", "", text)

    # step 2: join words split across lines by a hyphen
    text = text.replace("-\n", "-")

    # step 3: collapse all whitespace into single spaces
    text = re.sub(r"\s+", " ", text).strip()

    # step 4: fix space before punctuation
    for bad, good in PUNCT_FIXES:
        text = text.replace(bad, good)

    # step 5: patch known glitches
    for bad, good in GLITCH_FIXES.items():
        text = text.replace(bad, good)

    return text


if __name__ == "__main__":
    with open(IN_PATH, encoding="utf-8") as f:
        pages = json.load(f)

    cleaned_pages = []
    for page in pages:
        cleaned_pages.append(
            {"pdf_page": page["pdf_page"], "text": clean_text(page["text"])}
        )

    # --- tests ---
    by_page = {p["pdf_page"]: p["text"] for p in cleaned_pages}
    assert by_page[3].startswith("Part-1 Preliminary 1. Constitution as the fundamental l aw: (1) This Constitution is")
    assert by_page[64].startswith("(2) Election under clause (1) shall be so held that")
    assert "46. Right to constitutional remedies: There shall be a right to obtain constitutional remedies" in by_page[26]
    for p in cleaned_pages:
        assert "\n" not in p["text"] and "  " not in p["text"], p["pdf_page"]

    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(cleaned_pages, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(cleaned_pages)} cleaned pages to {OUT_PATH}")