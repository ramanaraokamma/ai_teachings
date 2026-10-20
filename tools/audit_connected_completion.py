"""Audit current complete reading flows, historical checks and local review navigation."""
from pathlib import Path
import datetime,hashlib,json,re
R=Path(__file__).resolve().parents[1]
d=json.loads((R/'content/programme.json').read_text());weeks=d['weeks'][:108]+d['python_bridge']+d['weeks'][108:]
p=json.loads((R/'reports/CONNECTED_READING_PROGRESS.json').read_text())
assert len(weeks)==p['completed_lessons']==264 and p['remaining_lessons']==0 and p['next']=='complete'
assert [x['week'] for x in p['completed']]==[w['id'] for w in weeks]
legacy={'ai-1/'+str(n) for n in range(1,6)};records=[];section_count=0;links_checked=0
for w,row in zip(weeks,p['completed']):
 level,n=w['id'].split('/');prefix=f'week{n}' if level=='ai-1' else f'{level}-week{n}'
 report=json.loads((R/f'reports/{prefix}-connected-reading.json').read_text())
 browser=report['browser_validation'];assert len(browser['checks'])==6 and not browser['errors'],w['id']
 fingerprint=hashlib.sha256(json.dumps(w,sort_keys=True).encode()).hexdigest()
 historical=report.get('week_sha256')
 if historical:assert historical==fingerprint,w['id']
 else:assert w['id'] in legacy,w['id']
 count=0
 for role in ['sections','teacher','workbook']:
  for section in w[role]:
   flow=section['reading_flow'];indices=[i for group in flow['groups'] for i in group['indices']]
   assert sorted(indices)==list(range(len(section['blocks']))),(w['id'],role)
   assert all(group['title'].strip() for group in flow['groups'])
   count+=1
 assert count==report['sections_reviewed'],w['id'];section_count+=count
 review=R/row['review'];html=review.read_text();label=level.replace('ai-','Level ').replace('python-bridge','Python bridge')
 assert f'<h1>{label} · Week {n}</h1>' in html,w['id']
 for href in re.findall(r'(?:href|src)="([^"]+)"',html):
  assert (review.parent/href).exists(),(w['id'],href);links_checked+=1
 records.append({'week':w['id'],'sections':count,'current_sha256':fingerprint,
                 'historical_fingerprint':'matched' if historical else 'not recorded in legacy report',
                 'hosted_checks_recorded':len(browser['checks']),'review':row['review']})
assert len(list((R/'downloads').rglob('*.docx')))==792
assert len(list((R/'downloads').rglob('*.pdf')))==792
result={'audited_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lessons':264,'sections':section_count,
        'role_editions':792,'word_pdf_downloads':1584,'review_links_checked':links_checked,
        'historical_fingerprints_matched':sum(r['historical_fingerprint']=='matched' for r in records),
        'legacy_reports_without_historical_fingerprint':sorted(legacy),'weeks':records,'errors':[],
        'scope':'Current source partitions, source fingerprints where historically recorded, prior hosted-check records and refreshed local review links. Fresh global/download checks are recorded separately. This does not establish classroom learning outcomes.'}
(R/'reports/connected-programme-completion.json').write_text(json.dumps(result,indent=2)+'\n')
(R/'reports/CONNECTED_READING_COMPLETION.md').write_text(f'''# Complete connected-reading review

All **264 lessons** are reviewed and verified: 252 weeks across Levels 1–7, plus the 12-lesson Python Readiness Bridge. Their **{section_count:,} sections** cover student lessons, teacher guides and standalone workbooks.

The complete editions contain clearer headings, shorter explanations, explicit worked inputs and results, labelled graphics, prediction before feedback, retained independent cases, checked teacher keys and honest evidence limits. Original response positions and saved-draft keys are preserved; exact source corrections have a separate ledger.

Open the [student lessons](../student/index.html), [teacher guides](../teacher/index.html) or [workbooks](../workbook/index.html). The repository review navigator is `outputs/connected-reading-review/START_HERE.html`. All 792 Word and 792 PDF downloads are retained.

The current audit checks every section partition and review link. Historical fingerprints match for {result['historical_fingerprints_matched']} lessons; the first five Level 1 reports predate that fingerprint field, and their existing review records are retained without inventing historical fingerprints. Current hashes for every lesson are in `connected-programme-completion.json`.

Each sequential weekly review passed production build, hosted desktop/phone and accessibility checks, offline desktop/phone checks, source preservation, access checks and Word/PDF verification. Automated checks establish content and implementation properties; classroom understanding and suitable pacing still require teacher observation.

No deployment, commit or push was performed for this review.
''')
print('Complete:',len(records),'lessons;',section_count,'sections;',links_checked,'local review links;',result['historical_fingerprints_matched'],'historical fingerprints matched.')
