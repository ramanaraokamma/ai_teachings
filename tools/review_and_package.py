"""Write coverage/review records and distributable archives after validation."""
from pathlib import Path
import json,csv,hashlib,zipfile,re,html,datetime
ROOT=Path(__file__).resolve().parents[1];D=json.loads((ROOT/'content/programme.json').read_text());S=json.loads((ROOT/'tools/source-inputs.json').read_text())
reports={name:json.loads((ROOT/'reports'/name).read_text()) for name in ['content-validation.json','browser-validation.json','download-validation.json','navigation-validation.json','teaching-method-validation.json','link-validation.json','weekly-agent-validation.json','bridge-readiness-alignment.json']}
for name,report in reports.items():
 if isinstance(report,dict):assert not report['errors'],name+' has unresolved errors'
 else:assert not any(row['overflow'] for row in report),name+' has overflow'
peer=json.loads((ROOT/'reports/independent-lesson-audit.json').read_text());root_review=json.loads((ROOT/'reports/root-lesson-audit.json').read_text())
assert not [x for x in peer['findings'] if x.get('severity')=='fix'], 'Unresolved peer finding'
assert len(set(peer['weeks_reviewed'])|set(root_review['weeks_reviewed']))==264, 'Editorial coverage incomplete'
coverage={}
for w in D['weeks']+D['python_bridge']:
 for source in [w['sources']['rebuilt']]+w['sources'].get('additional',[]):coverage.setdefault(source,[]).append(w['id'])
assert len(coverage)==252
with (ROOT/'reports/source-coverage.csv').open('w',newline='') as f:
 writer=csv.writer(f);writer.writerow(['Later source lesson','Source title','Required programme locations'])
 for source in sorted(coverage,key=lambda x:tuple(map(int,re.findall(r'\d+',x)))):writer.writerow([source,S['rebuilt'][source]['title'],'; '.join(coverage[source])])
lines=['# Week-by-week content review','', 'Every row has matching student, teacher and workbook resources in HTML, Word and PDF. Source preservation and answer checks are structural/text checks; they do not establish classroom learning outcomes.','', '| Week | Title | Student sections | Teacher sections | Workbook groups | Included later lessons |','|---|---|---:|---:|---:|---|']
for w in D['weeks']+D['python_bridge']:
 sources=[w['sources']['rebuilt']]+w['sources'].get('additional',[])
 lines.append(f"| {w['id']} | {w['title']} | {len(w['sections'])} | {len(w['teacher'])} | {len(w['workbook'])} | {', '.join(sources)} |")
(ROOT/'reports/WEEK_BY_WEEK.md').write_text('\n'.join(lines)+'\n')
c=reports['content-validation.json'];b=reports['browser-validation.json'];d=reports['download-validation.json']
review=f'''# Final review — dedicated complete programme

The package preserves all 144 original weeks, integrates all 252 later source lessons, and provides 252 main weeks plus 12 Python bridge lessons. Original student, teacher and workbook text and images are retained, apart from documented corrections and removed obsolete mastheads. Additional material is inside required weekly sections and matching workbooks.

- Original weeks checked for preserved blocks: {c['original_weeks_checked']}.
- Later source lessons represented: {c['later_lessons_covered']}.
- Active preserved instructional images: {c['unique_original_images']}.
- Executable Python examples checked: {c['source_python_examples']}; includes two original labs checked against published outputs and one intentionally failing indexing demonstration.
- Weekly audience resources checked in a browser: {b['resources']}; {b['viewportChecks']} viewport checks.
- Browser navigation checks for this revision: unavailable under workspace restrictions. Static local links are checked separately.
- Matching Word editions: {d['word_files']}; matching PDF editions: {d['pdf_files']}.
- PDF pages checked for matching canonical text: {d['pdf_pages']}.
- Unresolved content, teaching-method or export-text errors: zero. Browser checks remain pending; PDF exports use the local PyMuPDF renderer.

Three lesson agents authored a concrete worked case for every week. Peer editorial review covers 176 cases and root review covers the other 88. Added illustrations: 264 pictorial traces plus 110 actual-value plots/grids/weighted models. Matching end goals, explanation questions, teacher keys and project evidence are integrated into the full original sections. The Python readiness checks were realigned to the actual twelve topics; base and changed/error traces passed. Download checks also verify the actual PNG pixels painted in each PDF and the matching files embedded in Word.

The teaching cycle covers all 264 lessons: retrieval, modelling, fading support, individual reasoning checks, independent transfer, actionable feedback and delayed return. Fresh parallel cases replace reused sources for assessment; older questions remain practice. Teacher and learner method guides and a blank classroom pilot record accompany the course. Classroom impact is not yet established.

Read source-coverage.csv for the location of every later topic. WEEK_BY_WEEK.md lists every main and bridge lesson. Detailed JSON reports retain per-resource evidence. Prior-edition browser screenshots are archived as historical evidence only. This revision has no browser visual verification. Representative current PDFs were inspected; text preservation is checked for every Word and PDF edition.

## Corrections

1. Foundations Week 4: replace the unrelated food/clock explanation with the stated motion-light and animal-recognition mechanisms.
2. Foundations Week 12: distinguish travelling three squares from reaching a fixed destination; test starts 0 and 2.
3. Algorithms and Data Week 8: treat 7/8 agreement as a disagreement to review, not proof that the rule must be changed.
4. Generative AI Week 10: identify the noise/refinement example as diffusion-style generation rather than every image-generation method.
5. Machine Learning Weeks 10 and 34: use TP=5, FN=3, TN=10, FP=2 for 75% accuracy and 62.5% spotted recall on the stated 12/8 dataset.
6. Machine Learning Week 12: name Manhattan distance and its coordinate-difference procedure.
7. Machine Learning Week 14: distinguish selected-label correctness probability from positive-class probability.
8. Machine Learning Week 35: mark the disputed label as overlapping one of the six failed cases.
9. Seven inherited worked-image cards are replaced in active lessons by corrected native diagrams; originals remain in private source provenance.
10. Later figure excerpts that stopped mid-sentence: complete them from their corresponding source explanations; see diagram-clarifications.json.

## Limits of the checks

Code execution establishes runnable examples; it does not prove that every real-world model or statistical claim generalises. Export comparison checks paragraphs, code, table cells and figure text, not Word pagination. Browser checks for this revision remain pending. Earlier browser reports are historical only. Local PDF rendering and actual export-text comparison establish current downloadable content; representative PDFs received visual inspection. Teacher judgement and classroom observation must establish appropriate age placement, support and pacing.

The restored root project has not been edited or deployed. This dedicated folder is the complete teaching package. Canonical content and source inputs contain teacher answers and are excluded from the learner archive.
'''
(ROOT/'reports/REVIEW.md').write_text(review)
# Capture content hashes without including the manifest in its own hash set.
files=[]
for p in sorted(ROOT.rglob('*')):
 if p.is_file() and p.name!='file-manifest.json':files.append({'file':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'reports/file-manifest.json').write_text(json.dumps(files,indent=2))
student_home='''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Academy · Student programme</title><link rel="stylesheet" href="assets/programme.css"></head><body><main><header class="hero"><p class="kicker">AI Academy · Student programme</p><h1>Understand AI. Build thoughtfully. Explain your evidence.</h1><p>252 complete weekly lessons, twelve Python readiness lessons, and matching workbooks.</p></header><div class="actions"><a href="student/index.html">Open student lessons</a><a href="workbook/index.html">Open workbooks</a><a href="student/LEARNING_GUIDE.html">Projects and learning guide</a><a href="PICTORIAL_LESSONS.html">Explore pictorial lessons</a></div><section class="chapter"><h2>How to learn</h2><p>Read the explanation, predict a result, trace the worked case and practise with changed inputs. Keep actual evidence in your project portfolio. Attempt the independent case before asking for feedback. Print or save your response to keep it.</p></section></main></body></html>'''
student_files=[ROOT/'PICTORIAL_LESSONS.html']
for prefix in ['student','workbook','downloads/student','downloads/workbook']:
 student_files.extend(p for p in (ROOT/prefix).rglob('*') if p.is_file())
# Include only assets referenced by student/workbook pages, plus shared stylesheet/script.
asset_names={'programme.css','programme.js'}
for p in student_files:
 if p.suffix=='.html':asset_names.update(re.findall(r'(?:\.\./)?assets/([^"\s<>]+)',p.read_text()))
student_files.extend(ROOT/'assets'/name for name in sorted(asset_names))
student_zip=ROOT.parent/'ai-academy-student-bundle.zip'
with zipfile.ZipFile(student_zip,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in student_files:z.write(p,'ai-academy-student/'+str(p.relative_to(ROOT)))
 z.writestr('ai-academy-student/START_HERE.html',student_home);z.writestr('ai-academy-student/index.html',student_home)
 guide=(ROOT/'student/LEARNING_GUIDE.html').read_text().replace('../START_HERE.html','START_HERE.html').replace('href="index.html"','href="student/index.html"').replace('../assets/','assets/')
 z.writestr('ai-academy-student/PROGRAMME_GUIDE.html',guide)
 z.writestr('ai-academy-student/README.txt','Open START_HERE.html. Student lessons and workbooks include matching Word/PDF editions. Teacher solutions and source data are excluded. Typed responses last while the page is open; print or save to keep them.\n')
teacher_zip=ROOT.parent/'ai-academy-teacher-bundle.zip'
with zipfile.ZipFile(teacher_zip,'w',zipfile.ZIP_DEFLATED,compresslevel=5) as z:
 for p in sorted(ROOT.rglob('*')):
  if p.is_file():z.write(p,ROOT.name+'/'+str(p.relative_to(ROOT)))
print('Created',student_zip.name,student_zip.stat().st_size,'bytes')
print('Created',teacher_zip.name,teacher_zip.stat().st_size,'bytes')
