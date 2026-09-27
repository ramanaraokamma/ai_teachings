from pathlib import Path
import json,hashlib,re,zipfile
from pypdf import PdfReader
from lxml import etree
root=Path('.')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return re.sub(r'[^a-z0-9]','',s.lower())
review={'checked':'PENDING visual review','method':'Automated canonical text and answer-separation audit. Visual inspection must be recorded separately before release.','renderers':{p:sha(Path(p)) for p in ['scripts/build-v3-documents.py','scripts/render-v3-diagrams.cjs']},'chapters':{}}
for source in sorted(Path('curriculum-v3').glob('ai-*-week-*.json')):
 w=json.loads(source.read_text());stem=source.stem
 r={'sourceHash':sha(source),'visualReview':'PENDING visual inspection of every page','documents':{},'diagrams':[]}
 for role in ['lesson','workbook','guide']:
  doc=Path('work/v3-docs')/f'{stem}-{role}.docx';folder=Path('work/v3-render')/f'{stem}-{role}';pdf=folder/f'{stem}-{role}.pdf'
  pages=sorted(folder.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1]));reader=PdfReader(pdf)
  assert len(pages)==len(reader.pages)
  with zipfile.ZipFile(doc) as z:
   xml=etree.fromstring(z.read('word/document.xml'));doc_text=' '.join(xml.xpath('//w:t/text()',namespaces={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}))
  pdf_text=' '.join(p.extract_text() for p in reader.pages)
  expected=[w['title']]
  if role=='lesson':
   expected+=w['goals']+[w['prerequisite']['prompt']]
   for section in w['lesson']:
    expected.append(section['title'])
    for b in section['blocks']:
     expected+=([b['text']] if b['type'] in ['paragraph','code'] else [b['label']] if b['type']=='response' else [b['title'],b['caption']] if b['type']=='diagram' else b['headers']+[v for row in b['rows'] for v in row])
   expected +=[v for row in w['vocabulary'] for v in row]
  elif role=='workbook':expected+=[x for t in w['workbook'] for x in [t['title'],t['prompt']]]
  else:
   t=w['teacher'];expected+=w['goals']+[w['prerequisite']['prompt'],w['prerequisite']['answer'],t['background'],t['guidedAnswer'],t['assessment'],t['support'],t['next']]+t['materials']+[v for row in t['sessions']+t['misconceptions'] for v in row]+[task['answer'] for task in w['workbook']]
  for text in expected:
   for label,actual in [('docx',doc_text),('pdf',pdf_text)]:assert norm(text) in norm(actual),(stem,role,label,text[:80])
  if role!='guide':
   for task in w['workbook']:assert norm(task['answer']) not in norm(doc_text)
  r['documents'][role]={'docx':sha(doc),'pdf':sha(pdf),'pages':[sha(p) for p in pages]}
 for p in sorted(Path('work/v3-diagrams').glob(stem+'-diagram-*.png')):r['diagrams'].append(sha(p))
 review['chapters'][f'{w["level"]}/{w["week"]}']=r
Path('work/v3-review-candidate.json').write_text(json.dumps(review,indent=2)+'\n')
print('Text audit passed. Candidate receipt saved in work/v3-review-candidate.json. Inspect all pages before completing and copying the review receipt.')
