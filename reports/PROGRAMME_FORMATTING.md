> A subsequent [complete weekly review](WEEKLY_REVIEW.md) corrected content and refreshed the teaching editions while retaining this approved reading hierarchy. File-preservation statements below describe the original formatting rollout.

# Approved reading format across the complete programme

The approved Level 1 Week 1 design is applied throughout all 264 lessons: seven 36-week levels and the 12-week Python Readiness Bridge. The section audit covers **12,086 sections** in student lessons, teacher guides and workbooks. The approved Week 1 canonical object and its six downloads were retained.

Each section has a purpose line and a visible heading hierarchy. Explanations use shorter reading chunks and selective emphasis from the learner glossary. Examples, questions, teacher keys, cautions, numbered steps and genuine checklists have distinct treatments. Parallel Input–Process–Output definitions use aligned cards where the source supplies that structure; the cards stack on a phone.

The formatting rules use each lesson’s own titles, cases, vocabulary and existing section roles. They do not copy Week 1’s bus or umbrella explanations into other topics. The migration retains the original text and cells; 49 separately stored table headers were restored to their displayed header rows. Graphics, coding labs, question/key content and independent assessment cases remain present. A repeated case is identified as practice or the same recorded attempt, rather than new mastery evidence.

All three editions are updated. Editable Word files use real headings, paragraph breaks, emphasis and shaded notes. PDFs use the browser layout; unusually wide or text-heavy tables print as labelled records so complete cell text remains readable. Normal grids and short tables retain their table layout. Dynamic browser practice controls are excluded from the printable lessons because their canonical practice content already appears in the lesson.

Implementation and evidence:

- `tools/format_programme.py` applies the approved rules and checks source-text/cell preservation while retaining the approved Week 1 reference.
- `reports/programme-formatting.json` lists every section, its purpose and formatting coverage.
- `tests/reading-format.mjs` checks reconstruction of original text, headings, checklist structure and all section-purpose records.
- `tools/export_formatted_week.mjs` prints selected lessons in a bounded browser pool; `tools/export_pdf_local.py` dispatches formatted editions to it.
- `reports/download-validation.json` checks actual Word/PDF text and embedded or painted diagrams against canonical content.
- `tests/programme-reading-browser.mjs` checks representative first/middle/final lessons across all eight programme groups, all three views and both desktop and phone widths, including accessibility audits.

These are presentation and content-retention checks. They do not establish classroom learning outcomes or replace a screen-reader user study. Real classroom pilot materials remain available for collecting actual evidence.

Complete teaching folder: `outputs/ai-academy-complete-programme/`. The website source remains at the repository root. No deployment is included.

Final validation results: all 792 Word files and 792 PDFs passed text and image checks, covering 26,139 PDF pages and 5,874 pictorial placements. The production build, TypeScript checks and all 276 access/lesson checks passed. All 5,416 protected resources decrypted successfully. Representative browser checks passed on 144 pages across the first/middle/final lessons in all eight programme groups, with 48 accessibility audits reporting no violations. The existing 24 learning-feature accessibility audits and portfolio/practice/Python checks also passed. The approved Week 1 download bytes were retained.
