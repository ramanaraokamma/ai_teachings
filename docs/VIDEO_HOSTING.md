# Current playback choice: YouTube Unlisted

AI-1 Weeks 1–10 now use the supplied YouTube links; 62 weeks remain pending. No R2 setup is required for these YouTube embeds. See [YOUTUBE_VIDEOS.md](YOUTUBE_VIDEOS.md) for importing later batches. AI-3 remains paused.

The R2 material below records the earlier alternative design. The active website player now uses YouTube; an R2 binding alone does not switch the selected player back.

# AI-1 and AI-2: Git storage and website video hosting

AI-3 is paused at the user's request. AI-1 and AI-2 each have 36 completed, validated videos.

## Recommended arrangement

Keep website source, the small `lib/lesson-videos.json` catalogue, chapter times, provenance and publishing tools in the website Git repository. Upload the videos, captions, posters and transcripts to **private Cloudflare R2**. The existing website Worker streams them through `/api/lesson-video/:level/:week/:asset` after checking the same signed student/teacher login used by the lessons.

This works at the existing address, `https://ai-teachings.academy-ai.workers.dev/`, without a new public media domain. The R2 bucket should remain private: no public `r2.dev` endpoint is needed. Students can watch the student-facing videos; teacher-only assessment answers remain outside these videos.

The repository currently points to **GitHub**, not GitLab. Nothing in this change changes its remote, pushes source, uploads media, creates billable resources or deploys the site.

## Measured size and platform limits

The originals total **10.48 GiB**, approximately **3,560 minutes** of video. Individual movies are **71–183 MiB**. The website catalogue is about **200 KiB**, not 10 GiB. The generated upload plan includes 288 objects: one movie, VTT caption file, JPEG poster and transcript for each of 72 weeks. Exact current values are in `outputs/video-publishing/size-report.json`.

Cloudflare Workers static assets have a **25 MiB per-file limit**. Video masters must not be placed in `public/`, imported into application JavaScript, or copied into `dist/`. The build guard rejects video files and oversized static assets. Git LFS does not remove these deployment limits: a checked-out LFS movie is still a large movie.

GitLab.com Free provides **10 GiB per project for repository plus LFS**. This video collection alone exceeds that allowance; a paid/additional storage allocation is needed even for one complete archive revision. More versions consume more LFS storage. Do not add the 72 masters to the website repository.

R2 Standard is suitable for these existing MP4 files: the published rate is $0.015/GB-month, with 10 GB-month free allocation and free direct R2 egress; operations and Worker requests have their own allowances/billing. This is not a promise of zero cost: allocation may already be used by other account data, and usage is rounded under Cloudflare's billing rules.

Cloudflare Stream is an alternative when adaptive quality and managed transcoding become important. Its current storage price is $5 per 1,000 minutes per month, in prepaid capacity blocks; this library would need four blocks, about $20/month, plus $1 per 1,000 minutes delivered. R2 is the prepared path here; it serves the existing 1080p MP4 without adaptive bitrate conversion.

## Prepare and review

The following preparation is already complete locally:

```sh
work/video-python/bin/python tools/package_lesson_videos.py
node scripts/upload-lesson-videos.mjs --bucket ai-teachings-videos
```

The uploader defaults to **dry run**. The preparation validates each movie's SHA-256 against its production record, checks saved media/audio/browser validation, maps chapter bookmarks to the source student/workbook sections, and creates small posters. Original files remain in their production output directories; they are not copied into the website bundle.

The catalogue uses versioned object keys. Each object's content hash is part of its key, so a later edition can coexist with the old one. The upload plan contains relative local file paths and checksums; it is ignored generated state, not a secret-bearing credential file.

## Upload and enable playback

Run these steps only when ready to publish the media to your Cloudflare account:

1. Authenticate Wrangler and create the private bucket:

   ```sh
   npx wrangler login
   npx wrangler r2 bucket create ai-teachings-videos
   ```

2. Upload the prepared 288 objects:

   ```sh
   node scripts/upload-lesson-videos.mjs --bucket ai-teachings-videos --execute
   ```

   It checks source sizes/hashes and records successful uploads under ignored `outputs/video-publishing/`. Rerunning resumes from that receipt. To deliberately re-upload after deleting remote objects, remove `outputs/video-publishing/uploaded-ai-teachings-videos.json` first. Keep credentials in Wrangler's authenticated session or protected environment variables; never put credentials in Git.

3. In the Cloudflare build settings, add the **build environment variable**:

   ```text
   ACADEMY_VIDEO_BUCKET=ai-teachings-videos
   ```

   The Vite configuration emits the `LESSON_VIDEOS` R2 binding into `dist/server/wrangler.json`. It preserves any existing storage bindings. Keep the generated config as the deploy input; a dashboard-only binding can be lost on the next config-based deployment.

4. Use the existing build/deploy workflow after committing the reviewed source changes:

   ```text
   Build:  node scripts/verify-curriculum.mjs --decrypt && npm run build
   Deploy: npx wrangler deploy --config dist/server/wrangler.json --name ai-teachings
   ```

   Cloudflare already installs npm dependencies; do not repeat `npm ci` inside the build command. To build locally with the same binding:

   ```sh
   ACADEMY_VIDEO_BUCKET=ai-teachings-videos npm run build
   ```

5. Sign in and check `/learn/student/ai-1/1` and `/learn/student/ai-2/36`, plus the matching teacher pages. Seek to a later chapter, turn on captions, open a matching written section and download a transcript. Unauthenticated API requests must return 401. No movie or poster is requested merely by opening a week page: the viewer chooses “Load this week's video”.

Until the R2 binding is configured, the prepared section explains that online playback is being prepared and leaves the written lesson available. The new site integration is local until source is committed/pushed and your normal Cloudflare deployment runs. This task did not perform those external actions.

## Where each video appears

Each AI-1/AI-2 week has a **Lesson video** navigation link and a **Watch this week's lesson** section before the written lesson. The teacher guide includes the same student-facing video with teaching guidance. The workbook links to its own week's lesson video rather than duplicating the player inside an independent task.

Chapter buttons seek within that week's movie. “Read the matching section” goes to the mapped source student section; collapsed references are expanded when followed. On a teacher guide it opens the corresponding student lesson within the teacher portal. Other levels receive no placeholder or incorrect video, and AI-3 is not generated.

Playback uses native browser controls and same-origin VTT captions. The route supports GET, HEAD, byte ranges, suffix ranges, conditional requests and seeking, and returns the R2 `ReadableStream` directly. It never decrypts or buffers a whole movie in the Worker's 128 MB memory. Access-controlled media uses private response headers rather than a shared public cache.

## Optional: check the originals into a separate GitLab LFS archive

For version-controlled archival copies, first provision enough GitLab LFS capacity and create an empty **separate** GitLab project. Export a new archive directory (this copies about 10.5 GiB; no Git or network operation is run by the exporter):

```sh
work/video-python/bin/python tools/package_lesson_videos.py --archive "$HOME/AI/ai-academy-video-archive"
cd "$HOME/AI/ai-academy-video-archive"
git init -b main
git lfs install --local
git add .gitattributes README.md catalogue.json upload-plan.json objects/
git commit -m "Archive validated AI-1 and AI-2 teaching videos"
git remote add origin git@gitlab.com:YOUR_NAMESPACE/ai-academy-video-archive.git
git push -u origin main
```

The exporter supplies `.gitattributes` to store MP4s in LFS; posters, captions, transcripts and the catalogue remain ordinary small Git files. A clone with LFS downloads disabled must run `git lfs pull` before uploading videos. The uploader detects pointer files by their wrong size instead of uploading them as movies.

GitLab is the archive, not the playback origin. The website repository contains no media submodule and its build does not clone the archive. Its existing `content/programme.json` LFS configuration is preserved. If you prefer no second Git repository, retain the validated originals in local backup plus private R2 and version just the catalogue and authoring source.

## Verification commands

```sh
node --experimental-strip-types tests/lesson-video-http.mjs
node tests/video-asset-guard.mjs
node scripts/upload-lesson-videos.mjs --bucket ai-teachings-videos
npx tsc --noEmit
ACADEMY_VIDEO_BUCKET=ai-teachings-videos npm run build
node --loader ./tests/cloudflare-loader.mjs tests/lesson-video-access.mjs
```

## Official references (checked 2026-10-25)

- [Cloudflare Workers limits: static assets and Worker memory](https://developers.cloudflare.com/workers/platform/limits/)
- [Cloudflare R2 Workers API: streaming objects and ranged reads](https://developers.cloudflare.com/r2/api/workers/workers-api-reference/)
- [R2 Standard pricing, allowances and rounding](https://developers.cloudflare.com/r2/pricing/)
- [Cloudflare Stream pricing](https://developers.cloudflare.com/stream/pricing/)
- [GitLab LFS](https://docs.gitlab.com/topics/git/lfs/)
- [GitLab.com repository and LFS storage quotas](https://docs.gitlab.com/user/storage_usage_quotas/)
