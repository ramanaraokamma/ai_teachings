"""Build a local review entry for an individually authored connected week."""
from pathlib import Path
from html import escape
import json,sys
from connected_paths import config
level,week,prefix,folder=config();label=level.replace('ai-','Level ').replace('python-bridge','Python bridge');R=Path(__file__).resolve().parents[1];stem=f"{'bridge' if level=='python-bridge' else level}-week-{week:02}";out=R/'outputs'/folder;out.mkdir(parents=True,exist_ok=True)
d=json.loads((R/'content/programme.json').read_text());w=next(w for w in d['weeks']+d['python_bridge'] if w['id']==f'{level}/{week}')
cards=[]
for label,role,shot in [('Student lesson','student','lesson'),('Teacher guide','teacher','guide'),('Student workbook','workbook','workbook')]:
 cards.append(f'''<article><h2>{label}</h2><p><a href="../../{role}/{stem}.html">Open complete {label.lower()}</a></p><p><a href="../../downloads/{role}/{stem}.pdf">PDF</a> · <a href="../../downloads/{role}/{stem}.docx">Word</a></p><a href="{shot}-website-explanation.png"><img src="{shot}-website-explanation.png" alt="Preview of the {label.lower()} explanation layout"></a><p><a href="{shot}-website-390.png">Phone preview</a> · <a href="{shot}-website-1280.png">Desktop preview</a></p></article>''')
flow=w['sections'][0]['reading_flow']['overview']
(out/'START_REVIEW.html').write_text(f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Review {label} Week {week}</title><style>body{{font:18px/1.65 system-ui;background:#f3f7f8;color:#173344;max-width:1100px;margin:40px auto;padding:20px}}h1{{line-height:1.15}}a{{color:#075c98}}main{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px}}article{{background:white;border:1px solid #ccdce1;border-radius:16px;padding:24px}}img{{width:100%;max-height:360px;object-fit:cover;object-position:top;border:1px solid #dce5eb}}p{{margin:12px 0}}</style><h1>{label} · Week {week}</h1><h2>{escape(flow['title'])}</h2><p>{escape(flow['lead'])}</p><p>All {sum(len(w[role]) for role in ['sections','teacher','workbook'])} sections reviewed across the three editions. The main learning path comes first; extra practice and repeated material sit in labelled references. Links open the local programme files. Screenshots show the website presentation.</p><main>{''.join(cards)}</main><p>{escape(flow['outcome'])}</p></html>''')
print(out/'START_REVIEW.html')
