"""Append public code examples without renumbering saved lab drafts."""
from pathlib import Path
import copy,json,sys
R=Path(__file__).resolve().parents[1]
def sync_labs(week,entry):
 entry=copy.deepcopy(entry);labs=entry['labs'];codes={lab['code']:i for i,lab in enumerate(labs)}
 for n,section in enumerate(week['sections'],1):
  if n==14:continue
  for block in section['blocks']:
   if block['type']=='code' and block.get('teaching_method',{}).get('kind')!='independent-transfer' and block['text'] not in codes:
    codes[block['text']]=len(labs);labs.append({'title':block.get('title') or f'Supported code example {len(labs)+1}','code':block['text']})
 preferred=None;overview=week['sections'][0].get('reading_flow',{}).get('overview',{})
 for n in overview.get('order',[]):
  if n==14:continue
  section=week['sections'][n-1];flow=section['reading_flow']
  if flow['optional']:continue
  for group in flow['groups']:
   if group.get('collapsed') or group['kind']=='reference':continue
   for i in group['indices']:
    block=section['blocks'][i]
    if block['type']=='code':preferred=block['text'];break
   if preferred is not None:break
  if preferred is not None:break
 for lab in labs:lab.pop('primary',None)
 if preferred is not None:labs[codes[preferred]]['primary']=True
 return entry
if __name__=='__main__':
 programme=json.loads((R/'content/programme.json').read_text());data=json.loads((R/'content/learning-tools.json').read_text());selected=set(sys.argv[1:])
 for w in programme['weeks']+programme['python_bridge']:
  if w['id'] in selected or (not selected and w['sections'][0].get('reading_flow')):data[w['id']]=sync_labs(w,data[w['id']])
 for p in ['content/learning-tools.json','lib/learning-tools.json']:(R/p).write_text(json.dumps(data,ensure_ascii=False))
 report_path=R/'reports/learning-tools-coverage.json'
 if report_path.exists():
  report=json.loads(report_path.read_text());report['lessons_with_code']=sum(bool(v['labs']) for v in data.values());report['supported_code_examples']=sum(len(v['labs']) for v in data.values());report_path.write_text(json.dumps(report,indent=2)+'\n')
 print('Public code labs synchronized; existing example indices retained.')
