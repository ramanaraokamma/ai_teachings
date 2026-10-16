# Approved graphic approach across the programme

All 264 lessons now include a six-picture visual concept journey in the student lesson, teacher guide and workbook: 1,584 SVG illustrations with matching high-resolution PNGs and 4,752 placements across the three editions. The six approved Level 1 Week 1 illustrations are retained exactly.

Each journey connects the lesson’s supplied case and facts, deciding steps, close-up mechanism or numerical model, changed condition, explanation and limits, and project evidence. Charts retain the reviewed values and labels. Examples include colour-counting pencils, a branching decision flowchart, session-state changes, tensor values, error-rate plots, storage copies and restricted identity linkage. Labels carry meaning alongside colour. Icons are schematic cues, not claims about an actual model’s architecture.

Student lessons include plain-language transcripts and pause-and-explain prompts. Teacher guides add presentation guidance, misconception checks and the existing supported practice reasoning. Workbooks include places to draw and explain. Worked graphics remain separate from the reserved independent assessment.

Website lessons link directly to the six-picture journey. The image viewer provides Fit whole picture and Read labels modes, including horizontal scrolling on a phone. Offline pages link to PNG and editable SVG versions. Full Word and PDF editions include the same graphics and explanations.

Source and validation:

- `tools/build_graphic_journeys.py` rebuilds the journeys from canonical lesson content; approved references are retained in `tools/graphic-references/week1/`.
- `scripts/render-graphic-journeys.mjs` renders PNGs and checks every SVG’s text bounds in a real browser.
- `reports/graphic-content-validation.json` checks lesson/role coverage, source boundaries, references and resolution.
- `reports/graphic-render-validation.json` records geometry checks for all 1,584 graphics.
- `reports/graphic-browser-validation.json` records representative website checks across all eight programme groups, desktop and phone.
- `reports/download-validation.json` checks the Word/PDF text and actual embedded/painted pictures against canonical content.

These checks establish rendering and content consistency. They do not establish improved classroom outcomes; the prepared real classroom pilot remains the next way to assess that.

Complete final teaching folder: `outputs/ai-academy-complete-programme/`. The website source remains at the repository root. No deployment is part of this update.

Verified website results: production build and 276 access/lesson checks passed. All 5,416 protected resources decrypted successfully. The representative graphic checks passed on 32 student/teacher desktop/phone pages across all eight programme groups. The 24 automated accessibility page audits reported no violations or browser errors; keyboard and image-view controls passed. This is automated testing, not a screen-reader user study.

All 792 Word files and 792 PDFs passed text and image validation: 18,829 PDF pages and 5,874 checked pictorial placements. Original-content checks retained 144 original weeks, all 252 later lessons, 1,874 original pictures and 118 executable source examples. All 811 local HTML pages passed link checks.
