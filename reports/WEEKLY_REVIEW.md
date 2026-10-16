# Complete weekly verification and corrections

Review date: 16 October 2026. Three delegated agents reviewed disjoint curriculum groups, and the parent reviewed the research level and integrated the corrections. Every lesson has an individual record in [weekly-review.json](weekly-review.json).

| Review assignment | Lessons | Detailed record |
| --- | ---: | --- |
| Levels 1–2 | 72 | [Week records](review-levels-1-2.json) |
| Level 3, Python bridge, Level 4 | 84 | [Week records](review-levels-3-bridge-4.json) |
| Levels 5–6 | 72 | [Week records](review-levels-5-6.json) |
| Level 7 | 36 | [Week records](review-level-7.json) |
| **Total** | **264** | **12,086 student, teacher and workbook sections** |

## What was checked

Each review covers the week's substantive explanation, supplied facts, worked and changed cases, calculations, teacher reasoning, independent question/key, workbook instructions, diagram source labels and project connection. Structural checks cover all sections and their reading metadata. Repeated common scaffolding was reviewed together and checked wherever it occurs; reviewers did not claim an independent word-by-word proof of every repeated sentence.

All existing sections and their order remain intact. The 268 original code placements remain byte-identical, and all 11,719 existing response positions are retained. Corrections retain the approved reading hierarchy and illustrations. Where a workbook needed a missing rule or data reference, that reference was added without moving its existing response fields. Supported examples and previously used W4 practice remain distinct from the currently selected independent assessment.

## Corrections made

- Level 1 Week 7: replaced an ambiguous fruit/seed classification rule with explicit observable toy labels and a review outcome for unknown contents.
- Level 1 Week 14: a square requires four right angles as well as four equal sides; equal sides alone also describe nonsquare rhombi.
- Level 1 Week 22: corrected a changed-case request that exceeded the remaining distinct cards in the stated fixed target.
- Level 2 Week 16: explained mean absolute error before asking learners to compare it.
- Level 2 Week 27: distinguished deterministic greedy token selection from probabilistic sampling.
- Level 2 Week 30: made replacement of the original state edge explicit before declaring the old trace invalid.
- Level 4 Week 24 and Level 5 calculation examples: repaired corrupted words and duplicated equals signs, including their graphical copies.
- Level 6 Weeks 6, 13, 18, 20 and 31: replaced stale selected-assessment keys with reasoning for the actual permission scope, transition graph, identifier inputs, retention boundary and source-injection disclosure case.
- Level 7: supplied missing sampling data, statistical assumptions, interval/test rules, pairing/units and named reporting metrics in standalone workbook exercises; corrected ambiguous condition wording.
- Across the programme: repaired stale section-number pointers, clarified compact versus full-week plans, corrected grade-transition labels and supplied missing workbook references where identified.

Fifty-six six-picture journeys were refreshed from corrected source facts or diagrams, covering 336 story graphics. Matching source diagrams and editable case packs were updated. Website route/project metadata and all supported practice were regenerated from the reviewed canonical source, so interactive prompts use the corrected facts too. Approved Level 1 Week 1 artwork remains unchanged.

Exact reviewed source replacements are recorded in [reviewed-source-corrections.json](reviewed-source-corrections.json). Preservation validation still requires every original explanation or its explicitly recorded correction to appear in the same week and edition; the ledger does not waive missing content.

## Validation

- All 264 week records are present, with 12,086 sections retained and no unresolved source issues reported by reviewers.
- [Content validation](content-validation.json): original material or exact reviewed correction retained; 118 source Python examples checked; no errors.
- [Teaching-method validation](teaching-method-validation.json): 264 distinct selected assessments, matched questions/keys, no teacher-only material in student metadata; no errors.
- [Download validation](download-validation.json): all **792 Word files and 792 PDFs**, **26,295 PDF pages**, and **5,874 checked pictorial placements**; no text/image errors.
- [Graphic validation](graphic-content-validation.json) and [browser SVG bounds](graphic-render-validation.json): 1,584 story graphics, including 336 regenerated graphics; no coverage, resolution or out-of-bounds text errors.
- 143 supported Python examples execute in the vendored browser runtime. All 528 formative questions and 719 repair links pass their checks.
- [Local links](link-validation.json): 811 HTML pages and 42,690 local targets checked with no errors.
- Final production build and TypeScript check pass. All 276 access/lesson checks pass. [Browser reading/accessibility checks](programme-format-browser.json) pass on 144 representative desktop/phone pages, with 48 automated accessibility audits and no reported page errors.
- All 5,416 protected image/download resources decrypt successfully. Website route metadata and interactive changed-case answers agree with the reviewed source for every week.

## Practical limits

This review checks curriculum content, internal consistency, toy calculations and executable examples. It does not establish learning outcomes, independently confirm every scientific claim, or substitute for observing actual students and teachers. Browser and automated accessibility audits do not constitute a screen-reader user study. The fictional-policy lessons do not determine real institutional or legal requirements.

The current teaching source is `content/programme.json`; `tools/build_programme.py` is the historical importer and would replace subsequent reviewed edits. Use the rendering/export workflow described in the repository README. Nothing was deployed, committed or pushed as part of this review.
