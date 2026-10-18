"""Independent arithmetic and policy checks for reviewed Level 1 examples."""
from pathlib import Path
import json,re
R=Path(__file__).resolve().parents[1];d=json.loads((R/'content/programme.json').read_text());rows=[]
def record(week,name,result):rows.append({'week':f'ai-1/{week}','case':name,'verified':result})
# Sound: use values from the actual published sample record.
w=d['weeks'][5];t=w['sections'][5]['blocks'][21]['text'];a=list(map(int,re.search(r'Signal A: ([\d,]+)',t)[1].split(',')));b=list(map(int,re.search(r'Signal B: ([\d,]+)',t)[1].split(',')))
assert max(a)==max(b)==3 and a.index(3)==1 and b.index(3)==3 and [a[i] for i in (0,2,4)]==[b[i] for i in (0,2,4)]==[0,0,0]
assert len([0,2,4,6,8])-1==4 and 8-0==8
record(6,'sample order, equal maxima and retained zeros',True)
def peaks(values):return [i for i in range(1,len(values)-1) if values[i]>=3 and values[i]>values[i-1] and values[i]>values[i+1]]
assert peaks([0,4,0,4,0])==[1,3] and peaks([0,4,4,4,0])==[];record(6,'declared detector peak and plateau cases',True)
# Labels: known invalid fields precede unknown fields.
def label(number,code,maximum,allowed):
 if (number is not None and (not isinstance(number,int) or number<1 or number>maximum)) or (code is not None and code not in allowed):return 'revise'
 if number is None or code is None:return 'review'
 return 'ready'
assert [label(n,c,4,{'red','blue'}) for n,c in [(4,'red'),(5,None),(2,None)]]==['ready','revise','review']
assert label(4,None,4,{'red','blue'})=='review'
assert [label(n,c,7,{'X','Y'}) for n,c in [(7,'X'),(8,'Y'),(None,'X'),(8,None)]]==['ready','revise','review','revise']
assert sum(a==b for a,b in zip(['ready','revise','review','ready'],['ready','review','review','revise']))==2;record(7,'known-failure priority, independent forms and annotator agreement',True)
# Feature comparisons: parse the published P/Q/R/S records, then check controlled pairs.
w=d['weeks'][7];text=w['sections'][5]['blocks'][20]['text'];boxes={k:(int(x),int(y),pattern) for k,x,y,pattern in re.findall(r'([PQRS])=\((\d+),(\d+),(\w+)\)',text)};assert len(boxes)==4
p,q,r,s=[boxes[k] for k in 'PQRS'];assert p[0]!=q[0] and p[1:]==q[1:];assert s[1]!=r[1] and s[0]==r[0] and s[2]==r[2];assert p[:2]==s[:2] and p[2]!=s[2]
assert [x<=6 and y<=4 for x,y,_ in [p,q,r,s]]==[True,False,False,True]
assert 'comparing S with R isolates height' in w['sections'][5]['blocks'][26]['text'];record(8,'controlled pairs and shelf acceptance',True)
if d['weeks'][8]['sections'][0].get('reading_flow'):
 def recipe(start,ops):
  out=[start]
  for op,n in ops:start=start+n if op=='+' else start-n if op=='-' else start*n;out.append(start)
  return out
 assert recipe(3,[('*',2),('+',4),('-',1)])==[3,6,10,9]
 assert recipe(3,[('+',4),('*',2),('-',1)])==[3,7,14,13]
 assert recipe(0,[('*',2),('+',4),('-',1)])[-1]==3 and recipe(0,[('+',4),('*',2),('-',1)])[-1]==7
 x,y=4,1;y=x;x+=3;y*=2;assert (x,y)==(7,8)
 x,y=4,1;x+=3;y=x;y*=2;assert (x,y)==(7,14);record(9,'recipe order, changed starts and independent number boxes',True)
if d['weeks'][9]['sections'][0].get('reading_flow'):
 def counter(start,strict=False):
  current=start+2;test=current>6 if strict else current>=6;return current-1 if test else current*2
 assert [counter(s) for s in [3,4,5]]==[10,5,6] and [counter(s,True) for s in [3,4,5]]==[10,12,6]
 def brightness(start,strict=False):
  current=start+3;test=current<7 if strict else current<=7;return current-2 if test else current+1
 assert [brightness(s) for s in [3,4,5]]==[4,5,9] and brightness(4,True)==8;record(10,'inclusive/strict branch comparisons and independent brightness runs',True)
if d['weeks'][10]['sections'][0].get('reading_flow'):
 def loop(start,test,step):
  trace=[start]
  while test(start):
   start+=step;trace.append(start)
   if len(trace)>20:raise AssertionError('Unexpected nontermination in finite example')
  return trace
 assert loop(2,lambda x:x<10,3)==[2,5,8,11] and loop(10,lambda x:x<10,3)==[10]
 assert loop(7,lambda x:x>1,-2)==[7,5,3,1] and loop(6,lambda x:x>1,-2)==[6,4,2,0] and loop(1,lambda x:x>1,-2)==[1];record(11,'loop updates, zero iterations, overshoot and independent countdown',True)
if d['weeks'][11]['sections'][0].get('reading_flow'):
 expected=lambda x:2*(x+3)-2;add4=lambda x:x+3+4-2;addstart=lambda x:x+3+x-2
 assert [expected(x) for x in [4,2,5]]==[12,8,14]
 assert [add4(x) for x in [4,2,5]]==[9,7,10] and [addstart(x) for x in [4,2,5]]==[9,5,11]
 assert 6+6==2*6==12 and 2+6==8 and 2*2==4
 intended=['Group' if x+1>=5 else 'Single' for x in [3,4,5]];copied=['Group' if x+1>5 else 'Single' for x in [3,4,5]]
 assert intended==['Single','Group','Group'] and copied==['Single','Single','Group'];record(12,'distinguishing fault predictions and independent ticket boundary',True)
if d['weeks'][12]['sections'][0].get('reading_flow'):
 def errors(xs,ys,t):return sum(('tall' if x>=t else 'short')!=y for x,y in zip(xs,ys))
 xs=[2,4,6,8];ys=['short','short','tall','tall']
 assert [errors(xs,ys,t) for t in [3,5,6,7]]==[1,0,0,1]
 assert [errors(xs+[5],ys+['short'],t) for t in [3,5,6,7]]==[2,1,0,1]
 assert [errors([1,3,5,7],['short','tall','tall','tall'],t) for t in [2,4,6]]==[0,1,2]
 assert [errors([3,5,4],['short','tall','short'],t) for t in [4,5]]==[1,0];record(13,'per-candidate counts, added-label refit and independent distance task',True)
if d['weeks'][13]['sections'][0].get('reading_flow'):
 def classify(x,unit,low,high,boundary):
  if x is None or unit!='cm' or not isinstance(x,int) or not low<=x<=high:return None
  return 'long' if x>=boundary else 'short'
 assert [classify(x,'cm',0,15,9) for x in [0,8,9,16]]==['short','short','long',None] and classify(9,'mm',0,15,9) is None
 assert [classify(x,'cm',1,12,8) for x in [7,8,None,13]]==['short','long',None,None];record(14,'contract before threshold and independent Ribbon1 records',True)
if d['weeks'][14]['sections'][0].get('reading_flow'):
 xs=[3,5,6,9];labels=['short','long','long','long'];pred=['long' if x>=6 else 'short' for x in xs]
 assert pred==['short','short','long','long'] and sum(p==y for p,y in zip(pred,labels))==3
 assert sum(('long' if x>=5 else 'short')==y for x,y in zip(xs,labels))==4
 xs=[5,7,9,11];labels=['short','short','long','long'];assert sum(('long' if x>=6 else 'short')==y for x,y in zip(xs,labels))==3 and sum(('long' if x>=8 else 'short')==y for x,y in zip(xs,labels))==4;record(15,'original frozen agreement and feedback-guided replays',True)
if d['weeks'][15]['sections'][0].get('reading_flow'):
 assert {x<=5 for x in [4,5]}=={True} and {x<=5 for x in [5,6]}=={False,True} and {x<=5 for x in [6,7]}=={False}
 assert [{'far' if x>=4 else 'near' for x in group} for group in [[2,3],[3,4],[4,5]]]==[{'near'},{'near','far'},{'far'}];record(16,'stable and boundary-crossing complete possibility sets',True)
if d['weeks'][16]['sections'][0].get('reading_flow'):
 pred=['far' if h>=6 else 'near' for h in [4,6,8]];obs=['far' if distance>=4 else 'near' for distance in [3,3,5]];assert sum(p==y for p,y in zip(pred,obs))==2
 pred=['slow' if score>=7 else 'quick' for score in [6,7,9,5]];obs=['slow' if minutes>10 else 'quick' for minutes in [12,10,14]];assert pred==['quick','slow','slow','quick'] and sum(p==y for p,y in zip(pred[:3],obs))==1;record(17,'two distinct rules, original ramp matches and independent drying outcomes',True)
if d['weeks'][17]['sections'][0].get('reading_flow'):
 assert 7+2+1==10 and 7/(7+2)==7/9 and (7+2)/10==.9
 assert [7/10,(7+1)/10]==[.7,.8]
 assert 6+1+1==8 and 6/(6+1)==6/7 and [6/8,7/8]==[.75,.875];record(18,'assessed fractions, missing coverage and bounded overall agreement',True)
if d['weeks'][20]['sections'][0].get('reading_flow'):
 values=[4,None,0,80/10];assessed=[v for v in values if v is not None]
 assert len(values)==4 and len(assessed)==3 and sum(v>=5 for v in assessed)==1
 assert len(set(['T1','T2','T3','T4','T1']))==4;record(21,'source-supported unit conversion, distinct identity and missing/zero separation',True)
if d['weeks'][21]['sections'][0].get('reading_flow'):
 assert 6*4==24 and 5/6!=5/24 and 2+8*2==18
 assert 2+2+2+1==7 and 8-7==1;record(22,'target coverage, duplicated file counts and selected-versus-assessed plan',True)
if d['weeks'][22]['sections'][0].get('reading_flow'):
 from fractions import Fraction as F
 assert F(8+1,8+4)==F(3,4) and F(6+2,12)==F(2,3)
 assert F(9+3,16)==F(3,4) and F(8+5,16)==F(13,16)
 assert (F(9,10)+F(3,6))/2==F(7,10) and (F(8,10)+F(5,6))/2==F(49,60)
 assert 7+1==5+3==8 and F(2+4,2+8)==F(3,5)
 assert F(10+2,20)==F(3,5) and F(9+5,20)==F(7,10);record(23,'shared tests, per-card versus equal-group weighting and independent sound totals',True)
if d['weeks'][23]['sections'][0].get('reading_flow'):
 assert 8+7+5==20 and 9+7+4==20;record(24,'fictional workshop and lunch totals',True)
if d['weeks'][24]['sections'][0].get('reading_flow'):
 assert 6*4-3==21 and 3*4-2==10 and 3*4-4==8
 assert 4*5-3==17 and 18//3==6 and 5*6-4==26;record(25,'complete capacity expressions, changed reservations and independent record B',True)
if d['weeks'][26]['sections'][0].get('reading_flow'):
 assert 4*200-12*50==200 and 4*2-12*.5==2
 assert 4*150-8*50==200 and 4*150-10*50==100
 assert 5*250-3*300==350 and 350/1000==.35 and 18/24==.75;record(27,'two distinct ribbon datasets, changed bookmarks, independent mass units and percentage correction',True)
if d['weeks'][29]['sections'][0].get('reading_flow'):
 def activity(minutes,quiet):
  if type(minutes) is not int or not 0<=minutes<=30 or quiet not in ('Yes','No'):return 'clarify'
  return next((name for name,time,isquiet in [('B1',10,True),('B2',8,False),('B3',12,True),('B4',15,False)] if time<=minutes and (quiet=='No' or isquiet)),'no match')
 assert [activity(*case) for case in [(10,'Yes'),(8,'No'),(7,'No'),(12,'No'),(8,'Yes'),(None,'Yes'),(0,'Yes')]]==['B1','B2','no match','B1','no match','clarify','no match']
 def room(size,quiet):return next((name for name,capacity,isquiet in [('R1',6,True),('R2',10,False)] if capacity>=size and (quiet=='No' or isquiet)),'no match')
 assert [room(*case) for case in [(6,'Yes'),(8,'No'),(8,'Yes')]]==['R1','R2','no match'];record(30,'activity baseline conditions, equality, order, missing/zero distinction and independent room catalogue',True)
if d['weeks'][30]['sections'][0].get('reading_flow'):
 assert activity(9,'No')=='B2' and activity(5,'Yes')=='no match' and activity(11,'No')=='B1' and activity(15,'No')=='B1'
 kits=[('K1',False,2),('K2',True,2),('K3',True,4)]
 assert [next((name for name,glue,count in kits if glue and count>=needed),'no match') for needed in [2,3]]==['K2','K3']
 assert next(name for name,cap in [('C1',4),('C2',8)] if cap>=6)=='C2';record(31,'ordered activity stops, both kit conditions and independent room capacity',True)
if d['weeks'][31]['sections'][0].get('reading_flow'):
 assert next(name for name,cap in [('X',3),('Y',7)] if cap>=4)=='Y'
 assert [next((name for name,cap in [('E1',3),('E2',6)] if cap>=size),'no match') for size in [5,7]]==['E2','no match']
 assert [activity(*case) for case in [(9,'No'),(11,'No'),(7,'No'),(None,'Yes')]]==['B2','B1','no match','clarify'];record(32,'prototype required expectations, bin correction and independent equipment runs',True)
if d['weeks'][32]['sections'][0].get('reading_flow'):
 routine=[(11,'Yes'),(9,'No'),(6,'No'),(9,'Yes')]
 assert [activity(*case) for case in routine]==['B1','B2','no match','no match']
 assert {activity(m,q) for m in range(31) for q in ['Yes','No']}=={'B1','B2','no match'}
 expected=[next((n for n,c in [('P1',3),('P2',7)] if c>=x),'none') for x in [2,4,6,8]]
 assert expected==['P1','P2','P2','none'] and sum(a==b for a,b in zip(expected,['P1','P2','P1','none']))==3
 assert [next((n for n,c in [('E1',4),('E2',8)] if c>=x),'none') for x in [3,6,9]]==['E1','E2','none'];record(33,'routine expectations, unreachable later outputs, retained pouch failure and independent equipment expectations',True)
if d['weeks'][33]['sections'][0].get('reading_flow'):
 def variant(m,q,times,strict=False,ignorequiet=False):
  if type(m) is not int or not 0<=m<=30 or q not in ['Yes','No']:return 'clarify'
  return next(('B'+str(i+1) for i,(time,isquiet) in enumerate(zip(times,[True,False,True,False])) if (time<m if strict else time<=m) and (ignorequiet or q=='No' or isquiet)),'no match')
 assert [variant(m,'Yes',[10,8,12,15]) for m in [9,10,11]]==['no match','B1','B1']
 assert variant(10,'Yes',[10,8,12,15],True)=='no match'
 assert [variant(*case,[10,8,12,15],True) for case in routine]==[activity(*case) for case in routine]
 assert variant(12,'Yes',[20,8,12,15])=='B3' and variant(15,'No',[20,18,17,15])=='B4' and variant(15,'Yes',[20,18,17,15])=='no match'
 assert [next((n for n,c in [('E1',4),('E2',8)] if c>x),'none') for x in [3,4,5,8]]==['E1','E2','E2','none'];record(34,'equality blind spot, documented catalogue variations and strict capacity errors',True)
if d['weeks'][34]['sections'][0].get('reading_flow'):
 assert all(variant(m,q,[10,8,12,15])==activity(m,q) for m in range(31) for q in ['Yes','No'])
 cases=[(10,'Yes'),(9,'Yes'),(8,'No'),(6,'No')]
 assert [variant(*case,[10,8,12,15],True) for case in cases]==['no match','no match','no match','no match']
 assert [variant(*case,[10,8,12,15],ignorequiet=True) for case in cases]==['B1','B2','B2','no match']
 assert [variant(*case,[10,8,12,15]) for case in cases]==['B1','no match','B2','no match']
 assert [next((n for n,c in [('E1',4),('E2',8)] if c>x),'none') for x in [8,3]]==['none','E1']
 assert [[n for n,c in [('E1',4),('E2',8)] if c>=x][-1] for x in [8,3]]==['E2','E2'];record(35,'targeted equality repair, introduced quiet regression and independent last-fit regression',True)
if d['weeks'][35]['sections'][0].get('reading_flow'):
 final=[(7,'No'),(11,'Yes'),(14,'No'),(18,'Yes'),(6,'No'),(7,'Yes'),(0,'No'),(30,'Yes'),(31,'No'),(None,'Yes')]
 assert [variant(*case,[18,14,11,7]) for case in final]==['B4','B3','B2','B1','no match','no match','no match','B1','clarify','clarify']
 assert 6/8==.75 and 8/10==.8 and 9/10==.9 and (10+2)/(12+4)==.75 and 4/6<5/6;record(36,'teacher-reserved catalogue key, separate demonstration denominators and independent library comparison',True)
(R/'reports/connected-reasoning-checks.json').write_text(json.dumps({'checks':rows,'errors':[]},indent=2)+'\n');print(len(rows),'reasoning checks passed.')
