import importlib.util,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('importer',ROOT/'tools/import_youtube_links.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
ids=json.loads((ROOT/'lib/youtube-videos.json').read_text());assert len(ids)==72
assert all(ids[f'ai-1/{n}'] for n in range(1,11))
# Fresh Git checkouts have the tracked catalogue but not the ignored local upload CSV.
csv_path=ROOT/'outputs/youtube-upload-ai-1-ai-2/youtube-links.csv'
if csv_path.exists():
 with csv_path.open(newline='') as f:assert m.import_rows(csv.DictReader(f),ids,ids)==ids
assert m.import_rows([{'lesson_id':'ai-1/1','youtube_url':''}],ids,ids)==ids
for url in ['https://youtu.be/TjzAlY3rLg0?si=test','https://www.youtube.com/watch?v=TjzAlY3rLg0&t=15','https://www.youtube.com/embed/TjzAlY3rLg0','TjzAlY3rLg0']:assert m.video_id(url)=='TjzAlY3rLg0'
for url in ['https://youtube.com.evil.test/watch?v=TjzAlY3rLg0','https://www.youtube.com/watch?v=bad','javascript:alert(1)','https://evil.test/TjzAlY3rLg0','http://youtu.be/TjzAlY3rLg0']:
 try:m.video_id(url);raise AssertionError('Invalid link accepted')
 except ValueError:pass
for rows in [[{'lesson_id':'ai-3/1','youtube_url':'TjzAlY3rLg0'}],[{'lesson_id':'ai-1/1','youtube_url':'TjzAlY3rLg0'}]*2,[{'lesson_id':'ai-1/2','youtube_url':'TjzAlY3rLg0'}]]:
 try:m.import_rows(rows,ids,ids);raise AssertionError('Invalid mapping accepted')
 except ValueError:pass
print('YouTube week mappings, blank-link preservation, URL validation, duplicate and unknown-lesson rejection passed.')
