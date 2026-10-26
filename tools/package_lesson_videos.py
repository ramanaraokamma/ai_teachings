"""Prepare a small website catalogue and R2 upload plan; optionally export a separate Git LFS archive.
Never uploads, commits, pushes, deploys or changes original videos.
"""
from pathlib import Path
import argparse,json,hashlib,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--archive',type=Path);args=ap.parse_args()
 out=ROOT/'outputs/video-publishing';out.mkdir(exist_ok=True);catalogue={};objects=[];total=0
 for level in ['ai-1','ai-2']:
  base=ROOT/'outputs/ai-academy-context-videos'/('ai-2' if level=='ai-2' else '')
  queue=json.loads((base/'queue-progress.json').read_text());assert queue['completed']==36
  for entry in queue['weeks']:
   n=entry['number'];folder=(base/entry['watch']).parent.resolve();v=json.loads((folder/'validation.json').read_text());browser=json.loads((folder/'browser-validation.json').read_text());coverage=json.loads((folder/'coverage.json').read_text());chapters=json.loads((folder/'chapters.json').read_text())
   assert v['decode_errors']==0 and browser['accessibility_violations']==0
   audio=v['encoded_audio'];assert abs(float(audio['input_i'])+16)<=.5 and float(audio['input_tp'])<=-1.5
   movie=folder/(f'{level}-week-{n}-context-v4.mp4' if entry['week']!='ai-1/1' else 'ai-1-week-1-context-v4.mp4')
   sha=digest(movie);assert sha==v['sha256'];total+=movie.stat().st_size
   work=out/'assets'/level/f'{n:02d}';work.mkdir(parents=True,exist_ok=True)
   with Image.open(folder/'previews/001.png') as im:
    im.convert('RGB').resize((1280,720),Image.Resampling.LANCZOS).save(work/'poster.jpg',quality=82,optimize=True)
   prefix=f'academy-videos/v1/{level}/{n:02d}/{sha[:20]}'
   assets={}
   for name,path,mime,filename in [('video',movie,'video/mp4','lesson.mp4'),('captions',folder/'captions.vtt','text/vtt; charset=utf-8','captions.vtt'),('poster',work/'poster.jpg','image/jpeg','poster.jpg'),('transcript',folder/'transcript.md','text/plain; charset=utf-8','transcript.md')]:
    asset_sha=sha if name=='video' else digest(path)
    key=prefix+'/'+asset_sha[:20]+'-'+filename
    asset={'key':key,'bytes':path.stat().st_size,'sha256':asset_sha,'mime':mime,'filename':f'{level}-week-{n}-{filename}'}
    assets[name]=asset;objects.append({**asset,'source':str(path.relative_to(ROOT))})
   catalogue[entry['week']]={'title':entry['title'].split(': ',1)[-1],'seconds':v['seconds'],'resolution':v['resolution'],'assets':assets,'chapters':[{**c,'studentSections':m['student_sections'],'workbookSections':m['workbook_sections']} for c,m in zip(chapters,coverage['chapter_mapping'])]}
 assert len(catalogue)==72 and len(objects)==288
 (ROOT/'lib/lesson-videos.json').write_text(json.dumps(catalogue,separators=(',',':'))+'\n')
 plan={'version':1,'videos':72,'videoBytes':total,'objects':objects};(out/'upload-plan.json').write_text(json.dumps(plan,indent=2)+'\n')
 (out/'size-report.json').write_text(json.dumps({'videos':72,'videoBytes':total,'videoGiB':total/1024**3,'totalMinutes':sum(v['seconds'] for v in catalogue.values())/60,'minMiB':min(v['assets']['video']['bytes'] for v in catalogue.values())/1024**2,'maxMiB':max(v['assets']['video']['bytes'] for v in catalogue.values())/1024**2,'catalogueBytes':(ROOT/'lib/lesson-videos.json').stat().st_size},indent=2)+'\n')
 if args.archive:
  dest=args.archive.expanduser().resolve();assert not dest.exists(),'Use a new, empty archive directory'
  # Keep the optional multi-GB archive out of website source and build directories.
  assert not dest.is_relative_to(ROOT) or dest.is_relative_to(ROOT/'outputs'),'Archive must be outside the website repo or under ignored outputs/'
  dest.mkdir(parents=True);export=[]
  for obj in objects:
   relative=Path('objects')/obj['key'];target=dest/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/obj['source'],target);export.append({**obj,'source':str(relative)})
  (dest/'upload-plan.json').write_text(json.dumps({**plan,'objects':export},indent=2)+'\n');shutil.copy2(ROOT/'lib/lesson-videos.json',dest/'catalogue.json')
  (dest/'.gitattributes').write_text('*.mp4 filter=lfs diff=lfs merge=lfs -text\n')
  (dest/'README.md').write_text('# AI Academy video archive\n\n72 validated AI-1/AI-2 masters, captions, posters and transcripts. MP4 files use Git LFS. Requires more than 10 GiB LFS capacity for one revision; storage grows with revisions. This is a separate archive, not a website deployment source. Git LFS is archival; Cloudflare R2 serves playback. Use the website repository uploader with --plan pointing here and --root set to this directory.\n')
 print(f'Prepared 72 videos, {total/1024**3:.2f} GiB; catalogue {(ROOT/"lib/lesson-videos.json").stat().st_size/1024:.1f} KiB. No upload or Git operation performed.')
if __name__=='__main__':main()
