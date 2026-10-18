"""A correction spanning formatted paragraphs must reach every edition."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from connected_authoring import Author
from connected_paths import config
a=Author.__new__(Author);a.w={'id':'ai-2/2','sections':[{'blocks':[{'text':'First sentence. Second sentence.','presentation':{'paragraphs':['First sentence.','Second sentence.']}}]}]};a.changes=[]
a.replace_text('First sentence. Second sentence.','Corrected first. Corrected second.')
b=a.w['sections'][0]['blocks'][0];assert b['presentation']['paragraphs']==[b['text']];assert a.changes[0]['path']=='/sections/0/blocks/0/text'
a.replace_text('Corrected first.','Corrected first. Expanded.')
assert b['presentation']['paragraphs']==[b['text']] and b['text'].count('Expanded.')==1
assert config('1')[2:] == ('week1','week-01-connected-review')
assert config('ai-2/1')[2:] == ('ai-2-week1','ai-2-week-01-connected-review')
print('Cross-paragraph corrections and level-specific review paths verified.')

a.w={'id':'ai-2/8','teacher':[{'blocks':[{'type':'table','rows':[['Heading','Meaning'],['Recall','Wrong week reference']]}]}]};a.changes=[]
a.replace_text('Wrong week reference','Correct week reference')
assert a.w['teacher'][0]['blocks'][0]['rows'][1][1]=='Correct week reference'
assert a.changes==[{'week':'ai-2/8','path':'/teacher/0/blocks/0/rows/1/1','old':'Wrong week reference','new':'Correct week reference'}]
print('Table-cell corrections retain exact source-preservation ledger paths.')
