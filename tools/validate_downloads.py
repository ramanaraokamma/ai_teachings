"""Compare actual export text with each role's canonical paragraphs and cells."""
from pathlib import Path
import json,re,unicodedata,zipfile,os,hashlib,xml.etree.ElementTree as ET
import fitz
ROOT=Path(__file__).resolve().parents[1];D=json.loads((ROOT/'content/programme.json').read_text())
def normal(t):
 t=unicodedata.normalize('NFKC',t).replace('\u00ad','').replace('\u200b','')
 return re.sub(r'\s+','',t)
def expected(b):
 if b['type']=='image':return []
 if b['type']=='gallery':return [x for cell in b['cells'] for c in cell for x in expected(c)]
 if b['type']=='diagram':return [b.get('title',''),b.get('caption',''),b.get('key','')]+[str(c) for row in b.get('rows',b.get('values',[])) for c in row]+[s['label'] for s in b.get('series',[])]+[str(v) for s in b.get('series',[]) for v in s['values']]
 if b['type']=='table':return [str(c) for row in b['rows'] for c in row]
 if b['type']=='response':return [b.get('label','')]
 return [b.get('text','')]
scope=set(filter(None,os.environ.get("CHECK_WEEKS","").split(",")))
errors=[];rows=[];total_pages=0;visual_cache={}
if scope:
 previous=json.loads((ROOT/"reports/download-validation.json").read_text());assert not previous["errors"]
 rows=[row for row in previous["results"] if row["week"] not in scope];total_pages=sum(row["pdf_pages"] for row in rows)
for w in D['weeks']+D['python_bridge']:
 if scope and w['id'] not in scope:continue
 stem=('bridge-' if w['id'].startswith('python') else f"ai-{w['level']}-")+f"week-{w['week']:02}"
 for role,key in [('student','sections'),('teacher','teacher'),('workbook','workbook')]:
  wanted=[x for sec in w[key] for b in sec['blocks'] for x in expected(b) if x.strip()]
  row={'week':w['id'],'role':role,'checked_text_items':len(wanted)}
  visual_names={b['src'].split('/')[-1]+'.png' for sec in w[key] for b in sec['blocks'] if b.get('academy_visual')}
  expected_visuals=[]
  for name in visual_names:
   if name not in visual_cache:
    asset=ROOT/'assets'/name;pix=fitz.Pixmap(asset)
    visual_cache[name]={'name':name,'width':pix.width,'height':pix.height,'pixels':hashlib.md5(pix.samples).digest(),'file_hash':hashlib.sha256(asset.read_bytes()).digest()}
   expected_visuals.append(visual_cache[name])
  row['pictorial_images_checked']=len(expected_visuals)
  for ext in ['docx','pdf']:
   path=ROOT/'downloads'/role/(stem+'.'+ext)
   if not path.exists():errors.append({'file':str(path.relative_to(ROOT)),'error':'missing'});continue
   if ext=='docx':
    with zipfile.ZipFile(path) as z:
     tree=ET.fromstring(z.read('word/document.xml'))
     text=''.join(n.text or '' for n in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'))
     embedded={hashlib.sha256(z.read(name)).digest() for name in z.namelist() if name.startswith('word/media/')}
     for visual in expected_visuals:
      if visual['file_hash'] not in embedded:errors.append({'file':str(path.relative_to(ROOT)),'missing_pictorial_image':visual['name']})
   else:
    with fitz.open(path) as pdf:
     row['pdf_pages']=len(pdf);total_pages+=len(pdf)
     painted=set();wanted_shapes={(v['width'],v['height']) for v in expected_visuals}
     for page in pdf:
      if any((info['width'],info['height']) in wanted_shapes for info in page.get_image_info()):
       painted.update(info['digest'] for info in page.get_image_info(hashes=True))
     for visual in expected_visuals:
      if visual['pixels'] not in painted:errors.append({'file':str(path.relative_to(ROOT)),'missing_painted_pictorial_image':visual['name']})
     text=''.join(re.sub(r'AI Academy\s*\|\s*\d+\s*/\s*\d+\s*', '', page.get_text()) for page in pdf)
   full=normal(text);missing=[x for x in wanted if normal(x) not in full]
   row[ext+'_missing_text']=len(missing)
   if missing:errors.append({'file':str(path.relative_to(ROOT)),'missing':missing})
  rows.append(row)
  if len(rows)%90==0:print('Checked export text:',len(rows),flush=True)
report={'weekly_resources':len(rows),'word_files':len(list((ROOT/'downloads').rglob('*.docx'))),'pdf_files':len(list((ROOT/'downloads').rglob('*.pdf'))),'pdf_pages':total_pages,'pictorial_image_instances_checked':sum(row.get('pictorial_images_checked',0) for row in rows),'errors':errors,'results':rows}
(ROOT/'reports/download-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:v if k!='errors' else len(v) for k,v in report.items() if k!='results'},indent=2))
if errors:raise SystemExit(1)
