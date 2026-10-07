"""Local paginated PDF fallback; browser interactive/layout checks remain pending."""
from pathlib import Path
import json,html,re,os,textwrap
import fitz
from PIL import Image
R=Path(__file__).resolve().parents[1];D=json.loads((R/'content/programme.json').read_text());e=lambda x:html.escape(str(x))
CSS='''body{font-family:sans-serif;font-size:10.5pt;line-height:1.45;color:#183249}h1{font-size:24pt;color:#123b52}h2{font-size:17pt;color:#174c69;page-break-after:avoid}h3{font-size:12pt;color:#126878;page-break-after:avoid}p{margin:8pt 0}table{border-collapse:collapse;width:100%;font-size:9pt;margin:10pt 0}td,th{border:1px solid #bacfdc;padding:7pt;vertical-align:top}th{background-color:#e6f2f5}img{margin:10pt 0}.note{background-color:#fff7e8;padding:10pt}.response{background-color:#f0f6f9;padding:10pt}.code{font-family:monospace;font-size:8.5pt;background-color:#f0f5f8;padding:8pt}.caption{font-size:9pt;color:#466378}'''
def table(rows):
 if not rows:return ''
 headers=rows[0]
 out='<div class="note"><p><b>'+ ' · '.join(e(x) for x in headers)+'</b></p></div>'
 for row in rows[1:]:
  for i,c in enumerate(row):
   out+='<p><b>'+e(headers[i] if i<len(headers) else 'Value')+':</b> '+(e(c) if str(c).strip() else '________________________')+'</p>'
  out+='<p>────────────────────────</p>'
 return out

def block(b):
 t=b['type'];text=b.get('text','')
 if t=='image':
  name=b['src'].split('/')[-1]+'.png'
  with Image.open(R/'assets'/name) as im:width,height=im.size
  scale=min(490/width,(468 if b.get("academy_visual") else 252)/height,1)
  return '<p><img src="assets/'+name+'" width="'+str(int(width*scale))+'" height="'+str(int(height*scale))+'"></p>'
 if t=='gallery':return ''.join(block(x) for cell in b['cells'] for x in cell)
 if t=='diagram':
  text='<h3>'+e(b.get('title',''))+'</h3>'
  if b.get('rows'):text+=table([b.get('columns',['Stage','Evidence','Result'])]+b['rows'])
  elif b.get('values'):text+='<p>'+e(b.get('key',''))+'</p>'+table(b['values'])
  return text+'<p class="caption">'+e(b.get('caption',''))+'</p>'
 if t=='table':return table(b['rows'])
 if t=='code':return '<div class="code">'+''.join('<p>'+e(line).replace(' ','&#160;')+'</p>' for original in text.splitlines() for line in (textwrap.wrap(original,width=76,replace_whitespace=False,drop_whitespace=False,break_on_hyphens=False) or ['']))+'</div>'
 if t=='response':return '<div class="response"><p><b>'+e(b.get('label',''))+'</b></p>'+('<p>________________________________________________________________</p>'*min(b.get('lines',4),8))+'</div>'
 if t=='sensor':return '<h3>The sensor measures. The rule decides.</h3><p>Light scale:0 darker,100 brighter. Written rule: reading below30 → lamp ON; otherwise OFF. Trace29 → ON and30 → OFF. Use the HTML slider to investigate.</p>'
 if t in ['heading','title','subheading']:return '<h3>'+e(text)+'</h3>'
 return '<p'+(' class="note"' if t=='callout' else '')+'>'+e(text)+'</p>'
def save(body,path):
 story=fitz.Story(html=body,user_css=CSS,archive=fitz.Archive(str(R)))
 writer=fitz.DocumentWriter(str(path))
 def rectfn(n,filled):
  page=fitz.Rect(0,0,612,792);return page,page+(47,47,-47,-47),None
 story.write(writer,rectfn);writer.close()
 with fitz.open(path) as doc:
  for i,page in enumerate(doc):page.insert_text((47,768),'AI Academy  |  '+str(i+1)+' / '+str(len(doc)),fontsize=8,color=(.25,.38,.45))
  temp=path.with_suffix('.tmp.pdf');doc.save(temp,garbage=4,deflate=True)
 temp.replace(path)
rows=[]
for w in ([] if os.environ.get('ONLY_GUIDES') else D['weeks']+D['python_bridge']):
 if os.environ.get('CHECK_WEEKS') and w['id'] not in os.environ['CHECK_WEEKS'].split(','):continue
 stem=('bridge-' if w['id'].startswith('python') else f"ai-{w['level']}-")+f"week-{w['week']:02}"
 for role,key in [('student','sections'),('teacher','teacher'),('workbook','workbook')]:
  body='<p>AI Academy · '+e(w['id'])+' · '+role+'</p><h1>'+e(w['title'])+'</h1><p>Project: '+e(w['project'])+'</p>'
  body+=''.join('<h2>'+str(i+1)+'. '+e(s['title'])+'</h2>'+''.join(block(b) for b in s['blocks']) for i,s in enumerate(w[key]))
  path=R/'downloads'/role/(stem+'.pdf');save(body,path);rows.append(str(path.relative_to(R)))
  if len(rows)%90==0:print('Local PDFs:',len(rows),flush=True)
for file in ['TEACHING_METHOD.html','PROGRAMME_GUIDE.html','student/LEARNING_GUIDE.html']:
 source=(R/file).read_text();body=re.search(r'<main>(.*)</main>',source,re.S).group(1);save(body,R/file.replace('.html','.pdf'))
if rows:(R/'reports/pdf-rendering.json').write_text(json.dumps({'renderer':'PyMuPDF Story','weekly_files':len(list((R/'downloads').rglob('*.pdf'))),'guide_files':3,'browser_layout_verified':False,'reason':'Chrome launch aborted in restricted workspace; no permission escalation available.'},indent=2))
