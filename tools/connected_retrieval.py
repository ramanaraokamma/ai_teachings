"""Refresh a named earlier lesson's retrieval guidance without touching other goals."""
def refresh(a,week,goal,expected):
 entries=a.w.get('method',{}).get('retrieval',[])
 for k,entry in enumerate(entries):
  if entry['week']!=week:continue
  oldgoal=entry['goal'];title=entry['title']
  for field,value in [('goal',goal),('expected',expected)]:
   old=entry[field]
   if old!=value:
    entry[field]=value;a.changes.append({'week':a.w['id'],'path':f'/method/retrieval/{k}/{field}','old':old,'new':value})
  blocks=a.w['teacher'][0]['blocks'];start=next(i for i,b in enumerate(blocks) if b.get('text')==title and b['type']=='subheading')
  stop=next((i for i in range(start+1,len(blocks)) if blocks[i]['type'] in ('subheading','heading')),len(blocks))
  for i in range(start+1,stop):
   text=blocks[i].get('text','')
   if text.startswith('Look for:') and text!='Look for: '+goal:a.fix('teacher',1,i,'Look for: '+goal)
   if text.startswith('Reference example, not the only acceptable wording:') and text!='Reference example, not the only acceptable wording: '+expected:a.fix('teacher',1,i,'Reference example, not the only acceptable wording: '+expected)
  for role in ['sections','workbook']:
   for n,s in enumerate(a.w[role],1):
    for i,b in enumerate(s['blocks']):
     text=b.get('text','');prefix=f'Review {title} ({week}). Goal: {oldgoal}.'
     if b['type']=='paragraph' and text.startswith(prefix) and oldgoal!=goal:a.fix(role,n,i,text.replace(prefix,f'Review {title} ({week}). Goal: {goal}.',1))

REVIEWED_PRIORS={
 'ai-3/16':('Verify a numeric claim using its source, denominator and units','Identify the source and population, retain units, and recompute with the correct denominator. Calendar validity does not establish the intended event date; preserve missing authority rather than guessing a replacement.'),
 'ai-3/6':('Distinguish a format example from approved factual evidence','A format example demonstrates structure; approved N supplies the frog fact. The original card fails mandatory support despite a score of 3/4; an answer-only correction still lacks the Question field. Check each required criterion separately.'),
 'ai-3/11':('Check object counts, spatial relations and arrow meaning separately','Correct object counts do not establish position or semantic arrow flow. Moving bottles left fixes position without changing beaker→bottles meaning. A native reconstruction is not the original generated output.'),
 'ai-3/13':('Keep visible evidence, hidden contents and caption claims separate','Three reported visible pencils support a lower bound, not a verified total. Hidden contents remain unknown; a caption does not reveal them. Only the supplied new observation and complete-location scope support the changed total.')}

def refresh_reviewed_priors(a):
 prior={w['id']:w for w in a.data['weeks']}
 for week,(goal,expected) in REVIEWED_PRIORS.items():
  w=prior[week]
  if w['sections'][0].get('reading_flow') and w['method']['goal']==goal:
   refresh(a,week,goal,expected)
