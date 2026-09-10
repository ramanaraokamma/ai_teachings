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
- Protected curriculum illustrations
- Responsive desktop, tablet and mobile layouts

## Access configuration

The application reads three server-side environment values:

- `STUDENT_PASSCODE`
- `TEACHER_PASSCODE`
- `ACADEMY_SESSION_SECRET`

For this edition, configure the requested passcodes as `student1234` and `teacher1234`. Use a long random value for `ACADEMY_SESSION_SECRET`.

Passcodes are deliberately not stored in source code or browser JavaScript.

## Local build

```bash
npm ci
npm run build
```

The Cloudflare Worker output is written to `dist/server`, and its static assets are written to `dist/client`.

## Cloudflare hosting

Follow [CLOUDFLARE_DEPLOYMENT.md](CLOUDFLARE_DEPLOYMENT.md). This portal must be deployed as a Worker application; deploying only the static asset folder would remove its access protection.

## Curriculum refresh

The website data is produced from the refined Word curriculum by `scripts/extract_curriculum.py`. The included `lib/academy-data.json` and 144 concept images are already generated and ready to build.
