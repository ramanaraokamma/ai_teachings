"""A revised lesson must not rewrite another lesson with the same earlier goal."""
import copy,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from connected_authoring import Author
from connected_retrieval import refresh
old='A shared earlier goal'
entries=[dict(week='ai-3/6',title='Examples and Rubrics',goal=old,expected='old rubric guidance'),dict(week='ai-3/5',title='Prompt as a Contract',goal=old,expected='keep contract guidance')]
blocks=[]
for e in entries:blocks += [dict(type='subheading',text=e['title']),dict(type='paragraph',text='Look for: '+old),dict(type='paragraph',text='Reference example, not the only acceptable wording: '+e['expected'])]
review=lambda e:dict(type='paragraph',text=f'Review {e["title"]} ({e["week"]}). Goal: {old}. Short practice: keep the case.')
a=Author.__new__(Author);a.w=dict(id='ai-3/7',method=dict(retrieval=copy.deepcopy(entries)),teacher=[dict(blocks=blocks)],sections=[dict(blocks=[review(e) for e in entries])],workbook=[dict(blocks=[review(e) for e in entries])]);a.changes=[]
protected=copy.deepcopy((a.w['method']['retrieval'][1],blocks[3:],a.w['sections'][0]['blocks'][1],a.w['workbook'][0]['blocks'][1]))
refresh(a,'ai-3/6','new rubric goal','new rubric guidance')
assert protected==(a.w['method']['retrieval'][1],blocks[3:],a.w['sections'][0]['blocks'][1],a.w['workbook'][0]['blocks'][1])
assert a.w['method']['retrieval'][0]['goal']=='new rubric goal' and blocks[1]['text']=='Look for: new rubric goal'
count=len(a.changes);refresh(a,'ai-3/6','new rubric goal','new rubric guidance');assert len(a.changes)==count
assert all(c['old']!=c['new'] for c in a.changes)
print('Named-prior retrieval refresh preserves unrelated equal goals and is idempotent.')
