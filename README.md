> **Curriculum 3 update:** The rebuilt Grade 6 sequence (Weeks 1–36) and Grade 7 AI 2 Weeks 1–36, plus Grade 8 AI 3 Weeks 1–36 and Grade 9 AI 4 Weeks 1–32, now have matching web, Word and PDF resources. The seven-level map marks the remaining 112 weeks as planned. See [CURRICULUM3.md](CURRICULUM3.md) for scope, access and validation.

# AI Academy — Grade 6 Entry Edition

The redesign reviews all 144 existing weeks across four levels, with prerequisite retrieval, fresh transfer assessments, optional hints and teacher-only solutions. Typical entry grades are 6–9; readiness determines placement. See [the week-by-week review](GRADE6_REVIEW.md). This is an extension and correction of the existing four-level curriculum, not the proposed seven-level replacement.

There are 258 authored vocabulary definitions, filling 288 empty student definition cells and their corresponding teacher meanings. The ML code labs retain Python indentation and include executable source examples. Use the portal print action for the current edition; original protected DOCX downloads are explicitly marked as the earlier edition.

Cloudflare Worker hosting, signed sessions and student/teacher permissions are retained. Runtime secrets are unchanged. The response edition header is `grade6-entry-2026-09-14`. `npm run build` now also works on macOS without Linux flock or GNU timeout.

A protected learning portal containing the complete AI‑1 through AI‑4 curriculum.

## What is included

- AI‑1 Explorer, AI‑2 Thinker, AI‑3 Creator and AI‑4 ML Builder
- 36 weeks per level, organized into six curriculum phases
- 144 illustrated student lessons
- 144 teacher guides
- 144 aligned workbook missions
- Student and Teacher role dashboards
- Server-side passcode validation and signed, HTTP-only sessions
- Teacher-only guide protection
- Original story and vocabulary artwork, plus 144 topic-specific HTML/SVG teaching diagrams
- 292 editable Word downloads: 144 student modules, 144 teacher guides and four workbooks
- On-page response fields and print layouts (responses are cleared on navigation or reload)
- Responsive desktop, tablet and mobile layouts
- Complete continuous student lesson books with all chapters, worked reasoning and practice
- Pixel grids, signal traces, fraction models, confusion matrices, context windows, proportional partitions, decision paths, code traces and learning curves selected for the actual weekly concept
- A misconception discussion, worked-case panel and comparison practice in every lesson
- AI-1 Week 3 sensor-matching diagrams and an interactive light-sensor / fixed-rule demonstration
- A topic-specific diagram and teaching prompt in all 144 teacher guides; matching practice prompts in all 144 workbook missions
- Larger text for younger learners, expandable illustrations, illustrated week cards, and complete chapter-based print styling
- Build-time checks for all 144 visual plans, source curriculum coverage and all 292 downloads; missing media stops the build

The original 292 DOCX files are retained unchanged. These refinements apply to the website and printable HTML. Generic raster stage/case cards are replaced in the main student reading flow; original instructional text is retained. The separately delivered offline collection contains 432 HTML resources (144 lessons, 144 guides, 144 workbook pages), including teacher answers, and must not be put in a public static folder.

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
