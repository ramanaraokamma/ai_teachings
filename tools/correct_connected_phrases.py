"""Apply exact, recorded refinements to an already authored week's wording."""
import json
from connected_authoring import Author,ROOT
from connected_paths import config
def correct(week,pairs):
 a=Author.__new__(Author);a.data=json.loads((ROOT/'content/programme.json').read_text());a.w=next(w for w in a.data['weeks']+a.data['python_bridge'] if w['id']==week);a.changes=[]
 for old,new in pairs:
  before=len(a.changes);a.replace_text(old,new);assert len(a.changes)>before,(week,old)
 (ROOT/'content/programme.json').write_text(json.dumps(a.data,ensure_ascii=False,indent=2))
 p=ROOT/'reports/reviewed-source-corrections.json';d=json.loads(p.read_text());d['corrections'].extend(a.changes);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
 _,_,prefix,_=config(week);p=ROOT/f'reports/{prefix}-connected-reading.json';r=json.loads(p.read_text());r['wording_corrections'].extend(a.changes);p.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
