# Complete programme deployment

The repository root now includes the complete offline programme and the protected Cloudflare application. The website uses all 252 AI lessons across seven levels and the 12-lesson Python bridge. Student lessons, teacher guides, workbooks, and current Word/PDF downloads share one curriculum.

Run `npm ci && npm test` before publishing. Cloudflare Git builds can use `npm ci && npm run build`, followed by `npx wrangler deploy --config dist/server/wrangler.json --name ai-teachings`. Preserve existing runtime secrets STUDENT_PASSCODE, TEACHER_PASSCODE and ACADEMY_SESSION_SECRET.

The deployed response header is `x-academy-edition: complete-programme-2026-10-07`. A repository update changes the live website only after the connected build deploys successfully.

Only `public/` contains deployable static assets. Curriculum resources in `public/curriculum-blobs/` are encrypted; `/api/resource/` decrypts them after session and role checks. Never host the entire repository or the offline teacher package as a public static directory. Source files, `content/`, `teacher/`, `tools/`, `reports/` and `dist/server/` contain teacher material and belong in a private repository.

To import a newly rebuilt offline edition, run `node scripts/import-complete-programme.mjs outputs/ai-academy-complete-programme`. This copies the edition to the repository root and rebuilds the website dataset and protected resources. Existing Cloudflare application infrastructure is preserved. Old Curriculum 3 URLs redirect into the unified portal.

## Existing Cloudflare Git settings

These settings remain compatible with the complete programme:

- Build: `node scripts/verify-curriculum.mjs --decrypt && npm ci && npm run build`
- Deploy: `npx wrangler deploy --config dist/server/wrangler.json --name ai-teachings`
- Version: `npx wrangler versions upload --config dist/server/wrangler.json --name ai-teachings`

The validator now checks all 264 lessons and role-specific Word/PDF downloads. Its `--decrypt` option authenticates every encrypted resource and checks the resulting file signatures. The former 144-week renderer check is replaced by complete-programme checks.
