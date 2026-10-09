# Commodities Handbook

A specialist reference across all major commodities, kept as editable Markdown and rebuilt into a PDF.

## Build the PDF

```
python commodities/build_pdf.py
```

Output: `commodities/output/Commodities_Handbook.pdf` (cover, clickable contents, PDF bookmarks, page numbers).
Requires `reportlab` (`pip install reportlab`).

## Add or update information

- **Edit a chapter:** open the relevant file in `commodities/sections/` and add text (each chapter ends with a *Desk notes* section for your own observations).
- **Add a commodity:** create a new `.md` file in the right folder, e.g. `sections/04_base_metals/06_cobalt.md`, starting with `# Title`. The number prefix sets the order.
- **Add a new part:** create a new folder, e.g. `sections/11_crypto_and_digital/`. The folder name becomes the part title (put a custom title in `_title.txt` inside the folder if you want punctuation).
- **Ask Claude:** `/commodity add <info>` files the info in the right chapter and rebuilds the PDF.

Supported formatting: `#`/`##`/`###` headings, paragraphs, `- ` bullets (indent 2 spaces for sub-bullets), `1. ` lists, `| tables |`, `> ` callout boxes, `**bold**`, `*italic*`.

> Contract specifications change. Verify against the exchange rulebook before trading. Nothing here is investment advice.
