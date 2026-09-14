"""Export the authenticated SSR fixtures as a private, printable HTML collection.

Run EXPORT_BOOKS=1 node --loader ./tests/cloudflare-loader.mjs tests/academy-access.mjs first.
The output contains teacher material. Do not copy this collection into public hosting.
"""
from pathlib import Path
import base64, html, json, re, shutil, sys, zipfile
from bs4 import BeautifulSoup
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

root=Path(__file__).resolve().parents[1]
out=Path(sys.argv[1]).resolve()
out.mkdir(parents=True,exist_ok=True)
(out/'assets').mkdir(exist_ok=True)
data=json.loads((root/'lib/academy-data.json').read_text())
manifest=json.loads((root/'lib/resource-manifest.json').read_text())
key=base64.b64decode(re.search(r'[\"\x27]([A-Za-z0-9+/]{43}=)[\"\x27]',(root/'lib/resource-key.ts').read_text()).group(1))
css_seen={};images=set();reports=[]
script="""document.querySelectorAll('textarea').forEach(t=>t.addEventListener('input',()=>{const p=t.parentElement.querySelector('.print-answer');if(p)p.textContent=t.value;}));let opened=[];addEventListener('beforeprint',()=>{opened=[...document.querySelectorAll('details.topic-solution:not([open])')];opened.forEach(d=>d.open=true)});addEventListener('afterprint',()=>{opened.forEach(d=>d.open=false)});"""
for level in data['levels']:
    folder=out/level['slug'];folder.mkdir(exist_ok=True)
    for week in level['weeks']:
        for resource in ['lesson','guide','workbook']:
            name=f"week-{week['number']:02}-{resource}.html"
            source=root/'outputs/books'/level['slug']/name
            soup=BeautifulSoup(source.read_text(),'html.parser')
            for tag in soup.select('script, .portal-header, .resource-nav, .week-pagination, .lesson-breadcrumbs'):
                tag.decompose()
            for link in soup.select('link'):
                href=link.get('href','')
                if 'stylesheet' in link.get('rel',[]) and href.startswith('/'):
                    css_seen[href]=(root/'dist/client'/href.lstrip('/')).read_text()
                link.decompose()
            stylelink=soup.new_tag('link',attrs={'rel':'stylesheet','href':'../assets/book.css'})
            soup.head.append(stylelink)
            for img in soup.select('img'):
                rid=img.get('src','').split('/')[-1]
                assert rid in manifest, f'Unknown image {rid}'
                assert resource=='guide' or manifest[rid]['role']=='student'
                assert manifest[rid]['mime']=='image/png'
                if rid not in images:
                    packed=(root/f'public/curriculum-blobs/{rid}.bin').read_bytes()
                    decoded=AESGCM(key).decrypt(packed[:12],packed[12:],rid.encode())
                    assert decoded[:8]==b'\x89PNG\r\n\x1a\n'
                    (out/'assets'/f'{rid}.png').write_bytes(decoded)
                    images.add(rid)
                img['src']=f'../assets/{rid}.png';img['loading']='eager'
                img.attrs.pop('srcset',None)
            for tag in soup.select('.visual-zoom-label'):tag.decompose()
            for tag in soup.select('.visual-expand'):
                tag.name='div'
                for attr in ['type','aria-haspopup','aria-expanded','data-state','aria-label']:tag.attrs.pop(attr,None)
                tag['style']='cursor:default'
            for tag in soup.select('.resource-actions'):
                tag.clear()
                home=soup.new_tag('a',attrs={'href':'../index.html','class':'resource-action'});home.string='All levels and weeks';tag.append(home)
                for r,label in [('lesson','Student lesson'),('guide','Teacher guide'),('workbook','Workbook')]:
                    if r!=resource:
                        a=soup.new_tag('a',attrs={'href':f"week-{week['number']:02}-{r}.html",'class':'resource-action'});a.string=label;tag.append(a)
                b=soup.new_tag('button',attrs={'class':'resource-action','onclick':'window.print()'});b.string='Print this resource';tag.append(b)
            for tag in soup.select('.sensor-control'):
                tag.clear();p=soup.new_tag('p');p.string='Worked reading: 18 on the classroom model’s made-up 0–100 scale.';tag.append(p)
            intro=soup.select_one('.sensor-lab>p')
            if intro:intro.string='Follow the fixed-rule demonstration at a reading of 18. This printable model uses a made-up light scale from 0 to 100.'
            js=soup.new_tag('script');js.string=script;soup.body.append(js)
            soup.title.string=f"{level['code']} · {week['student']['title']} · {resource.title()}"
            final=str(soup)
            assert '/api/resource/' not in final
            assert not re.search(r'(?:src|href)=[\"\x27]/',final),f'Nonportable link: {name}'
            if resource=='lesson':
                assert len(soup.select('.book-chapter'))==len(week['student']['pages'])
                assert len(soup.select('.topic-diagram'))==1
                assert len(soup.select('.instruction-visual'))==5
            (folder/name).write_text(final)
            reports.append({'level':level['slug'],'week':week['number'],'resource':resource,'images':len(soup.select('img')),'file':f"{level['slug']}/{name}"})
css='\n'.join(css_seen.values())
# Local font/image dependencies in generated CSS must also remain portable.
for match in set(re.findall(r'url\([\"\x27]?(/[^)\"\x27]+)',css)):
    path=root/'dist/client'/match.lstrip('/')
    if path.is_file():
        shutil.copy2(path,out/'assets'/path.name);css=css.replace(match,path.name)
(out/'assets/book.css').write_text(css)
sections=[]
for level in data['levels']:
    cards=[]
    for w in level['weeks']:
        links=''.join(f'<a href="{level["slug"]}/week-{w["number"]:02}-{r}.html">{label}</a>' for r,label in [('lesson','Lesson'),('guide','Teacher guide'),('workbook','Workbook')])
        cards.append(f'<article><span>WEEK {w["number"]:02}</span><h3>{html.escape(w["student"]["title"].split(": ",1)[-1])}</h3><nav>{links}</nav></article>')
    sections.append(f'<section id="{level["slug"]}"><h2>{level["code"]} {level["name"]} <small>{level["ages"]}</small></h2><div class="weeks">'+''.join(cards)+'</div></section>')
(out/'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Academy — Complete Visual Teaching Collection</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#15334b;background:#f3f8fc;margin:0}main{max-width:1200px;margin:auto;padding:32px 20px}h1{font-size:clamp(2rem,5vw,3.5rem);line-height:1.15;max-width:800px}h2{margin-top:3rem}h2 small{display:block;font-size:1rem;font-weight:400}.weeks{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}article{background:white;border:1px solid #c4d7e7;border-top:4px solid #175cd3;border-radius:8px;padding:20px}article span{color:#245e85;font-weight:750;font-size:.875rem}article h3{line-height:1.4;min-height:3rem}nav{display:flex;gap:12px;flex-wrap:wrap}a{color:#175cd3;font-weight:650}a:focus-visible{outline:3px solid #175cd3;outline-offset:3px}.intro{max-width:780px}.note{padding:16px;background:#e4f2ee;border-left:4px solid #0f766e}header nav{margin:24px 0}header a{background:white;border:1px solid #c4d7e7;padding:10px 18px;border-radius:6px}</style></head><body><main><header><p>AI ACADEMY · CURRICULUM 2.0</p><h1>A visual teaching journey, one week at a time.</h1><p class="intro">Four levels. Thirty-six weeks each. Open a student lesson, the matching teacher guide, or workbook practice. Each resource can be read offline and printed from your browser.</p><p class="note">This private teaching collection includes teacher answers. Use the separate protected website package for hosting. Written responses in these HTML files last only while the page stays open; print to preserve your work.</p><nav>'''+''.join(f'<a href="#{l["slug"]}">{l["code"]} {l["name"]}</a>' for l in data['levels'])+'</nav></header>'+''.join(sections)+'</main></body></html>')
shutil.copy2(root/'VISUAL_COVERAGE.md',out/'VISUAL_COVERAGE.md')
(out/'README.txt').write_text('Open index.html in a browser. Keep the assets folder beside the four level folders.\nIncludes 144 student lessons, 144 teacher guides and 144 workbook practice pages.\nTeacher answers are included: this is a private offline collection, not a public hosting package.\nPrint from each resource page; worked explanations expand for printing.\nResponses clear when you reload or navigate away.\nThe separately delivered website ZIP retains passcode protection and all 292 original DOCX downloads.\n')
assert len(reports)==432
(out/'coverage.json').write_text(json.dumps({'edition':'topic-studio-2026-09-14','pages':432,'student_lessons':144,'teacher_guides':144,'workbooks':144,'unique_images':len(images),'resources':reports},indent=2))
target=out.with_suffix('.zip')
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(out.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(out))
with zipfile.ZipFile(target) as z:assert z.testzip() is None
print(json.dumps({'zip':str(target),'html_resources':len(reports),'unique_images':len(images),'bytes':target.stat().st_size}))
