# Curriculum 3 learning sequence

Curriculum 3 is a new seven-level progression beginning in Grade 6. This release contains **AI 1 Weeks 1–36, AI 2 Weeks 1–36, AI 3 Weeks 1–36 and AI 4 Weeks 1–4**, each authored as a complete student lesson, workbook and teacher guide. It does not claim to complete all seven levels. The other **140 week positions are a proposed sequence**, explicitly labelled Planned with no lesson links. The existing four-level, 144-week edition remains available.

## Released packages

| Week | Chapter | Independent evidence |
| --- | --- | --- |
| 1 | Evidence and decision mechanisms | Classify the components of a new hybrid system and limit the conclusion |
| 2 | Representations and information paths | Construct different records with the same total and explain lost information |
| 3 | Sensors and measurement | Design a comparison that separates location from device differences |
| 4 | Rules and learned patterns | Fit a threshold, trace a new prediction and distinguish fitting from independent checking |
| 5 | Images as numerical grids | Encode different grids with equal counts and identify discarded spatial information |
| 6 | Sound as sampled information | Construct different sequences consistent with the same retained samples |
| 7 | Categories and operational labels | Apply ordered category rules to unfamiliar equipment requests and distinguish agreement from correctness |
| 8 | Features and useful distinctions | Construct examples with identical inputs but different labels and reject a copied target |
| 9 | Algorithms and changing state | Trace two variables, explain copied values and locate the first incorrect update |
| 10 | Conditions and boundary cases | Trace one branch using current values and test equality in an unfamiliar display procedure |
| 11 | Loops and stopping rules | Trace a countdown, include zero iterations and explain a loop that cannot stop |
| 12 | Debugging with revealing tests | Choose revealing boundary tests, repair a comparison and retain regression evidence |
| 13 | Fitting a pattern from examples | Fit a new distance task with fresh error counts and a justified limit on predictions |
| 14 | Constructing a classifier | Construct and trace a new ribbon classifier with valid inputs, explicit rejection and recorded model version |
| 15 | Keeping final tests unseen | Preserve predictions and distinguish an independent ribbon test from a revision informed by its results |
| 16 | Uncertainty and review | Comparing distance possibilities, matching review evidence to the missing fact, and preserving an unresolved outcome |
| 17 | Predictions and observations | Separating model outputs from observed outcomes, applying the exact boundary rule, and reporting assessed and unassessed cases honestly |
| 18 | Confidence and correctness | Separating score meanings from probabilities and checking confidence claims without hiding missing outcomes |
| 19 | Similarity and selected features | Computing feature contributions, preserving ties, and separating similarity from mandatory requirements |
| 20 | Recommendations and feedback | Eligibility before scoring, a tied activity recommendation, the inclusive time boundary, unknown availability and limits of click feedback |
| 21 | Data quality and documented repair | Source-backed repairs, distinct trial identity, preserved measured zero, explicit missing and conflicting records, and the corrected reporting denominator |
| 22 | Sampling and coverage | Target and sample distinctions, missing feature combinations, distinct-case counts, feasible coverage plans and seven assessed outcomes from eight selected cases |
| 23 | Fractions and performance comparisons | Exact fractions independently checked; all canonical and browser print pages visually inspected. |
| 24 | Privacy and data minimisation | Purpose-to-field choices, coded-record links and small-group disclosure examples checked independently; all print pages inspected. |
| 25 | Generation retrieval and calculation | Notice versions, unsupported claims and all four capacity calculations independently checked. |
| 26 | Specifying and testing prompts | Complete, missing and conflicting record cases checked against explicit criteria; fair prompt-comparison reasoning reviewed. |
| 27 | Verifying claims and quantities | Checking each claim against its source and recalculating length and mass with consistent units |
| 28 | Human authority and permission | Matching proposed actions to the approved actor, version, destination, time and quantity limits |
| 29 | A problem worth solving | Defining a bounded user problem and measuring useful matches alongside avoided errors |
| 30 | Requirements and a simple baseline | Applying complete compatibility requirements and comparing a prototype fairly with a credible manual baseline |
| 31 | Designing a complete decision process | Complete algorithm traces preserve validation, both compatibility conditions, first-match selection and finite termination; independent room cases distinguish no match from missing input |
| 32 | Building and tracing a paper prototype | Independent equipment traces cover first-fit selection, catalogue exhaustion and validation; saved instruction versions distinguish execution mistakes from design defects |
| 33 | Testing routine cases | Routine-case expectations and independent equipment results were checked; all 62 valid catalogue-B requests confirm that B3 and B4 cannot be first-match outputs |
| 34 | Testing boundaries and varied conditions | Inclusive boundaries, invalid-field responses and third- and fourth-row successes under labelled catalogue variations were independently checked |
| 35 | Improving and checking regressions | Distinguishing an equality repair from a new first-fit regression, preserving evidence and protecting reserved final evaluation cases |
| 36 | Evaluating and explaining your project | Comparing final evidence with a manual baseline, rejecting unsupported reliability and speed claims, and distinguishing repair checks from unseen evaluation |

Each package has a prerequisite check, three outcomes, five explanatory sections, a labelled figure, worked reasoning, supported practice, five workbook tasks, answer explanations, two 45-minute teaching sequences, misconceptions, assessment criteria, support, extension and a next-week connection. Classroom effectiveness and pacing have not yet been validated with students.

## Seven-level proposal

| Level | Typical grade | Focus | Rebuilt packages |
| --- | --- | --- | --- |
| AI 1 | 6 | Foundations | 36 of 36 |
| AI 2 | 7 | Programming and Data | 36 of 36 |
| AI 3 | 8 | Machine Learning | 36 of 36 |
| AI 4 | 9 | Neural Networks | 4 of 36 |
| AI 5 | 10 | Generative AI Systems | 0 of 36 |
| AI 6 | 11 | AI Engineering | 0 of 36 |
| AI 7 | 12 | Research and Advanced Projects | 0 of 36 |

The 252 individually named week positions, level prerequisites and exit evidence are in `curriculum-v3/progression.json`. Grade is a pacing guide, not an automatic placement rule. The sequence is not an assertion that corresponding complete lessons exist.

## Access and hosting

Sign in through the existing student or teacher passcode flow. The role dashboard links to `/learn/student/curriculum` or `/learn/teacher/curriculum`. New chapters live at `/learn/{role}/curriculum/{level}/{week}` with `resource=lesson`, `workbook` or `guide`.

The existing Cloudflare Worker, ASSETS binding, signed sessions and protected resource endpoint are preserved. Teacher guides and their Word/PDF downloads require a teacher session. Student URLs requesting a guide return 404. Planned chapters return 404. Unauthenticated chapter/map requests redirect to sign-in; unauthenticated downloads return 401. Protected responses remain private and no-store.

Canonical JSON and answer keys are imported only by server code. The 784 Curriculum 3 public blobs are encrypted: 336 DOCX files, 336 PDFs and 112 diagram PNGs. No plaintext teacher documents are placed under `public/`. The source repository itself contains private teacher material and must be shared accordingly.

This revision has been tested locally. It has not been deployed to the live Cloudflare site.

## One source for web and print

`curriculum-v3/ai-*-week-*.json` holds the content. The web renderer and document generator read the same source. `curriculum-v3/releases.json` records the exact source hash and protected document/diagram references. `print-review.json` binds the print review to the source, renderer scripts and rendered artifact bytes.

`npm run build` now rejects released packages whose source no longer matches their reviewed downloads. It also verifies role assignments and decrypts/hash-checks all new resources. This is an alignment check, not an automated judgment of educational quality.

### Revising or adding a package

1. Author the canonical chapter and update the roadmap if necessary. Add its server import in `lib/curriculum-v3.ts`.
2. Render figures with `scripts/render-v3-diagrams.cjs`, providing `ACADEMY_NODE_PACKAGES` pointing to the bundled Node packages containing Sharp.
3. Run `scripts/build-v3-documents.py --out work/v3-docs --diagrams work/v3-diagrams` using the bundled Python runtime with python-docx.
4. Render **every** generated DOCX using the Documents skill's `render_docx.py --emit_pdf`. Place its PDF and page PNGs under `work/v3-render/{document-stem}/`.
5. Run `scripts/check-v3-print.py` to compare canonical content with the DOCX and PDF text. It creates a candidate receipt; it does not certify visual quality.
6. Inspect every page image for readability, clipping, table breaks, diagrams, writing space and pagination. Correct issues and rerender. After that review, complete the candidate's date/method and set each reviewed chapter's `visualReview` to `Every rendered page inspected`; save it as `curriculum-v3/print-review.json`.
7. Run `node scripts/release-v3-resources.mjs`. It refuses changed or unreviewed artifact bytes and registers the complete package in protected storage.
8. Run the build, TypeScript and access tests; check the web pages on desktop/mobile and browser print. Keep planned weeks unlinked until their complete package is ready.

Do not update a source hash simply to suppress the mismatch check. It protects students and teachers from receiving different editions.

## Validation of Weeks 1–6 (2026-09-14)

- Production Cloudflare build and TypeScript check passed.
- 31 test groups passed, retaining all 432 existing lesson/workbook/guide route checks and adding all 18 rebuilt routes.
- All 36 new document downloads were checked for authentication, role separation and exact byte hashes.
- All 2,215 protected resources decrypted successfully.
- All 18 Word documents were rendered; all **72 PDF page images** were visually inspected. Canonical text was checked in every DOCX and PDF, with teacher answers excluded from student documents.
- All 18 rebuilt pages passed desktop 1280-pixel and mobile 390-pixel checks: 36 viewport checks, no horizontal page overflow or broken images. Both role maps were checked at both widths.
- All 18 web resources were printed to PDF for browser-print inspection. Downloadable PDFs are the reviewed, paginated print editions.
- A deliberate source change was rejected by the stale-download guard, then the source was restored.

Grade 6 AI 1 Foundations, Grade 7 AI 2 Programming and Data, and Grade 8 AI 3 Machine Learning are complete with 36 weekly packages each. Grade 9 AI 4 has Weeks 1–4 complete. Grade 9 Weeks 5–36 and Grades 10–12 require individually authored chapters, exercises, solutions and print review; the progression map is not a substitute for that work.

## Week 7 completion (2026-09-15)

Categories and operational labels adds a complete 90-minute package: a five-page lesson, three-page workbook, four-page teacher guide, and ordered-check diagram. All 12 Word/PDF page images were visually reviewed; source text and teacher-answer separation passed.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with seven released packages: 21 rebuilt routes and 42 matching document downloads. All 2,222 protected resources decrypted successfully. Week 7 passed six desktop/mobile viewport checks plus both protected maps. Its three browser-print layouts were inspected; a print rule now keeps workbook questions with their response space. Word/PDF downloads remain the fixed, reviewed print editions.

Weeks 1–7 are complete in the repository; 245 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed.

## Week 8 completion (2026-09-15)

Features and useful distinctions includes a five-page lesson, three-page workbook, four-page teacher guide and a four-row feature-selection diagram. Students construct counterexamples, separate features from targets and explain information leakage through an inspection timeline. Definitions were cross-checked against [Google feature representations](https://developers.google.com/machine-learning/crash-course/numerical-data/feature-vectors) and [scikit-learn data leakage guidance](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage); the classroom scenarios and exercises are original.

All 12 print pages were visually inspected and canonical text matched the Word/PDF editions. The Cloudflare build, TypeScript and all 31 access-test groups passed, including 24 rebuilt routes and 48 document downloads. All 2,229 resources decrypted. Week 8 passed six chapter viewport checks and both maps at desktop/mobile widths. All three browser-print layouts were reviewed and workbook prompts remain with their response areas.

Weeks 1–8 are complete in the repository; 244 remain planned. Hosting and authentication code are unchanged. This revision has not been deployed.

## Week 9 completion (2026-09-15)

Algorithms and changing state adds a five-page lesson, three-page workbook, four-page teacher guide and an annotated transition diagram. It introduces current-state updates, replacement versus addition, instruction order, number-value copying and the limits of a matching final result. Independent work traces two variables and a reordered procedure; the teacher guide includes an uncoached retry.

All 12 print pages were visually reviewed and canonical text matched the Word/PDF editions. Production build, TypeScript and all 31 access-test groups passed with 27 rebuilt routes and 54 document downloads. All 2,236 protected resources decrypted. Six chapter viewport checks and both maps passed. Browser-print text matched every canonical section, and the three browser-print layouts were visually reviewed.

Weeks 1–9 are complete in the repository; 243 remain planned. Cloudflare hosting and role controls are unchanged; no deployment has been performed.

## Week 10 completion (2026-09-15)

Conditions and boundary cases adds a complete 90-minute package: a five-page lesson, three-page workbook, four-page teacher guide and a diagram comparing values below, at and above a threshold. Students distinguish current state from starting state, inclusive from strict comparisons, one selected branch from repeated testing, and unknown input from false. An independent brightness-display task and fresh retry check transfer. All 12 rendered page images were inspected, and canonical text and student/teacher answer separation passed.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with ten released packages: 30 rebuilt routes and 60 matching document downloads. All 2,243 protected resources decrypted successfully. Week 10 passed six desktop/mobile chapter checks plus both protected maps. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–10 are complete in the repository; 242 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes still require student use and teacher feedback.

## Week 11 completion (2026-09-15)

Loops and stopping rules is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: trace a countdown, include zero iterations and explain a loop that cannot stop.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 11 released packages, 33 rebuilt routes and 66 matching document downloads. All 2,250 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–11 are complete in the repository; 241 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 12 completion (2026-09-15)

Debugging with revealing tests is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: choose revealing boundary tests, repair a comparison and retain regression evidence.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 12 released packages, 36 rebuilt routes and 72 matching document downloads. All 2,257 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–12 are complete in the repository; 240 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 13 completion (2026-09-15)

Fitting a pattern from examples is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: fit a new distance task with fresh error counts and a justified limit on predictions.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 13 released packages, 39 rebuilt routes and 78 matching document downloads. All 2,264 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–13 are complete in the repository; 239 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

Conceptual check for Week 13: evidence used to choose a model must be distinguished from evaluation on held-out examples, following [scikit-learn evaluation guidance](https://scikit-learn.org/stable/modules/cross_validation.html). The paper examples and exercises are original classroom tasks.

## Week 14 completion (2026-09-15)

Constructing a classifier is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: construct and trace a new ribbon classifier with valid inputs, explicit rejection and recorded model version.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 14 released packages, 42 rebuilt routes and 84 matching document downloads. All 2,271 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–14 are complete in the repository; 238 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

Teacher browser-print regression: all 14 released guides retained their complete canonical text after spacing adjustments. Every printed page was inspected; closing assessment, support and next-week sections now stay together. Type remains 11 pt.

## Week 15 completion (2026-09-15)

Keeping final tests unseen is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: preserve predictions and distinguish an independent ribbon test from a revision informed by its results.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 15 released packages, 45 rebuilt routes and 90 matching document downloads. All 2,278 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–15 are complete in the repository; 237 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 16 completion (2026-09-15)

Uncertainty and review is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: comparing distance possibilities, matching review evidence to the missing fact, and preserving an unresolved outcome.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 16 released packages, 48 rebuilt routes and 96 matching document downloads. All 2,285 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–16 are complete in the repository; 236 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 17 completion (2026-09-16)

Predictions and observations is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: separating model outputs from observed outcomes, applying the exact boundary rule, and reporting assessed and unassessed cases honestly.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 17 released packages, 51 rebuilt routes and 102 matching document downloads. All 2,292 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–17 are complete in the repository; 235 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 18 completion (2026-09-16)

Confidence and correctness is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: separating score meanings from probabilities and checking confidence claims without hiding missing outcomes.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 18 released packages, 54 rebuilt routes and 108 matching document downloads. All 2,299 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–18 are complete in the repository; 234 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 19 completion (2026-09-16)

Similarity and selected features is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: computing feature contributions, preserving ties, and separating similarity from mandatory requirements.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 19 released packages, 57 rebuilt routes and 114 matching document downloads. All 2,306 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–19 are complete in the repository; 233 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 20 completion (2026-09-16)

Recommendations and feedback is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: eligibility before scoring, a tied activity recommendation, the inclusive time boundary, unknown availability and limits of click feedback.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 20 released packages, 60 rebuilt routes and 120 matching document downloads. All 2,313 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–20 are complete in the repository; 232 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 21 completion (2026-09-16)

Data quality and documented repair is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: source-backed repairs, distinct trial identity, preserved measured zero, explicit missing and conflicting records, and the corrected reporting denominator.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 21 released packages, 63 rebuilt routes and 126 matching document downloads. All 2,320 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–21 are complete in the repository; 231 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 22 completion (2026-09-16)

Sampling and coverage is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: target and sample distinctions, missing feature combinations, distinct-case counts, feasible coverage plans and seven assessed outcomes from eight selected cases.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 22 released packages, 66 rebuilt routes and 132 matching document downloads. All 2,327 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–22 are complete in the repository; 230 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 23 completion (2026-09-16)

Fractions and performance comparisons is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: exact fractions independently checked; all canonical and browser print pages visually inspected..

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 23 released packages, 69 rebuilt routes and 138 matching document downloads. All 2,334 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–23 are complete in the repository; 229 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 24 completion (2026-09-16)

Privacy and data minimisation is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: purpose-to-field choices, coded-record links and small-group disclosure examples checked independently; all print pages inspected..

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 24 released packages, 72 rebuilt routes and 144 matching document downloads. All 2,341 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–24 are complete in the repository; 228 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 25 completion (2026-09-16)

Generation retrieval and calculation is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: notice versions, unsupported claims and all four capacity calculations independently checked..

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 25 released packages, 75 rebuilt routes and 150 matching document downloads. All 2,348 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–25 are complete in the repository; 227 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 26 completion (2026-09-17)

Specifying and testing prompts is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: complete, missing and conflicting record cases checked against explicit criteria; fair prompt-comparison reasoning reviewed..

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 26 released packages, 78 rebuilt routes and 156 matching document downloads. All 2,355 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–26 are complete in the repository; 226 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 27 completion (2026-09-17)

Verifying claims and quantities is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: checking each claim against its source and recalculating length and mass with consistent units.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 27 released packages, 81 rebuilt routes and 162 matching document downloads. All 2,362 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–27 are complete in the repository; 225 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 28 completion (2026-09-17)

Human authority and permission is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: matching proposed actions to the approved actor, version, destination, time and quantity limits.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 28 released packages, 84 rebuilt routes and 168 matching document downloads. All 2,369 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–28 are complete in the repository; 224 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 29 completion (2026-09-17)

A problem worth solving is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: defining a bounded user problem and measuring useful matches alongside avoided errors.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 29 released packages, 87 rebuilt routes and 174 matching document downloads. All 2,376 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–29 are complete in the repository; 223 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 30 completion (2026-09-17)

Requirements and a simple baseline is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: applying complete compatibility requirements and comparing a prototype fairly with a credible manual baseline.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 30 released packages, 90 rebuilt routes and 180 matching document downloads. All 2,383 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–30 are complete in the repository; 222 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 31 completion (2026-09-23)

Designing a complete decision process is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: complete algorithm traces preserve validation, both compatibility conditions, first-match selection and finite termination; independent room cases distinguish no match from missing input.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 31 released packages, 93 rebuilt routes and 186 matching document downloads. All 2,390 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–31 are complete in the repository; 221 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 32 completion (2026-09-23)

Building and tracing a paper prototype is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: independent equipment traces cover first-fit selection, catalogue exhaustion and validation; saved instruction versions distinguish execution mistakes from design defects.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 32 released packages, 96 rebuilt routes and 192 matching document downloads. All 2,397 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–32 are complete in the repository; 220 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 33 completion (2026-09-23)

Testing routine cases is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: routine-case expectations and independent equipment results were checked; all 62 valid catalogue-B requests confirm that B3 and B4 cannot be first-match outputs.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 33 released packages, 99 rebuilt routes and 198 matching document downloads. All 2,404 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–33 are complete in the repository; 219 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 34 completion (2026-09-24)

Testing boundaries and varied conditions is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: inclusive boundaries, invalid-field responses and third- and fourth-row successes under labelled catalogue variations were independently checked.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 34 released packages, 102 rebuilt routes and 204 matching document downloads. All 2,411 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–34 are complete in the repository; 218 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 35 completion (2026-09-25)

Improving and checking regressions is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: distinguishing an equality repair from a new first-fit regression, preserving evidence and protecting reserved final evaluation cases.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 35 released packages, 105 rebuilt routes and 210 matching document downloads. All 2,418 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–35 are complete in the repository; 217 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Week 36 completion (2026-09-25)

Evaluating and explaining your project is a complete 90-minute package with 5 lesson pages, 3 workbook pages, 4 teacher-guide pages and a labelled explanatory diagram. All 12 rendered pages were visually inspected. Canonical text and student/teacher answer separation passed. The independent task checks: comparing final evidence with a manual baseline, rejecting unsupported reliability and speed claims, and distinguishing repair checks from unseen evaluation.

The Cloudflare build, TypeScript check and all 31 access-test groups passed with 36 released packages, 108 rebuilt routes and 216 matching document downloads. All 2,425 protected resources decrypted successfully. Six desktop/mobile chapter checks and both protected maps passed. All three browser-print layouts were inspected, with canonical text present and workbook questions kept with their response spaces.

Weeks 1–36 are complete in the repository; 216 weekly packages remain planned. Cloudflare hosting and role controls are preserved. These changes have not been deployed. Classroom pacing and learning outcomes require student use and teacher feedback.

## Grade 7 AI 2 Weeks 1–6 completion (2026-09-26)

Six 90-minute packages now have aligned student lessons, workbooks, teacher guides, explanatory diagrams and protected Word/PDF downloads. The programming renderer preserves Python indentation and uses the Grade 7 level identity.

| Week | Chapter |
| --- | --- |
| 1 | From a paper algorithm to Python |
| 2 | Values variables and types |
| 3 | Expressions and operator order |
| 4 | Boolean conditions |
| 5 | Branching and boundary tests |
| 6 | Loops and trace tables |

Every canonical print page and each browser print layout was visually reviewed. Text checks confirm lesson, workbook and guide alignment. Executed examples and independent cases cover arithmetic, copied values, Boolean boundaries, branch selection and loop accumulation. All six weeks passed desktop/mobile checks for the three resources and protected maps.

The Cloudflare build, TypeScript check and all 31 access-test groups passed. The release contains 42 rebuilt packages, 126 resource pages and 252 matching document downloads; all 2,467 protected resources decrypted. Student sessions cannot access teacher guides or teacher downloads. Hosting configuration and session controls are preserved.

Grade 7 Weeks 7–36 remain planned. These changes have not been deployed; classroom pacing and learning outcomes have not been validated with students.

## Grade 7 AI 2 Week 7 completion (2026-09-26)

Lists and indexing includes a five-page student lesson, three-page workbook, four-page teacher guide and a position-to-value diagram. Every canonical print page and all three browser print layouts were inspected. Executable checks cover worked examples, intentional IndexError, repaired access, list updates, repeated values, independent running totals, empty lists and fresh retry cases.

The build, TypeScript check and all 31 access-test groups passed with 43 rebuilt packages and 258 matching document downloads. All 2,474 protected resources decrypted. Six desktop/mobile resource checks and both protected maps passed. Browser print text matches the source and workbook prompts stay with response spaces.

Grade 7 Weeks 1–7 are complete; Weeks 8–36 remain planned. Cloudflare hosting and student/teacher controls are preserved. Changes are not deployed, and classroom effectiveness remains untested.

## Grade 7 AI 2 Week 8 completion (2026-09-26)

Functions and arguments includes a five-page student lesson, three-page workbook, four-page teacher guide and an argument-to-parameter diagram. Every canonical print page and all three browser print layouts were inspected. Executable checks cover definition versus call, positional arguments, zero results, missing-argument TypeError, ignored-argument repairs, independent functions, swapped inputs, fresh retry cases and the limits of input validation.

The build, TypeScript check and all 31 access-test groups passed with 44 rebuilt packages and 264 matching document downloads. All 2,481 protected resources decrypted. Six desktop/mobile resource checks and both protected maps passed. Browser print text matches the source and workbook prompts stay with response spaces.

Grade 7 Weeks 1–8 are complete; Weeks 9–36 remain planned. Cloudflare hosting and student/teacher controls are preserved. Changes are not deployed, and classroom effectiveness remains untested.

## Grade 7 AI 2 Week 9 completion (2026-09-26)

Return values and local state includes a five-page student lesson, three-page workbook, four-page teacher guide and a call-to-return diagram. Every canonical print page and all three browser print layouts were inspected. Executable checks cover worked examples, missing returns, None arithmetic TypeError, local-name NameError, repaired returns, independent calculations, repeated calls, zero results, unreachable statements and fresh retry cases.

The build, TypeScript check and all 31 access-test groups passed with 45 rebuilt packages and 270 matching document downloads. All 2,488 protected resources decrypted. Six desktop/mobile resource checks and both protected maps passed. Browser print text matches the source and workbook prompts stay with response spaces.

Grade 7 Weeks 1–9 are complete; Weeks 10–36 remain planned. Cloudflare hosting and student/teacher controls are preserved. Changes are not deployed, and classroom effectiveness remains untested.


## Grade 7 AI 2 Weeks 10–36 completion (2026-09-26)

All 27 remaining weeks now have individually authored student lessons, workbooks, teacher guides and explanatory diagrams. The sequence develops records, validation, data interpretation, rule-based recommendations, files, privacy and a tested capstone application. Each package includes an independent task, explained teacher answers and a fresh retry case.

The continuation print renderer produces three-page lessons, three-page workbooks and four-page guides. All 270 downloadable print pages were visually inspected; canonical text and teacher-answer separation passed. All 81 web resources were also printed and their 263 browser-print pages inspected. Workbook prompts remain with response space. All 162 desktop/mobile resource checks passed without broken images or horizontal page overflow; representative screen layouts were visually reviewed.

All 27 worked Python examples were executed against expected outputs. Additional checks cover independent and retry calculations, boundaries, invalid types, missing data, parsing, empty inputs, tie order and capstone integration. These checks verify the executed cases, not every possible input.

The production build, TypeScript check and all 31 access-test groups passed. The repository now contains 72 rebuilt weekly packages and 432 matching Word/PDF downloads across Grades 6 and 7. All 2,677 protected resources decrypted successfully. Grade 7 alone has 36 lessons, 36 workbooks, 36 teacher guides and 216 Word/PDF downloads.

Grade 7 Weeks 1–36 are complete in the repository; 180 weekly positions across the other five levels remain planned. Cloudflare hosting and student/teacher access controls are preserved. No live deployment was performed. Classroom pacing and learning effectiveness still require student use and teacher feedback.


## Grade 8 AI 3 Week 1 completion (2026-09-26)

The machine learning lifecycle introduces fitting a threshold from labelled training examples, freezing the choice, evaluating separate cards and reporting limited evidence. The complete 90-minute package includes a four-page student lesson, three-page workbook, four-page teacher guide, a lifecycle diagram, independent assessment and a fresh retry. A vocabulary table split was corrected during visual review. Every final downloadable print page and all 12 browser-print pages were inspected; canonical text and answer separation passed.

Executable checks verified the exact worked Python output, independent and retry calculations, threshold equality, declared tie handling and reversed input order. Six desktop/mobile resource checks and both role maps passed. The production build, TypeScript check and all 31 access-test groups passed. The unreleased-route test now derives its examples from the progression and release manifest instead of treating Grade 8 Week 1 as permanently unavailable.

There are now 73 rebuilt packages and 438 matching Word/PDF downloads. All 2,684 protected resources decrypted successfully. Grade 8 has 1 of 36 weeks complete; Weeks 2–36 remain planned. The seven-level sequence has 179 remaining planned positions. Cloudflare hosting and student/teacher access controls are preserved. Changes have not been deployed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 2 completion (2026-09-26)

Features labels and prediction time adds a complete 90-minute package: a four-page lesson, three-page workbook, four-page teacher guide and information-timing diagram. It separates available inputs, historical targets and tracking metadata; explains outcome leakage despite separate test rows; and requires an independent feature contract for a new task. A fresh retry and teacher explanations distinguish unknown outcomes from negative labels.

The exact worked Python output, feature order, unchanged source records, exclusion of later fields, missing-field behavior and assessment boundaries passed executable checks. Every downloadable print page and all 12 browser-print pages were inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are now 74 rebuilt weekly packages with 444 matching Word/PDF downloads. All 2,691 protected resources decrypted successfully. Grade 8 Weeks 1–2 are complete; Weeks 3–36 remain planned. Across seven levels, 178 weekly positions remain planned. Cloudflare hosting and student/teacher access controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 3 completion (2026-09-26)

Classification and regression includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram comparing numerical error with category agreement. The 90-minute sequence distinguishes target meaning from number formatting, evaluates supplied estimates without claiming a model was fitted, and includes an independent task and fresh retry with explained answers.

The exact worked Python, guided fractional boundary, independent and retry categories, absolute errors, means and category recoding passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text and workbook response spaces passed, as did six desktop/mobile resource checks and both protected maps.

The production build, TypeScript check and all 31 access-test groups passed. There are 75 rebuilt weekly packages and 450 matching Word/PDF downloads. All 2,698 protected resources decrypted successfully. Grade 8 Weeks 1–3 are complete; Weeks 4–36 remain planned. Across seven levels, 177 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 4 completion (2026-09-26)

Dataset inspection and cards includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram connecting findings to evidence and source checks. The 90-minute sequence explains provenance, schema, missing values, repeated identifiers and overlapping flags. Students preserve raw records, reject unsupported repairs and produce a dataset card that separates observed findings from unknowns. Independent practice and a fresh retry include explained teacher answers.

The worked Python output, independent and retry counts, overlapping flags, zero versus unknown values, row reversal, repeated rows and empty-input counts passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 76 rebuilt weekly packages and 456 matching Word/PDF downloads. All 2,705 protected resources decrypted successfully. Grade 8 Weeks 1–4 are complete; Weeks 5–36 remain planned. Across seven levels, 176 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 5 completion (2026-09-27)

Label definitions and disagreement includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram linking disagreements to evidence and recorded decisions. The 90-minute sequence defines observable labels and boundaries, preserves uncertainty through review status, measures exact agreement on matched items and distinguishes agreement from correctness. Independent practice and a fresh retry require rule-based decisions, explicit denominators and preservation of original labels.

The worked Python output, guided subset, independent and retry agreement counts, reversed pairs, empty-pair handling and shared-error example passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 77 rebuilt weekly packages and 462 matching Word/PDF downloads. All 2,712 protected resources decrypted successfully. Grade 8 Weeks 1–5 are complete; Weeks 6–36 remain planned. Across seven levels, 175 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 6 completion (2026-09-27)

Splits and related examples includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram separating whole trips into training, validation and test roles. The 90-minute sequence connects the split unit to the intended prediction claim, distinguishes row and group counts, audits every pair of group sets and preserves final evaluation. Independent practice and a fresh retry require repairs that retain every frame exactly once and acknowledge the limits of tiny fictional samples.

The worked Python output, all three overlap pairs, guided counts, independent and retry repairs, source-row coverage and deliberately injected overlaps passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 78 rebuilt weekly packages and 468 matching Word/PDF downloads. All 2,719 protected resources decrypted successfully. Grade 8 Weeks 1–6 are complete; Weeks 7–36 remain planned. Across seven levels, 174 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 7 completion (2026-09-27)

A baseline before a model includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram separating baseline fitting from scoring. The 90-minute sequence fits a majority-label constant from training labels, uses a declared tie rule, compares supplied candidate predictions on identical validation rows and distinguishes percentage points from relative improvement. Independent practice and a fresh retry emphasize honest comparison and error patterns hidden by overall accuracy.

The worked code, all 126 nonempty binary training sequences through six rows with three validation variants, tie handling, validation-independent predictions, equal-accuracy counterexample and assessment calculations passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 79 rebuilt weekly packages and 474 matching Word/PDF downloads. All 2,726 protected resources decrypted successfully. Grade 8 Weeks 1–7 are complete; Weeks 8–36 remain planned. Across seven levels, 173 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 8 completion (2026-09-27)

Searching candidate rules includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram separating training search from validation comparison. The 90-minute sequence fits a threshold from a declared candidate list, distinguishes prediction boundaries from search tie handling and compares the frozen rule with a training-derived baseline. Independent practice and a fresh retry include tied candidates and a case where the learned rule performs worse than the baseline.

The exact worked code, all 16 binary labelings of four training rows, row-order invariance, threshold equality and nearby values, reversed candidate order and assessment scores passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 80 rebuilt weekly packages and 480 matching Word/PDF downloads. All 2,733 protected resources decrypted successfully. Grade 8 Weeks 1–8 are complete; Weeks 9–36 remain planned. Across seven levels, 172 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 9 completion (2026-09-27)

Fitting a decision tree includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram tracing the two paths through a learned root. The 90-minute sequence fits a depth-one tree using branch label majorities and total training mistakes, explicitly distinguishing this classroom procedure from general library tree algorithms. Independent practice reverses the learned leaves; a fresh retry selects the other feature. Both require comparison with a training-majority baseline.

The worked code, all 64 binary labelings of the six feature rows, row-order invariance, root and leaf tie policies, branch counts and assessment scores passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 81 rebuilt weekly packages and 486 matching Word/PDF downloads. All 2,740 protected resources decrypted successfully. Grade 8 Weeks 1–9 are complete; Weeks 10–36 remain planned. Across seven levels, 171 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 10 completion (2026-09-27)

Nearest neighbours and distances includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram connecting feature distances to selected label votes. The 90-minute sequence calculates absolute distances, declares k and an alphabetical ID tie policy, and compares predictions with a training-majority baseline. Independent practice and a fresh retry distinguish distance ties from label votes and keep evaluation labels outside the neighbour pool.

The exact worked code, assessment rankings and predictions, validation and baseline scores, all 120 row permutations for each example query, and positive unit conversions passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 82 rebuilt weekly packages and 492 matching Word/PDF downloads. All 2,747 protected resources decrypted successfully. Grade 8 Weeks 1–10 are complete; Weeks 11–36 remain planned. Across seven levels, 170 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 11 completion (2026-09-27)

Scaling without leakage includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram distinguishing training-only fitting from transformation of every split. The 90-minute sequence calculates two-feature min-max scales, compares raw and scaled nearest neighbours, evaluates fixed predictions against a training-majority baseline, and explains values outside the training range. Independent practice and a fresh retry require new calculations; a zero-range guard and a documented constant-feature policy prevent division by zero.

The exact worked code, independent and retry calculations, validation and baseline scores, training row permutations, positive unit conversions, outside-range values, zero-range guards and unchanged fitted values during prediction passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 83 rebuilt weekly packages and 498 matching Word/PDF downloads. All 2,754 protected resources decrypted successfully. Grade 8 Weeks 1–11 are complete; Weeks 12–36 remain planned. Across seven levels, 169 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 12 completion (2026-09-27)

A reproducible classifier pipeline includes a four-page lesson, three-page workbook, four-page teacher guide and a diagram separating fit, predict and evaluate. The 90-minute sequence combines training-only min-max scaling with a deterministic one-neighbour classifier. Students trace the fitted state, preserve feature order and units, record runs, reproduce individual predictions including errors, and distinguish repeatability from a valid evaluation. Independent practice and a fresh retry use separate training examples.

The exact complete program, worked and independent predictions, retry calculations, fitted values, validation and baseline scores, training and query order invariance, unchanged prediction-time state, swapped-feature counterexample, alphabetical distance tie and both zero-range guards passed executable checks. All 11 downloadable print pages and 12 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 84 rebuilt weekly packages and 504 matching Word/PDF downloads. All 2,761 protected resources decrypted successfully. Grade 8 Weeks 1–12 are complete; Weeks 13–36 remain planned. Across seven levels, 168 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 13 completion (2026-09-28)

Confusion matrices includes a four-page lesson, three-page workbook, four-page teacher guide, a labelled count matrix and a visual connecting all four outcomes to example IDs. The 90-minute sequence counts matched reference/prediction pairs, declares blocked positive, audits row and column totals, and compares equal-accuracy classifiers with different false-positive and false-negative counts. Independent practice and a fresh retry require labelled axes and complete error interpretations.

The exact worked code, all 256 prediction combinations for eight reference records, independent and retry matrices, Week 12 continuity, row and column totals, reversed record order, transposed axes, equal-accuracy comparison and empty/absent-class counts passed executable checks. All 11 downloadable print pages and 11 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 85 rebuilt weekly packages and 510 matching Word/PDF downloads. All 2,768 protected resources decrypted successfully. Grade 8 Weeks 1–13 are complete; Weeks 14–36 remain planned. Across seven levels, 167 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 AI 3 Week 14 completion (2026-09-28)

Accuracy and class imbalance includes a four-page lesson, three-page workbook, four-page teacher guide and a visual comparing overall and class-specific correct fractions. The 90-minute sequence contrasts a training-majority baseline with a frozen candidate, explains balanced accuracy as an equal-class average, and keeps false alarms, missed cases and denominators visible. Independent practice includes a candidate with lower ordinary but higher balanced accuracy, requiring an explicit tradeoff rather than an automatic winner.

The exact worked code, independent and retry calculations, changed-class-mix comparison, all 625 small count matrices, missing-class guards, weighted accuracy identity and class-order invariance passed executable checks. All 11 downloadable print pages and 13 browser-print pages were visually inspected. Canonical text, workbook response spaces, six desktop/mobile resource checks and both protected maps passed.

The production build, TypeScript check and all 31 access-test groups passed. There are 86 rebuilt weekly packages and 516 matching Word/PDF downloads. All 2,775 protected resources decrypted successfully. Grade 8 Weeks 1–14 are complete; Weeks 15–36 remain planned. Across seven levels, 166 weekly positions remain planned. Cloudflare hosting and student/teacher controls are preserved. No live deployment was performed; classroom pacing and effectiveness remain untested.


## Grade 8 completion — Weeks 15–36 (2026-09-28)

Completed the remaining 22 Machine Learning packages, bringing Grade 8 AI 3 to 36 of 36 weeks. Weeks 15–18 cover precision/recall, thresholds, calibration and error analysis; Weeks 19–24 cover regression, baselines, loss, line fitting, validation and final testing; Weeks 25–32 cover capacity, learning curves, features, reproducibility, distribution shift, subgroup evaluation, proxies and model cards. Weeks 33–36 guide a complete classroom capstone from a data proposal through model comparison, frozen evaluation and project defense.

Each week includes a student lesson, five-task workbook, explanatory visual, teacher solutions, two 45-minute teaching sequences, an independent task and a fresh retry. The capstone includes a reproducible 72-record fictional dataset recipe, an explicit 40/20/12 split, teacher-held final labels and time for building and presenting. Its worked results are labelled illustrative; students report their actual results, including when a baseline wins.

Validation completed:

- 56 arithmetic assertions and nine executable Python lesson examples passed. The capstone recipe was independently checked for 72 unique records, split counts, unique parcel dimensions and both classes in each split.
- All 66 new Word documents and 66 matching PDF downloads passed canonical-text and student-answer-separation audits. Every one of their 242 rendered pages was visually reviewed.
- All 66 browser print resources passed canonical-text checks, nonblank-page checks and workbook response-placement checks; every one of their 218 pages was visually reviewed.
- 132 chapter viewport checks passed across 390px and 1280px layouts; all new mobile lesson headers were visually reviewed. Both protected seven-level maps passed and show 144 planned positions.
- Production build, TypeScript check and all 31 access-test groups passed. All 2,929 protected resources decrypted successfully.

Grades 6–8 are complete in the repository: 108 weekly packages with 648 matching Word/PDF downloads. The 144 weeks across Grades 9–12 remain planned. Cloudflare hosting and student/teacher access controls are preserved. No live deployment was performed. Classroom pacing and learning outcomes still require student use and teacher feedback.

## Grade 9 opening — Weeks 1–4 (2026-09-28)

Completed four Neural Networks packages: Representing inputs as vectors; Dot products and weighted sums; Bias terms and decision boundaries; Activation functions. Each has an original student lesson, workbook, teacher guide, explanatory visual, independent transfer task and fresh assessment retry. The progression connects Grade 8 feature schemas to explicit numerical computations before introducing training.

Checked feature ordering and unit conversion, missing-value rejection, guarded dot products, signed contributions, equality at decision boundaries, bias shifts, nonlinear chains and stable sigmoid calculations including extreme inputs. The activation visual shows separate functions receiving the same input, avoiding an implied sequence between ReLU and sigmoid. Examples use fictional data and optional standard-library Python without external accounts.

All 44 canonical document pages and 40 browser-print pages were visually inspected. Text audits verified canonical content and answer separation across all 12 documents and browser resources. A Grade 9 print rule keeps explanatory paragraphs intact across page boundaries. All 24 chapter viewport checks passed at 1280 and 390 pixels, along with both protected maps, production build, TypeScript and all 31 access-check groups. All 2,957 protected resources decrypted successfully.

There are now 112 complete rebuilt weekly packages and 672 matching Word/PDF downloads. Grade 9 has 4 of 36 weeks complete; the seven-level progression has 140 planned positions remaining. Next: AI 4 Week 5, Composing layers. Cloudflare configuration and student/teacher controls are preserved. These changes have not been deployed. Classroom pacing and learning effectiveness still require student trials.
