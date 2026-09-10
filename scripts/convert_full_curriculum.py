#!/usr/bin/env python3
"""Faithful Word-to-web conversion with authenticated media and downloads.

Public assets contain only AES-GCM ciphertext. The key and role manifest are
server-only; the resource route verifies the session before decryption.
"""
import base64, hashlib, json, os, re, shutil, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from docx import Document
from docx.oxml.ns import qn
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table
from docx.text.paragraph import Paragraph
from extract_curriculum import LEVELS, find_week_file

PROJECT=Path(__file__).resolve().parents[1]
OUT=PROJECT/'public/curriculum-blobs'
MANIFEST={}
KEY=AESGCM.generate_key(bit_length=256)
CIPHER=AESGCM(KEY)
IMAGE_OCCURRENCES=0

def asset(data,mime,role='student',filename=None):
    digest=hashlib.sha256(role.encode()+data).hexdigest()
    if digest not in MANIFEST:
        nonce=os.urandom(12)
        packed=nonce+CIPHER.encrypt(nonce,data,digest.encode())
        temporary=OUT/(digest+'.tmp')
        temporary.write_bytes(packed)
        temporary.replace(OUT/(digest+'.bin'))
        MANIFEST[digest]={'mime':mime,'role':role,'filename':filename}
    return '/api/resource/'+digest

def iter_items(parent):
    element=parent.element.body if hasattr(parent,'element') else parent._tc
    for child in element.iterchildren():
        if isinstance(child,CT_P): yield Paragraph(child,parent)
        elif isinstance(child,CT_Tbl): yield Table(child,parent)

def paragraph(p,role):
    global IMAGE_OCCURRENCES
    result=[]
    style=(p.style.name or '').lower()
    text=p.text.replace('\u00a0',' ').strip()
    if text:
        if re.fullmatch(r'[_\-–—. ]{10,}',text):kind='response'
        elif 'code' in style:kind='code'
        elif style=='title':kind='title'
        elif style in ['heading 1','refine heading']:kind='heading'
        elif style in ['heading 2','heading 3','refine subheading']:kind='subheading'
        else:kind='paragraph'
        block={'type':kind,'text':text}
        if 'list' in style:
            block.update(type='list',marker='number' if 'number' in style else 'bullet')
        tones={'key idea':'idea','think box':'think','caution box':'caution','teacher note':'teacher','answer box':'answer'}
        if style in tones:block.update(type='callout',tone=tones[style])
        result.append(block)
    for drawing in p._p.xpath('.//w:drawing'):
        props=drawing.xpath('.//wp:docPr')
        extent=drawing.xpath('.//wp:extent')
        for blip in drawing.xpath('.//a:blip'):
            part=p.part.related_parts[blip.get(qn('r:embed'))]
            src=asset(part.blob,part.content_type,role)
            alt=(props[0].get('descr') or props[0].get('title') or props[0].get('name')) if props else 'Lesson diagram'
            result.append({'type':'image','src':src,'alt':alt,'width':round(int(extent[0].get('cx'))/9525) if extent else 640,'height':round(int(extent[0].get('cy'))/9525) if extent else 480})
            IMAGE_OCCURRENCES+=1
    return result

def compact(blocks):
    output=[]
    for block in blocks:
        if block['type']=='response' and output and output[-1]['type']=='response':continue
        output.append(block)
    return output

def table(t,role):
    rich=[]
    has_images=False
    for row in t.rows:
        cells=[]
        seen=set()
        for cell in row.cells:
            if cell._tc in seen:continue
            seen.add(cell._tc)
            blocks=[]
            for item in iter_items(cell):
                blocks.extend(paragraph(item,role) if isinstance(item,Paragraph) else [table(item,role)])
            has_images=has_images or any(b['type']=='image' for b in blocks)
            cells.append(blocks)
        rich.append(cells)
    if has_images:return {'type':'gallery','cells':[c for r in rich for c in r]}
    return {'type':'table','rows':[['\n'.join(b.get('text','') for b in c) for c in r] for r in rich]}

def label(blocks,index):
    for b in blocks:
        if b['type'] in ['heading','title']:return re.sub(r'^Week \d+\s*[:—]?\s*','',b['text'])
    for b in blocks:
        text=b.get('text','')
        if text.isupper() and len(text)<50:return text.title()
    return f'Practice and evidence {index}'

def parse_module(path,week,role):
    d=Document(path);pages=[];current=[]
    def finish():
        nonlocal current
        if current:
            n=len(pages)+1
            pages.append({'number':n,'label':label(current,n),'blocks':compact(current)})
            current=[]
    for item in iter_items(d):
        if isinstance(item,Paragraph):
            text=item.text.strip()
            if text.startswith('AI ACADEMY') and 'WEEK' in text:
                finish();continue
            if item.paragraph_format.page_break_before:finish()
            current.extend(paragraph(item,role))
            if item._p.xpath('.//w:br[@w:type="page"]'):finish()
        else:current.append(table(item,role))
    finish()
    title=next((b['text'] for page in pages[:2] for b in page['blocks'] if b['type']=='title'),None)
    if not title:
        title=re.sub(r'^AI-\d_Week_\d+_|_(Student|Teacher)_Refined$','',path.stem).replace('_',' ')
        title=f'Week {week}: {title}'
    return {'title':title,'pages':pages,'download':asset(path.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document',role,path.name)}

def parse_workbook(path):
    d=Document(path);weeks={};week=None
    for item in iter_items(d):
        if isinstance(item,Paragraph):
            m=re.match(r'Week (\d+)\s*:',item.text)
            if m and item.style.name in ['Title','Heading 1']:
                week=int(m[1]);weeks[week]=[]
            if week is not None:weeks[week].extend(paragraph(item,'student'))
        elif week is not None:weeks[week].append(table(item,'student'))
    assert sorted(weeks)==list(range(1,37))
    return {w:compact(b) for w,b in weeks.items()},asset(path.read_bytes(),'application/vnd.openxmlformats-officedocument.wordprocessingml.document','student',path.name)

PHASES={
 'ai-1':['Discover AI and signals','Represent and follow algorithms','Learn and predict','Recommend and examine data','Generate, verify and design','Build, test and defend'],
 'ai-2':['Trace algorithms','Structure data and classify','Analyze errors and data quality','Fair data and recommendations','Generative systems and tools','Boundaries and capstone'],
 'ai-3':['Generation and prompt foundations','Refine prompts and media','Verify and retrieve evidence','Build a grounded assistant','Evaluate and design responsibly','Boundaries and creator capstone'],
 'ai-4':['ML and data foundations','Sampling, leakage and baselines','Train and evaluate classifiers','Regression and data splits','Experiment and generalize','Fairness and ML capstone'],
}

def main(source):
    OUT.mkdir(parents=True,exist_ok=True)
    for p in OUT.iterdir():p.unlink()
    levels=[]
    for folder,meta in LEVELS.items():
        root=source/folder
        wb,wb_download=parse_workbook(next((root/'Workbooks').glob('*.docx')))
        level={k:v for k,v in meta.items() if k!='phaseNames'}
        level['phases']=[{'number':i+1,'name':n,'weeks':f'{i*6+1}–{i*6+6}'} for i,n in enumerate(PHASES[level['slug']])]
        level['weeks']=[]
        for w in range(1,37):
            student=parse_module(find_week_file(root/'Student_Modules',w),w,'student')
            teacher=parse_module(find_week_file(root/'Teacher_Guides',w),w,'teacher')
            hero=next((b['src'] for p in student['pages'] for b in p['blocks'] if b['type']=='image'),None)
            workbook={'title':next(b['text'] for b in wb[w] if b['type']=='title'),'blocks':wb[w],'download':wb_download}
            level['weeks'].append({'number':w,'phase':(w-1)//6+1,'student':student,'teacher':teacher,'workbook':workbook,'hero':hero})
        levels.append(level)
    (PROJECT/'lib/academy-data.json').write_text(json.dumps({'version':'Curriculum 2.0 — Illustrated Web Edition','levels':levels},ensure_ascii=False,separators=(',',':')))
    (PROJECT/'lib/resource-manifest.json').write_text(json.dumps(MANIFEST,separators=(',',':')))
    (PROJECT/'lib/resource-key.ts').write_text('import "server-only";\nexport const resourceKey = '+json.dumps(base64.b64encode(KEY).decode())+';\n')
    old=PROJECT/'public/academy-art'
    if old.exists():shutil.rmtree(old)
    report={'levels':4,'weeks':144,'inline_image_occurrences':IMAGE_OCCURRENCES,'protected_resources':len(MANIFEST),'downloads':sum(bool(v['filename']) for v in MANIFEST.values())}
    (PROJECT/'conversion-audit.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report))

if __name__=='__main__':main(Path(sys.argv[1]))
