"""Mirror the complete offline edition and package explicitly allowed teaching files."""
from pathlib import Path
import shutil,json,zipfile,re,hashlib
R=Path(__file__).resolve().parents[1]
O=R/'outputs/ai-academy-complete-programme'
if R.name=='ai-academy-complete-programme':raise SystemExit('Run from the website repository root')
O.mkdir(parents=True,exist_ok=True)
folders=['assets','content','downloads','reports','student','teacher','tools','workbook']
names=['PICTORIAL_LESSONS.html','PROGRAMME_GUIDE.html','PROGRAMME_GUIDE.pdf','START_HERE.html','TEACHING_METHOD.html','TEACHING_METHOD.pdf','index.html']
for folder in folders:shutil.copytree(R/folder,O/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__','*.tmp.pdf'))
for name in names:shutil.copy2(R/name,O/name)
shutil.copytree(R/'public/python-runtime',O/'public/python-runtime',dirs_exist_ok=True)
shutil.copy2(R/'public/python-lab-worker.mjs',O/'public/python-lab-worker.mjs')
readme=(R/'README.md').read_text();readme=readme[readme.index('# AI Academy — Complete Learning Programme'):]
(O/'README.md').write_text(readme)
files=[f for f in O.rglob('*') if f.is_file() and f.name!='file-manifest.json']
(O/'reports/file-manifest.json').write_text(json.dumps([{'file':str(f.relative_to(O)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in sorted(files)],indent=2))
student_files=[O/'PICTORIAL_LESSONS.html']
for prefix in ['student','workbook','downloads/student','downloads/workbook']:student_files.extend(f for f in (O/prefix).rglob('*') if f.is_file())
assets={'programme.css','programme.js','learning-tools.js'}
student_files.extend(f for f in (O/'public/python-runtime').rglob('*') if f.is_file())
student_files.append(O/'public/python-lab-worker.mjs')
for f in student_files:
 if f.suffix=='.html':assets.update(re.findall(r'(?:\.\./)?assets/([^"\s<>]+)',f.read_text()))
student_files.extend(O/'assets'/name for name in sorted(assets))
home='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="assets/programme.css"><title>AI Academy student programme</title></head><body><main><header class="hero"><h1>Your complete AI learning journey</h1><p>Levels 1–3 → Python Readiness Bridge → Levels 4–7.</p></header><div class="actions"><a href="student/index.html">Student lessons</a><a href="workbook/index.html">Workbooks</a><a href="student/LEARNING_GUIDE.html">Learning guide</a></div><p>Use fictional data. Drafts stay in this browser when storage is available; print or save evidence for your portfolio.</p></main></body></html>'
student_zip=O.parent/'ai-academy-student-bundle.zip'
with zipfile.ZipFile(student_zip,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for f in student_files:z.write(f,'ai-academy-student/'+str(f.relative_to(O)))
 for name in ['START_HERE.html','index.html']:z.writestr('ai-academy-student/'+name,home)
 guide=(O/'student/LEARNING_GUIDE.html').read_text().replace('../START_HERE.html','START_HERE.html').replace('href="index.html"','href="student/index.html"').replace('../assets/','assets/')
 z.writestr('ai-academy-student/PROGRAMME_GUIDE.html',guide)
 z.writestr('ai-academy-student/README.txt','Open START_HERE.html. Keep printed or downloaded evidence. Teacher solutions and canonical source data are excluded. Clear drafts on shared devices.\n')
 # Enforce the role boundary for the distributable learner edition.
 assert not any('/teacher/' in n or '/content/' in n or '/tools/' in n or '/reports/' in n for n in z.namelist())
teacher_zip=O.parent/'ai-academy-teacher-bundle.zip'
with zipfile.ZipFile(teacher_zip,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for f in sorted(O.rglob('*')):
  if f.is_file():z.write(f,O.name+'/'+str(f.relative_to(O)))
print('Mirrored complete offline edition; recreated learner and private teacher bundles.')
