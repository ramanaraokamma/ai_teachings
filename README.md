# AI Academy — unified Grades 6–12 pathway

AI Academy now presents one current curriculum: seven levels with 36 weeks each, covering **252 student lessons, 252 workbook missions and 252 teacher guides**, with 756 reviewed Word files and 756 matching PDFs. Student and teacher sign-in both open the same current seven-level map. Deployment is outside this content-preparation task.

The earlier four-level edition has been compared against the latest curriculum. All 144 earlier topics have an explicit current destination, and their complete illustrated lessons, visual activities, workbooks, teacher explanations and fresh transfer tasks are retained as optional practice alongside the relevant current lessons. Previous week bookmarks redirect by topic, preserving lesson/workbook/guide selection and access controls. The old level numbers must not be interpreted as equivalent current topics.

See [the 144-topic coverage crosswalk](curriculum-v3/UNIFIED_COVERAGE.md) and [the 252-week content review](curriculum-v3/CONTENT_REVIEW.md). Several topics move to a later grade in the current progression; introductory retained cases remain available after a readiness check. The audit establishes source preservation and topic continuity, not proven classroom outcomes.

## Prepared collections

- [Student study collection](outputs/curriculum-reviewed/student-study-complete.zip): 252 latest lesson/workbook editions plus 144 optional illustrated practice chapters.
- [Teacher preparation collection](outputs/curriculum-reviewed/teacher-study-complete.zip): 252 latest guides plus 144 matching practice editions with teacher explanations.
- [Core student Word/PDF collection](outputs/curriculum-complete/student-complete.zip) and [core teacher Word/PDF collection](outputs/curriculum-complete/teacher-complete.zip): original reviewed core downloads, unchanged.

Extract a study archive and open `index.html`. Additional practice is linked from its current lesson and leads back to it. Every chapter contains its own images and works offline. Teacher solutions belong only in the separate teacher collection. New reading supports and presentation refinements are in the study editions and portal; they are not silently included in unchanged core Word/PDF files.

Recreate study collections with `node scripts/review-v3-content.mjs`, then verify continuity with `python3 scripts/verify-unified-coverage.py`. Recreate core archives with `node scripts/package-v3-complete.mjs`.

## What is included

- Seven current levels: foundations; Python and data; machine learning; neural networks; generative systems; AI engineering; research.
- Vocabulary before technical reading, worked cases, diagrams and text descriptions, coding examples, response space and independent transfer assessments.
- 27 additional student explanations, 47 expanded teacher answers, and specific targets and complete evidence traces for 96 later weeks.
- Teacher topic primers, board walkthroughs, timed two-session plans, misconceptions, support and fresh reassessment guidance.
- Editable on-page answer fields with print support; responses clear when leaving or reloading the page.
- 144 retained practice topics with original artwork, topic-specific visual models and teacher-only transfer solutions.
- Server-side passcode checks, signed HTTP-only sessions, protected downloads and role-specific teacher access.
- Responsive reading and print layouts, with source/hash audits and access tests.

## Access configuration

The application reads three server-side environment values:

- `STUDENT_PASSCODE`
- `TEACHER_PASSCODE`
- `ACADEMY_SESSION_SECRET`

For this edition, configure the requested passcodes as `student1234` and `teacher1234`. Use a long random value for `ACADEMY_SESSION_SECRET`.

Passcodes are read from runtime secrets, never from browser JavaScript. The example values appear only in administrator documentation and test fixtures.

## Local build

```bash
npm ci
npm run build
```

The Cloudflare Worker output is written to `dist/server`, and its static assets are written to `dist/client`.

## Cloudflare hosting

Follow [CLOUDFLARE_DEPLOYMENT.md](CLOUDFLARE_DEPLOYMENT.md). This portal must be deployed as a Worker application; deploying only the static asset folder would remove its access protection.

## Curriculum refresh

The website data is produced from the refined Word curriculum by `scripts/convert_full_curriculum.py`. The generated data, resource manifest and encrypted media are included and ready to build. To refresh all content, use Python with python-docx and cryptography:

```bash
python scripts/convert_full_curriculum.py /absolute/path/to/refined-document-folders
npm run build
```

The converter preserves paragraph headings, code indentation, table response rows and diagrams within galleries. It rotates the content encryption key whenever resources are regenerated; deploy the manifest, server key and encrypted assets together.

## Verification

```bash
npx tsc --noEmit
node scripts/verify-curriculum.mjs --decrypt
npm run build
node --loader ./tests/cloudflare-loader.mjs tests/academy-access.mjs
```

The integration suite exercises the compiled Worker with a Node environment-binding shim. It covers public landing content, passcode and session handling, role restrictions, student and teacher pages, encrypted media, Word downloads and logout. It does not emulate Cloudflare resource limits or replace a post-deployment smoke check.

Shared passcodes provide two access modes; there are no individual student accounts, synchronized progress records or cloud-saved answers in this edition.
