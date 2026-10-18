"""Record a week's verified review and advance the sequential progress ledger."""
from pathlib import Path
import json,sys,hashlib,re
from connected_paths import config
level,n,prefix,folder=config();label=level.replace('ai-','Level ').replace('python-bridge','Python bridge');R=Path(__file__).resolve().parents[1];p=R/f'reports/{prefix}-connected-reading.json';r=json.loads(p.read_text());d=json.loads((R/'content/programme.json').read_text());w=next(w for w in d['weeks']+d['python_bridge'] if w['id']==f'{level}/{n}')
browser=json.loads((R/f'reports/{prefix}-connected-browser.json').read_text());assert not browser['errors'] and len(browser['checks'])==6
logs=R/'work/week1-presentation'
assert '276 access and lesson checks passed' in (logs/f'{prefix}-access.log').read_text()
assert (logs/f'{prefix}-offline.log').read_text().count('passed')==6
assert not json.loads((R/'reports/content-validation.json').read_text())['errors']
assert not json.loads((R/'reports/download-validation.json').read_text())['errors']
assert not json.loads((R/'reports/link-validation.json').read_text())['errors']
for role in ('sections','teacher','workbook'):
 for s in w[role]:assert sorted(i for g in s['reading_flow']['groups'] for i in g['indices'])==list(range(len(s['blocks'])))
 r['roles'][role]['sections']=[{'title':s['reading_flow']['title'],'groups':[g['title'] for g in s['reading_flow']['groups']]} for s in w[role]]
r['browser_validation']=browser;r['preservation_note']='Original block and response positions retained; exact wording corrections are recorded separately.';r['review_entry']=f'outputs/{folder}/START_REVIEW.html';r['week_sha256']=hashlib.sha256(json.dumps(w,sort_keys=True).encode()).hexdigest();r['validation']={'offline_desktop_and_phone':True,'source_preservation':True,'word_pdf_text_and_images':True,'access_and_lesson_checks':276};p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
review=R/r['review_entry']
for target in re.findall(r'(?:href|src)="([^"]+)"',review.read_text()):assert (review.parent/target).exists(),target
(R/f'reports/{prefix.upper()}_CONNECTED_READING.md').write_text(f'''# {label} Week {n}: {w['title']}

[Open all editions, downloads and previews](../{r['review_entry']}).

All {r['sections_reviewed']} sections were reviewed as one learning experience across student, teacher and workbook editions. Main explanations use authored chunks, matched diagrams, prediction before folded feedback, a supplied investigation and one reserved independent case. Repeated source material remains in labelled references. Exact source corrections and the complete section review are recorded in {prefix}-connected-reading.json.

Verification: six hosted desktop/phone checks and six automated accessibility audits passed, including complete sections, loaded images, no page overflow, restored workbook drafts, reference anchors, keyboard feedback and complete print expansion. Six offline desktop/phone checks, source preservation, Word/PDF text and images, local links, 276 access/lesson checks and production build passed. Automated checks do not establish classroom learning outcomes.

No deployment or push was performed for this review.
''')
p=R/'reports/CONNECTED_READING_PROGRESS.json';progress=json.loads(p.read_text());completed={row['week']:row for row in progress['completed']};completed[w['id']]={'week':w['id'],'status':'reviewed and verified','sections':r['sections_reviewed'],'review':r['review_entry']};order=d['weeks'][:108]+d['python_bridge']+d['weeks'][108:];positions={w['id']:i for i,w in enumerate(order)};progress['completed']=sorted(completed.values(),key=lambda row:positions[row['week']]);progress['completed_lessons']=len(completed);progress['remaining_lessons']=264-len(completed);progress['next']=next((w['id'] for w in order if w['id'] not in completed),'complete');p.write_text(json.dumps(progress,indent=2)+'\n');print(w['id'],'verified; next:',progress['next'])
