"""Refine appended answer guidance; all original source blocks remain untouched."""
import sys,json
from connected_authoring import Author,ROOT
from connected_teacher_lab_keys import apply
n=int(sys.argv[1]);a=Author.__new__(Author);a.data=json.loads((ROOT/'content/programme.json').read_text());a.w=next(w for w in a.data['weeks'] if w['id']==f'ai-2/{n}');a.tag=f'connected-reading-ai-2-{n}'
apply(a,n)
(ROOT/'content/programme.json').write_text(json.dumps(a.data,ensure_ascii=False,indent=2))
p=ROOT/f'reports/ai-2-week{n}-connected-reading.json';r=json.loads(p.read_text());r['teacher_lab_key']='Reviewed appended key uses complete sentences and short paragraphs; original source blocks unchanged.';p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(f'Refined ai-2/{n} teacher investigation guidance')
