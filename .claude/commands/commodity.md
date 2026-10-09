---
description: Add information to the Commodities Handbook and rebuild the PDF
argument-hint: add <information> | new <commodity> | build
---

You maintain the Commodities Handbook in `commodities/` (see `commodities/README.md`).
Source of truth: Markdown chapters in `commodities/sections/<NN_part>/<NN_chapter>.md`.

Request: $ARGUMENTS

1. **add <info>**: Find the chapter this belongs to (Grep `commodities/sections`). Put it in the most
   specific existing `##` section; dated market observations go under that chapter's `## Desk notes`
   as a bullet starting with today's date (`- **YYYY-MM-DD:** ...`), newest first. Cross-commodity
   ideas go in `10_appendix/02_trading_journal.md`. Keep the trader's wording; tidy only for clarity.
   If the info contradicts existing text, update the text and mention the change.
2. **new <commodity>**: Create a chapter in the right part folder, following the structure of
   existing chapters (contract specs table, supply, demand, price drivers, trading notes, Desk notes).
3. **build** (and after every add/new): run `python commodities/build_pdf.py` and report the page count.

Only use the Markdown subset documented in `commodities/README.md`. Don't state current prices
as facts unless the user supplied them; specs should match the exchange rulebook.
