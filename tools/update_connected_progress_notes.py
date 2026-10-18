"""Refresh human-readable progress from verified ledger entries only."""
import json,re
from pathlib import Path
R=Path(__file__).resolve().parents[1];p=json.loads((R/'reports/CONNECTED_READING_PROGRESS.json').read_text());d=json.loads((R/'content/programme.json').read_text());weeks={w['id']:w for w in d['weeks']+d['python_bridge']}
for level in ['ai-2','ai-3']:
 rows=[x for x in p['completed'] if x['week'].startswith(level+'/')]
 if not rows:continue
 number=level.split('-')[1];path=R/f'reports/LEVEL{number}_CONNECTED_READING_PROGRESS.md'
 old=path.read_text() if path.exists() else ''
 narrative=old[old.index('\n\nThe reviewed lessons'):] if '\n\nThe reviewed lessons' in old else '\n\nThe reviewed lessons include matched diagrams, complete supplied investigations, separate practice and independent tasks, readable teacher guidance and standalone workbook references.\n\nVerification covers production builds, hosted and offline desktop/phone checks, accessibility, source preservation, saved-answer keys, Word/PDF text and images, local links and published Python examples where provided. These checks do not establish classroom learning outcomes.\n'
 narrative=re.sub(r'\n\nOverall: [^\n]+','',narrative)
 title=f'# Level {number} connected-reading progress\n\n'
 intro=f'Weeks 1–{len(rows)} are reviewed and verified across all student, teacher and workbook sections ({sum(x["sections"] for x in rows)} sections; {len(rows)*6} weekly Word/PDF downloads).\n\n[Open all reviewed editions and previews](../outputs/connected-reading-review/START_HERE.html).\n\n'
 links='\n'.join(f'- Week {weeks[x["week"]]["week"]}: {weeks[x["week"]]["title"]} — [review](../{x["review"]})' for x in rows)
 overall=f'\n\nOverall: {p["completed_lessons"]} of 264 lessons reviewed; {p["remaining_lessons"]} remain in their previous presentation. Next: {p["next"]}.\n'
 path.write_text(title+intro+links+narrative+overall)
print(p['completed_lessons'],'reviewed;',p['next'],'next')
