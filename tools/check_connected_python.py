"""Execute authored Python teaching examples in fresh namespaces."""
from pathlib import Path
import contextlib,io,json
R=Path(__file__).resolve().parents[1];d=json.loads((R/'content/programme.json').read_text());weeks={w['id']:w for w in d['weeks']};checks=[]
def run(code,expected=None,error=None):
 out=io.StringIO();caught=None;namespace={}
 try:
  with contextlib.redirect_stdout(out):exec(compile(code,'<academy-example>','exec'),namespace)
 except Exception as e:caught=type(e).__name__
 assert caught==error,(code,caught,error)
 if expected is not None:assert out.getvalue()==expected,(code,out.getvalue(),expected)
 return namespace
def authored(n):return weeks[f'ai-2/{n}']['sections'][0].get('reading_flow')
if authored(1):
 w=weeks['ai-2/1'];code=w['sections'][2]['blocks'][12]['text'];run(code,'24\n');run(w['sections'][7]['blocks'][9]['text'],'30\n')
 run(code.replace('packs = 4','packs = 0'),'0\n');run('print(total)\n'+code,error='NameError')
 run('boxes=3\ntotal=boxes*5\ntotal=total+2\nprint(total)','17\n');checks.append({'week':'ai-2/1','verified':'published scripts, zero packs, fresh-name error and book-box update'})
if authored(2):
 w=weeks['ai-2/2'];run(w['sections'][2]['blocks'][11]['text'],'8\n3\n');run(w['sections'][7]['blocks'][8]['text'],'8\n8\n')
 definition=w['sections'][2]['blocks'][11]['text'].split('\n\n')[0];run(definition,'');run(definition+'\nshow_remaining(12)',error='TypeError');run(definition+'\nshow_remaining(9,9)\nshow_remaining(9,0)','0\n9\n')
 preview=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title','').startswith('Optional return-value'))
 run(preview,'24\n');assert run(preview.replace('print(needed)',''),'')['needed']==24
 checks.append({'week':'ai-2/2','verified':'published correct/faulty functions, definition-only run, argument errors and boundary calls'})
if authored(3):
 w=weeks['ai-2/3'];code=w['sections'][2]['blocks'][12]['text']
 for value,label in [(-1,'Invalid'),(0,'Short'),(11,'Short'),(12,'Short'),(13,'Long')]:run(code.replace('minutes = 12',f'minutes = {value}'),label+'\n')
 run(w['sections'][7]['blocks'][8]['text'],'Short\n');run(code.replace('<= 12','< 12'),'Long\n')
 other=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title','').startswith('Separate reading-time'))
 for value,label in [(-1,'Invalid'),(0,'Empty'),(10,'Short'),(11,'Long')]:run(other.replace('minutes = 0',f'minutes = {value}'),label+'\n')
 checks.append({'week':'ai-2/3','verified':'published main and separate chains, inclusive boundaries and overwritten-label bug'})
if authored(4):
 w=weeks['ai-2/4'];code=w['sections'][2]['blocks'][11]['text'];run(code,'6\n');run(w['sections'][7]['blocks'][8]['text'],'3\n')
 for expression,expected in [('range(1, 1)','0\n'),('range(1, 2)','1\n'),('range(2, 5)','9\n')]:run(code.replace('range(1, 4)',expression),expected)
 run(code.replace('\nprint(total)','\n    print(total)'),'1\n3\n6\n')
 jar=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title','').startswith('Separate token-jar'))
 run(jar,'13\n');run(jar.replace('range(4)','range(0)'),'1\n');run(jar.replace('\nprint(total)','\n    print(total)'),'4\n7\n10\n13\n')
 checks.append({'week':'ai-2/4','verified':'published loops, reset defect, zero/one/several iterations and print placement'})
if authored(5):
 w=weeks['ai-2/5'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title','').startswith('While-loop stopping'))
 for start,expected in [(3,'3\n'),(4,'0\n'),(12,'0\n')]:run(code.replace('count = 12',f'count = {start}'),expected)
 prefix=[12-4*i for i in range(6)];assert prefix==[12,8,4,0,-4,-8] and all(x%4==0 for x in prefix)
 run('count=1\nwhile count<8:\n    count=count+3\nprint(count)','10\n')
 checks.append({'week':'ai-2/5','verified':'complete while script, zero/one/several updates, finite defect prefix and independent increasing loop'})
if authored(6):
 w=weeks['ai-2/6'];code=w['sections'][2]['blocks'][11]['text'];run(code,'True\nTrue\nTrue\n')
 run(code.replace('return capacity - used','return capacity + used'),'False\nFalse\nTrue\n')
 run(code.replace('return capacity - used','return 5'),'True\nFalse\nFalse\n')
 run(code.replace('return capacity - used','return capacity + used').replace('print(actual == expected)','assert actual == expected'),error='AssertionError')
 shelf=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title','').startswith('Separate shelf bug'))
 run(shelf,'18\n18\n12\n');run(shelf.replace('(bundle_count + loose) * 6','bundle_count * 6 + loose'),'13\n3\n12\n')
 checks.append({'week':'ai-2/6','verified':'published harness, addition/constant defects, first-failure assertion and shelf formula repair'})
if authored(7):
 w=weeks['ai-2/7'];code=w['sections'][2]['blocks'][11]['text'];run(code,'True\nTrue\n')
 body=code[code.index('for row in rows:'):]
 for value,expected in [(0,True),(60,True),(-1,False),(61,False),("12",False),(12,True),(True,False)]:
  run('rows='+repr([{'activity':'Reading','minutes':value}])+'\n'+body,str(expected)+'\n')
 run("rows=[{'activity':'Reading'}]\n"+body,error='KeyError')
 run("rows=[{'activity':'   ','minutes':12}]\n"+body,'True\n')
 checks.append({'week':'ai-2/7','verified':'published validator, inclusive boundaries, exact types, missing-key limitation and explicit whitespace limitation'})
if authored(11):
 w=weeks['ai-2/11'];code=w['sections'][2]['blocks'][12]['text'];run(code,'[]\n3 1 2\n')
 moved=code.replace('train_groups = {"A", "B", "C"}','train_groups = {"A", "B", "C", "D"}')
 run(moved,"['D']\n4 1 2\n")
 run(code.replace('test_groups = {"E", "F"}','test_groups = {"A", "D", "E", "F"}'),"['A', 'D']\n3 1 4\n")
 table=w['sections'][1]['blocks'][13]['rows'][1:];counts={'Training':0,'Validation':0,'Test':0};inventory=[]
 for trip,frames,role in table:
  ids=frames.split();assert all(frame.startswith(trip) for frame in ids);inventory.extend(ids);counts[role]+=len(ids)
 assert list(counts.values())==[6,2,4] and len(set(inventory))==len(inventory)==12
 checks.append({'week':'ai-2/11','verified':'published group-intersection script, multiple pair overlaps, moved-D group counts and source-table frame inventory'})
if authored(12):
 import math
 w=weeks['ai-2/12'];code=w['sections'][2]['blocks'][11]['text'];namespace=run(code,'baseline 80.0 50.0\ncandidate 80.0 87.5\n');score=namespace['scores']
 for matrix,expected in [([[8,0],[8,0]],(0.5,0.5)),([[6,2],[0,8]],(0.875,0.875)),([[18,0],[2,0]],(0.9,0.5)),([[15,3],[1,1]],(0.8,2/3))]:
  assert all(math.isclose(actual,target) for actual,target in zip(score(matrix),expected))
 run(code+'\nprint(scores([[10,0],[0,0]]))',error='ValueError')
 run(code+'\nprint(scores([[0,0],[0,2]]))',error='ValueError')
 poll=w['sections'][2]['blocks'][15]['text'];run(poll,'0.75\n')
 line=poll.splitlines()[0]
 run(poll.replace(line,'responses = ["Unknown", "Unknown", "Unknown"]'),'No known responses\n')
 run(poll.replace(line,'responses = ["Yes", "Yes", "No", "Unknown", "No", "Yes"]'),'0.6\n')
 checks.append({'week':'ai-2/12','verified':'published score and poll scripts, changed class mix, independent matrices, both missing-class branches and zero-known poll guard'})
if authored(13):
 w=weeks['ai-2/13'];code=w['sections'][2]['blocks'][11]['text'];ns=run(code,'[[2, 1], [2, 3]]\n5 8\n');pairs=ns['pairs']
 assert len({item[0] for item in pairs})==len(pairs)==8
 run(code.replace('labels = [','pairs.append(pairs[0])\nlabels = [',1),'[[3, 1], [2, 3]]\n6 9\n')
 run(code.replace('("V1", "clear", "clear")','("V1", "unreviewed", "clear")'),error='KeyError')
 reverse=run(code.replace('labels = ["clear", "blocked"]','labels = ["blocked", "clear"]'),'[[3, 2], [1, 2]]\n5 8\n')
 assert sum(map(sum,reverse['counts']))==8
 checks.append({'week':'ai-2/13','verified':'published linked-record matrix, unique source IDs, reversed label order, duplicate-count limitation and unknown-label error'})
if authored(14):
 w=weeks['ai-2/14'];code=w['sections'][2]['blocks'][11]['text'];ns=run(code,'0 1\n1 2\n0 clear blocked\n');assert ns['tree']==(0,{0:'clear',1:'blocked'})
 assert ns['majority'](['clear','blocked'])=='clear' and ns['majority']([])=='clear'
 tail=code[code.index('def majority'):]
 run('rows = [(0,0,"clear"),(1,1,"blocked")]\n'+tail,'0 0\n1 0\n0 clear blocked\n')
 independent=[(1,0,'clear'),(1,1,'clear'),(1,0,'clear'),(0,1,'blocked'),(0,0,'blocked'),(0,1,'clear')]
 new=run('rows = '+repr(independent)+'\n'+tail,'0 1\n1 2\n0 blocked clear\n')
 assert new['tree']==(0,{0:'blocked',1:'clear'})
 full=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title','').startswith('Complete training-then-validation'))
 evaluated=run(full);assert evaluated['predictions']==['blocked','clear','clear','blocked'] and sum(p==y for p,y in zip(evaluated['predictions'],evaluated['reference']))==2
 checks.append({'week':'ai-2/14','verified':'published candidate learner and validation script, leaf/candidate ties, independent reversed leaves and explicit empty-branch limitation'})
if authored(15):
 w=weeks['ai-2/15'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title','').startswith('Worst-case question audit'))
 ns=run(code,'mystery? 4 4 4\npaperback? 6 2 6\nEnglish? 8 0 8\nchosen mystery?\nmystery? 4 0 4\npaperback? 3 1 3\nEnglish? 4 0 4\nafter mystery Yes paperback?\n')
 assert len({c[0] for c in ns['cards']})==8 and len(ns['remaining'])==4
 for population in [ns['cards'],ns['remaining']]:
  for name,col,value in ns['questions']:
   yes=sum(c[col]==value for c in population);no=sum(c[col]!=value for c in population);assert yes+no==len(population)
 assert max(6,4)<max(10,0)
 checks.append({'week':'ai-2/15','verified':'published worst-case question audit, complete joint card table, restricted-set recount, branch partition totals and independent count comparison'})
if authored(17):
 w=weeks['ai-2/17'];code=w['sections'][2]['blocks'][11]['text'];ns=run(code,'6.0\n3\n');assert ns['values']==[2,3,3,4,18]
 run(code.replace('[2, 3, 3, 4, 18]','[2, 3, 3, 4, 8]'),'4.0\n3\n')
 run(code.replace('[2, 3, 3, 4, 18]','[2, 3, 3, 4, 3]'),'3.0\n3\n')
 run(code.replace('[2, 3, 3, 4, 18]','[]'),error='ZeroDivisionError')
 general=next(b['text'] for b in w['sections'][7]['blocks'] if b.get('title','').startswith('Complete odd, even and empty'))
 ns=run(general,'(6.0, 3)\n(5.0, 5.0)\n(None, None)\n');summaries=ns['summaries']
 assert summaries([9,1,3])==(13/3,3) and summaries([1,2,2,3,12])==(4,2) and summaries([1,2,2,3,2])==(2,2)
 assert summaries([0])==(0,0) and summaries([])==(None,None)
 checks.append({'week':'ai-2/17','verified':'published odd-only and complete summary scripts, hypothetical/authorised changes, empty-error/guard paths, even median and independent list arithmetic'})
if authored(18):
 w=weeks['ai-2/18'];code=w['sections'][2]['blocks'][11]['text'];run(code,'[0, 12]\n3\n')
 initial=code[:code.index('accepted = []')]
 edges=[{'minutes':60},{'minutes':'5'},{'minutes':True},{'minutes':False},{'minutes':0.0},{'minutes':0}]
 run(code.replace(initial,'rows = '+repr(edges)+'\n'),'[60, 0]\n4\n')
 full=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title','').startswith('Extended duration audit'))
 ns=run(full,'[0, 12, 60]\n5\n');assert [row[0] for row in ns['review']]==[2,4,5,7,8] and ns['rows'][1]=={}
 stock=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title','').startswith('Separate stock-count validator'))
 run(stock,'[0, 4]\n4\n');run(stock.replace('{"count": "4"}','{"count": 4}'),'[0, 4, 4]\n3\n')
 independent=code.replace(initial,'rows = '+repr([{'count':3},{},{'count':0},{'count':11},{'count':'3'}])+'\n').replace('"minutes"','"count"').replace('<= 60','<= 10')
 run(independent,'[3, 0]\n3\n')
 checks.append({'week':'ai-2/18','verified':'published duration/stock/reason scripts, zero and inclusive maximum, Boolean/text/float rejection, authorised conversion, retained raw rows and independent bound change'})
if authored(19):
 w=weeks['ai-2/19'];run(w['sections'][2]['blocks'][11]['text'],'2 3\n')
 run(w['sections'][2]['blocks'][17]['text'],'Drawing ######## 8\nBuilding ########## 10\n')
 assert 12/15==0.8 and 12/60==0.2 and 10/8==1.25 and (10-7)/(8-7)==3
 checks.append({'week':'ai-2/19','verified':'published respondent-count/text-chart scripts, separate invitation/population denominators and truncated-bar contrast'})
if authored(20):
 w=weeks['ai-2/20'];code=w['sections'][2]['blocks'][11]['text'];run(code,'0.8\n0.2\n0.5\n')
 run(code.replace('club_yes, club_n = 8, 10','club_yes, club_n = 72, 90'),'0.8\n0.2\n0.74\n')
 assert (3+2)/(4+6)==0.5 and (18+2)/(20+10)==2/3
 assert abs(0.25*(12/15)+0.75*(3/15)-0.35)<1e-10
 checks.append({'week':'ai-2/20','verified':'published combined-rate script, fixed within-group rates under changed respondent mix and independent/weighted arithmetic'})
if authored(21):
 w=weeks['ai-2/21'];run(w['sections'][2]['blocks'][11]['text'],'Sketch 2\nRelay 3\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title','').startswith('Six-book equal and weighted'))
 ns=run(code);assert ns['distances']=={'A':3,'B':4,'C':3,'D':9,'E':11,'F':6} and ns['closest']==['A','C']
 equal={name:sum(abs(x-y) for x,y in zip(v,ns['target'])) for name,v in ns['books'].items()};assert equal=={'A':3,'B':2,'C':2,'D':7,'E':8,'F':3}
 assert [sum(abs(x-y) for x,y in zip(v,[3,2])) for v in [[1,2],[3,4],[4,2]]]==[2,2,1]
 checks.append({'week':'ai-2/21','verified':'published activity/six-book scripts, coordinate weights, all equal/weighted ties and independent distance arithmetic'})
if authored(22):
 w=weeks['ai-2/22'];run(w['sections'][2]['blocks'][11]['text'],"['A', 'B', 'C']\nclear\n")
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title','').startswith('Complete neighbour and frozen-validation'))
 ns=run(code);assert ns['correct']==ns['baseline_correct']==1 and ns['predict'](3,1)==(['A'],'blocked') and ns['predict'](3,3)==(['A','B','C'],'clear')
 original=list(ns['train']);ns['train'].reverse();assert ns['predict'](3,3)==(['A','B','C'],'clear');ns['train']=original
 ns['train']=[('P',1,'clear'),('Q',5,'blocked'),('R',7,'blocked'),('S',11,'clear'),('T',13,'blocked')]
 assert ns['predict'](6,3)==(['Q','R','P'],'blocked')
 predictions=[ns['predict'](query,3)[1] for query in [6,10,12]];assert predictions==['blocked']*3
 assert sum(p==y for p,y in zip(predictions,['blocked','clear','blocked']))==2
 checks.append({'week':'ai-2/22','verified':'published stored-neighbour scripts, k1/k3 disagreement, row-order invariance under ID ties, fixed validation/baseline and independent pool'})
if authored(23):
 w=weeks['ai-2/23'];code=w['sections'][2]['blocks'][11]['text'];run(code,'A 10\n');run(code.replace('"minutes": 25','"minutes": 20'),'A 10\nB 11\n')
 full=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title','').startswith('Complete eligible-score'))
 ns=run(full);assert ns['scores']=={'A':11,'C':11} and ns['tied']==['A','C'] and ns['review']==[('B','exceeds time limit')]
 empty=run(full.replace('limit = 14','limit = 0'));assert empty['scores']=={} and len(empty['review'])==3
 invalid=run(full.replace('"interest": 3','"interest": True',1));assert invalid['review'][0]==('A','missing or invalid input')
 checks.append({'week':'ai-2/23','verified':'published eligibility/score scripts, inclusive boundary, changed-weight tie, empty eligible set and exact-type rejection'})
if authored(24):
 w=weeks['ai-2/24'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title','').startswith('Complete scripted exposure'))
 ns=run(code);simulate=ns['simulate'];log,exposure,clicks=simulate();assert [row[1] for row in log]==['A']*3 and exposure=={'A':3,'B':0} and clicks=={'A':3,'B':0}
 log,exposure,clicks=simulate(['A','B','A']);assert exposure=={'A':2,'B':1} and clicks=={'A':2,'B':0} and log[0][3]=={'A':1,'B':0} and log[1][2] is False
 run(w['sections'][2]['blocks'][11]['text'],'A\n')
 assert 1/4==0.25 and 2/4==0.5
 checks.append({'week':'ai-2/24','verified':'published scripted exposure policies, separate display/click totals, immutable round snapshots, retained implementation review and independent rate arithmetic'})
if authored(25):
 w=weeks['ai-2/25'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title','').startswith('Complete exact longest-match'))
 ns=run(code);encode=ns['encode'];vocab=ns['vocabulary'];assert encode('cats sat',vocab)==([1,5,6,7],None) and encode('Cat',vocab)==([],(0,'C'))
 assert encode('sat cats',vocab)==([7,6,1,5],None) and encode('sat cat!',vocab)==([7,6,1],(7,'!'))
 assert encode('books book!',{1:'book',2:'books',3:' '})==([2,3,1],(10,'!'))
 ids,error=encode('cats sat',ns['character_entries']);assert len(ids)==8 and ''.join(ns['character_entries'][i] for i in ids)=='cats sat' and error is None
 assert encode('',vocab)==([],None)
 checks.append({'week':'ai-2/25','verified':'published longest-match encoder, exact spaces/case, overlapping chunks, independent partial-failure positions, character-only round trip and empty text'})
if authored(30):
 w=weeks['ai-2/30'];run(w['sections'][5]['blocks'][16]['text'],'looking_up\n')
 code=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title','').startswith('Complete bounded structural'))
 ns=run(code,'complete; lookups=1\ninvalid edge: review->looking_up\nlookup budget exceeded\nincomplete; lookups=1\n');audit=ns['audit_trace']
 assert audit(['ready','looking_up','review','done'])=='complete; lookups=1'
 assert audit(['ready','looking_up','done','review'])=='invalid edge: done->review'
 assert audit([])=='invalid start' and audit(['ready'])=='incomplete; lookups=0'
 try:audit(['ready'],True)
 except ValueError:pass
 else:raise AssertionError('Boolean budget accepted')
 checks.append({'week':'ai-2/30','verified':'published transition and complete trace-validator scripts, first invalid edge, zero/Boolean budget, incomplete and terminal behavior; authorisation explicitly outside validator scope'})
if authored(31):
 w=weeks['ai-2/31'];ns=run(w['sections'][2]['blocks'][15]['text'],'True\nFalse\nFalse\n')
 assert ns['allowed']('teacher','read_review') and not ns['allowed']('unknown','read_summary')
 checks.append({'week':'ai-2/31','verified':'published role-policy script and extension teacher/unknown queries; authentication and resource scopes explicitly separate'})
if authored(32):
 w=weeks['ai-2/32'];run(w['sections'][2]['blocks'][11]['text'],'20\nname ascending\n')
 code=w['sections'][2]['blocks'][17]['text'];run(code,'3 2\n10.0\n')
 run(code.replace('raw = [10, 0, 20, None, -2]','raw = [True, None, -2, 61]'),'0 4\nNo valid observations\n')
 run(code.replace('raw = [10, 0, 20, None, -2]','raw = [10, 0, 20, None, -2, 30]'),'4 2\n15.0\n')
 checks.append({'week':'ai-2/32','verified':'published configuration and accepted-duration scripts, exact-type rejection, zero-valid branch and changed-denominator mean'})
if authored(33):
 w=weeks['ai-2/33'];ns=run(w['sections'][2]['blocks'][11]['text'],'A\n');recommend=ns['recommend'];items=ns['items']
 assert recommend(list(reversed(items)),10)=='A' and recommend(items,8) is None and recommend([],10) is None
 vs=run(w['sections'][2]['blocks'][17]['text'],'True\nFalse\n');valid=vs['valid_item'];assert not valid({'name':'A','minutes':10,'fun':2}) and not valid({'name':'A','minutes':True,'fun':2,'learning':3})
 code=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete pictured book ranking')
 bs=run(code,"[('D', 3), ('A', 2), ('B', 1)]\n[('A', 2), ('B', 1)]\n[]\n");assert bs['choose_book'](list(reversed(bs['books'])),'animal',90)==[('D',3),('A',2),('B',1)]
 full=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete validation-to-ranking activity pipeline')
 ns=run(full);pipe=ns['pipeline'];raw=ns['raw'];r=pipe(raw,20);assert r['winner']=='A' and r['accepted']==3 and r['rejected']==[(4,'invalid fun')] and r['ineligible']==['B']
 duplicate=pipe(raw+[dict(raw[0])],20);assert duplicate['winner']=='C' and duplicate['rejected']==[(1,'duplicate name'),(4,'invalid fun'),(5,'duplicate name')]
 assert pipe([],20)['winner'] is None and pipe(raw,True)=={'error':'invalid request'} and pipe(raw,0)['winner'] is None
 checks.append({'week':'ai-2/33','verified':'all published activity/validator/book/pipeline scripts, row-order ties, all-duplicate rejection, invalid request, no match and changed-book exclusion'})
if authored(34):
 w=weeks['ai-2/34'];run(w['sections'][2]['blocks'][11]['text'],'5 6\n')
 assert 5+10==15 and 6+10==16 and sum([4,1,2,1])==8 and sum([4,3,3,2])==12
 checks.append({'week':'ai-2/34','verified':'published outcome-counter script, duplicated-pass arithmetic, disjoint pictured category totals and preserved weak slices'})
if authored(35):
 w=weeks['ai-2/35'];run(w['sections'][2]['blocks'][11]['text'],'9 True\n10 True\n11 False\n');run(w['sections'][2]['blocks'][17]['text'],'3 score cases passed\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Exact Week33 pipeline with independent integration checks')
 ns=run(code);assert ns['pipeline'](ns['fixture'],10)==ns['expected']
 mutated=code.replace("if r['minutes'] <= limit]","if r['minutes'] < limit]")
 assert mutated!=code
 run(mutated,error='AssertionError')
 assert [x<=12 for x in [11,12,13,0]]==[True,True,False,True]
 checks.append({'week':'ai-2/35','verified':'published boundary/score/integration scripts, exact prior pipeline reuse, reversed-order report, empty/invalid/no-match cases and failing strict-comparison mutation'})
if authored(36):
 w=weeks['ai-2/36'];run(w['sections'][2]['blocks'][11]['text'],'A 8\n')
 code=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete pictured capstone book report');ns=run(code)
 original=ns['original'];assert original['selected']=='B' and original['ranked']==[('B',8),('A',7)] and original['accepted']==3 and original['rejected']==[(4,'invalid interest')] and original['over_limit']==['C']
 changed=ns['book_report'](ns['changed'],120);assert changed['selected']=='D' and changed['ranked']==[('D',9),('B',8),('A',7)] and changed['accepted']==4
 assert ns['books'][3]['interest']=='4' and ns['book_report'](ns['books'],0)['selected'] is None
 assert ns['book_report']([],120)['supplied']==0 and ns['book_report'](ns['books'],True)=={'error':'invalid page limit'}
 checks.append({'week':'ai-2/36','verified':'published count-consistency and complete book-report scripts, exact-type rejection, independent copied correction, counts/ranking, no-match, invalid request and reversed input'})
if weeks['ai-3/2']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/2'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete exact conditional-path audit');ns=run(code);F=ns['F'];paths=ns['paths']
 assert sum(paths.values())==1 and paths[('ready','end')]==F(2,5) and paths[('busy','end')]==F(3,20) and paths[('unknown','end')]==F(1,5)
 assert sum(ns['ends'].values())==F(5,8)
 assert sum(F(x)*F(y) for x,y in [('0.4','0.5'),('0.35','0.8'),('0.25','1')])==F(73,100)
 checks.append({'week':'ai-3/2','verified':'published exact conditional-path script, full versus partial event sums, separate sun/rain tree and independent end-path total'})
if weeks['ai-3/3']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/3'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete explicit toy tokenisation and exact round trip');ns=run(code);encode=ns['encode']
 assert encode('Ada!')==([1,4],None) and encode('AI🙂')==([2,5],None) and encode('schoolbook')==([8],None)
 assert encode('school book')==([6,3,7],None) and encode('ada')==([],(0,'a')) and encode('Ada?')==([1],(3,'?')) and encode('')==([],None)
 checks.append({'week':'ai-3/3','verified':'published explicit longest-match encoder, exact case/space/emoji, partial failures, empty input and successful round trips'})
if weeks['ai-3/4']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/4'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete exact half-temperature and cumulative-interval simulation');ns=run(code);F=ns['F'];sample=ns['sample'];half=ns['half_temperature']
 assert ns['q']==[F(18,23),F(9,46),F(1,46)] and [sample(ns['p'],u) for u in [F(0),F(6,10),F(9,10)]]==[0,1,2]
 assert [sample(ns['q'],u) for u in [F(2,10),F(6,10),F(9,10)]]==[0,0,1]
 try:sample(ns['p'],F(1))
 except ValueError:pass
 else:raise AssertionError('out-of-range draw accepted')
 independent=[F(1,2),F(3,10),F(1,5)];adjusted=half(independent);assert adjusted==[F(25,38),F(9,38),F(4,38)]
 assert [sample(independent,F(x)) for x in ['0.5','0.9']]==[1,2] and [sample(adjusted,F(x)) for x in ['0.5','0.9']]==[0,2]
 checks.append({'week':'ai-3/4','verified':'published exact temperature/sampling program, half-open endpoints, invalid draw rejection, paired draws and independent adjusted-table outcomes'})
if weeks['ai-3/6']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/6'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Complete supplied-rubric-outcome score and mandatory-gate audit')
 ns=run(code,'original 3 of 4 full pass: False\nchanged 2 of 4 full pass: False\nrepaired 4 of 4 full pass: True\n')
 assert [sum(flags) for flags in ns['reviewed'].values()]==[3,2,4]
 checks.append({'week':'ai-3/6','verified':'published reviewed-flag rubric audit, mandatory gates distinct from point totals, complete original/changed/repaired outcomes'})
if weeks['ai-3/8']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/8'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete classroom JSON/schema/source validator and six candidate cards')
 ns=run(code,'1 accepted\n2 syntax\n3 schema: capacity\n4 schema: capacity\n5 schema: exact fields required\n6 semantic: unsupported claims\n');validate=ns['validate'];sources=ns['sources'];base=ns['cards'][0]
 assert validate(base.replace(':12',':0'),sources).startswith('semantic:')
 assert validate(base.replace('"capacity":12,',''),sources).startswith('schema:')
 assert validate(base.replace('"Q"','"Z"'),sources).startswith('schema:')
 assert validate(base.replace(':12',':NaN'),sources)=='syntax'
 assert validate(base.replace('"status":"supported",','"status":"supported","status":"supported",'),sources)=='schema: duplicate field policy'
 review='{"status":"needs_review","room":null,"capacity":null,"source_ids":[]}'
 assert validate(review,{})=='accepted' and validate(review,sources).startswith('semantic:')
 zero={k:dict(v,capacity=0) if v['kind']=='capacity' else dict(v) for k,v in sources.items()}
 assert validate(base.replace(':12',':0'),zero)=='accepted'
 checks.append({'week':'ai-3/8','verified':'published six-card validator, exact types, known IDs, null fallback, legitimate zero, duplicate-field policy, non-JSON constants and source consistency'})
(R/'reports/connected-python-checks.json').write_text(json.dumps({'checks':checks,'errors':[]},indent=2)+'\n');print(len(checks),'authored Python weeks verified in fresh execution namespaces.')
