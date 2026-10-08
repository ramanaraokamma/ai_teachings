# Classroom improvements — 7 October 2026

The repository root is the unified complete programme. The offline edition in `outputs/ai-academy-complete-programme/` mirrors the teaching content. This update completes the eight requested improvements in order.

1. **Learning sequence:** Levels 1–3, the unnumbered Python Readiness Bridge, then Levels 4–7. The bridge includes an independent placement discussion covering tracing, conditions, loops, lists, functions, dictionaries, debugging and testing. A teacher checks a further changed program before allowing a skip.
2. **Curriculum map:** Each hosted level card explains prerequisites, an exit outcome and its cumulative project. The level page repeats the readiness requirements and explains portfolio evidence.
3. **Lesson flow:** All 264 lessons have six explicit navigation steps. The original sections remain in their original order, preserving teacher cross-references. Each lesson adds a route, end goals and a finish-and-return check.
4. **Teaching visuals:** Every lesson uses its reviewed, topic-specific question and changed condition beside the matching pictorial case. Numerical series now have a plotted website chart, with the exact values preserved in website, HTML, Word and PDF tables. Learners can enlarge pictures and predict before revealing worked explanations.
5. **Teacher guidance:** Each teacher guide adds preparation, staged timing, the actual practice answer and misconception repair, support, a changed-condition extension, assessment criteria and a project checkpoint. The original explanations, answers and laboratory guidance remain available.
6. **Understanding checks:** The existing reserved independent cases and teacher keys are retained. Explanation, trace/test and limits are judged separately as not yet, with support or independent. Progress ticks record practice rather than certifying mastery.
7. **Connected projects:** Each AI level has six cumulative milestones. Every workbook adds a portfolio record for its named project, with inputs, predicted and observed results, changes, failures and the next test. The Python bridge uses a readiness portfolio.
8. **Classroom usability:** Drafts and progress persist in the current browser, with clear-draft controls and a storage-unavailable message. Students can find previously practised weeks; the last week links to the next part of the sequence. Keyboard focus, responsive lesson routes, enlarged visuals, printable answers and role-protected Word/PDF downloads are retained or improved.

## Benchmark

Level 1 Week 1, **AI or Not?**, is the benchmark. Its pictorial umbrella case distinguishes a learned rain forecast, a written display rule and a teacher’s action. Its reserved greenhouse assessment asks learners to apply those distinctions to a different hybrid system. Its project checkpoint connects that reasoning to the Helpful Classroom Sorter. The topic-specific teacher answer explains why a correctly displayed message does not prove an accurate prediction.

## Verification

- Original source preservation: all 144 original weeks, all 252 later lessons and 1,874 original images checked; no errors.
- Existing source Python: 118 examples checked, including the declared error demonstration.
- Lesson route and project alignment: all 264 lessons and 1,584 route links checked; seven levels have six milestones.
- Teaching method, reserved question/key alignment, pictorial data and Python bridge checks passed.
- All 792 Word and 792 PDF downloads compared with canonical role content, including 1,122 pictorial image placements; no missing text or images detected.
- All 3,832 protected resources authenticated and decrypted successfully.
- Production build and 275 access/lesson checks passed, including bridge placement, continuation and teacher download protection.
- 68 desktop and phone browser navigation checks passed for both roles, with draft save/reload/clear, progress, picture enlargement, worked-explanation reveal, readiness and print checks. Browser console errors: zero. Drafts remain separate when navigating between weeks. Offline phone layout and draft save/reload/clear also passed. Results are recorded in `classroom-browser-validation.json`.

These checks establish content alignment and technical behaviour. Classroom observation is still needed to assess learning gains and adjust pacing. Nothing was deployed by this update.

## Updating the content

`tools/improve_classroom.py` applies the additions without removing original sections and can be rerun. Render HTML with `tools/render_programme.py`; export Word/PDF with `tools/export_word.py` and `tools/export_pdf_local.py`. Run content, teaching-method, picture, bridge, classroom, link and download validators. Then run `node scripts/import-complete-programme.mjs --root`, `node scripts/verify-curriculum.mjs --decrypt` and `npm test` to refresh and verify the protected website. The importer reuses unchanged encrypted resources.

Optional reproducible browser checks live in `tests/classroom-browser.mjs`. Run after `npm test` with Playwright Core available (or set `ACADEMY_PLAYWRIGHT_MODULE` to its module file), using the Cloudflare loader. Set `ACADEMY_CHROME_PATH` if Chrome is elsewhere. Screenshots and print examples are kept under `work/classroom-browser/`.
