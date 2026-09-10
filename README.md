# AI Academy Curriculum 2.0 — Refined Website

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
- All 2,880 original illustration placements, including instructional diagrams
- 292 editable Word downloads: 144 student modules, 144 teacher guides and four workbooks
- On-page response fields and print layouts (responses are cleared on navigation or reload)
- Responsive desktop, tablet and mobile layouts

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
npm run build
node --loader ./tests/cloudflare-loader.mjs tests/academy-access.mjs
```

The integration suite exercises the compiled Worker with a Node environment-binding shim. It covers public landing content, passcode and session handling, role restrictions, student and teacher pages, encrypted media, Word downloads and logout. It does not emulate Cloudflare resource limits or replace a post-deployment smoke check.

Shared passcodes provide two access modes; there are no individual student accounts, synchronized progress records or cloud-saved answers in this edition.
