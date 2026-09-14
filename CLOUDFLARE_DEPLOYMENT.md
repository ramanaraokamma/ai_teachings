# Cloudflare deployment

## Replace the old edition completely

This source package replaces the earlier document reader with a continuous illustrated lesson book. It contains 2,173 protected resources in `public/curriculum-blobs`, the matching data and server key, and all book components. Copy the entire extracted package into your local `ai_teachings` repository, including `.openai`, while preserving your repository's `.git` folder. Review `git status`, commit all source and resource changes, and push to your connected production branch. Do not upload only `app` or `dist`, and do not rely on GitHub's browser uploader for thousands of files.

Before committing, run `node scripts/compile-topic-plans.mjs` and `node scripts/verify-curriculum.mjs --decrypt`. These check all 144 individual visual plans, the complete assets, and that the week route uses the book reader. This edition adds `components/topic-studio.tsx`, `app/topic-studio.css`, `lib/topic-plans.txt`, `lib/topic-plans.json`, and `scripts/compile-topic-plans.mjs`. It also updates `scripts/protect-static-assets.mjs`. Include every added and modified file, not just the lesson component. `VISUAL_COVERAGE.md` maps every week to its diagram.

Keep the repository private if the curriculum must remain confidential: source access includes the content and decryption key. Website passcodes protect website access, not a public GitHub repository.

## Cloudflare Git build settings

Use these settings when connecting the repository in Cloudflare:

- Root directory: the folder containing this `README.md`
- Build command: `npm ci && npm run build`
- Deploy command: `npx wrangler deploy --config dist/server/wrangler.json --name ai-teachings`
- Version command: `npx wrangler versions upload --config dist/server/wrangler.json --name ai-teachings`

The package sets the Worker name to `ai-teachings`. Version upload creates a version; the deployment step must activate it before the live site changes. The output includes a curriculum verification line before the build starts and a deployment-ready line confirming all 2,173 resources in the build output. A successful live update shows **Visual Teaching Edition · 14 September 2026** in the landing-page footer. Every week has its own topic diagram, misconception discussion, worked case, teacher prompt and workbook case.

Confirm the deployed edition after Cloudflare reports a successful deployment:

```bash
curl -sI https://ai-teachings.academy-ai.workers.dev/
```

The response must include `x-academy-edition: topic-studio-2026-09-14`. If it does not, the live Worker is still running another version. Check Cloudflare's active deployment and its Git commit. Examples after sign-in: AI-1 Week 5 has a numeric pixel grid; AI-2 Week 3 has page-boundary decisions; AI-3 Week 3 has a token-window overflow diagram; AI-4 Week 15 has an actual-row/predicted-column confusion matrix.

The separate offline collection contains teacher answers and unencrypted images. It is for local reading and printing, not public hosting. Deploy this protected source package instead. The original DOCX downloads remain the earlier approved editions; the new visual teaching refinements are in the website and printable HTML.

Do not use `wrangler deploy --assets ./dist`. The curriculum requires the generated Worker for server-side access control.

## Required secrets

Retain these runtime secrets under **Workers & Pages → ai-teachings → Settings → Variables and Secrets**, not only under Build variables. You do not need to rotate working secrets when replacing the website source:

| Variable | Value |
|---|---|
| `STUDENT_PASSCODE` | `student1234` |
| `TEACHER_PASSCODE` | `teacher1234` |
| `ACADEMY_SESSION_SECRET` | A private random value of at least 32 bytes |

When deploying from a local terminal, the same values can be stored with Wrangler:

```bash
npx wrangler secret put STUDENT_PASSCODE --config dist/server/wrangler.json
npx wrangler secret put TEACHER_PASSCODE --config dist/server/wrangler.json
npx wrangler secret put ACADEMY_SESSION_SECRET --config dist/server/wrangler.json
npx wrangler deploy --config dist/server/wrangler.json
```

Enter `student1234` and `teacher1234` when prompted for the first two secrets. Generate a new random value for the session secret.

## Expected behavior

- `/` shows only the academy landing and passcode forms.
- Student access opens student lessons and workbook practice.
- Student access cannot open teacher guides.
- Teacher access opens teacher guides, student lessons and workbook practice.
- Signing out clears the signed session.
- Curriculum images are also routed through the protected Worker.
- Word downloads use the same role checks. A student cannot retrieve a teacher file by copying its URL.
- Public `curriculum-blobs` files contain encrypted bytes only. Keep the server output private; never host `lib` or `dist/server` as a static directory.
- Answer fields are temporary to the current page. Print completed work or use the downloadable Word workbook for a saved record.

After deployment, check the landing page while signed out, sign in with each passcode, open one lesson and workbook per level, download a Word file, and confirm that a student session cannot open a copied teacher-guide URL.
