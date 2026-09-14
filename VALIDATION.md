# Grade 6 Entry Edition — validation

Edition: `grade6-entry-2026-09-14`.

- All 144 existing weeks have a distinct prerequisite retrieval prompt, transfer task, hint and teacher solution.
- The 258 authored vocabulary definitions fill 288 formerly blank student definition cells and matching teacher meanings. No student vocabulary meaning is blank.
- Production Cloudflare Worker build and TypeScript checks passed.
- All 26 access/route test groups passed. The suite renders all 432 resources and now checks the new transfer material and teacher-answer exclusion.
- Browser checks passed for all 432 resources at 1280px desktop and 390px mobile widths: no page-wide overflow, broken images or incorrect teacher-solution visibility.
- All 432 resources rendered to A4 PDFs. A text audit found every transfer task intact, teacher transfer solutions only in guides, and no blank pages. Representative first pages, diagrams, workbook pages, teacher solution pages and ML code pages were visually inspected. This is not a claim of manual visual inspection of every printed page.
- Python threshold-classifier and regression examples ran with their documented outputs. The displayed code comes from these executable files; indentation is preserved. Printed code blocks remain together.
- All 2,173 protected resources decrypted successfully; all 292 original DOCX downloads remain intact and explicitly labelled as prior-edition material.
- Authentication, passcode handling, resource permissions, encryption key, resource manifest and Sites identity configuration are unchanged. The Vite configuration now declares the existing ASSETS binding so local previews can load protected media. The Worker edition header changed; access logic did not.

## Scope and remaining boundaries

The four existing levels now have typical entry grades 6–9 and readiness guidance. The proposed seven-level replacement is not presented as completed. This is a substantive extension and correction of the existing curriculum, not a replacement of every legacy paragraph. Classroom pilots and learner-outcome validation remain future work.

Use the portal print action for the current student lessons, workbooks and teacher guides. Original DOCX files remain the earlier edition. No runtime secrets were changed and no production deployment was made: Cloudflare CLI authentication was unavailable.

## Reproduce core verification

```bash
npm ci
npm run build
npx tsc --noEmit
node scripts/verify-curriculum.mjs --decrypt
node --loader ./tests/cloudflare-loader.mjs tests/academy-access.mjs
python3 examples/threshold_classifier.py
python3 examples/linear_regression.py
```

The browser and PDF sweeps used temporary local test passcodes and generated private QA files outside the publishable source. No test credentials or QA PDFs are included in the source patch.
