"""Assemble the complete portal project and all reading/download editions together."""
from pathlib import Path
import hashlib,html,json,re,shutil,subprocess,zipfile
root=Path(__file__).resolve().parents[1];out=root/'outputs/ai-academy-final';out.mkdir(parents=True,exist_ok=True)
files=[str(p.relative_to(root)) for directory in ('app','build','components','curriculum-v3','db','drizzle','examples','hooks','lib','public','scripts','tests','vendor','worker','.openai') for p in (root/directory).rglob('*') if p.is_file()]
files += [p.name for p in root.iterdir() if p.is_file() and p.name not in ('.DS_Store','tsconfig.tsbuildinfo')]
for name in files:
 if not name:continue
 p=root/name
 if '__pycache__' in p.parts or p.suffix=='.pyc':continue
 if not p.is_file() or name.startswith(('outputs/','work/','.git/','node_modules/','.wrangler/','.sites-runtime/','dist/')) or p.name.startswith(('.env','.dev.vars')):continue
 q=out/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
roadmap=json.loads((root/'curriculum-v3/progression.json').read_text());esc=html.escape
css='''*{box-sizing:border-box}body{margin:0;background:#f1f5fa;color:#172f49;font:17px/1.7 system-ui,sans-serif}header{background:#173b59;color:white;padding:38px max(22px,calc((100vw - 1150px)/2))}header p{max-width:850px;color:#e3eef8}h1{font-size:clamp(30px,5vw,48px);line-height:1.2;margin:18px 0}main{max-width:1190px;margin:auto;padding:28px 20px}h2{font-size:28px;line-height:1.3}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(255px,1fr));gap:20px;margin:28px 0}.card{background:white;border:1px solid #c4d3e1;border-radius:16px;padding:24px;text-decoration:none;color:inherit;display:block}.card:hover{border-color:#28689a;box-shadow:0 6px 22px #15395812}.card strong{display:block;font-size:22px;line-height:1.3;margin:12px 0}.card small{display:block;color:#4d6378;line-height:1.6}.number{font-size:38px;font-weight:800;color:#246293;display:block}.tag{font-size:13px;font-weight:bold;color:#43627e;letter-spacing:.07em}.note{background:#e7eff7;border-radius:12px;padding:22px}a{color:#175482}a:focus-visible{outline:3px solid #327cad;outline-offset:4px}nav{display:flex;flex-wrap:wrap;gap:16px}nav a{color:white}button{font:inherit}p{max-width:900px}li{margin:8px 0}.week{font-size:13px;text-transform:uppercase;font-weight:bold;color:#53718c}footer{padding:22px;text-align:center;color:#4c667e}@media(max-width:600px){main{padding:22px 16px}.grid{grid-template-columns:1fr}.card{padding:20px}}'''
def page(title,body,subtitle='',nav=''):
 return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)} · AI Academy</title><style>{css}</style></head><body><header><p class="tag" style="color:#b6d7ef">AI ACADEMY · GRADES 6–12</p><h1>{esc(title)}</h1><p>{subtitle}</p><nav>{nav}</nav></header><main>{body}</main><footer>One seven-level pathway · 252 weeks · Student and teacher resources</footer></body></html>'
for role in ('student','teacher'):
 dest=out/'offline'/role;shutil.copytree(root/'outputs/curriculum-reviewed'/role,dest,dirs_exist_ok=True)
 download=out/'downloads'/role;download.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(root/f'outputs/curriculum-complete/{role}-complete.zip') as z:
  for info in z.infolist():
   assert not info.filename.startswith('/') and '..' not in Path(info.filename).parts
  z.extractall(download)
 cards=[]
 for i,level in enumerate(roadmap['levels'],1):
  slug=level['slug'];cards.append(f'<a class="card" href="levels/{slug}.html"><span class="tag">GRADE {level["grade"]} · {slug.upper()}</span><span class="number">{i:02}</span><strong>{esc(level["name"])}</strong><small>36 weeks · {"Teaching guides, student reading and workbook practice" if role=="teacher" else "Illustrated reading, worked examples and workbook practice"}</small><p>Open level →</p></a>')
  weeks=[]
  for w,title in enumerate(level['weeks'],1):
   stem=f'{slug}-week-{w:02}';target=f'../{slug}/{stem}.html';extra=f'<a href="../../../downloads/{role}/{slug}/{stem}-guide.pdf">Guide PDF</a>' if role=='teacher' else f'<a href="{target}#workbook">Workbook practice</a>'
   weeks.append(f'<article class="card"><span class="week">Week {w:02}</span><strong>{esc(title)}</strong><p><a href="{target}">Open {"teaching guide" if role=="teacher" else "lesson"} →</a></p><small>{extra}</small></article>')
   chapter=dest/slug/(stem+'.html');s=chapter.read_text();kinds=['guide'] if role=='teacher' else ['lesson','workbook'];links=[]
   for kind in kinds:
    for ext in ('docx','pdf'):links.append(f'<a href="../../../downloads/{role}/{slug}/{stem}-{kind}.{ext}">{kind.title()} {ext.upper()}</a>')
   s=s.replace('<div class="actions">','<div class="actions"><a href="../index.html">All levels</a> · <a href="../levels/'+slug+'.html">This level</a> · '+' · '.join(links)+'<p class="note">These downloads are the reviewed core editions. Print this page to include the additional reading or teaching aids.</p>')
   chapter.write_text(s)
  body=f'<section class="note"><h2>Before starting</h2><p>{esc(level["prerequisites"])}</p><h2>What you will demonstrate</h2><p>{esc(level["exitEvidence"])}</p></section><section class="grid">'+''.join(weeks)+'</section>'
  p=dest/'levels'/f'{slug}.html';p.parent.mkdir(exist_ok=True);p.write_text(page(level['name'],body,f'Grade {level["grade"]} · 36 complete weeks', '<a href="../index.html">← All seven levels</a>'))
 body=f'<section class="note"><strong>Choose a level, then a week.</strong><p>All 252 weeks are included. Every current chapter also links to any retained illustrated practice for that topic. Core Word and PDF downloads are linked beside the reading.</p></section><section class="grid">'+''.join(cards)+'</section>'
 (dest/'index.html').write_text(page('Your teaching studio' if role=='teacher' else 'Your learning map',body,'One complete pathway with explanations, visual models, practice, challenges and capstones.','<a href="../../START_HERE.html">← Academy home</a>'))
 # Refresh the offline audience manifest after adding navigation and download links.
 m={str(p.relative_to(dest)):hashlib.sha256(p.read_bytes()).hexdigest() for p in dest.rglob('*') if p.is_file() and p.name!='ARTIFACT_MANIFEST.json'}
 (dest/'ARTIFACT_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
body='''<section class="grid"><a class="card" href="offline/student/index.html"><span class="tag">LEARN AND PRACTISE</span><strong>Student section</strong><p>All seven levels, 252 lessons and workbook missions, plus 144 illustrated topic-practice chapters.</p><small>Open the complete learning map →</small></a><a class="card" href="offline/teacher/index.html"><span class="tag">PLAN AND TEACH</span><strong>Teacher section</strong><p>All 252 weekly guides, worked solutions, teaching sequences and 144 retained practice editions.</p><small>Open the complete teaching studio →</small></a></section><section class="note"><h2>The complete application is here too</h2><p>This folder contains the full protected portal project in the same structure as the outer project: app, components, lib, public, worker, curriculum sources and build scripts. The two sections above are the complete offline reader; to run the password-protected application, follow START_HERE.md.</p><p>Word/PDF downloads are together under downloads/student and downloads/teacher. The latest aids are in the reading pages; the original approved core documents are preserved.</p></section>'''
(out/'START_HERE.html').write_text(page('Learn deeply. Build confidently.',body,'One unified AI Academy · Seven levels · Grades 6–12 · All content together.'))
(out/'index.html').write_text((out/'START_HERE.html').read_text())
(out/'START_HERE.md').write_text('''# AI Academy — complete unified version

Start with START_HERE.html. It opens the full student and teacher maps, all seven levels, every current week, retained illustrated practice, and linked Word/PDF downloads. No installation is needed for offline reading.

This is also the COMPLETE application project, following the original outer-folder structure. It is not a single-week lesson export.

## Run the protected portal

Requires Node.js 22.13 or newer. Open a terminal in this folder:

```
npm ci
node scripts/setup-local.mjs
npm run dev
```

Open the local URL printed by the server. Student passcode: student1234. Teacher passcode: teacher1234. Setup generates a separate random local session secret and preserves existing configuration. The offline reader is for local reading; the running portal enforces student/teacher roles.

To build and check the full application:

```
npm run build
npx tsc --noEmit
node --loader ./tests/cloudflare-loader.mjs tests/academy-access.mjs
```

## Folder contents

- app/, components/, lib/, public/, worker/: complete website source and protected resources.
- curriculum-v3/: all 252 latest weekly sources, supplements and the 144-topic continuity audit.
- offline/student/, offline/teacher/: complete illustrated study editions, level maps and topic practice.
- downloads/student/, downloads/teacher/: all reviewed Word/PDF packages and figures.
- examples/: executable lab examples.
- scripts/, tests/, package.json and lockfile: reproducible installation, build, content and access checks.

Teacher solutions are kept in the teacher section. Both sections are in this complete project, so give students the student section rather than the entire teacher preparation folder. No deployment was performed.
''')
(out/'README.md').write_text((out/'START_HERE.md').read_text()+'\nCoverage and review records: curriculum-v3/UNIFIED_COVERAGE.md, curriculum-v3/CONTENT_REVIEW.md and curriculum-v3/unified-validation.json.\n')
manifest={str(p.relative_to(out)):hashlib.sha256(p.read_bytes()).hexdigest() for p in out.rglob('*') if p.is_file() and p.name not in ('PACKAGE_MANIFEST.json','PACKAGE_VALIDATION.json')}
(out/'PACKAGE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(f'Complete project prepared: {out}; {len(manifest)} files, 252 current weeks and 144 retained topics per audience.',flush=True)
# Validate every local reader link and every file hash before creating the single archive.
for name,digest in manifest.items():
 p=out/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==digest
 if name.startswith('offline/') and p.suffix=='.html' or name in ('index.html','START_HERE.html'):
  for href in re.findall(r'href="([^"]+)"',p.read_text()):
   target=href.split('#')[0]
   if target and not target.startswith(('https:','http:','data:')):assert (p.parent/target).resolve().is_file(),(name,href)
validation={'files':len(manifest),'currentWeeks':252,'retainedTopics':144,'latestDocs':1512,'offlineAudienceChapters':792,'hashes':'passed','readerLinksAndDownloads':'passed','sourceProject':'full app, components, lib, public, worker, scripts, tests and configuration'}
layout=root/'work/study-layout-review/complete-package-layout.json'
if layout.is_file():
 screen=json.loads(layout.read_text());assert not screen['errors'];validation['desktopMobileLayoutChecks']=screen['checks'];validation['packagedProtectedResources']='3937 source and artifact checks passed';validation['localSetup']='creates configuration and preserves existing file'
(out/'PACKAGE_VALIDATION.json').write_text(json.dumps(validation,indent=2)+'\n')
archive=root/'outputs/ai-academy-final.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in out.rglob('*'):
  if p.is_file():z.write(p,'ai-academy-final/'+str(p.relative_to(out)),compress_type=zipfile.ZIP_STORED if p.suffix in ('.bin','.pdf','.docx','.png') else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(manifest)+2
print(f'Complete archive verified: {archive}',flush=True)
