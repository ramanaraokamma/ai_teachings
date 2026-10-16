> This was the approved Week 1 review stage. The format has since been applied throughout the programme; see `PROGRAMME_FORMATTING.md`.

# Level 1 Week 1 — reading format review

This is a presentation revision of the complete student lesson, teacher guide and workbook for `ai-1/1`. All 48 sections were reviewed: 18 student sections, 9 teacher sections and 21 workbook sections. The remaining 263 lessons retain their existing format.

The teacher guide’s Section 2, **Explain the mechanism**, now has an explicit section heading, three Input–Process–Output definition cards, descriptive subheadings, shorter paragraphs, bold key terms, distinct example and question panels, numbered reasoning steps and visible precision/caution notes. The Claim–Evidence–Conclusion table now uses its real column headers rather than the first answer row.

The same hierarchy is applied across every Week 1 section. Each has a purpose line; existing subheadings are visibly styled. Teacher questions and keys have distinct labels, the learner self-check uses a real checklist, alternative timing plans are identified, and repeated greenhouse tasks point to one recorded first attempt. Original text, diagrams, questions and assessments remain in canonical content. Presentation metadata changes how they are displayed rather than replacing the explanations with summaries. Desktop definition cards stack vertically on a phone.

The Week 1 Word editions use real headings, paragraph breaks, emphasis and shaded teaching notes. PDFs are printed from the actual formatted browser layout. Text/image checks caught the older PDF renderer omitting a run of content; the browser exporter retains that complete explanation and passes validation.

Review:

- `teacher/ai-1-week-01.html#section-2`
- `student/ai-1-week-01.html`
- `workbook/ai-1-week-01.html`
- `downloads/teacher/ai-1-week-01.pdf`
- `outputs/week-01-format-review/index.html`

Implementation: `tools/format_week1.py`, `tools/reading_style.py`, `tools/export_formatted_week.mjs`, `components/formatted-reading.tsx`, and `lib/reading-format.ts`. The browser exporter uses the optional Playwright module configured by `ACADEMY_PLAYWRIGHT_MODULE` (or the existing local rendering tools) and Chrome/Chromium.

Validation: original-content preservation; formatted-text reconstruction and Week 1 scope checks; real-browser desktop/phone layout checks; production build/access checks; and text plus actual-image validation for all six changed Word/PDF downloads. No deployment is included.

All 48 section overviews and visible heading treatments passed website checks, including all 21 workbook section headings and the four-item self-check. Desktop and phone definition-card layouts passed. All 24 automated accessibility audits passed with no violations; the production build and all 276 access checks passed. Original-content and changed-download text/image checks passed. This is a review edition for Week 1 only.
