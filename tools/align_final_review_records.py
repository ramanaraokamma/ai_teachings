"""Align two legacy metadata keys and editable review packs with reviewed content."""
from pathlib import Path
import copy,hashlib,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from connected_authoring import Author
R=Path(__file__).resolve().parents[1];path=R/'content/programme.json';d=json.loads(path.read_text());weeks=d['weeks']+d['python_bridge'];by_id={w['id']:w for w in weeks}
changes=[]
w=by_id['ai-2/9'];old=w['pictorial_case']['teacher_answer'];new=w['teacher'][2]['blocks'][26]['text']
assert old.startswith('No. It shows one topic-fixed') and new.startswith('No. In the explicitly hypothetical changed case')
a=Author.__new__(Author);a.w=w;a.changes=[];a.replace_text(old,new);changes+=a.changes
w=by_id['ai-3/25'];old=w['independent_answer'];new=w['method']['independent']['answer']
assert old.startswith('Teacher explanation: 6/8=75%') and new.startswith('Support fails:')
w['independent_answer']=new;changes.append({'week':w['id'],'path':'/independent_answer','old':old,'new':new})
ledger_path=R/'reports/reviewed-source-corrections.json';ledger=json.loads(ledger_path.read_text());ledger['corrections']+=changes;ledger_path.write_text(json.dumps(ledger,ensure_ascii=False,indent=2)+'\n')
path.write_text(json.dumps(d,ensure_ascii=False,indent=2))
synced=[]
for w in weeks:
 target=R/'tools/lesson-upgrades'/(w['id'].replace('/','-')+'.json');old_bytes=target.read_bytes();prior=json.loads(old_bytes)
 if prior!=w['pictorial_case']:
  new_bytes=json.dumps(w['pictorial_case'],ensure_ascii=False,indent=2).encode();target.write_bytes(new_bytes)
  synced.append({'week':w['id'],'changed_fields':[k for k in w['pictorial_case'] if prior.get(k)!=w['pictorial_case'][k]],'prior_sha256':hashlib.sha256(old_bytes).hexdigest(),'canonical_sha256':hashlib.sha256(new_bytes).hexdigest()})
(R/'reports/final-review-record-alignment.json').write_text(json.dumps({'exact_corrections':changes,'editable_review_packs_synchronized':synced,'scope':'Align editable source packs with already-reviewed canonical corrections. Two legacy metadata references are corrected; affected rendered weeks require fresh verification. No new independent assessment cases or saved response indices are introduced.'},ensure_ascii=False,indent=2)+'\n')
print('Aligned',len(changes),'exact key references and',len(synced),'editable review packs.')
