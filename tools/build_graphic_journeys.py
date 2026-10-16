"""Extend the approved Week 1 graphic language using each reviewed lesson's own facts.
All graphics are supported teaching examples. Reserved independent cases are never sources.
"""
from pathlib import Path
import json,html,re,math,shutil
import fitz
from draw_lesson_visuals import ICONS
R=Path(__file__).resolve().parents[1];D=json.loads((R/'content/programme.json').read_text());A=R/'assets';font=fitz.Font('helv');bold=fitz.Font('hebo')
INK='#17384c';MUTED='#476176';TEAL='#086c68';BLUE='#205fa1';PURPLE='#6541a5';ORANGE='#975014'
E=lambda x:html.escape(str(x),quote=True)
# Fit text using conservative Latin width estimates; browser geometry is checked separately.
def wrap(s,width,size):
 result=[]
 for para in str(s).splitlines():
  row=''
  for word in para.split():
   if row and font.text_length(row+' '+word,fontsize=size)*1.07>width:result.append(row);row=word
   else:row=(row+' '+word).strip()
  result.append(row)
 return result or ['']
def txt(x,y,s,size=23,color=INK,weight=500,width=None):
 rows=wrap(s,width,size) if width else ([s] if isinstance(s,str) else s)
 return '<text x="%s" y="%s" fill="%s" font-size="%s" font-weight="%s">'%(x,y,color,size,weight)+''.join(f'<tspan x="{x}" dy="{0 if i==0 else size*1.42}">{E(line)}</tspan>' for i,line in enumerate(rows))+'</text>',len(rows)*size*1.42
def t(*args,**kwargs):return txt(*args,**kwargs)[0]
def box(x,y,w,h,fill='#fff',stroke='#cbdce5',rx=20):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
def arrow(x,y,xx,yy,dashed=False):return f'<path d="M{x} {y} L{xx} {yy}" stroke="#7892a4" stroke-width="3" fill="none" marker-end="url(#arrow)"'+(' stroke-dasharray="7 7"' if dashed else '')+'/>'
def icon(kind,x,y,scale=.8,color=TEAL):return f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{color}" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round">{ICONS.get(kind,ICONS["question"])}</g>'
def header(w,title,kicker):
 s=t(38,44,f'AI ACADEMY / {w["id"].upper()} · {kicker}',15,TEAL,750);tt,h=txt(38,94,title,34,INK,750,width=1115)
 return s+tt,math.ceil(94+h+18)
def panel(x,y,w,label,content,kind='data',color=TEAL):
 labeltext,lh=txt(x+110,y+40,label,24,color,750,width=w-140);body,bh=txt(x+25,y+100,content,23,width=w-50);height=max(220,math.ceil(125+bh))
 return box(x,y,w,height)+icon(kind,x+23,y+17,.72,color)+labeltext+body,height

def write(w,n,title,body,height,desc,source,kind):
 stem=f'academy-story-{w["id"].replace("/","-")}-{n:02}'
 markup=f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="title desc"><title id="title">{E(title)}</title><desc id="desc">{E(desc)}</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0 0L10 5L0 10" fill="#7892a4"/></marker></defs><rect width="1200" height="{height}" rx="24" fill="#f4f8fb"/><g font-family="Arial, Helvetica, sans-serif">{body}</g></svg>'
 (A/(stem+'.svg')).write_text(markup)
 return {'asset':stem,'number':n,'title':title,'alt':desc,'width':1200,'height':height,'source':source,'kind':kind}

def describe_numbers(v):
 kind=v['kind'];parts=[v['title']]
 if kind=='grid':
  for label,row in zip(v['row_labels'],v['cells']):parts.append(str(label)+': '+', '.join(str(c)+' = '+str(value) for c,value in zip(v['column_labels'],row)))
 elif kind=='bars':parts.append('Units: '+v['unit']);parts.extend(str(label)+': '+str(value) for label,value in zip(v['labels'],v['values']))
 elif kind=='scatter':
  parts.extend(str(p['label'])+': ('+str(p['x'])+', '+str(p['y'])+')' for p in v['points'])
  if v.get('query'):parts.append('Query '+str(v['query']['label'])+': ('+str(v['query']['x'])+', '+str(v['query']['y'])+')')
  parts.append('Axes: '+v.get('x_label','first coordinate')+'; '+v.get('y_label','second coordinate'))
  if v.get('metric'):parts.append('Distance: '+v['metric'])
 elif kind=='weights':parts.append('Inputs: '+str(v['inputs'])+'; weights: '+str(v['weights'])+'; bias: '+str(v['bias'])+'; activation: '+v['activation']+'; output: '+str(v['output']))
 return '. '.join(parts)+'.'

def special_model(w):
 id=w['id'];a=w['pictorial_case']
 if id=='ai-1/2':
  title='Different pencil colours. The same total.';b,y=header(w,title,'03 · COUNT WHAT THE SUMMARY LOSES')
  for row,(name,red,blue) in enumerate([('Box A',2,4),('Box B',5,1)]):
   yy=y+row*190;b+=box(38,yy,1124,165)+t(62,yy+44,name,27,INK,750)
   for i in range(red+blue):
    color='#a43135' if i<red else BLUE;x=260+i*91
    b+=f'<rect x="{x}" y="{yy+31}" width="22" height="96" rx="5" fill="{color}"/><path d="M{x} {yy+127}l11 21 11-21" fill="#e5caa5" stroke="{color}" stroke-width="2"/>'
   b+=t(861,yy+55,'Total = 6',31,TEAL,750)+t(861,yy+97,f'Red {red} · Blue {blue}',22)
  y+=408;b+=t(62,y,'Saving only “6” hides which box has more red pencils.',26,TEAL,750);y+=65
  return title,b,y,'Box A: 2 red pencils and 4 blue, total 6. Box B: 5 red pencils and 1 blue, total 6. The equal totals do not preserve the colour counts.','pictorial-pencils'
 if id=='ai-3/20':
  title='The session record changes — the model is not retrained';b,y=header(w,title,'03 · TRACK ONE PIECE OF MEMORY')
  for i,(heading,value,detail,color) in enumerate([('Choose a book','Cedar','Store the first selection.',BLUE),('Correct the choice','Maple','Replace Cedar; do not keep two active choices.',PURPLE),('Exit the session','Unset','Clear the record under this toy policy.',TEAL)]):
   yy=y+i*155;b+=box(38,yy,1124,125)+icon(['data','person','clock'][i],60,yy+25,.7,color)+t(166,yy+37,heading,23,color,750)+t(166,yy+83,detail,22)+box(920,yy+22,215,75,'#e2f1ed','#b5d8ce',12)+t(946,yy+70,value,29,color,750)
   if i<2:b+=arrow(600,yy+129,600,yy+151)
  y+=492;b+=t(62,y,'A new session needs a new selection. This record is not permanent model learning.',23,TEAL,650,width=1070);y+=75
  return title,b,y,'The selected_book session state is Cedar after the first choice, Maple after correction, and unset after exit. This is an application record, not proof of permanent learning.','state-map'
 if id=='python-bridge/5':
  title='Check invalid values before the size rule';b,y=header(w,title,'03 · FOLLOW THE FIRST MATCHING BRANCH')
  for yy,label in [(y+82,'count < 0 ?'),(y+270,'count < 5 ?')]:
   b+=f'<path d="M600 {yy-65}L805 {yy}L600 {yy+65}L395 {yy}Z" fill="#eee8f7" stroke="{PURPLE}" stroke-width="3"/>'+t(513,yy+8,label,25,PURPLE,750)
  b+=arrow(390,y+82,240,y+82)+t(281,y+66,'yes',20)+box(38,y+43,195,78)+t(64,y+91,'invalid',28,ORANGE,750)
  b+=arrow(600,y+152,600,y+199)+t(620,y+180,'no',20)
  b+=arrow(390,y+270,240,y+270)+t(281,y+252,'yes',20)+box(38,y+231,195,78)+t(64,y+279,'small',28,TEAL,750)
  b+=arrow(810,y+270,962,y+270)+t(862,y+251,'no',20)+box(970,y+231,192,78)+t(994,y+279,'large',28,BLUE,750)
  y+=390
  b+=box(38,y,1124,148,'#e2f1ed','#b5d8ce')+t(62,y+40,'Trace separate inputs through the same procedure:',24,TEAL,750)+t(62,y+91,'−2 → invalid   |   4 → small   |   5 → large',29)
  y+=187;b+=t(62,y,'A chosen branch ends the chain. Equality with 5 reaches the “large” branch.',23,width=1070);y+=65
  return title,b,y,'First ask count less than zero: yes selects invalid. Otherwise ask count less than five: yes selects small; no selects large. Separate input traces are minus two invalid, four small, five large.','branch-flowchart'
 if id=='ai-6/20':
  title='A deletion rule needs an inventory of copies';b,y=header(w,title,'03 · CHECK AGE AND EVERY LISTED LOCATION')
  b+=box(38,y,1124,90,'#e2f1ed','#b5d8ce')+t(62,y+39,'At least 7 days old → delete all listed copies.',27,TEAL,750)+t(62,y+71,'T1: 6 days → keep for now.     T2: 7 days → deletion boundary reached.',22)
  y+=124
  for x,label in [(38,'Primary storage'),(627,'Listed backup')]:
   b+=box(x,y,535,274)+icon('data',x+210,y+28,1,BLUE)+t(x+24,y+169,label,28,BLUE,750)+t(x+24,y+217,'T2: remove, then verify.',24,ORANGE,650)
  y+=320;b+=t(62,y,'Two declared T2 locations → two removal checks.',28,TEAL,750)+t(62,y+48,'Removing the visible copy alone is incomplete. Unknown copies need investigation.',23,width=1070);y+=100
  return title,b,y,'The toy retention boundary is seven days or older. Keep six-day T1 for now. Seven-day T2 appears in primary storage and one listed backup; both locations need removal verification. This diagram specifies required checks, not an actual deletion run.','copy-inventory'
 if id=='ai-7/20':
  title='Keep analysis records separate from the identity key';b,y=header(w,title,'03 · MAP PURPOSE AND ACCESS')
  for x,label,body,kind,color in [(38,'Analysis table','Random codes + task scores','data',BLUE),(627,'Restricted identity key','Codes linked to names','shield',PURPLE)]:
   b+=box(x,y,535,300)+icon(kind,x+205,y+24,1,color)+t(x+25,y+170,label,26,color,750)+t(x+25,y+219,body,24,width=480)
  y+=335;b+=box(38,y,1124,132,'#e2f1ed','#b5d8ce')+t(62,y+39,'Analysts receive codes and scores, not the name linkage.',25,TEAL,750)+t(62,y+84,'Authorised withdrawal handling may use the restricted key.',23)
  y+=174;b+=t(62,y,'Pseudonymous is not guaranteed anonymous: a linkage key still exists.',25,ORANGE,750,width=1070);y+=75
  return title,b,y,'Analysts receive random participant codes and scores. A separate restricted key links codes to names only for authorised withdrawal handling. Keeping the key restricted reduces exposure; it does not guarantee anonymity.','access-map'
 return None

def make(w):
 a=w['pictorial_case'];out=[]
 # 1. A concrete case and its declared facts.
 title=a['title']+': the case';b,y=header(w,title,'01 · LOOK AT THE FACTS');left,hl=panel(38,y,535,'The situation',a['scenario'],a['steps'][0]['icon'],BLUE);right,hr=panel(627,y,535,'Supplied evidence','\n\n'.join(a['given']),'data',TEAL);b+=left+right;y+=max(hl,hr)+30
 line,lh=txt(62,y+33,a['outcome'],23,TEAL,650,width=1076);b+=box(38,y,1124,math.ceil(lh+47),'#e2f1ed','#b5d8ce')+line;y+=lh+76
 out.append(write(w,1,title,b,math.ceil(max(y,620)),a['scenario']+' Supplied facts: '+' '.join(a['given']),['pictorial_case.scenario','pictorial_case.given'],'case'))
 # 2. Numbered, explicitly connected stages. Arrows show the stipulated reasoning order.
 title='Follow the deciding steps';b,y=header(w,title,'02 · TRACE THE CASE');
 for i,s in enumerate(a['steps']):
  color=[BLUE,PURPLE,TEAL,ORANGE,BLUE][i];detail,dh=txt(204,y+82,s['detail'],24,width=915);height=max(136,math.ceil(105+dh));b+=box(38,y,1124,height)+icon(s['icon'],62,y+34,.9,color)+t(203,y+38,f'{i+1:02}  {s["label"]}',26,color,750)+detail;y+=height
  if i<len(a['steps'])-1:b+=arrow(600,y+5,600,y+30);y+=40
 out.append(write(w,2,title,b,math.ceil(y+35),' → '.join(s['label']+': '+s['detail'] for s in a['steps']),['pictorial_case.steps'],'pathway'))
 # 3. Use the actual quantitative chart when supplied; otherwise map the lesson's own conceptual diagram.
 v=a.get('mini_visual');title=v['title'] if v else a['title']+': inspect the mechanism';b,y=header(w,title,'03 · LOOK MORE CLOSELY')
 special=special_model(w)
 if special:
  title,b,y,desc,kind=special;source=['pictorial_case.given','pictorial_case.steps']
 elif v:
  b='';y=16
  # Existing numerical renderer already checks coordinates, denominators and weighted outputs.
  p=A/('academy-detail-'+w['id'].replace('/','-')+'.svg');raw=p.read_text();vb=re.search(r'viewBox="([^"]+)"',raw).group(1);_,_,sw,sh=map(float,vb.split());inner=re.sub(r'^<svg[^>]*>|</svg>$','',raw)
  inner=re.sub(r'>(-?\d+\.\d{6,})<',lambda m:'>'+format(float(m.group(1)),'.4g')+'<',inner)
  # Remove its duplicate heading so the numbers remain the focus.
  scale=min(1080/sw,790/sh);b+=f'<g transform="translate(60 {y}) scale({scale})">{inner}</g>';y+=sh*scale+30;desc=describe_numbers(v);source=['pictorial_case.mini_visual'];kind=v['kind']
 else:
  candidates=[block for sec in w['sections'] if sec['title'] not in ['Try a new case independently','Show what you know'] for block in sec['blocks'] if block['type']=='diagram' and block.get('rows') and not block.get('lesson_upgrade')]
  model=next((b for b in candidates if b.get('kind')=='lanes'),None)
  if model:
   title=model.get('title',title);b,y=header(w,title,'03 · INSPECT THE LESSON MODEL');cols=model.get('columns',[]);rows=model['rows'];width=1124/max(len(row) for row in rows)
   if cols:
    h=max(len(wrap(str(label),width-30,21)) for label in cols)*30+28
    for j,label in enumerate(cols):b+=box(38+j*width,y,width-6,h,'#e2f1ed','#bed5cf',10)+t(52+j*width,y+31,str(label),21,TEAL,750,width=width-35)
    y+=h+10
   for row in rows:
    h=max(len(wrap(str(cell),width-30,23)) for cell in row)*33+28
    for j,cell in enumerate(row):b+=box(38+j*width,y,width-6,h,rx=10)+t(52+j*width,y+31,str(cell),23,width=width-35)
    y+=h+10
   if model.get('caption'):
    cap,ch=txt(50,y+29,model['caption'],22,MUTED,width=1100);b+=cap;y+=ch+38
   desc=title+'. '+'. '.join(' | '.join(map(str,row)) for row in rows);source=['sections.diagram:'+title];kind='concept-map'
  else:
   for i,s in enumerate(a['steps']):
    color=[BLUE,PURPLE,TEAL,ORANGE,BLUE][i];part,h=panel(38,y,1124,s['label'],s['detail'],s['icon'],color);b+=part;y+=h+18
   desc=' '.join(s['label']+': '+s['detail'] for s in a['steps']);source=['pictorial_case.steps'];kind='stage-focus'
 out.append(write(w,3,title,b,math.ceil(max(y+25,620)),desc,source,kind))
 # 4. An actual stipulated counterfactual, not a fabricated model run.
 c=a['counterfactual'];title='Change one thing. Trace what follows.';b,y=header(w,title,'04 · COMPARE THE CASES');left,hl=panel(38,y,535,'Original case',a['steps'][-1]['detail'],a['steps'][-1]['icon'],BLUE);right,hr=panel(627,y,535,'Changed condition',c['change'],'experiment',PURPLE);b+=left+right;y+=max(hl,hr)+28
 reason=c['prediction']+'\n\nWhy: '+c['reason'];p,h=panel(38,y,1124,'Worked changed-case result',reason,'output',TEAL);b+=p;y+=h+30
 out.append(write(w,4,title,b,math.ceil(y),'Original case: '+a['steps'][-1]['detail']+' Changed condition: '+c['change']+' Expected result: '+c['prediction']+' Reason: '+c['reason'],['pictorial_case.steps[-1]','pictorial_case.counterfactual'],'comparison'))
 # 5. The explanation and its actual boundary sit side by side.
 title='Connect the explanation to its limit';b,y=header(w,title,'05 · EXPLAIN WITH CARE');left,hl=panel(38,y,535,'What the case explains',a['explanation'],'search' if 'search' in ICONS else 'check',TEAL);right,hr=panel(627,y,535,'What it does not establish',a['limits'],'shield',ORANGE);b+=left+right;y+=max(hl,hr)+30
 out.append(write(w,5,title,b,math.ceil(max(y,620)),a['explanation']+' Limit: '+a['limits'],['pictorial_case.explanation','pictorial_case.limits'],'claim-and-limit'))
 # 6. A blank evidence canvas, with a topic-specific project prompt.
 title='Make the idea visible in your project';b,y=header(w,title,'06 · DRAW AND EXPLAIN');prompt,ph=txt(62,y+37,a['project_evidence'],23,width=1075);b+=box(38,y,1124,ph+65,'#e2f1ed','#b5d8ce')+prompt;y+=ph+105
 for x,label,kind in [(38,'Input or case','data'),(432,'Deciding step','rule'),(826,'Result + limit','output')]:
  b+=box(x,y,336,245)+icon(kind,x+120,y+18,.65,TEAL)+t(x+22,y+115,label,25,TEAL,750)+f'<path d="M{x+24} {y+157}h288 M{x+24} {y+191}h288" stroke="#9db3c1" stroke-width="2" stroke-dasharray="5 5"/>'
  if x<826:b+=arrow(x+346,y+123,x+382,y+123)
 y+=290;task,th=txt(62,y+33,a['student_task'],23,INK,650,width=1075);b+=box(38,y,1124,th+55,'#fff3df','#e8c995')+task;y+=th+85
 out.append(write(w,6,title,b,math.ceil(y),a['project_evidence']+' Draw your input, deciding step, result and limit. Supported question: '+a['student_task'],['pictorial_case.project_evidence','pictorial_case.student_task'],'project-canvas'))
 return out

def approved(w):
 review=R/'tools/graphic-references/week1';manifest=json.loads((review/'review-manifest.json').read_text());out=[]
 # Copy the approved six illustrations exactly, including the specific bus and umbrella scenes.
 for i,g in enumerate(manifest['graphics'],1):
  stem=f'academy-story-ai-1-1-{i:02}';shutil.copy2(review/(g['id']+'.svg'),A/(stem+'.svg'))
  out.append({'asset':stem,'number':i,'title':g['title'],'alt':g['alt'],'width':1200,'height':720,'source':['approved-week-1-review:'+g['id']],'kind':'approved-illustration'})
 return out

def integrate(w,graphics):
 for key in ['sections','teacher','workbook']:
  w[key]=[s for s in w[key] if not s.get('graphic_journey')]
  blocks=[]
  if key=='teacher':blocks.append({'type':'paragraph','text':'Use one picture at a time. Hide a worked result before asking for a prediction, then reveal it for feedback. These are supported teaching cases; retain the separate independent assessment for a fresh first attempt.'})
  for g in graphics:
   blocks.extend([{'type':'subheading','text':f'{g["number"]:02}. {g["title"]}'},{'type':'image','src':'/api/resource/'+g['asset'],'alt':g['alt'],'width':g['width'],'height':g['height'],'academy_visual':True,'graphic_journey':True},{'type':'paragraph','text':g['alt']}])
   if w['id']=='ai-1/1':
    prompts=['Name one observation and one claim that needs more evidence.','Point to who or what makes each decision.','Trace the number, colour and override separately.','Which steps use earlier examples, and which use a fitted model?','Keep the forecast fixed at 70%. What changes when the boundary becomes 80%?','Which evidence would change your answer about the vacuum?']
    prompt=prompts[g['number']-1]
   else:prompt=['Point to the given fact that matters most. Explain why it matters.','Point to each numbered stage and explain which recorded input it uses.','Read the labels and values. Explain the relationship the model shows.','Predict before checking the worked changed-case result. Name what changed and what the supplied facts allow you to conclude.','Explain the case, then point to a limit on the claim.','Draw your project trace and justify the deciding step using evidence.'][g['number']-1]
   blocks.append({'type':'callout','tone':'think','text':prompt})
   if key=='teacher':
    note=f'Teacher prompt: {prompt} Ask learners to describe one label or arrow in ordinary words. Use the adjacent transcript if the image is difficult to see.'
    if g['number']==3 and w['pictorial_case'].get('mini_visual'):note+=' Check row/column meanings, units and denominators before discussing a difference. Supplied toy values are not real class or model results.'
    if g['number']==4:note+=' Changed-case reasoning: '+w['pictorial_case']['counterfactual']['reason']
    if g['number']==5:note+=' Keep the stated scope: '+w['pictorial_case']['limits']
    if g['number']==6:note+=' Supported practice key: '+w['pictorial_case']['teacher_answer']
    blocks.append({'type':'paragraph','text':note})
   elif key=='workbook':blocks.append({'type':'response','label':'My picture explanation, deciding evidence and one limit','lines':4})
  w[key].append({'title':'Visual concept journey','graphic_journey':True,'blocks':blocks})
 w['graphic_story']=graphics

rows=[]
for w in D['weeks']+D['python_bridge']:
 graphics=approved(w) if w['id']=='ai-1/1' else make(w);integrate(w,graphics);rows.append({'week':w['id'],'title':w['title'],'graphics':graphics})
D['graphic_journey_design']={'approved_reference':'Level 1 Week 1, approved by user','graphics_per_lesson':6,'scope':'Supported case, labelled mechanism, close-up model, changed case, claim boundary, project evidence','reserved_assessment_used':False}
(R/'content/programme.json').write_text(json.dumps(D,ensure_ascii=False,indent=2))
(R/'reports/graphic-journeys.json').write_text(json.dumps({'lessons':len(rows),'graphics':sum(len(r['graphics']) for r in rows),'weeks':rows},ensure_ascii=False,indent=2))
print(f'Prepared {len(rows)} six-picture journeys; {sum(len(r["graphics"]) for r in rows)} SVGs. PNG rendering is next.')
