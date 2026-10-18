"""Navigation for completed, individually verified connected-week reviews."""
from pathlib import Path
from html import escape
import json,os
R=Path(__file__).resolve().parents[1];out=R/'outputs/connected-reading-review';out.mkdir(parents=True,exist_ok=True)
p=json.loads((R/'reports/CONNECTED_READING_PROGRESS.json').read_text());d=json.loads((R/'content/programme.json').read_text());lookup={w['id']:w for w in d['weeks']+d['python_bridge']};cards=[]
for row in p['completed']:
 target=R/row['review'];assert target.exists();w=lookup[row['week']];relative=os.path.relpath(target,out)
 cards.append(f'<article><p class="label">{escape(row["week"])} · {row["sections"]} sections verified</p><h2>{escape(w["title"])}</h2><p><a href="{escape(relative)}">Review student, teacher and workbook editions →</a></p></article>')
(out/'START_HERE.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Academy · Connected reading reviews</title><style>body{{font:18px/1.7 system-ui;max-width:1100px;margin:40px auto;padding:20px;background:#f3f7f8;color:#17384e}}h1{{line-height:1.2}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}}article{{background:#fff;border:1px solid #cbdce5;border-radius:16px;padding:24px}}h2{{font-size:23px;line-height:1.35}}a{{color:#075c98}}.label{{font-size:14px;color:#375d6d}}</style><h1>AI Academy · Connected reading reviews</h1><p><strong>{p['completed_lessons']} of {p['programme_lessons']} weekly lessons reviewed and verified.</strong> Each review brings together the student lesson, teacher guide, workbook, downloads and desktop/phone previews.</p><p>Next in sequence: {escape(p['next'])}. Remaining weeks retain their previous presentation while review continues.</p><main>{''.join(cards)}</main></html>''');print(out/'START_HERE.html')
