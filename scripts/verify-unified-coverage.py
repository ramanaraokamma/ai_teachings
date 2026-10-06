"""Check source continuity, latest destinations, offline text and audience separation."""
import base64, hashlib, json, re
from pathlib import Path
from html.parser import HTMLParser
class Text(HTMLParser):
 def __init__(self): super().__init__(); self.parts=[]
 def handle_data(self,data): self.parts.append(data)
def norm(s): return ' '.join(s.split())
def strings(blocks):
 for b in blocks:
  if b['type']=='gallery':
   for cell in b['cells']: yield from strings(cell)
  elif b['type']=='table':
   for row in b['rows']: yield from row
  elif b.get('text'): yield b['text']
old=json.load(open('lib/academy-data.json'));rows=json.load(open('curriculum-v3/edition-coverage.json'));reviews=json.load(open('lib/grade6-review.json'));release=json.load(open('curriculum-v3/releases.json'));report=json.load(open('outputs/curriculum-reviewed/week-by-week-review.json'))
assert len(rows)==144 and len({r['legacy'] for r in rows})==144
checks=0; images=0
for l in old['levels']:
 for w in l['weeks']:
  key=f"{l['slug']}/{w['number']}";r=next(r for r in rows if r['legacy']==key)
  assert hashlib.sha256(json.dumps(w,sort_keys=True).encode()).hexdigest()==r['sourceHash']
  assert r['destination'] in release and release[r['destination']]['sourceHash']==r['destinationSourceHash']
  for role in ['student','teacher']:
   p=Path(f"outputs/curriculum-reviewed/{role}/practice/{key.replace('/','-')}.html");s=p.read_text();t=Text();t.feed(s);text=norm(' '.join(t.parts))
   pages=w['student']['pages'] if role=='student' else w['teacher']['pages']+w['student']['pages']
   for expected in strings([b for p in pages for b in p['blocks']]+w['workbook']['blocks']): assert norm(expected) in text,(key,role,expected[:80])
   assert norm(reviews[key]['task']) in text
   if role=='student': assert norm(reviews[key]['solution']) not in text,('answer leaked',key)
   else: assert norm(reviews[key]['solution']) in text
   for uri in re.findall(r'<img[^>]+src="([^"]+)"',s):
    assert uri.startswith('data:image/'); b=base64.b64decode(uri.split(',',1)[1]);assert b.startswith((b'\x89PNG\r\n\x1a\n',b'\xff\xd8\xff',b'RIFF'));images+=1
   checks+=1
for role,files in report['files'].items():
 root=Path('outputs/curriculum-reviewed')/role
 for name,digest in files.items():
  p=root/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
  if p.suffix=='.html':
   for href in re.findall(r'href="([^"]+)"',p.read_text()):
    if not href.startswith(('#','https:','http:')): assert (p.parent/href).resolve().is_file(),(p,href)
assert len(report['retainedPractice'])==144
print(f'144 source crosswalks; {checks} retained audience chapters with complete source text and role-separated transfer answers; {images} image placements; all offline hashes and links passed.')
