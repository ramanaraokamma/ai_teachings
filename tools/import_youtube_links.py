"""Import filled YouTube links; blank CSV cells preserve existing links for later batches."""
from pathlib import Path
import argparse,csv,json,re
from urllib.parse import urlparse,parse_qs
ROOT=Path(__file__).resolve().parents[1]
def video_id(value):
 value=value.strip()
 if re.fullmatch(r'[A-Za-z0-9_-]{11}',value):return value
 url=urlparse(value)
 if url.scheme!='https' or url.username or url.password:raise ValueError('Expected an HTTPS YouTube link')
 host=(url.hostname or '').lower();parts=url.path.strip('/').split('/')
 if host=='youtu.be':result=parts[0] if len(parts)==1 else ''
 elif host in ['youtube.com','www.youtube.com','m.youtube.com','youtube-nocookie.com','www.youtube-nocookie.com']:
  if url.path=='/watch':result=parse_qs(url.query).get('v',[''])[0]
  elif len(parts)==2 and parts[0] in ['embed','shorts','live']:result=parts[1]
  else:result=''
 else:raise ValueError('Expected a YouTube host')
 if not re.fullmatch(r'[A-Za-z0-9_-]{11}',result):raise ValueError('Missing or invalid YouTube video ID')
 return result

def import_rows(rows,known,existing):
 result={key:existing.get(key,'') for key in known};seen=set()
 for row in rows:
  key=(row.get('lesson_id') or '').strip()
  if key not in known or key in seen:raise ValueError('Unknown or duplicate lesson ID: '+key)
  seen.add(key);value=(row.get('youtube_url') or '').strip()
  if value:result[key]=video_id(value)
 ids=[v for v in result.values() if v]
 if len(ids)!=len(set(ids)):raise ValueError('The same YouTube video is assigned to more than one lesson')
 return result

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv',nargs='?',type=Path,default=ROOT/'outputs/youtube-upload-ai-1-ai-2/youtube-links.csv');args=p.parse_args()
 target=ROOT/'lib/youtube-videos.json';catalogue=json.loads((ROOT/'lib/lesson-videos.json').read_text());existing=json.loads(target.read_text()) if target.exists() else {}
 with args.csv.expanduser().open(encoding='utf-8-sig',newline='') as f:
  reader=csv.DictReader(f)
  if not {'lesson_id','youtube_url'}.issubset(reader.fieldnames or []):raise ValueError('CSV requires lesson_id and youtube_url columns')
  result=import_rows(reader,catalogue,existing)
 temp=target.with_suffix('.json.tmp');temp.write_text(json.dumps(result,indent=2)+'\n');temp.replace(target)
 filled=[k for k,v in result.items() if v];print(f'Imported {len(filled)} YouTube links; {len(result)-len(filled)} weeks remain pending. Blank cells preserve previously imported links.');print(', '.join(filled))
if __name__=='__main__':main()
