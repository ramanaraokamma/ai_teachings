"""Correct the retained corpus-task label without changing saved response positions."""
import json
from connected_authoring import Author,ROOT,g
p=ROOT/'content/programme.json';a=Author.__new__(Author);a.data=json.loads(p.read_text());a.w=next(w for w in a.data['weeks'] if w['id']=='ai-3/1')
a.design('workbook',15,'Additional practice · Analyse the signal corpus','This retained quantitative task is separate from the selected Moon-workflow assessment.',[g('Earlier corpus task and saved answer',[0,1],'prompts')],True)
p.write_text(json.dumps(a.data,ensure_ascii=False,indent=2))
print('Clarified ai-3/1 retained signal-corpus reference')
