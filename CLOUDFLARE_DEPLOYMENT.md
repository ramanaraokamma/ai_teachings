# Cloudflare deployment

## Cloudflare Git build settings

Use these settings when connecting the repository in Cloudflare:

- Root directory: the folder containing this `README.md`
- Build command: `npm ci && npm run build`
- Deploy command: `npx wrangler deploy --config dist/server/wrangler.json`

Do not use `wrangler deploy --assets ./dist`. The curriculum requires the generated Worker for server-side access control.

## Required secrets

Add these production environment variables in the Cloudflare Worker settings:

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
