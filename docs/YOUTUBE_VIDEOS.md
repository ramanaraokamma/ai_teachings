# YouTube lesson links

The active website uses YouTube Unlisted videos. All 36 AI-1 weeks and all 36 AI-2 weeks have YouTube links configured. AI-3 remains paused. The R2 publishing tools are retained as an optional alternative; they are not needed for these embeds.

## Import more links

Fill the `youtube_url` cells in:

```text
outputs/youtube-upload-ai-1-ai-2/youtube-links.csv
```

Then, from the repository root:

```sh
python3 tools/import_youtube_links.py
```

This imports nonempty entries into the small tracked `lib/youtube-videos.json`. Blank cells preserve previously imported links. Unknown lesson IDs, duplicate lesson rows, invalid URLs and a video accidentally assigned to multiple lessons are rejected before the file is changed. Standard watch, share, embed, Shorts and live URLs are accepted; tracking and start-time query parameters are not stored. The website uses each video's original chapter times.

The local CSV is under ignored `outputs/`; commit the resulting `lib/youtube-videos.json`, together with the player source changes, so Cloudflare builds have the links. Do not put MP4s in Git, public/ or the Worker bundle. No build-time access to local videos or the CSV is required. A normal website rebuild/deployment picks up later catalogue updates. For YouTube-only hosting, leave the `ACADEMY_VIDEO_BUCKET` build variable unset; no R2 binding or media upload is required.

## Student and teacher experience

- Every linked week has one player in “Watch this week's lesson”. It loads after the learner chooses the load button or a chapter/section shortcut.
- The player uses `youtube-nocookie.com`, a descriptive iframe title, inline mobile playback and an explicit origin/referrer policy. The official IFrame API supports chapter seeking without creating another player for each written section.
- Chapters and “Watch this section in the video” use the existing source-section mappings. Teacher guides link to the corresponding student section within the teacher portal.
- Weeks without a link show a simple coming-soon message. Their written lesson and workbook remain available, and no broken player or R2 download link appears.
- Video downloads/transcript links from the R2 prototype are not shown for YouTube playback. YouTube controls provide captions when the uploader supplies them; the movies also retain their authored on-screen narration captions.
- If YouTube is blocked or an upload cannot be embedded, the player offers the matching “Open it on YouTube” link and keeps the written lesson available.

YouTube links remain unlisted rather than private: anyone who obtains a link may share it. Website login protects the lesson page; it does not add YouTube-level access restrictions. Keep Allow embedding enabled in YouTube Studio and use the supplied SRT captions. No YouTube upload, change of video visibility, commit, push or deployment is performed by the importer.

## Verification

```sh
python3 tests/youtube-link-import.py
node --experimental-strip-types tests/youtube-player-url.mjs
npx tsc --noEmit
npm run build
node --loader ./tests/cloudflare-loader.mjs tests/lesson-video-access.mjs
node --loader ./tests/cloudflare-loader.mjs tests/youtube-lesson-browser.mjs
```

The browser test uses a controlled YouTube API/player fixture to verify lazy loading, matching IDs, initial and later chapter seeking, section shortcuts, pending states and mobile accessibility without depending on YouTube's network/bot restrictions. Real link titles/availability are checked separately through YouTube's oEmbed endpoint. That metadata check does not prove full playback on every viewer's network.

Official implementation references:

- https://developers.google.com/youtube/iframe_api_reference
- https://support.google.com/youtube/answer/171780?hl=en
