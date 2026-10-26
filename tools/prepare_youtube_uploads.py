"""Collect validated masters for manual YouTube uploads; preserve old player paths with symlinks."""
from pathlib import Path
import csv,hashlib,json,os,re,shutil,unicodedata
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'outputs/youtube-upload-ai-1-ai-2'
def digest(path):
 h=hashlib.sha256()
 with path.open('rb') as stream:
  for b in iter(lambda:stream.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def stamp(seconds):
 n=int(seconds);h,n=divmod(n,3600);m,s=divmod(n,60)
 return f'{h}:{m:02d}:{s:02d}' if h else f'{m}:{s:02d}'
def main():
 records=[]
 for level in ['ai-1','ai-2']:
  base=ROOT/'outputs/ai-academy-context-videos'/('ai-2' if level=='ai-2' else '')
  queue=json.loads((base/'queue-progress.json').read_text());assert queue['completed']==36
  for week in queue['weeks']:
   folder=(base/week['watch']).parent.resolve();v=json.loads((folder/'validation.json').read_text());assert v['decode_errors']==0
   movie=folder/f"{level}-week-{week['number']}-context-v4.mp4"
   assert movie.exists() and movie.stat().st_size==v['bytes'],movie
   title=week['title'].split(': ',1)[-1]
   slug=re.sub(r'[^A-Za-z0-9]+','-',unicodedata.normalize('NFKD',title).encode('ascii','ignore').decode()).strip('-')[:90]
   stem=f"{level.upper()}_Week-{week['number']:02d}_{slug}"
   target=DEST/'videos'/(stem+'.mp4')
   assert not target.exists() or (movie.is_symlink() and movie.resolve()==target.resolve()),f'Destination already occupied: {target}'
   assert (folder/'captions.srt').is_file()
   records.append({'id':week['week'],'level':level.upper(),'week':week['number'],'title':f"{level.upper()} | Week {week['number']:02d} | {title}",'source':str(movie.relative_to(ROOT)),'video_file':str(target.relative_to(DEST)),'captions_file':f'captions/{stem}.srt','description_file':f'descriptions/{stem}.txt','bytes':v['bytes'],'sha256':v['sha256'],'folder':folder})
 assert len(records)==72
 for name in ['videos','captions','descriptions']:(DEST/name).mkdir(parents=True,exist_ok=True)
 manifest=[{k:v for k,v in r.items() if k!='folder'} for r in records]
 (DEST/'upload-manifest.json').write_text(json.dumps({'videos':72,'totalBytes':sum(r['bytes'] for r in records),'lessons':manifest},indent=2)+'\n')
 # Keep any YouTube URLs entered during a previous run.
 urls={}
 if (DEST/'youtube-links.csv').exists():
  with (DEST/'youtube-links.csv').open(newline='') as f:urls={r['lesson_id']:r['youtube_url'] for r in csv.DictReader(f)}
 for i,r in enumerate(records,1):
  source=ROOT/r['source'];target=DEST/r['video_file']
  if not source.is_symlink():
   source.rename(target)
   try:source.symlink_to(os.path.relpath(target,source.parent))
   except BaseException:target.rename(source);raise
  assert source.resolve()==target.resolve() and target.stat().st_size==r['bytes']
  assert digest(target)==r['sha256'],f'Checksum mismatch: {target}'
  shutil.copy2(r['folder']/'captions.srt',DEST/r['captions_file'])
  chapters=json.loads((r['folder']/'chapters.json').read_text())
  description=r['title']+'\n\nOne connected classroom lesson with worked examples, thinking pauses and practice. Pause whenever you need time to write, draw or explain.\n\nChapters\n'+'\n'.join(f"{stamp(c['start'])} {re.sub(r'^\d+\s*·\s*', '', c['title'])}" for c in chapters)+'\n\nAI Academy. Synthetic teacher and learner narration; illustrative visuals. Teacher-only independent assessment answers are excluded.\n'
  (DEST/r['description_file']).write_text(description)
  print(f'{i:02d}/72 verified: {target.name}',flush=True)
 with (DEST/'youtube-links.csv').open('w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=['lesson_id','level','week','title','video_file','captions_file','description_file','youtube_url']);writer.writeheader()
  for r in records:writer.writerow({'lesson_id':r['id'],**{k:r[k] for k in ['level','week','title','video_file','captions_file','description_file']},'youtube_url':urls.get(r['id'],'')})
 (DEST/'README.txt').write_text('''AI ACADEMY — YOUTUBE UPLOAD FOLDER\n\n72 completed movies: AI-1 Weeks 01–36 and AI-2 Weeks 01–36.\n\n1. Open videos/: all 72 MP4s are together, sorted by level and week.\n2. Upload to your YouTube channel and choose Unlisted. Longer-than-15-minute uploads require channel verification.\n3. Use the matching captions/ file as English subtitles with timing.\n4. Copy the matching descriptions/ text for a title and chapter timestamps if useful.\n5. Paste the shareable YouTube URL into the youtube_url column of youtube-links.csv.\n6. Send back that CSV, or a list pairing each lesson ID (for example ai-1/1) with its YouTube URL. We can then embed each video in its matching week and retain section/chapter seeking.\n\nUnlisted links are shareable by anyone who obtains them; website login does not make a YouTube link private.\n\nThe movies were moved here, not duplicated. Their old production paths are relative symbolic links so existing offline players and publishing plans continue to work. Keep this folder in place until the website mapping is complete. AI-3 remains paused.\n''')
 (DEST/'verification.json').write_text(json.dumps({'videos':72,'verifiedSHA256':72,'originalPlayerPathsPreserved':True,'captions':72,'descriptions':72,'totalGiB':sum(r['bytes'] for r in records)/1024**3},indent=2)+'\n')
 print(f'Complete: {DEST}',flush=True)
if __name__=='__main__':main()
