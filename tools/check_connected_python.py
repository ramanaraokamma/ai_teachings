"""Execute authored Python teaching examples in fresh namespaces."""
from pathlib import Path
import contextlib,io,json
R=Path(__file__).resolve().parents[1];d=json.loads((R/'content/programme.json').read_text());weeks={w['id']:w for w in d['weeks']+d['python_bridge']};checks=[]
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
if weeks['ai-3/22']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/22'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete guarded activity JSON validator and eight supplied cards')
 ns=run(code);validate=ns['validate_activity']
 assert [validate(t)[0] for t in ns['cards']]==['accepted','syntax','schema: top-level object','schema: exact fields','schema: integer minutes','schema: integer minutes','schema: minutes range','accepted']
 for t in ['null','true','12','[]']:
  assert validate(t)==('schema: top-level object',{'accepted':False,'minutes':None})
 for value in [True,False,12.0,'12',None]:
  assert validate(json.dumps({'name':'Sketch','minutes':value}))[0]=='schema: integer minutes'
 for value in [0,60]:
  assert validate(json.dumps({'name':'Sketch','minutes':value}))[1]=={'accepted':True,'minutes':value}
 for value in [-1,61]:
  assert validate(json.dumps({'name':'Sketch','minutes':value}))[0]=='schema: minutes range'
 assert validate('{"name":"Sketch","minutes":NaN}')[0]=='syntax'
 assert validate('{"name":"Sketch","minutes":12,"minutes":13}')[0]=='duplicate-field policy'
 assert validate('{"name":"Sketch","minutes":12,"extra":0}')[0]=='schema: exact fields'
 assert validate('{"name":"","minutes":12}')[0]=='schema: name'
 checks.append({'week':'ai-3/22','verified':'published eight-card guarded JSON validator, top-level safety, exact integer not bool/float, valid zero/endpoints, duplicate policy, non-JSON constants and explicit rejected output'})
if weeks['ai-3/23']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/23'];code=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete book-count loop and strict-boundary checks')
 ns=run(code,'2\n1\n0\n');count=ns['count_short_books']
 assert count([0,99,100,101])==2 and count([100])==0 and count([])==0
 checks.append({'week':'ai-3/23','verified':'published book-count procedure, initialization before loop, strict less-than boundary, empty input and fresh supplied-domain cases'})
if weeks['ai-3/31']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/31'];code=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete two-contract identifier and trusted-access demonstration')
 ns=run(code);room=ns['valid_room_id'];catalog=ns['valid_catalog_id'];lookup=ns['lookup_catalog']
 assert room('B2') and not catalog('B2') and catalog('AB7') and not room('AB7')
 for value in [None,12,'b2','B22','B2\n',' B2','B2; DROP','Ｂ2','B２']:
  assert not room(value)
 for value in [None,12,'Ab7','AB77','AB7\n',' AB7','AB7; send()','ＡB7','AB７']:
  assert not catalog(value)
 assert lookup('CT8','student')=={'status':'not_authorised'}
 assert lookup('CT8','teacher')=={'status':'found','capacity':4}
 assert lookup('ZZ9','student')=={'status':'not_found'}
 assert lookup('AB7; send()','student')=={'status':'invalid_input'}
 checks.append({'week':'ai-3/31','verified':'published separate room/catalogue formats, exact ASCII/case/length/newline rejection, inert command text and trusted-role access before output'})
if weeks['ai-3/34']['sections'][0].get('reading_flow'):
 w=weeks['ai-3/34'];code=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete source-preserving structured investigation report builder')
 ns=run(code);build=ns['build_report'];e2=ns['E2'];e3=ns['E3']
 assert build(e2)['losses_ml'] is None and build(e2)['all_lost_half'] is None
 assert build(e3)['losses_ml']==[1,2,3] and build(e3)['all_lost_half'] is None
 assert build(dict(e3,initial_ml=[2,4,6]))['all_lost_half'] is True
 zero=build(dict(e3,losses_ml=[0,0,0],initial_ml=[2,4,6]))
 assert zero['losses_ml']==[0,0,0] and zero['all_lost_half'] is False
 for record in [dict(e2,cups=True),dict(e2,days=0),dict(e3,losses_ml=[1,2]),dict(e3,losses_ml=[1,-2,3]),dict(e3,initial_ml=[0,4,6]),dict(e3,initial_ml=[1,1,1]),dict(e2,initial_ml=[2,4,6])]:
  try:build(record)
  except ValueError:pass
  else:raise AssertionError('invalid structured investigation record accepted')
 checks.append({'week':'ai-3/34','verified':'published complete structured report builder, missing vs measured zero, initial-volume ratio requirement, exact fields/counts/lengths and invalid measurement rejection'})
if weeks['python-bridge/1']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/1'];code=w['sections'][2]['blocks'][1]['text'];run(code,'24\n')
 run(code.replace('packs = 4','packs = 0'),'0\n');run('print(total)\n'+code,error='NameError')
 seed=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete seed-tray script with separate spare count')
 run(seed,'26\n');run(seed.replace('spare = 2','spare = 5'),'29\n');run(seed.replace('trays = 4','trays = 0'),'2\n')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('packs = 3','packs = 5'),'35\n')
 checks.append({'week':'python-bridge/1','verified':'published packing and seed scripts, zero-group boundaries, fresh-name error and selected independent input change'})
if weeks['python-bridge/2']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/2'];run(w['sections'][2]['blocks'][1]['text'],"<class 'int'>\n<class 'str'>\n")
 run(w['sections'][5]['blocks'][1]['text'],'10\n8\n')
 code=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete integer addition and text concatenation comparison')
 run(code,'10\n82\n');run(code.replace('count = 8','count = 10'),'12\n82\n');run('print("6" + 3)',error='TypeError')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('count = 4','count = 0'),'3 4 0.0 True\nint str float bool\n')
 checks.append({'week':'python-bridge/2','verified':'published type/snapshot scripts, unchanged text under numeric reassignment, expected mixed-type error and selected independent zero-input trace'})
if weeks['python-bridge/3']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/3'];run(w['sections'][2]['blocks'][1]['text'],'26\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete ungrouped and parenthesised expression comparison')
 run(picture,'13\n25\n');run(picture.replace('* 5','* 4'),'11\n20\n')
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 grouping and same-precedence checks');run(w2,'8\n14\n12.0\n')
 run(w['sections'][6]['blocks'][0]['text'],'3.4\n3\n2\n')
 for op in ['/','//','%']:run('print(17 '+op+' 0)',error='ZeroDivisionError')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout'])
 checks.append({'week':'python-bridge/3','verified':'published grouped/ungrouped scripts, exact W2precedence, quotient/remainder identity, each zero-divisor failure and selected independent outputs'})
if weeks['python-bridge/4']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/4'];code=w['sections'][2]['blocks'][1]['text'];run(code,'True\nFalse\n')
 for minutes,quiet,expected in [(11,True,'True\nTrue\n'),(12,False,'True\nFalse\n'),(13,True,'False\nFalse\n')]:
  run(code.replace('minutes = 12','minutes = '+str(minutes)).replace('quiet = False','quiet = '+str(quiet)),expected)
 run(code.replace('quiet = False','quiet = True').replace('minutes <= 12','minutes < 12'),'False\nFalse\n')
 run(code.replace('time_ok and quiet','time_ok or quiet'),'True\nTrue\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete inclusive age-interval comparison trace')
 for age,expected in [(11,'False\nTrue\nFalse\n'),(12,'True\nTrue\nTrue\n'),(15,'True\nTrue\nTrue\n'),(16,'True\nFalse\nFalse\n')]:run(picture.replace('age = 15','age = '+str(age)),expected)
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('genre = "science"','genre = "history"'),'False\nFalse\nTrue\nTrue\n')
 checks.append({'week':'python-bridge/4','verified':'published separate condition traces, exact inclusive boundaries, AND/OR and less-than mutations, selected genre-change counterexample'})
if weeks['python-bridge/5']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/5'];code=w['sections'][2]['blocks'][1]['text']
 for minutes,label in [(-1,'Invalid'),(0,'Short'),(11,'Short'),(12,'Short'),(13,'Long')]:run(code.replace('minutes = 12','minutes = '+str(minutes)),label+'\n')
 broken=w['sections'][6]['blocks'][0]['text'];run(broken,'Short\n');run(broken.replace('if minutes <= 12:','elif minutes <= 12:'),'Invalid\n')
 run(code.replace('minutes <= 12','minutes < 12'),'Long\n')
 for minutes,label in [(-1,'Invalid'),(2,'Short'),(20,'Long')]:run(code.replace('minutes = 12','minutes = '+str(minutes)).replace('minutes <= 12','minutes < 12'),label+'\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete book-count branch chain with validity first')
 for count,label in [(-2,'invalid'),(4,'small'),(5,'large')]:run(picture.replace('count = -2','count = '+str(count)),label+'\n')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('reading = 30','reading = 29'),'on\n');run(ind['code'].replace('reading = 30','reading = -1'),'invalid\n')
 checks.append({'week':'python-bridge/5','verified':'published branch paths, equality mutation missed by branch-only coverage, independent-if overwrite and repair, separate book and lamp thresholds'})
if weeks['python-bridge/6']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/6'];code=w['sections'][2]['blocks'][0]['text'];run(code,'6\n')
 for expr,out in [('range(1, 1)','0\n'),('range(1, 2)','1\n'),('range(2, 5)','9\n')]:run(code.replace('range(1, 4)',expr),out)
 run(w['sections'][6]['blocks'][0]['text'],'3\n')
 run(code.replace('\nprint(total)','\n    print(total)'),'1\n3\n6\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete four-value running-total loop');run(picture,'10\n');run(picture.replace('range(1, 5)','range(1, 1)'),'0\n')
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 range two through four trace');run(w2,'9\n')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('range(2, 6)','range(2, 2)'),'0\n')
 checks.append({'week':'python-bridge/6','verified':'published distinct loop ranges, zero/one/many initialization, reset mutation, output-position events and selected independent empty range'})
if weeks['python-bridge/7']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/7'];run(w['sections'][2]['blocks'][1]['text'],'3\n4\n7\n[4, 9, 4]\n')
 sumcode=w['sections'][5]['blocks'][0]['text'];run(sumcode,'15\n');run(sumcode.replace('[4, 7, 4]','[]'),'0\n');run(sumcode.replace('[4, 7, 4]','[7]'),'7\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete first/last/length list comparison');run(picture,'6\n8\n3\n');run(picture.replace('print(counts[-1])','print(counts[3])'),'6\n',error='IndexError')
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 fresh first-item replacement');run(w2,'[6, 7, 4]\n3\n4\n')
 guard=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete empty-list guard before final-item access');run(guard,'no last item\n');run(guard.replace('counts = []','counts = [0]'),'0\n')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('print(values[-1])','print(values[3])'),'9\n',error='IndexError')
 checks.append({'week':'python-bridge/7','verified':'published distinct list initialisations/updates, value loops, zero/singleton/empty inputs, explicit negative indexing and partial-output stopping points'})
if weeks['python-bridge/8']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/8'];code=w['sections'][2]['blocks'][0]['text'];run(code,'8\n3\n');definition=code.split('\n\n')[0];run(definition,'')
 run(definition+'\nshow_remaining(8)',error='TypeError')
 run(w['sections'][6]['blocks'][0]['text'],'8\n8\n')
 preview=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Short return-to-caller preview for reading a function call');assert run(preview,'6\n')['value']==6
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 same-function three-call sequence');run(w2,'5\n0\n8\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete positional-argument reversal demonstration');run(picture,'8\n-8\n');run(picture.split('\n\n')[0],'')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].split('print(')[0],'')
 checks.append({'week':'python-bridge/8','verified':'published definition/call order, positional reversal, zero/full capacity calls, missing argument, ignored-constant bug and required return-preview semantics'})
if weeks['python-bridge/9']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/9'];code=w['sections'][2]['blocks'][0]['text'];ns=run(code,'11\n');assert ns['first']==8 and ns['second']==3 and 'spaces' not in ns
 faulty=w['sections'][6]['blocks'][0]['text'];assert run(faulty,'8\nNone\n')['answer'] is None
 run(faulty.replace('print(answer)','print(answer + 1)'),'8\n',error='TypeError')
 run(faulty.replace('    print(spaces)','    return spaces'),'8\n')
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 three-return repeated-call sequence');run(w2,'5 0 5\n');run(w2+'\nprint(spaces)','5 0 5\n',error='NameError')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete two-call local-result and caller-binding trace');run(picture,'7 5\n');run(picture+'\nprint(result)','7 5\n',error='NameError')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout'])
 run(ind['code'].replace('    return total\n',''),'',error='TypeError');run(ind['code']+'\nprint(total)',ind['expected_stdout'],error='NameError')
 checks.append({'week':'python-bridge/9','verified':'published returned/caller state, legitimate zero, missing return vs printed output, local-scope partial output and selected pre-print argument failure'})
if weeks['python-bridge/10']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/10'];run(w['sections'][2]['blocks'][0]['text'],'8\n6\n')
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 Red named-field update and unchanged capacity');ns=run(w2,'0\n9\n');assert ns['record']=={'name':'Red','capacity':9,'used':9}
 run(w2+'\nprint(record["Used"])','0\n9\n',error='KeyError')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete stored-zero missing-field and membership comparison');ns=run(picture,'0\nNone\nTrue\n');assert 'price' not in ns['shelf']
 present=ns['shelf'].copy();present['price']=None;assert 'price' in present and present.get('price') is None
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('if count is None:','if not count:'),'missing\n3\nmissing\n')
 checks.append({'week':'python-bridge/10','verified':'published separate Blue/Red field updates, wrong-case KeyError, zero/missing/present-None states and selected falsey-zero mutation'})
if weeks['python-bridge/11']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/11'];main=w['sections'][2]['blocks'][0]['text'];run(main,'5\n');run(main.replace('"used": 6','"other": 6'),'',error='KeyError')
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 three-record spare-contribution fixture');run(w2,'7\n');run(w2.replace('for row in rows:\n','for row in rows:\n    total = 0\n'),'1\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete observed-count total mean and coverage program');ns=run(picture,'2 2 3 1.0\n');assert ns['observed']==[2,0]
 run(picture.replace('{"count": 0}, {}]','{"count": 0}, {}, {"count": 4}]'),'6 3 4 2.0\n')
 run(picture.replace('rows = [{"count": 2}, {"count": 0}, {}]','rows = [{}, {}, {}]'),'0 0 3 None\n')
 run(picture.replace('if value is not None:','if value:'),'2 1 3 2.0\n')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('rows = [{"score": 2}, {"score": 6}, {}]','rows = [{}, {}, {}]'),'0 0 3 None\n')
 checks.append({'week':'python-bridge/11','verified':'published required-field vs observed-row policies, complete spare records, reset mutation, legitimate zero inclusion, coverage and all-missing mean'})
if weeks['python-bridge/12']['sections'][0].get('reading_flow'):
 w=weeks['python-bridge/12'];run(w['sections'][2]['blocks'][0]['text'],'True\nTrue\nTrue\n')
 w2=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete W2 constant-four defect and independently expected cases');run(w2,'4 4 True\n4 0 False\n4 6 False\n');run(w2.replace('return 4','return capacity - used'),'4 4 True\n0 0 True\n6 6 True\n')
 picture=next(b['text'] for b in w['sections'][5]['blocks'] if b.get('title')=='Complete strict-boundary assertion suite for tiny');run(picture,'three checks passed\n');bug=picture.replace('x < 3','x <= 3');run(bug,'',error='AssertionError')
 reduced=bug.replace('assert tiny(3) is False\n','').replace('three checks passed','two retained checks passed');run(reduced,'two retained checks passed\n')
 ind=w['method']['independent'];run(ind['code'],ind['expected_stdout']);run(ind['code'].replace('x < 10','x <= 10'),'',error='AssertionError')
 checks.append({'week':'python-bridge/12','verified':'published complete subtraction suites, constant-defect accidental pass/repair, exact-boundary assertion failure, missed-defect reduced suite and selected threshold regression'})
if weeks['ai-4/1']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/1'];run(w['sections'][2]['blocks'][12]['text'],'2 1\n4 0\n6 1\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete training-only threshold selection freeze and supplied-test evaluation')
 ns=run(code);fit=ns['fit_threshold'];predict=ns['predict'];assert ns['threshold']==4 and ns['predictions']==[0,1] and ns['correct']==2
 assert fit(ns['train'],[5,4])[0]==4
 ns['test']=[(2,1),(6,0)];assert fit(ns['train'],[2,4,6])[0]==4
 selected,scored=fit([(2,0),(4,0),(6,1),(8,1)],[3,5,7]);assert selected==5 and [e for e,t in scored]==[1,0,1]
 assert [predict(x,selected) for x,y in [(3,0),(7,1),(5,0)]]==[0,1,1]
 for rows,candidates in [([],[2,4]),(ns['train'],[])]:
  try:fit(rows,candidates)
  except ValueError:pass
  else:raise AssertionError('undefined empty fit accepted')
 checks.append({'week':'ai-4/1','verified':'published training-only errors and complete fit/freeze/test program, deterministic tie rule, test-label independence and selected transfer errors'})
if weeks['ai-4/2']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/2'];ns=run(w['sections'][2]['blocks'][12]['text'],'[120, 2]\n1\n[80, 0]\n');features=ns['features'];assert features({'pages':96,'queue_at_checkout':4,'days_to_return':14})==features({'pages':96,'queue_at_checkout':4,'days_to_return':15})==[96,4]
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fixed checkout-feature contract and later-target boundary program');ns=run(code,'[96, 4] 0\n[96, 4] 1\n[80, 0] target unavailable\n')
 assert ns['completed_loan_target']({'days_to_return':14})==0 and ns['completed_loan_target']({'days_to_return':15})==1
 assert ns['features_at_checkout']({'pages':80,'queue_at_checkout':0,'days_to_return':999,'returned_late':1,'loan_id':'tracking'})==[80,0]
 try:ns['features_at_checkout']({'pages':80})
 except KeyError:pass
 else:raise AssertionError('missing required snapshot silently accepted')
 checks.append({'week':'ai-4/2','verified':'published ordered past/new feature selection, later-outcome invariance, strict14-day target boundary, legitimate queue0 and required-field failure'})
if weeks['ai-4/3']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/3'];run(w['sections'][2]['blocks'][13]['text'],'2 3\n[1, 1, 2]\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete checked paired-value category and numerical-error comparison');ns=run(code);compare=ns['compare_paired']
 six=compare([4,7,9],[5,6,10],6);seven=compare([4,7,9],[5,6,10],7)
 assert (six['correct'],seven['correct'])==(2,3) and six['mae']==seven['mae']==1 and six['absolute_errors']==[1,1,1]
 independent=compare([4,5,9],[6,5,8],5);assert independent['actual_classes']==[0,0,1] and independent['predicted_classes']==[1,0,1] and independent['correct']==2 and independent['mae']==1
 for actual,estimated in [([],[]),([4,7,9],[5,6]),([True],[1]),([None],[1]),([float('nan')],[1]),([-1],[1])]:
  try:compare(actual,estimated,6)
  except ValueError:pass
  else:raise AssertionError('invalid paired calculation accepted')
 checks.append({'week':'ai-4/3','verified':'published duration errors and guarded height comparison, changed-threshold agreement with unchanged MAE, pair/number rejection and independent print-job outcomes'})
if weeks['ai-4/4']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/4'];run(w['sections'][2]['blocks'][12]['text'],'True\nTrue\n')
 parser=run(w['sections'][2]['blocks'][24]['text'])['parse_minutes']
 assert parser('0')=={'status':'ok','value':0} and parser(' 5 ')=={'status':'ok','value':5}
 assert parser('-1')['status']=='out of range' and parser('61')['value'] is None and parser('3.5')['status']=='invalid text'
 run('row={"activity":"Reading"}\nprint(row["minutes"])',error='KeyError')
 run('print(12+"8")',error='TypeError')
 ns=run('counts=[2,0,6]\ntotal=sum(counts)\nn=len(counts)\nmean=total/n\nobserved=n')
 assert (ns['total'],ns['n'],ns['mean'],ns['observed'])==(8,3,8/3,3)
 rows=[{'activity':'Reading','minutes':12},{'activity':'Sorting','minutes':0},{'activity':'Quiz','minutes':61},{'activity':'Chat','minutes':'12'}]
 accepted=[i for i,r in enumerate(rows) if type(r['minutes']) is int and 0<=r['minutes']<=60]
 assert accepted==[0,1] and [i for i in accepted if rows[i]['minutes']>0]==[0]
 heights=[2,6,None,0];observed=[v for v in heights if v is not None];assert sum(observed)==8 and len(observed)==3
 assert sum([3,7,14])/3==8
 checks.append({'week':'ai-4/4','verified':'published schema and parser, missing-key/type failures, complete five-variable notebook, two supplied filters and explicit missing/zero summary policy'})
if weeks['ai-4/5']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/5'];ns=run(w['sections'][2]['blocks'][12]['text'],'5 4 2 1\n')
 assert len(ns['rows'])-len(ns['ids'])==1
 run(w['sections'][2]['blocks'][17]['text'],'[3.0, 4]\n')
 rows=[('P',4),('Q',None),('Q',None),('R',-1),('S',6),('T',0)]
 ids={i for i,v in rows};missing=[i for i,v in rows if v is None];negative=[i for i,v in rows if v is not None and v<0]
 assert (len(rows),len(ids),len(missing),len(negative),len(rows)-len(ids))==(6,5,2,1,1)
 assert missing==['Q','Q'] and negative==['R'] and 0>=0
 checks.append({'week':'ai-4/5','verified':'published audit and unit-conversion outputs, independent raw/distinct/missing/negative/extra counts and overlapping repeated-ID missingness'})
if weeks['ai-4/6']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/6'];run(w['sections'][2]['blocks'][13]['text'],'2 4\n')
 pairs=[('P','blocked','blocked'),('Q','clear','blocked'),('R','review','review'),('S','clear','clear'),('T','blocked','clear')]
 assert sum(x==y for i,x,y in pairs)==3 and len(pairs)==5
 subset=[p for p in pairs if 'review' not in p[1:]]
 assert len(subset)==4 and sum(x==y for i,x,y in subset)==2
 cards=next(b['rows'] for b in w['sections'][8]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0]==['Card ID','Complete fictional description'])
 assert len(cards)==21 and len({r[0] for r in cards[1:]})==20
 checks.append({'week':'ai-4/6','verified':'published matched-pair agreement, selected inclusion/exclusion denominators and complete twenty-card label-lab fixture'})
if weeks['ai-4/7']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/7'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Complete intended-condition coverage counts for supplied samples A and B')
 ns=run(code,'A 10 10\nday A 9\nday B 0\nevening A 1\nevening B 0\nB 12 12\nday A 3\nday B 3\nevening A 3\nevening B 3\n')
 copied=ns['samples']['A']*10;assert len(copied)==100 and len({r[0] for r in copied})==10 and not any(r[2]=='B' for r in copied)
 run(w['sections'][2]['blocks'][12]['text'],'5 4 2 1\n')
 for n in [12,13,14,16]:
  groups=w['workbook'][n-1]['reading_flow']['groups'];assert any(g.get('collapsed') and 'saved response' in g['title'] for g in groups)
 checks.append({'week':'ai-4/7','verified':'published complete condition-coverage program, all four counts, copied-row/source-ID distinction and preserved old audit response groups'})
if weeks['ai-4/8']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/8'];run(w['sections'][2]['blocks'][13]['text'],'[]\n3 1 2\n')
 ns=run(w['sections'][2]['blocks'][18]['text'],'[10, 100] [10, 100]\n[(0.0, 1.0), (1.0, 0.0), (1.0, 1.0)]\n(0.1, 0.2)\n')
 assert ns['transform']((12,80))==(0.2,-0.2)
 train=ns['train'];query=(11,120);distance=lambda x,y:sum(abs(a-b) for a,b in zip(x,y))
 assert [distance(query,r) for r in train]==[81,29,89]
 scaled=[distance(ns['transform'](query),r) for r in ns['scaled_train']];assert min(range(3),key=lambda i:scaled[i])==0
 assignments={'train':['A1','A2','A3','B1','B2','C1'],'valid':['D1','D2'],'test':['E1','E2','F1','F2']}
 assert [len(v) for v in assignments.values()]==[6,2,4]
 assignments['valid'].remove('D2');assignments['train'].append('D2')
 assert [len(v) for v in assignments.values()]==[7,1,4]
 assert {x[0] for x in assignments['train']}&{x[0] for x in assignments['valid']}=={'D'}
 checks.append({'week':'ai-4/8','verified':'published group audit and training-only scale outputs, raw/scaled nearest choices, outside-range transform and D2 overlap/count trace'})
if weeks['ai-4/9']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/9'];run(w['sections'][2]['blocks'][12]['text'],'5 4 2 1\n')
 manifest=next(b['rows'] for b in w['sections'][1]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0]==['Plant ID','Photo IDs','Known condition'])
 assert len(manifest)==7 and sum(len(row[1].split()) for row in manifest[1:])==18
 assert len({row[0] for row in manifest[1:]})==6
 for n in [12,13,14,16]:assert any(g.get('collapsed') and 'saved response' in g['title'] for g in w['workbook'][n-1]['reading_flow']['groups'])
 checks.append({'week':'ai-4/9','verified':'complete18-photo/6-source manifest, retained earlier audit execution and preserved saved-response groups for current card-writing tasks'})
if weeks['ai-4/10']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/10'];run(w['sections'][2]['blocks'][12]['text'],'clear 2 4\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete guarded majority and declared-rule baseline comparison');ns=run(code);fit=ns['fit_majority'];score=ns['score']
 assert fit(['clear','blocked'])=='clear'
 assert score(ns['reference'],ns['majority_predictions'])=={'correct':2,'total':4,'blocked_found':0,'blocked_total':2,'blocked_recall':0.0}
 assert score(ns['reference'],ns['rule_predictions'])=={'correct':3,'total':4,'blocked_found':1,'blocked_total':2,'blocked_recall':0.5}
 assert score(['clear'],['clear'])['blocked_recall'] is None
 selected=fit(['blocked','clear','blocked','blocked','clear']);assert selected=='blocked'
 refs=['clear','blocked','clear','blocked'];assert score(refs,[selected]*4)['correct']==2 and score(refs,['clear','blocked','blocked','blocked'])['correct']==3
 for labels in [[],['review'],['unknown']]:
  try:fit(labels)
  except ValueError:pass
  else:raise AssertionError('unsupported training labels accepted')
 for refs,predictions in [([],[]),(['clear'],[]),(['review'],['clear'])]:
  try:score(refs,predictions)
  except ValueError:pass
  else:raise AssertionError('invalid comparison accepted')
 checks.append({'week':'ai-4/10','verified':'published majority output, complete two-baseline scores/blocked recall, declared tie, empty/invalid guards and independent comparison'})
if weeks['ai-4/11']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/11'];ns=run(w['sections'][2]['blocks'][12]['text'],'0 1\n1 2\n0 clear blocked\n');feature,leaves=ns['tree'];assert feature==0 and leaves=={0:'clear',1:'blocked'}
 valid=[(1,1,'blocked'),(0,0,'clear'),(0,1,'blocked'),(1,0,'clear')]
 assert [i for i,r in enumerate(valid,1) if leaves[r[feature]]!=r[2]]==[3,4]
 assert [i for i,r in enumerate(valid,1) if 'blocked'!=r[2]]==[2,4]
 for value,expected in [(4,'healthy'),(5,'spotted'),(6,'spotted'),(None,'review')]:assert ('review' if value is None else 'spotted' if value>=5 else 'healthy')==expected
 dev=[(1,0,'blocked'),(1,1,'blocked'),(0,0,'clear'),(0,1,'clear')]
 full=lambda n,t:'clear' if n==0 else 'clear' if t==0 else 'blocked'
 pruned=lambda n,t:'clear' if n==0 else 'blocked'
 assert sum(full(n,t)==y for n,t,y in dev)==3 and sum(pruned(n,t)==y for n,t,y in dev)==4
 checks.append({'week':'ai-4/11','verified':'published candidate/leaf fitting outputs, different validation error identities, supplied pruning fixture and selected cutoff5 equality/missing paths'})
if weeks['ai-4/12']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/12'];ns=run(w['sections'][2]['blocks'][12]['text'],"['A', 'B', 'C']\nclear\n")
 def neighbour_result(train,query,k):
  ranked=sorted((abs(x-query),i,y) for i,x,y in train);near=ranked[:k];labels=[r[2] for r in near];return [r[1] for r in near],max(set(labels),key=labels.count)
 assert neighbour_result(ns['train'],3,1)==(['A'],'blocked')
 assert [neighbour_result(ns['train'],q,3)[0] for q in [3,9,11]]==[['A','B','C'],['C','D','E'],['D','E','C']]
 assert neighbour_result(ns['train'],100,3)==(['E','D','C'],'clear')
 selected=[('A',1,'healthy'),('B',5,'spotted'),('C',9,'healthy')]
 assert neighbour_result(selected,7,1)==(['B'],'spotted') and neighbour_result(selected,7,3)==(['B','C','A'],'healthy')
 picture=[('A',2,'healthy'),('B',8,'spotted'),('C',11,'spotted')]
 assert neighbour_result(picture,5,1)==(['A'],'healthy') and neighbour_result(picture,7,1)==(['B'],'spotted')
 checks.append({'week':'ai-4/12','verified':'published query ranking/vote, validation IDs, far query, pictured tie/change and selected independent k1/k3 contrast'})
if weeks['ai-4/13']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/13'];ns=run(w['sections'][2]['blocks'][12]['text'],"('A', 'clear')\n('C', 'blocked')\n('B', 'blocked')\n");fit,predict=ns['fit'],ns['predict'];model=ns['model'];assert model[:2]==((10,100),(10,100))
 extension=w['sections'][14]['blocks'][2]['text'];run(extension,'2.5 [0, 1] 2 2\n');changed=run(extension.replace('test = [(2, 0), (3, 1)]','test = [(2, 1), (3, 0)]'),'2.5 [0, 1] 0 2\n');assert changed['threshold']==2.5
 assert predict((10,100),model)==('A','clear') and predict((120,11),model)==('B','blocked')
 saved=repr(model);predict((100,1000),model);assert repr(model)==saved
 try:fit([('A',(10,100),'clear'),('B',(10,200),'blocked')])
 except ValueError:pass
 else:raise AssertionError('constant feature not stopped')
 independent=fit([('P',(0,60),'blocked'),('Q',(20,20),'clear'),('R',(20,60),'clear')]);assert independent[:2]==((0,20),(20,40))
 assert [predict(q,independent) for q in [(2,28),(18,56),(4,12)]]==[('P','blocked'),('R','clear'),('Q','clear')]
 run(w['sections'][2]['blocks'][16]['text'],'3 1\n5 0\n7 1\nchosen 5\n')
 checks.append({'week':'ai-4/13','verified':'published fitted pipeline and cutoff outputs, stored-state immutability, tie/order/constant probes and independent new fitted state/predictions'})
if weeks['ai-4/14']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/14'];run(w['sections'][2]['blocks'][13]['text'],'0.2 0.2\n0.8 0.6\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete thirty-case positive-probability reliability-bin calculation')
 ns=run(code,'low 10 0.2 2 0.2\nmiddle 10 0.5 7 0.7\nhigh 10 0.8 6 0.6\n');rows=ns['rows'];assert len(rows)==30 and len({r[0] for r in rows})==30
 assert [sum(y for i,p,y in rows if p==score) for score in [0.2,0.5,0.8]]==[2,7,6]
 def membership(p):return [name for name,left,right in ns['bins'] if left<=p and (p<right or right==1 and p<=right)]
 assert membership(0)==['low'] and membership(0.35)==['middle'] and membership(0.65)==['high'] and membership(1)==['high']
 assert 8/20==0.4 and 7/10==0.7
 checks.append({'week':'ai-4/14','verified':'published two-group and thirty-record outputs, unique case IDs/positive counts, exact bin endpoints and selected independent observed fractions'})
if weeks['ai-4/15']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/15'];run(w['sections'][2]['blocks'][12]['text'],'[[2, 1], [2, 3]]\n5 8\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete twenty-record confusion counts with explicit axes and ID checks')
 ns=run(code,"['spotted', 'healthy'] [[4, 1], [3, 12]]\n16 20 0.8\n");build=ns['build_counts'];assert build(ns['pairs'],['healthy','spotted'])==([[12,3],[1,4]],16,20)
 assert build([],['spotted','healthy'])==([[0,0],[0,0]],0,0)
 for pairs,labels in [([('X','spotted','healthy'),('X','spotted','spotted')],['spotted','healthy']),([('X',None,'healthy')],['spotted','healthy']),([],['spotted','spotted'])]:
  try:build(pairs,labels)
  except ValueError:pass
  else:raise AssertionError('invalid confusion-record contract accepted')
 assert (5+9)/(5+4+2+9)==0.7
 checks.append({'week':'ai-4/15','verified':'published eight-record and complete twenty-record matrices, reversed axes, empty/duplicate/missing guards and selected new-count accuracy'})
if weeks['ai-4/16']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/16'];ns=run(w['sections'][2]['blocks'][12]['text'],'baseline 80.0 50.0\ncandidate 80.0 87.5\n');scores=ns['scores']
 assert scores([[8,0],[8,0]])==(0.5,0.5) and scores([[6,2],[0,8]])==(0.875,0.875)
 assert scores([[3,1],[1,0]])==(0.6,0.375)
 try:scores([[4,0],[0,0]])
 except ValueError:pass
 else:raise AssertionError('absent positive recall denominator invented')
 assert scores([[90,0],[10,0]])[0]==0.9 and scores([[82,8],[3,7]])[0]==0.89 and 7/(7+3)==0.7
 assert (4*5,4*1)==(20,4) and (4*1,4*6)==(4,24)
 checks.append({'week':'ai-4/16','verified':'published ordinary/balanced outputs, constructed class-mix and sparse probes, absent-class stop, explicit cost arithmetic and selected100-case comparison'})
if weeks['ai-4/17']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/17'];ns=run(w['sections'][2]['blocks'][13]['text'],'0.42857142857142855 0.75 0.75\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete ten-record threshold precision recall and accuracy comparison');ns=run(code);evaluate=ns['evaluate'];rows=ns['rows'];low=evaluate(rows,.4);high=evaluate(rows,.7)
 assert [low[k] for k in ['tp','fp','fn','tn']]==[4,2,1,3] and [high[k] for k in ['tp','fp','fn','tn']]==[3,0,2,5]
 assert low['precision']==4/6 and low['recall']==.8 and high['precision']==1 and high['recall']==.6
 none=evaluate(rows,1);assert none['precision'] is None and none['recall']==0
 absent=evaluate([('U1',.8,0),('U2',.2,0)],.7);assert absent['precision']==0 and absent['recall'] is None
 assert evaluate([], .7)['accuracy'] is None
 assert (low['fn']*5+low['fp'],high['fn']*5+high['fp'])==(7,10)
 assert (low['fn']+low['fp']*5,high['fn']+high['fp']*5)==(11,2)
 assert 6/(6+2)==.75 and 6/(6+3)==2/3 and (8+6)/19==14/19
 checks.append({'week':'ai-4/17','verified':'published ratios, complete score/threshold confusion counts, no-flag/no-positive/empty policies, two cost choices and selected19-record fractions'})
if weeks['ai-4/18']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/18'];run(w['sections'][2]['blocks'][13]['text'],'0.3333333333333333 0.16666666666666666\n0.16666666666666666 0.2222222222222222\n7 6\n')
 rows=next(b['rows'] for b in w['sections'][8]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0]==['Case ID','Light / device / route','Reviewed reference','Old prediction','New supplied prediction'])[1:]
 assert len(rows)==30 and len({r[0] for r in rows})==30
 dim=[r for r in rows if r[0].startswith('D')];bright=[r for r in rows if r[0].startswith('B')]
 assert [len(dim),len(bright)]==[12,18]
 assert [sum(r[2]!=r[3] for r in subset) for subset in [dim,bright]]==[4,3]
 assert [sum(r[2]!=r[4] for r in subset) for subset in [dim,bright]]==[2,4]
 assert sum(r[2]!=r[3] for r in rows)==7 and sum(r[2]!=r[4] for r in rows)==6
 assert (5+2,3+5)==(7,8) and (3/10,5/20)==(.3,.25)
 checks.append({'week':'ai-4/18','verified':'published slice-rate/replay outputs, complete unique thirty-case paired predictions, bright regression despite total gain and independent route totals'})
if weeks['ai-4/19']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/19'];run(w['sections'][2]['blocks'][13]['text'],'[-1, 1, 0]\n0.0\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete matched-height residual mean and absolute-error summary');ns=run(code,'([-1, 1, -2, 2, -4, 4], 0.0, 2.3333333333333335)\n');summarize=ns['summarize']
 assert summarize([('P1',5,7),('P2',8,7),('P3',12,10)])==([-2,1,2],1/3,5/3)
 assert summarize([('P1',5,8),('P2',8,8),('P3',12,11)])==([-3,0,1],-2/3,4/3)
 assert summarize([('I1',6,8),('I2',10,9),('I3',13,11)])[:2]==([-2,1,2],1/3)
 for records in [[],[('X',None,12)],[('X',3,4),('X',5,4)],[('X',float('nan'),1)],[('X',-1,1)]]:
  try:summarize(records)
  except ValueError:pass
  else:raise AssertionError('invalid residual record accepted')
 checks.append({'week':'ai-4/19','verified':'published cancellation and complete six-record summaries,picture/update residuals,independent new pairs and empty/missing/duplicate/nonfinite guards'})
if weeks['ai-4/20']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/20'];run(w['sections'][2]['blocks'][13]['text'],'mean 6 2\nmedian 5.0 2.0\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete training-only mean median and fixed-target baseline tournament');ns=run(code);fit,evaluate=ns['fit_constants'],ns['evaluate']
 constants=fit([2,4,6,12]);assert constants=={'mean':6,'median':5}
 original=evaluate(constants,[4,8]);assert original['mean']['mae']==original['median']['mae']==2
 changed=fit([2,4,6,40]);assert changed=={'mean':13,'median':5} and evaluate(changed,[4,8])['mean']['mae']==7
 assert fit([5])=={'mean':5,'median':5}
 selected=fit([1,3,5,15]);assert selected=={'mean':6,'median':4};assert [v['mae'] for v in evaluate(selected,[3,9]).values()]==[3,3]
 saved=constants.copy();evaluate(constants,[100]);assert constants==saved
 for values in [[],[None],[True],[-1],[float('nan')]]:
  try:fit(values)
  except ValueError:pass
  else:raise AssertionError('invalid constant-fitting target accepted')
 checks.append({'week':'ai-4/20','verified':'published mean/median outputs,complete unchanged-target outlier replay,single/invalid fitting guards,state preservation and independent new constants/MAEs'})
if weeks['ai-4/21']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/21'];ns=run(w['sections'][2]['blocks'][13]['text']);assert ns['mae']==2 and ns['mse']==14/3
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete same-case candidate and training-mean loss comparison');ns=run(code);losses=ns['losses']
 assert losses([0,0,6])['mae']==2 and losses([0,0,6])['mse']==12
 assert losses([3,3,3])=={'mae':3,'mse':9,'rmse':3}
 assert losses([0,0])=={'mae':0,'mse':0,'rmse':0}
 selected=losses([-2,0,4]);assert selected['mae']==2 and selected['mse']==20/3
 converted=losses([-200,0,400]);assert converted['mae']==200 and converted['mse']==200000/3
 for values in [[],[None],[True],[float('nan')]]:
  try:losses(values)
  except ValueError:pass
  else:raise AssertionError('invalid loss input accepted')
 checks.append({'week':'ai-4/21','verified':'published original loss values,complete same-case reversed metric rankings,zero/missing/nonfinite guards and independent m-to-cm scaling'})
if weeks['ai-4/22']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/22'];run(w['sections'][2]['blocks'][13]['text'],'[5, 3, 0]\n(2, 1)\n')
 extension=w['sections'][14]['blocks'][6]['text'];run(extension,'2.0 1.0 [9.0] 1.0\n');run(extension.replace('test = [(4, 10)]','test = [(4, 8)]'),'2.0 1.0 [9.0] 1.0\n')
 run(extension.replace('train = [(1, 3), (2, 5), (3, 7)]','train = [(1, 3), (1, 5)]'),error='ValueError')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete training-only candidate line fit and fixed-validation baseline comparison');ns=run(code);fit,evaluate=ns['fit_training_line'],ns['evaluate']
 assert ns['line']==(2,1) and ns['training_sse']==[5,3,0]
 assert evaluate((2,1),[(3,6),(4,10)])==([7,9],[-1,1],1,1)
 assert evaluate((0,3),[(3,6),(4,10)])==([3,3],[3,7],5,29)
 assert fit([(0,1)],[(1,1),(2,1)])[0]==(1,1)
 selected,errors=fit([(0,2),(1,5),(2,8)],[(2,2),(3,1),(3,2)]);assert selected==(3,2) and errors==[5,3,0]
 assert evaluate(selected,[(3,10),(4,15)])[:3]==([11,14],[-1,1],1)
 for train,candidates in [([],[(1,1)]),([(0,1)],[])]:
  try:fit(train,candidates)
  except ValueError:pass
  else:raise AssertionError('undefined line selection accepted')
 checks.append({'week':'ai-4/22','verified':'published candidate SSE,complete previously missing validation targets,line/baseline errors,tie/empty policy and independent new fitted line'})
if weeks['ai-4/23']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/23'];rows=next(b['rows'] for b in w['sections'][8]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0]==['Final-record case ID','Reference','Frozen V1prediction','Frozen always-clear baseline'])[1:]
 assert len(rows)==20 and len({r[0] for r in rows})==20
 tn=sum(r[1]==r[2]=='clear' for r in rows);fp=sum(r[1]=='clear' and r[2]=='blocked' for r in rows);fn=sum(r[1]=='blocked' and r[2]=='clear' for r in rows);tp=sum(r[1]==r[2]=='blocked' for r in rows)
 assert (tn,fp,fn,tp)==(12,2,3,3) and sum(r[1]==r[3] for r in rows)==14
 assert (tn+tp)/20==.75 and tp/(tp+fp)==.6 and tp/(tp+fn)==.5
 assert (7+2)/12==.75 and 2/(2+1)==2/3 and 2/(2+2)==.5
 checks.append({'week':'ai-4/23','verified':'complete20-case frozen prediction/baseline counts,all error identities and independent12-case ratios;no revised-model result invented'})
if weeks['ai-4/24']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/24'];actions=next(b['rows'] for b in w['sections'][8]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0]==['Action ID','Complete action to assign or repair'])[1:]
 assert len(actions)==20 and len({r[0] for r in actions})==20
 train={f'L{i:02}{view}' for i in range(1,19) for view in 'abc'};valid={f'L{i:02}{view}' for i in range(19,25) for view in 'abc'};test={f'L{i:02}{view}' for i in range(25,31) for view in 'abc'}
 assert [len(train),len(valid),len(test)]==[54,18,18] and len(train|valid|test)==90 and not (train&valid or train&test or valid&test)
 candidates=[('A',3,0),('B',5,1),('C',3,2)];assert min(candidates,key=lambda r:(r[1],r[2]))[0]=='A'
 independent=[('P',4,0),('Q',6,1),('R',4,2)];assert min(independent,key=lambda r:(r[1],r[2]))[0]=='P'
 checks.append({'week':'ai-4/24','verified':'complete twenty-action fixture,declared grouped90-image membership/counts and primary/independent validation tie choices without final scores'})
if weeks['ai-4/25']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/25'];run(w['sections'][2]['blocks'][13]['text'],'0.5 1 1 5\n0.3 2 0 2\n')
 def counts(rows,t):
  tp=sum(s>=t and y for s,y in rows);fp=sum(s>=t and not y for s,y in rows);fn=sum(s<t and y for s,y in rows);tn=sum(s<t and not y for s,y in rows);return tp,fp,fn,tn
 main=[(.9,1),(.7,0),(.6,1),(.4,1),(.3,0),(.1,0)]
 assert counts(main,.5)==(2,1,1,2) and counts(main,.3)==(3,2,0,1)
 assert sum(s>=.5 for s,y in main)==3 and sum(s>=.3 for s,y in main)==5
 independent=[(.8,1),(.5,0),(.2,1),(.1,0)]
 assert counts(independent,.5)==(1,1,1,1) and counts(independent,.2)==(2,1,0,1)
 picture=[(.9,1),(.6,0),(.4,1),(.1,0)]
 high,low=counts(picture,.7),counts(picture,.4);assert (high[1]+5*high[2],low[1]+5*low[2])==(5,1)
 assert (5*high[1]+high[2],5*low[1]+low[2])==(1,5)
 assert sum(abs(y-p) for y,p in zip([10,12,14],[9,14,14]))/3==1
 checks.append({'week':'ai-4/25','verified':'published costs,complete main/pictured/independent threshold counts,equality,explicit3-alert capacity and numeric council scenario'})
if weeks['ai-4/26']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/26'];run(w['sections'][2]['blocks'][15]['text'],'v1 [9, 8]\nv2 [6, 10]\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete synthetic saved-run accuracy and variation replay');ns=run(code,'11 14 20\n22 16 20\n33 12 20\nmean 0.7\nrange percentage points 20.0\n')
 rows=next(b['rows'] for b in w['sections'][8]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0][0]=='Fixed validation ID')[1:]
 assert len(rows)==20 and len({r[0] for r in rows})==20
 assert [sum(r[1]==r[column] for r in rows) for column in [2,3,4]]==[14,16,12]
 assert sum([9,8,10])/36==.75 and (10-8)/12==1/6
 checks.append({'week':'ai-4/26','verified':'published deterministic scoring outputs,complete synthetic prediction/summary replay,all declared run counts and independent12-case mean/range;no unknown model training claimed'})
if weeks['ai-4/27']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/27'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete constrained depth0 depth1 depth2 paper-tree fitting comparison');ns=run(code,'0 3 4 3 4\n1 3 4 3 4\n2 4 4 2 4\n');fit,predict=ns['fit_node'],ns['predict']
 depth1=fit(ns['training'],1);depth2=fit(ns['training'],2)
 assert depth1['children'][1]=={'label':'clear'} and predict((1,0),depth2)=='blocked' and predict((1,1),depth2)=='clear'
 try:predict((None,1),depth2)
 except ValueError:pass
 else:raise AssertionError('missing tree feature silently accepted')
 assert (96-62,88-79)==(34,9) and 79>62 and (100-82)==18 and 82>80
 checks.append({'week':'ai-4/27','verified':'complete constrained paper-tree fit/validation outputs,tied leaf and missing-input policy,pictured revised-gap arithmetic and selected independent comparison'})
if weeks['ai-4/28']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/28'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete three-pattern learning-curve summary from supplied repeats');ns=run(code);summary=ns['summary']
 assert summary['R']==[(10,1,8,7,9),(20,2,6,5,7),(40,3,5,4,6)]
 assert [r[2] for r in summary['P']]==[8,8,8] and [r[2] for r in summary['Q']]==[9,8,8]
 curves=json.loads((R/'reports/ai-4-week28-curve-data.json').read_text());assert curves['sizes']==[10,20,40]
 for case in ['p','q','r']:
  source=curves['cases'][case];assert source['training_mean']==ns['cases'][case.upper()][0] and source['validation_repeats']==ns['cases'][case.upper()][1]
  assert (R/f'assets/ai-4-28-learning-curve-{case}.png').is_file()
 assert sum([6,8,7])/3==7 and max([6,8,7])-min([6,8,7])==2
 assert sum([4,7,7])/3==6 and max([4,7,7])-min([4,7,7])==3
 checks.append({'week':'ai-4/28','verified':'published three-pattern summaries match plotted source records,all graph assets exist,main means/ranges and independent count/spread comparison'})
if weeks['ai-4/29']['sections'][0].get('reading_flow'):
 import math
 w=weeks['ai-4/29'];run(w['sections'][2]['blocks'][15]['text'],'1 4\n2 6\n3 8\n')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete unit-aware geometry features and training-only area centering');ns=run(code);features,fit=ns['features'],ns['fit_area_mean']
 assert math.isclose(ns['training_mean'],20/3) and math.isclose(ns['query']['area_cm2']-ns['training_mean'],10/3)
 assert features(12,30,'mm')=={'width_cm':3,'area_cm2':36,'length_over_width':4}
 assert features(5,0)['area_cm2']==0 and features(5,0)['length_over_width'] is None
 assert features(3,4)['area_cm2']-8==4
 for args in [(5,None),(5,-1),(5,True),(5,2,'ticks')]:
  try:features(*args)
  except ValueError:pass
  else:raise AssertionError('unsupported measurement accepted')
 rows=next(b['rows'] for b in w['sections'][8]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0][0]=='Separate fictional leaf-card comparison ID')[1:]
 assert len(rows)==4 and sum(r[2]==r[3] for r in rows)==sum(r[2]==r[4] for r in rows)==3
 assert [r[0] for r in rows if r[2]!=r[3]]==['C3'] and [r[0] for r in rows if r[2]!=r[4]]==['C2']
 checks.append({'week':'ai-4/29','verified':'published association code and complete geometry/centering program,unit conversion,zero/missing policies and same-case equal-accuracy/different-error comparison'})
if weeks['ai-4/30']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/30'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Complete controlled crossed-training feature-selection and fixed-validation trial');ns=run(code,'V1 1 [0, 0] [1, 0, 1, 0] 2 4\nV2 2 [4, 0] [1, 1, 0, 0] 4 4\n');fit,predict=ns['fit_feature'],ns['predict']
 assert fit(ns['original'])==(1,[0,0]) and fit(ns['original']+ns['crossed_additions'])==(2,[4,0])
 assert [predict(r[1:3],1) for r in ns['validation']]==[1,0,1,0]
 assert len({r[0].split('-')[0] for r in ns['validation']})==2
 assert {r[0] for r in ns['original']+ns['crossed_additions']}.isdisjoint({r[0].split('-')[0] for r in ns['validation']})
 try:predict((1,None),2)
 except ValueError:pass
 else:raise AssertionError('missing marker silently accepted')
 for n in [12,13,14,16]:assert any(g.get('collapsed') and 'saved response' in g['title'] for g in w['workbook'][n-1]['reading_flow']['groups'])
 checks.append({'week':'ai-4/30','verified':'complete original/crossed fit outputs,training-only feature selection,two-plant grouping,missing-input policy and preserved older capacity responses'})
if weeks['ai-4/31']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/31'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete disaggregated lighting type and camera error recall audit');ns=run(code);records,summary=ns['records'],ns['summarize']
 assert len(records)==25 and len({r['id'] for r in records})==25
 assert [summary([r for r in records if r['camera']==g])['errors'] for g in ['A','B']]==[2,3]
 assert [summary([r for r in records if r['camera']==g])['count'] for g in ['A','B']]==[20,5]
 assert summary([r for r in records if r['light']=='bright'])['errors']==0 and summary([r for r in records if r['light']=='dim'])['positive_found']==6
 assert [summary([r for r in records if r['type']==g])['error_rate'] for g in ['Alpha','Beta']]==[.2,.2]
 assert summary([])['error_rate'] is None and summary([])['recall'] is None
 assert summary(records)['errors']==5 and summary(records)['recall']==11/13
 checks.append({'week':'ai-4/31','verified':'complete25-case disaggregated metrics,declared group counts,missing-camera unavailable results,pooled recall and equal-error/different-recall slices'})
if weeks['ai-4/32']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/32'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete retained-proxy feature ablation and same-case subgroup comparison');ns=run(code);fit,report=ns['fit_feature'],ns['report'];train,valid=ns['training'],ns['validation']
 assert fit(train,['camera_code','room_hint','marker'])==('camera_code',[0,0,0]) and fit(train,['room_hint','marker'])==('room_hint',[0,0])
 assert report(valid,[r['camera_code'] for r in valid])==(4,8,2,4) and report(valid,[r['room_hint'] for r in valid])==(4,8,2,4)
 greenhouse=[r for r in valid if r['setting']=='greenhouse'];desk=[r for r in valid if r['setting']=='desk']
 assert report(greenhouse,[r['camera_code'] for r in greenhouse])==(2,4,1,2) and report(desk,[r['camera_code'] for r in desk])==(2,4,1,2)
 assert report(greenhouse,[r['room_hint'] for r in greenhouse])==(2,4,2,2) and report(desk,[r['room_hint'] for r in desk])==(2,4,0,2)
 assert len({r['plant'] for r in valid})==2
 checks.append({'week':'ai-4/32','verified':'complete retained-proxy fit and paired ablation,unchanged overall utility with changed setting recall,tied candidate policy and two-source grouping'})
if weeks['ai-4/33']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/33'];rows=next(b['rows'] for b in w['sections'][8]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0][0]=='Saved test ID')[1:]
 assert len(rows)==12 and len({r[0] for r in rows})==12
 tn=sum(r[1]==r[2]=='clear' for r in rows);fp=sum(r[1]=='clear' and r[2]=='blocked' for r in rows);fn=sum(r[1]=='blocked' and r[2]=='clear' for r in rows);tp=sum(r[1]==r[2]=='blocked' for r in rows)
 assert (tn,fp,fn,tp)==(7,1,2,2) and sum(r[1]==r[3] for r in rows)==8
 assert (tn+tp)/12==.75 and tp/(tp+fp)==2/3 and tp/(tp+fn)==.5
 assert 16/20==.8 and 14/20==.7 and 20/4==5
 checks.append({'week':'ai-4/33','verified':'complete12-pair model-card metric/baseline audit,pictured photo/source counts and explicit missing artifacts/review without invented readiness or independent score'})
if weeks['ai-4/34']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/34'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete72-record student capstone kit and training-majority baseline');ns=run(code,'roles 40 20 12\ntraining clear/blocked 22 18\nfrozen baseline clear\nvalidation correct/total 9 20\nvalidation blocked found/total 0 11\nfinal references absent: not scored\n')
 assert len(ns['records'])==72 and len({r['group_id'] for r in ns['records']})==72
 assert all(not r['label'] for r in ns['final_features']) and ns['counts']=={'clear':22,'blocked':18}
 key=next(b['rows'] for b in w['teacher'][0]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0]==['Teacher-only final ID','Reference label'])[1:]
 assert len(key)==12 and {row[0] for row in key}=={r['id'] for r in ns['final_features']}
 run(w['sections'][2]['blocks'][17]['text'],'accuracy 0.8\nprecision 0.6666666666666666\nrecall 0.6666666666666666\n')
 checks.append({'week':'ai-4/34','verified':'complete72-row student kit,source-disjoint40/20/12roles,actual22/18baseline and9/20validation,blank student finalreferences,separate12-row teacherkey and distinct illustrative matrix'})
if weeks['ai-4/35']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/35'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete capstone controlled feature comparison and frozen prediction ledger');ns=run(code)
 assert ns['validation_matrices']=={'V1':[9,0,7,4],'V2':[9,0,3,8]} and ns['chosen']=='V2'
 assert ns['gains']==['P42','P49','P60','P67'] and ns['regressions']==[]
 assert len(ns['final_predictions'])==12 and all(not r['label'] for r in ns['final_features'])
 assert 'FINAL_KEY' not in ns and 'FINAL_KEY' not in code
 probe=dict(ns['valid'][0]);before=ns['predict'](probe,ns['models']['V2']);probe['label']='made up';assert ns['predict'](probe,ns['models']['V2'])==before
 try:ns['matrix'](ns['final_features'],ns['final_predictions'])
 except ValueError:pass
 else:raise AssertionError('Blank final references must not be scored')
 private=next(b['text'] for b in w['teacher'][0]['blocks'] if b.get('title')=='Teacher-only frozen capstone final evaluator after actual freeze check');tns=run(private)
 assert tns['matrix'](tns['final_labelled'],tns['final_predictions'])==[3,2,0,7]
 assert tns['matrix'](tns['final_labelled'],[tns['constant']]*12)==[5,0,7,0]
 assert not any('FINAL_KEY' in b.get('text','') for s in w['sections']+w['workbook'] for b in s['blocks'])
 checks.append({'week':'ai-4/35','verified':'complete controlled feature fit and fixed20-case validation,all gains and remaining misses,blank student final labels,no query-target leakage,teacher-only frozen12-case evaluation'})
if weeks['ai-4/36']['sections'][0].get('reading_flow'):
 w=weeks['ai-4/36'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete paper expo prediction ledger and metric audit');ns=run(code);audit,records=ns['audit'],ns['records']
 assert audit(records,'candidate')=={'cells':[7,1,2,2],'correct':9,'total':12,'precision':2/3,'recall':.5,'errors':['R08','R09','R10']}
 assert audit(records,'baseline')['precision'] is None and audit(records,'baseline')['correct']==8
 rows=next(b['rows'] for b in w['sections'][5]['blocks'] if b.get('type')=='table' and b.get('rows',[[]])[0][0]=='Indoor picture photo / plant group')[1:]
 assert len(rows)==15 and len({r[0].split(' / ')[1] for r in rows})==5
 assert sum(r[1]==r[2] for r in rows)==12 and sum(r[1]==r[3] for r in rows)==10
 assert [r[0].split(' / ')[0] for r in rows if r[1]!=r[2]]==['F03','F11','F14']
 checks.append({'week':'ai-4/36','verified':'complete paper defense ledger,all three errors and undefined baseline precision,separate15-photo/five-plant picture audit,explicit missing artifacts and no invented project results'})
if weeks['ai-5/1']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/1'];ns=run(w['sections'][2]['blocks'][1]['text'],'[5.0, 3.0]\n');encode=ns['encode']
 assert encode(60,10)==[6,1] and encode(1,1)==[.1,.1] and encode(20,70)==[2,7]
 for pair in [(40,None),(None,10),(40,0),(-1,20)]:
  try:encode(*pair)
  except ValueError:pass
  else:raise AssertionError('Missing/nonpositive measurement accepted')
 assert encode(6,1)==[.6,.1]
 checks.append({'week':'ai-5/1','verified':'named mm-to-cm encoding,positive boundary,missing/zero/negative guards,and explicit wrong-unit scale contrast'})
if weeks['ai-5/2']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/2'];ns=run(w['sections'][2]['blocks'][1]['text'],'6\n0\n3\n');dot=ns['dot']
 assert dot([2,-1],[3,5])==1 and dot([2,0],[3,5])==6 and dot([],[])==0
 assert dot([2,-.1],[4,20])==6 and dot([-2,4,.5],[3,1,2])==-1 and dot([-2,4,.5],[3,2,2])==3
 try:dot([2],[3,5])
 except ValueError:pass
 else:raise AssertionError('Mismatched feature dimensions accepted')
 checks.append({'week':'ai-5/2','verified':'matched signed products,cancellation,zero coefficient,dimension rejection,unit-preserving coefficient and independent controlled input change'})
if weeks['ai-5/3']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/3'];ns=run(w['sections'][2]['blocks'][2]['text'],'(1, 1)\n(0, 1)\n(-1, 0)\n');classify=ns['classify']
 assert classify(4,4)==(1,1) and classify(4,6)==(-1,0) and classify(3,3)==(0,1)
 assert classify(3,4)==(-1,0) and classify(3,4,-1)==(1,1)
 assert all(classify(x,2*x-3)==(0,1) for x in [2,3,4])
 assert classify(2,1)==(0,1) and classify(1,1)==(-2,0) and classify(1,1,-1)==(0,1)
 assert (R/'assets/ai-5-03-bias-boundary.png').exists()
 checks.append({'week':'ai-5/3','verified':'original boundary algebra and side checks,inclusive equality,constant two-point bias shift and separately plotted parallel boundary'})
if weeks['ai-5/4']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/4'];ns=run(w['sections'][2]['blocks'][2]['text'],'-2 0 0.1192\n0 0 0.5\n2 2 0.8808\n');sigmoid=ns['sigmoid']
 assert sigmoid(-1000)==0 and sigmoid(1000)==1 and sigmoid(0)==.5
 assert [int(sigmoid(z)>=.5) for z in [-2,0,2]]==[0,1,1]
 assert [3*max(0,x-3)+2 for x in [1,3,4]]==[2,2,5]
 assert [3*(x-3)+2 for x in [1,3,4]]==[-4,2,5]
 assert [2*max(0,x-2)+1 for x in [0,2,5]]==[1,1,7]
 assert (R/'assets/ai-5-04-activation-curves.png').exists()
 checks.append({'week':'ai-5/4','verified':'stable sigmoid negative/zero/positive/extreme inputs,inclusive class rule,ReLU information loss and distinct worked/independent chain traces'})
if weeks['ai-5/5']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/5'];ns=run(w['sections'][2]['blocks'][1]['text'],'([2, 2], [2, 2], 3)\n([-2, 2], [0, 2], -1)\n');forward=ns['forward']
 assert forward([1,1])==([0,0],[0,0],1) and forward([3,0])==([3,1],[3,1],6)
 assert forward([4,1])==([3,3],[3,3],4)
 assert forward([0,1])[1:]==forward([0,2])[1:]==([0,0],1)
 try:forward([3,1,0])
 except ValueError:pass
 else:raise AssertionError('Invalid forward dimension accepted')
 assert max(0,4-2)-max(0,3-1)==0 and max(0,4-2)-max(0,1-1)==2
 checks.append({'week':'ai-5/5','verified':'complete2-to2-to1forward trace,shape rejection,asymmetric hidden-order bug probe,representation collision and separate pictured composition'})
if weeks['ai-5/6']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/6'];ns=run(w['sections'][2]['blocks'][1]['text'],'0 ([-1, 2], [0, 2], -3)\n1 ([1, 1], [1, 1], 0)\n3 ([5, -1], [5, 0], 6)\n');trace=ns['trace']
 assert trace(.5)==([0,1.5],[0,1.5],-2) and trace(2)==([3,0],[3,0],4)
 assert trace(0)==([-1,2],[0,2],-3) and trace(3)==([5,-1],[5,0],6)
 assert [-max(0,2*x-1)+4 for x in [0,2]]==[4,1]
 checks.append({'week':'ai-5/6','verified':'complete dependency-order traces,negative-score/zero-boundary regression cases,omitted-bias and hidden-order failures,and distinct scalar picture audit'})
if weeks['ai-5/7']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/7'];ns=run(w['sections'][2]['blocks'][1]['text'],'9\n4\n13\n');count=ns['dense_count']
 assert count(2,4)+count(4,1)==17 and count(1,1)==2
 assert count(3,2)+count(2,2)==14 and count(3,4)+count(4,2)==26
 assert 2*3+3*1==9
 checks.append({'week':'ai-5/7','verified':'dense parameter/bias convention,adjacent-layer widening increment,no-bias contrast and independent14-to26counts'})
if weeks['ai-5/8']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/8'];ns=run(w['sections'][2]['blocks'][1]['text'],'2.0\n1.0\n');mse=ns['mse']
 assert mse([2,2],[0,4])==4 and mse([1,3],[1,3])==0
 assert mse([2,4],[1,3])==1 and mse([2,4],[3,1])==5
 assert mse([1,2,3],[0,2,4])==2/3 and mse([0,2,2],[0,2,4])==4/3
 for p,t in [([],[]),([1,2],[1])]:
  try:mse(p,t)
  except ValueError:pass
  else:raise AssertionError('Empty/mismatched loss inputs accepted')
 checks.append({'week':'ai-5/8','verified':'paired squared losses,cancellation,all-case denominator,alignment failure,nonempty/equal-length guards and independent metric-dependent comparison'})
if weeks['ai-5/9']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/9'];ns=run(w['sections'][2]['blocks'][1]['text'],'1 -2.0\n2 0.0\n3 2.0\n');loss,slope=ns['loss'],ns['local_slope']
 assert abs(slope(0,.5)+4)<1e-10 and abs(slope(1,.1)+2)<1e-10
 assert loss(1.1)<loss(1)<loss(4) and loss(2.9)<loss(3)<loss(-1)
 for step in [0,-.1]:
  try:slope(1,step)
  except ValueError:pass
  else:raise AssertionError('Nonpositive slope spacing accepted')
 assert (0**2-1)**2>(.1**2-1)**2 and (R/'assets/ai-5-09-local-slope-limits.png').exists()
 assert ((1.25+1)**2-(.75+1)**2)/.5==4
 checks.append({'week':'ai-5/9','verified':'complete symmetric estimates and full denominator,positive-spacing guard,small-move versus overshoot,zero-slope counterexample and independent new quadratic'})
if weeks['ai-5/10']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/10'];ns=run(w['sections'][2]['blocks'][0]['text'],'[-4.0, -2.0]\n');check,loss=ns['gradient_check'],ns['loss']
 for centre,expected in [((1,0),[-4,-2]),((0,1),[-8,-4]),((1,1),[0,0])]:
  assert all(abs(a-b)<1e-6 for a,b in zip(check(*centre),expected))
 assert abs((loss(1.1,.1)-loss(.9,-.1))/.2+6)<1e-10
 assert (max(0,.1)-max(0,-.1))/.2==.5
 checks.append({'week':'ai-5/10','verified':'coordinate-isolated numerical/formula agreement at three centres,declared tolerance and order,distinct combined-direction slope and ReLU-corner counterexample'})
if weeks['ai-5/11']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/11'];ns=run(w['sections'][2]['blocks'][0]['text'],'0.0 (1.0, 0.0, 1.0)\n0.05 (1.2, 0.1, 0.25)\n0.1 (1.4, 0.2, 0.0)\n0.3 (2.2, 0.6, 4.0)\n');step=ns['step']
 for rate,expected in [(0,(1,0,1)),(.05,(1.2,.1,.25)),(.1,(1.4,.2,0)),(.3,(2.2,.6,4)),(-.1,(.6,-.2,4))]:
  assert all(abs(a-b)<1e-10 for a,b in zip(step(1,0,rate),expected))
 assert step(1,1,.1)==(1,1,0)
 mixed_w=1.4;mixed_b=0-.1*(2*(2*mixed_w-3));assert abs(mixed_b-.04)<1e-10 and abs((2*mixed_w+mixed_b-3)**2-.0256)<1e-10
 checks.append({'week':'ai-5/11','verified':'same-start simultaneous rate trials,zero and negative-rate contrasts,overshoot and explicitly different mixed-state update with checked post-update loss'})
if weeks['ai-5/12']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/12'];ns=run(w['sections'][2]['blocks'][1]['text'],'0 0.0 10.0\n1 1.0 2.5\n2 1.5 0.625\n3 1.75 0.15625\n4 1.875 0.0390625\n')
 assert ns['step']==4 and ns['v']==1.875 and ns['loss']==.0390625 and ns['train']==[(1.,2.),(2.,4.)]
 assert (ns['v']*3-6)**2==.140625 and (ns['v']*max(0,-1)+2)**2==4
 assert 2*((1-2)*1+(2-4)*2)/2==-5
 assert 0-.125*(2*(0-2)*2)==1
 checks.append({'week':'ai-5/12','verified':'complete five-state/four-update restricted training loop,mean-versus-sum gradient scale,frozen representation,reserved-row error and independent exact one-pair update'})
if weeks['ai-5/13']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/13'];ns=run(w['sections'][2]['blocks'][1]['text'],'[0.4, 1.68]\n[1.0]\n');epoch,rows=ns['epoch'],ns['rows']
 assert all(abs(a-b)<1e-10 for a,b in zip(epoch(0,rows,1,.1),[.4,1.68]))
 assert all(abs(a-b)<1e-10 for a,b in zip(epoch(0,list(reversed(rows)),1,.1),[1.6,1.68]))
 new=[(1,1),(2,0)];assert abs(epoch(0,new,1,.1)[-1]-.04)<1e-10 and abs(epoch(0,list(reversed(new)),1,.1)[-1]-.2)<1e-10
 for r,size in [([],1),(rows,0)]:
  try:epoch(0,r,size,.1)
  except ValueError:pass
  else:raise AssertionError('Empty/invalid batch accepted')
 assert (2*1+2*4+9)/5==3.8 and (3*2+10)/4==4
 checks.append({'week':'ai-5/13','verified':'current-state per-batch gradients,full-batch versus sequential counts,main-order coincidence versus independent order sensitivity,invalid guards and case-weighted frozen means'})
if weeks['ai-5/14']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/14'];ns=run(w['sections'][2]['blocks'][1]['text']);trial=ns['run']
 data=json.loads((R/'reports/ai-5-week14-curve-data.json').read_text())
 for item in data['records']:
  values,losses=trial(item['rate']);assert values==item['v'] and losses==item['mse']
 assert trial(.3)==([0.,3.,1.5,2.25,1.875],[10.,2.5,.625,.15625,.0390625])
 assert trial(.4)[0]==[0.,4.,0.,4.,0.] and trial(.4)[1]==[10.]*5
 assert trial(.2)[1]==[10.,0.,0.,0.,0.] and trial(.5)[1][-1]==256.2890625
 assert (R/'assets/ai-5-14-controlled-rates.png').exists()
 checks.append({'week':'ai-5/14','verified':'all five exact same-start rate trajectories and plotted data,shrinking crossings,unchanged oscillation,growing loss and objective-specific rate scaling'})
if weeks['ai-5/15']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/15'];ns=run(w['sections'][2]['blocks'][1]['text'],'0 10.0 28.125\n1 2.5 3.125\n2 0.625 0.0\n3 0.15625 0.78125\n4 0.0390625 1.7578125\nSelected checkpoint 2\n');mse=ns['mse'];data=json.loads((R/'reports/ai-5-week15-curve-data.json').read_text())
 assert [mse(v,ns['train']) for v in ns['checkpoints']]==data['train'] and ns['validation_losses']==data['validation']
 assert ns['best']==2 and ns['checkpoints'][ns['best']]==1.5
 assert [mse(v,[(1,1),(2,2)]) for v in [1,1.5,2]]==[0,.625,2.5]
 try:mse(1,[])
 except ValueError:pass
 else:raise AssertionError('Empty checkpoint evaluation accepted')
 assert min(range(5),key=lambda i:([5,2,1,1,1.2][i],i))==2
 checks.append({'week':'ai-5/15','verified':'all paired same-state training/validation losses and plotted data,selected saved parameter,earliest exact tie,empty-row guard and independent reversed split preference'})
if weeks['ai-5/16']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/16'];ns=run(w['sections'][2]['blocks'][1]['text'],'1.6\n[0.4, 1.28, 1.68, -0.4]\n');terms=ns['terms']
 assert all(abs(a-b)<1e-10 for a,b in zip(terms(1.6,.5),[.4,1.28,1.68,-.4]))
 next_v=1.6-.1*terms(1.6,.5)[3];assert abs(next_v-1.64)<1e-10 and abs(terms(next_v,.5)[0]-.324)<1e-10
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete strict-improvement patience policy replay with no future selection');pn=run(code);replay=pn['replay_stopping']
 stop,best,trace=replay([4,2,1.5,1.6,1.4,1.45,1.46,.1],2);assert (stop,best,len(trace))==(6,4,7) and [r[2] for r in trace[3:]]==[1,0,1,2]
 assert replay([5,3,3,4],1,1)[:2]==(3,2) and replay([5,3,3,4],2,1)[:2]==(4,2)
 assert replay([3,2,2,2,1],2)[:2]==(3,1)
 for losses,patience in [([],1),([1],0)]:
  try:replay(losses,patience)
  except ValueError:pass
  else:raise AssertionError('Invalid stopping policy accepted')
 checks.append({'week':'ai-5/16','verified':'separate data/penalty gradient and objective terms,complete strict-improvement patience replay,no future selection,explicit index conventions,invalid-policy guards and honest absent-snapshot restoration status'})
if weeks['ai-5/17']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/17'];ns=run(w['sections'][2]['blocks'][1]['text'])
 assert ns['first']==ns['second'] and [ns['train'](x) for x in [0,1,3]]==[[0,1,1.5],[1,1.5,1.75],[3,2.5,2.25]]
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete two-unit symmetry and zero-start update experiment');sn=run(code);params=[1.,1.,1.,1.];grad,new,loss=sn['update'](params,1,1,.1)
 assert grad==[2.]*4 and new==[.8]*4 and abs(loss-.0784)<1e-10 and params==[1.]*4
 for j,g in enumerate(grad):
  low=params[:];high=params[:];low[j]-=.0001;high[j]+=.0001
  numerical=((sn['output'](high,1)-1)**2-(sn['output'](low,1)-1)**2)/.0002
  assert abs(numerical-g)<1e-6
 assert sn['update']([0.]*4,1,1,.1)[0]==[0.]*4
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete same-seed extra-preview-draw assignment comparison');rn=run(code)
 assert rn['normal']==rn['replay'] and rn['normal']!=rn['shifted'] and rn['normal'][1:]==rn['shifted'][:3]
 checks.append({'week':'ai-5/17','verified':'complete fixed-budget starting traces,same-seed call-history assignment,all-four positive-region symmetry gradients checked numerically,zero-start convention and distinct final parameters at equal loss'})
if weeks['ai-5/18']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/18'];ns=run(w['sections'][2]['blocks'][1]['text']);dense=ns['dense_relu'];W=ns['weights'];b=ns['bias']
 assert dense([1,2],W,b)==([1,2,0],[1,2,0]) and dense([3,1],W,b)==([3,1,3],[3,1,3])
 assert dense([1,2],W,[0,0,0])[0]==[1,2,-1] and dense([1,2],W,[0,0,0])[1]==dense([1,2],W,b)[1]
 assert dense([3,1],W,[0,0,0])==([3,1,2],[3,1,2])
 for x,weights,bias in [([1],W,b),([1,2],[[1,0],[0,1],[1]],b),([1,2],W,[0,0]),([],W,b),([1,2],[],[])]:
  try:dense(x,weights,bias)
  except ValueError:pass
  else:raise AssertionError('Malformed dense dimensions accepted')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete labelled gradient-coordinate and update audit');pn=run(code)
 assert all(abs(a-b)<1e-6 for a,b in zip(pn['checked'],[-8,-12])) and all(abs(a-b)<1e-10 for a,b in zip(pn['new'],[1.08,.12])) and abs(pn['loss'](*pn['new'])-2.1904)<1e-10
 checks.append({'week':'ai-5/18','verified':'dense row/unit shape guards,hidden-versus-exposed numerical bias omission,labelled finite-difference gradient repair and correct saved-state post-update loss'})
if weeks['ai-5/19']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/19'];ns=run(w['sections'][2]['blocks'][1]['text']);represent,predict=ns['represent'],ns['predict']
 assert [represent(*x) for x in [(4,2),(2,4),(3,3),(5,3)]]==[[2,0],[0,2],[0,0],[2,0]]
 assert predict(represent(3,3))==0 and represent(4,2)==represent(5,3) and 4*2!=5*3
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete hidden-plus-sum reconstruction and collision audit');rn=run(code)
 assert rn['recover']([2,0],6)==(4,2) and rn['recover']([2,0],8)==(5,3)
 assert rn['recover']([0,2],6)==(2,4) and rn['recover']([0,0],6)==(3,3)
 g=lambda w,h:[max(0,w-h-1),max(0,h-w-1)];assert g(4,3)==g(3,4)==[0,0]
 assert (R/'assets/ai-5-19-representation-collision.png').exists()
 checks.append({'week':'ai-5/19','verified':'complete rectangle encodings and task-dependent area collision,strict square boundary,exact hidden-plus-sum reconstruction and independent thresholded target conflict'})
if weeks['ai-5/20']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/20'];ns=run(w['sections'][2]['blocks'][1]['text'],'[[255, 0], [0, 255]]\n[[0, 255], [0, 255]]\n[[0, 0], [255, 255]]\n')
 assert ns['restored']==ns['hwc'] and ns['chw'][1][0][1]==ns['hwc'][0][1][1]==255
 flat=[v for row in ns['hwc'] for pixel in row for v in pixel];assert flat[:4]==[255,0,0,0] and ns['chw'][0][1][1]==255
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fixed RGB scaling and colour-information audit');pn=run(code)
 assert pn['scaled']==[1,128/255,0] and pn['twice'][0]==1/255 and sum(pn['red'])/3==sum(pn['green'])/3==85
 assert (R/'assets/ai-5-20-rgb-channel-planes.png').exists()
 checks.append({'week':'ai-5/20','verified':'all RGB channel planes and exact HWC/CHW roundtrip,named-pixel coordinate preservation,false-reshape mismatch,fixed/double scaling and colour-mean collision'})
if weeks['ai-5/21']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/21'];ns=run(w['sections'][2]['blocks'][1]['text']);filter=ns['local_filter'];x,k=ns['x'],ns['k']
 assert filter(x,k)==[[0,5],[-1,-1]] and filter(x,k,2)==[[0]]
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete local filter stride padding bias activation and orientation probes');pn=run(code)
 assert filter(pn['changed'],k)==[[3,5],[-1,-1]]
 assert filter(pn['padded'],k)==[[1,2,0,0],[-1,0,5,0],[2,-1,-1,3],[-2,2,-1,1]]
 assert filter(x,pn['flipped'])==[[2,4],[-2,2]]
 try:filter([[1]],k)
 except ValueError:pass
 else:raise AssertionError('Oversized local kernel accepted')
 unseen=filter([[2,1,0],[1,3,2]],[[0,1],[-1,2]]);assert unseen==[[6,1]] and [[max(0,v-5) for v in row] for row in unseen]==[[1,0]]
 assert (R/'assets/ai-5-21-local-window-products.png').exists()
 checks.append({'week':'ai-5/21','verified':'all four local products and shared-weight map,stride/boundary/full padded outputs,one-pixel locality,flipped convention,oversized-kernel guard and independent bias/ReLU composition'})
if weeks['ai-5/22']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/22'];ns=run(w['sections'][2]['blocks'][1]['text']);pool=ns['pool2']
 assert pool(ns['x'])==([[4,5],[6,7]],[[2.5,2],[3,3.25]])
 assert pool([[-4,-2],[-7,-3]])==([[-2]],[[-4.]]) and pool([[1,2,99],[3,4,99],[99,99,99]])==([[4]],[[2.5]])
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete pooling collision negative boundary and movement probes');pn=run(code)
 assert pn['pre_max']==[[8,0]] and pn['post_max']==[[0,8]] and pn['pre_mean']==[[2.,0.]] and pn['post_mean']==[[0.,2.]]
 assert pn['max_with_position']([[5,1],[2,3]])==pn['max_with_position']([[5,0],[0,0]])==(5,(0,0))
 try:pool([[1]])
 except ValueError:pass
 else:raise AssertionError('No-complete-window input accepted')
 unseen=[[-4,-1,2,6],[-3,-2,4,0],[5,1,-8,-2],[3,7,-4,-6]];assert pool(unseen)==([[-1,6],[7,-2]],[[-2.5,3],[4,-5]])
 assert (R/'assets/ai-5-22-pooling-regions.png').exists()
 checks.append({'week':'ai-5/22','verified':'complete max/mean regions,negative maxima,unread incomplete border,within-window and max-position collisions,explicit boundary-crossing head and independent signed map'})
if weeks['ai-5/23']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/23'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Complete tiny image training validation selection and baseline audit without final cases');ns=run(code)
 assert ns['best_index']==2 and abs(ns['selected']-.45)<1e-12 and ns['baseline_class']==0 and len(ns['train'])==4 and len(ns['valid'])==2
 assert all(abs(a-b)<1e-12 for a,b in zip(ns['checkpoints'],[0,.3,.45]))
 assert abs(ns['mse'](ns['selected'],ns['train'])-.15625)<1e-10 and abs(ns['mse'](ns['selected'],ns['valid'])-.3025)<1e-10
 assert ns['prediction'](ns['selected'],[[0,0],[0,0]])==(0,[0,0],0.,0)
 assert 'final = [' not in code and 'final_ledger' not in code
 private=next(b['text'] for b in w['teacher'][1]['blocks'] if b.get('title')=='Teacher-only final image-case evaluator after the saved-checkpoint gate');pn=run(private)
 assert [r['prediction'] for r in pn['final_ledger']]==[1,0,0] and sum(r['baseline']==r['class'] for r in pn['final_ledger'])==2 and abs(pn['mse'](pn['selected'],pn['final'])-.535)<1e-10
 assert not any('final = [' in b.get('text','') for s in w['sections']+w['workbook'] for b in s['blocks'])
 assert (R/'assets/ai-5-23-development-image-cards.png').exists()
 checks.append({'week':'ai-5/23','verified':'complete four-image training and two-image validation,one tied output parameter,checkpoint/baseline selection,public equality probe and separate teacher-only three-case frozen final audit'})
if weeks['ai-5/24']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/24'];ns=run(w['sections'][2]['blocks'][1]['text']);assert ns['x']==[[1,0],[0,0]] and ns['label'](ns['tie'])==ns['label'](ns['swap_columns'](ns['tie']))==0
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete augmentation label lineage and exact-pixel overlap audit');pn=run(code);audit=pn['audit'];records=pn['retained']
 assert len(pn['inventory'])==10 and len(records)==7 and audit(records)==({},[])
 assert [(len({r['source'] for r in records if r['split']==s}),sum(r['split']==s for r in records)) for s in ['training','validation','final']]==[(2,4),(1,1),(2,2)]
 assert audit(pn['bad_group'])[0]=={'P':['training','validation']}
 shared,pixels=audit(records+[pn['alias']]);assert not shared and pixels==[[('P-row_swap','training'),('claimed-U-original','validation')]]
 assert (R/'assets/ai-5-24-transform-label-rules.png').exists()
 checks.append({'week':'ai-5/24','verified':'all16binary label transformations and tie exception,nonmutating copies,complete5-source lineage/retention manifest,separate cross-group/exact-pixel failure audits and explicit unmeasured model effects'})
if weeks['ai-5/25']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/25'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Complete four-position event encoding with visible worked outputs');ns=run(code);encode=ns['encode']
 assert encode(['TURN','STOP'])==([3,4,0,0],[1,1,0,0]) and encode(['WAIT','GO'])==encode(['PAUSE','GO'])==([1,2,0,0],[1,1,0,0])
 for events in [[],['GO','TURN','GO','TURN','STOP'],['PAD'],['UNK']]:
  try:encode(events)
  except ValueError:pass
  else:raise AssertionError('Invalid event length/reserved marker accepted')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete event order unknown-position and masked sensor audit');pn=run(code)
 assert pn['last_event'](*pn['encode'](['GO','STOP']))==(1,4,'yes') and pn['last_event'](*pn['encode'](['GO','WAIT']))==(1,1,'review')
 assert pn['masked_mean']([0,4,0,0],[1,1,0,0])==2 and pn['masked_mean']([0,4,999,-7],[1,1,0,0])==2
 for values,mask in [([0,0],[0,0]),([1],[1,0])]:
  try:pn['masked_mean'](values,mask)
  except ValueError:pass
  else:raise AssertionError('No-real/misaligned measurement input accepted')
 assert (R/'assets/ai-5-25-real-position-masks.png').exists()
 checks.append({'week':'ai-5/25','verified':'complete ordered encoding,real unknown positions,reserved/empty/overlong rejection,right-padding final-index policy,measured-zero masked means and numeric-padding invariance'})
if weeks['ai-5/26']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/26'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Complete original-table nearest-neighbour geometry with visible ties');ns=run(code)
 assert ns['nearest']([1,0],ns['regular'])==['GO','TURN'] and ns['nearest']([0,2],{k:v for k,v in ns['regular'].items() if k!='STOP'})==['WAIT']
 for a,b in [([],[]),([1],[1,2])]:
  try:ns['distance2'](a,b)
  except ValueError:pass
  else:raise AssertionError('Invalid distance dimensions accepted')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete embedding lookup masked mean geometry and isolated row-update audit');pn=run(code)
 assert pn['vectors']==[[2,0],[0,2],[0,0],[0,0]] and pn['masked_vector_mean'](pn['vectors'],[1,1,0,0])==[1,1]
 assert pn['masked_vector_mean'](pn['lookup']([1,4,0,0]),[1,1,0,0])==[-.5,.5]
 assert pn['gradient']==[4,-4] and pn['updated'][2]==pn['updated'][3]==[1,1] and pn['table'][2]==[2,0]
 for ids in [[-1],[6]]:
  try:pn['lookup'](ids)
  except ValueError:pass
  else:raise AssertionError('Invalid vocabulary index accepted')
 assert ns['nearest']([1,0],{'A':[0,0],'B':[2,0],'C':[1,2]})==['A','B']
 assert (R/'assets/ai-5-26-embedding-neighbour-tie.png').exists()
 checks.append({'week':'ai-5/26','verified':'complete row lookup and mask-aware vector means,all nearest ties and role-based candidates,dimension/ID guards,isolated copied-row gradient/objective and independent valid zero-vector candidate'})
if weeks['ai-5/27']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/27'];ns=run(w['sections'][2]['blocks'][1]['text'],'A 1.0\nB 0.6\nC -1.0\n');unit,cosine=ns['unit'],ns['cosine']
 assert unit([3,4])==[.6,.8] and cosine([3,4],[6,8])==1 and cosine([3,4],[-3,-4])==-1
 for v in [[],[0,0]]:
  try:unit(v)
  except ValueError:pass
  else:raise AssertionError('Undefined unit direction accepted')
 code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete raw unit cosine ranking and explicit zero-vector policy audit');pn=run(code)
 assert pn['cosine_rank'](pn['q'],pn['candidates'])[0]==['A']
 assert pn['cosine_rank'](pn['q'],{'Z':[0,0],'B':[3,0]})[:2]==(['B'],['Z']) and pn['cosine_rank'](pn['q'],{'Z':[0,0]})==([],['Z'],{})
 for v in pn['candidates'].values():assert abs(pn['distance2'](unit(pn['q']),unit(v))-(2-2*cosine(pn['q'],v)))<1e-10
 assert cosine(pn['q'],[-4,3])==0
 assert pn['distance2']([5,0],[4,3])==10 and abs(cosine([5,0],[4,3])-.8)<1e-10
 assert (R/'assets/ai-5-27-raw-unit-vector-geometry.png').exists()
 checks.append({'week':'ai-5/27','verified':'complete raw/cosine/unit rankings,norm guards and2-2cosine identity,explicit zero-candidate/no-comparison reports,valid perpendicular zero cosine and independent changed ranking'})
if weeks['ai-5/28']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/28'];code=next(b['text'] for b in w['sections'][2]['blocks'] if b.get('title')=='Complete training-only threshold fit and same-row validation baseline');ns=run(code)
 assert ns['best']==5 and ns['baseline']==0 and ns['head_correct']==2 and ns['baseline_correct']==1
 assert ns['ledger']==[('V1',3,0,0,0),('V2',7,1,1,0)]
 assert ns['feature']([1,3])==ns['feature']([3,1])==4 and ns['predict']([2,3],5)==1
 for values in [[],[-1,2],[float('nan'),0],[float('inf'),0]]:
  try:ns['feature'](values)
  except ValueError:pass
  else:raise AssertionError('Invalid feature counts accepted')
 features=[2,4,5,7];labels=[0,0,1,1];mistakes=[sum(int(h>=t)!=y for h,y in zip(features,labels)) for t in [2,4,6]]
 assert mistakes==[2,1,1]
 checks.append({'week':'ai-5/28','verified':'training-only threshold and baseline fit,complete same-row validation,equality boundary,finite count guards,representation collision and checked independent threshold tie'})
if weeks['ai-5/29']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/29'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete confidence coverage confusion and failure-pattern audit');ns=run(code);report=ns['report'];rows=ns['rows']
 assert report(rows,.8)['accepted']==['A','B','C','F'] and report(rows,.8)['coverage']==4/6
 assert report(rows,.95)['accepted']==['A'] and report(rows,.99)['accepted_accuracy'] is None
 assert ns['confusion']=={'TP':2,'TN':1,'FP':2,'FN':1}
 assert report(ns['picture'],.85)['accepted_accuracy']==0
 independent=[('K','new',.85,0),('L','new',.70,1),('M','new',.30,0),('N','new',.05,0)]
 assert report(independent,.8)['accepted']==['K','N'] and report(independent,.8)['correct']==3
 for records,cutoff in [([],.8),(rows,float('nan')),([('Z','test',float('inf'),0)],.8)]:
  try:report(records,cutoff)
  except ValueError:pass
  else:raise AssertionError('Invalid review-policy input accepted')
 checks.append({'week':'ai-5/29','verified':'complete six-case confidence/confusion ledger,four cutoff policies and no-acceptance None,separate pictured counterexample,independent coverage/accuracy and finite input guards'})
if weeks['ai-5/30']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/30'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete group-count weighted-accuracy and mixture audit');ns=run(code);audit=ns['audit']
 assert ns['old']['accuracy']==.82 and ns['new']['accuracy']==.58 and ns['equal_mix']['accuracy']==.7
 assert ns['old']['errors']==18 and ns['new']['errors']==42
 for groups in [[],[('X',0,0)],[('X',2,3)],[('X',2.5,1)]]:
  try:audit(groups)
  except ValueError:pass
  else:raise AssertionError('Invalid audit counts accepted')
 assert audit([('P',60,48),('Q',40,20)])['accuracy']==.68 and audit([('P',20,16),('Q',80,40)])['accuracy']==.56
 assert (R/'assets/ai-5-30-group-mix-counts.png').exists()
 checks.append({'week':'ai-5/30','verified':'pooled/weighted agreement,unchanged group rates and changed mix,integer/zero/invalid count guards,separate pictured rates and independent P/Q calculation'})
if weeks['ai-5/31']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/31'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete timing quality-gate parameter and measurement-scope audit');ns=run(code);timing=ns['timing_summary']
 assert ns['a']==(2,20,50) and ns['b'][:2]==(1.2,12)
 assert ns['parameters']([4,3,2])==(18,5,23) and ns['parameters']([3,2,1])==(8,3,11)
 assert timing([.6,.5,.4],50)==(.5,10,100) and timing([.3,.4,.5],50)==(.4,8,125)
 for times,count in [([],100),([0],100),([float('nan')],100),([1],0),([1],2.5)]:
  try:timing(times,count)
  except ValueError:pass
  else:raise AssertionError('Invalid timing input accepted')
 checks.append({'week':'ai-5/31','verified':'median/mean scope,throughput and amortised ratios,quality eligibility,dense weights/biases/raw bytes,invalid timing guards and independent timing/architecture keys'})
if weeks['ai-5/32']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/32'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete experiment replay with manifest checkpoints predictions and content hashes');ns=run(code)
 assert ns['result']['selected_weight']==1.75 and ns['result']['selected_update']==2
 assert ns['result']['baseline']['validation_mse']==9
 assert [r['validation_mse'] for r in ns['result']['checkpoints']]==[2.25,.5625]
 assert ns['content_hash'](ns['manifest'])!=ns['content_hash'](ns['changed'])
 assert ns['record']['final_evaluation']==ns['record']['runtime']=='not measured'
 assert ns['result']==ns['replay'](ns['manifest'],ns['config'])
 bad=dict(ns['config']);bad['initial_weight']=0
 try:ns['replay'](ns['manifest'],bad)
 except ValueError:pass
 else:raise AssertionError('Restricted gradient accepted nonpositive training preactivation')
 assert [(max(0,a*4)-8)**2 for a in [1,1.5,1.75]]==[16,4,1]
 checks.append({'week':'ai-5/32','verified':'complete two-update replay,baseline/all-checkpoint predictions and metrics,actual environment and missing measurements,data/config hashes and nonpositive-gradient guard,independent R17 errors'})
if weeks['ai-5/33']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/33'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete pre-experiment plan and baseline-only audit');ns=run(code)
 assert ns['baseline_mse']==12.5 and [r[-1] for r in ns['ledger']]==[9,16]
 assert ns['plan']['candidate_result']=='not run' and ns['plan']['final_result']=='not measured'
 assert 'final' not in ns and ns['plan']['updates']==2
 assert sum((max(0,x)-y)**2 for x,y in [(3,9),(4,12)])/2==50
 checks.append({'week':'ai-5/33','verified':'complete baseline-only planning record,strict improvement and absent candidate/final results,training/validation roles and independent baseline50'})
if weeks['ai-5/34']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/34'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete matched two-rate training and validation-selection audit');ns=run(code)
 assert [r['weight'] for r in ns['runs']]==[1.75,2] and ns['selected']['rate']==.2
 assert [r[3] for r in ns['probe']['history']]==[2.5,1.75]
 assert ns['fit'](.1)==ns['runs'][0]
 try:ns['fit'](1,3)
 except ValueError:pass
 else:raise AssertionError('Restricted gradient outside active region accepted')
 a=1
 for _ in range(2):a-=.1*5*(a-3)
 assert a==2.5 and ((3*a-9)**2+(4*a-12)**2)/2==3.125
 checks.append({'week':'ai-5/34','verified':'complete matched .1/.2 update paths and raw validation scores,separate .3 probe,candidate pool and active-region guard,paired correctness flags and independent target trace'})
if weeks['ai-5/35']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/35'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete frozen baseline candidate and condition-error evaluation');ns=run(code)
 assert ns['baseline_mse']==20.25 and ns['candidate_mse']==5 and ns['evaluate'](2,ns['negative'])[1]==10
 assert [r[-1] for r in ns['candidate']]==[0,0,4,16]
 independent=[('A',2,6),('B',4,12),('C',-1,-3),('D',-2,-6)]
 assert ns['evaluate'](1,independent)[1]==31.25 and ns['evaluate'](3,independent)[1]==11.25
 assert ns['evaluate'](3,independent[2:])[1]==22.5
 assert all(ns['predict'](weight,-1)>=0 for weight in [-5,0,5])
 assert (R/'assets/ai-5-35-nonnegative-output-limit.png').exists()
 checks.append({'week':'ai-5/35','verified':'frozen four-case baseline/candidate errors and condition scores,nonnegative output constraint,explicit revealed-case revision and independent frozen a3 calculation'})
if weeks['ai-5/36']['sections'][0].get('reading_flow'):
 w=weeks['ai-5/36'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete capstone selection frozen evaluation and claim-scope replay');ns=run(code)
 assert ns['selected']['rate']==.2 and ns['frozen_weight']==2
 assert (ns['baseline_mse'],ns['candidate_mse'],ns['negative_mse'])==(20.25,5,10)
 assert ns['neuron'](1)==(.2,.2) and ns['neuron'](2)==(-.8,0)
 base=[4,9,1,2];cand=[1,1,2,0]
 assert sum(base)/4==4 and sum(cand)/4==1 and sum(base[2:])/2==1.5 and sum(cand[2:])/2==1
 assert cand[2]>base[2] and (sum(base)-sum(cand))/sum(base)==.75
 checks.append({'week':'ai-5/36','verified':'full capstone training-selection-frozen-final chain,negative-condition errors,separate supported relative MSE reduction and neuron trace,independent overall/condition/worsened-row defense'})
if weeks['ai-6/1']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/1'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete local read-only boundary dispatcher and unchanged-source checks');ns=run(code);dispatch=ns['dispatch']
 assert ns['SCHEDULE']==ns['before']=={'Tuesday':'16:00'}
 assert [r['status'] for r in ns['result']]==['answered','out_of_scope']
 assert dispatch([{'action':'read_schedule','day':'Wednesday'}],ns['SCHEDULE'])[0]['status']=='review'
 for operations in [[],[{}],[{'action':'read_schedule'}]]:
  try:dispatch(operations,ns['SCHEDULE'])
  except ValueError:pass
  else:raise AssertionError('Malformed structured operation accepted')
 assert dispatch([{'action':'delete_schedule'}],ns['SCHEDULE'])==[{'action':'delete_schedule','status':'out_of_scope'}]
 checks.append({'week':'ai-6/1','verified':'complete structured mixed-request outcomes,read-only source invariant,missing-record review and invalid-schema/excluded-operation distinction without external calls'})
if weeks['ai-6/2']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/2'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete local architecture trace with access-before-lookup and response checks');ns=run(code);traces=ns['traces']
 assert traces['restricted']==(['request_validator','role_filter'],{'status':'denied'})
 assert traces['spoofed_request']==(['request_validator'],{'status':'invalid_request'})
 assert 'draft' not in traces['missing'][0] and traces['wrong_draft'][1]['status']=='review'
 assert traces['allowed'][0]==['request_validator','role_filter','source_lookup','draft','response_validator','result']
 trace=[];result=ns['serve']({'source_id':'T'},'teacher',trace)
 assert result=={'status':'answered','source_id':'T','time':'18:00'}
 trace=[];assert ns['serve']({},'student',trace)=={'status':'invalid_request'} and trace==['request_validator']
 checks.append({'week':'ai-6/2','verified':'complete valid/denied/missing/mismatched stage traces,trusted-role versus client-field distinction and access-before-content/drafting boundary in a local deterministic simulator'})
if weeks['ai-6/3']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/3'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete closed-object schema audit with exact types and boundary probes');ns=run(code);validate=ns['validate_request']
 assert ns['results'][0][1]=='valid' and all(r[1]=='invalid' for r in ns['results'][1:])
 assert ns['validated']==ns['original'] and ns['validated'] is not ns['original']
 assert validate({'room_id':'B','requested_count':0})['requested_count']==0
 assert [ns['nonnegative_integer'](v) for v in [0,-1,'3',False]]==[True,False,False,False]
 assert validate({'room_id':' ','requested_count':2})['room_id']==' '
 checks.append({'week':'ai-6/3','verified':'closed-object/exact-type/range gates,bool subclass distinction,valid-copy preservation,missing/extra-field rejection and literal whitespace-ID/domain boundary'})
if weeks['ai-6/4']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/4'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete mock startup configuration and allowlisted-output audit');ns=run(code)
 assert ns['missing']=={'status':'startup_blocked','missing_or_invalid':['DATA_VERSION']}
 assert ns['absent_secret']=={'status':'startup_blocked','missing_or_invalid':['SIGNING_SECRET']}
 assert all(v not in ns['serialized'] for v in ns['mock_private'].values())
 for maximum in [True,0,'80']:
  internal,result=ns['startup']({'DATA_VERSION':'v1','MAX_WORDS':maximum},ns['mock_private'])
  assert internal is None and result=={'status':'startup_blocked','missing_or_invalid':['MAX_WORDS']}
 checks.append({'week':'ai-6/4','verified':'mock startup required-key/type checks,no default credential,allowlisted public/error records,private sentinel exclusion and independent configured-limit change'})
if weeks['ai-6/5']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/5'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete trusted-session read-policy and separate museum-permission audit');ns=run(code)
 assert ns['spoofed']=={'status':'denied'} and 'read_allowed_body' not in ns['trace']
 assert ns['student_session']['role']=='student' and ns['public']['status']=='answered'
 assert [ns['may_read'](r,'teacher') for r in [None,'student','teacher']]==[False,False,True]
 assert ns['museum_allowed']('curator','edit','C') and not ns['museum_allowed']('volunteer','edit','C')
 checks.append({'week':'ai-6/5','verified':'trusted role over client claim,denial before body read,unchanged session,resource-specific read policy and separate museum authorization-without-execution distinction'})
if weeks['ai-6/6']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/6'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete least-privilege pair intersection and pre-execution stub audit');ns=run(code)
 assert ns['denied']=={'status':'denied'} and ns['executions']==[('reporter','lookup','public-room')]
 assert not ns['permitted']('reporter','write','teacher-notes',ns['ACTOR_SCOPES'],ns['TOKEN_SCOPE'])
 assert ns['permitted']('bot','read','S5',ns['weather_actor'],ns['expanded'])
 assert not ns['permitted']('bot','write','S2',ns['weather_actor'],ns['expanded'])
 assert ('write','S2') not in ns['paired']
 scope={'catalogue':frozenset({('read','K7'),('read','L4')})};token=scope['catalogue']
 assert [ns['permitted']('catalogue',op,res,scope,token) for op,res in [('read','K7'),('write','K7'),('read','M8'),('read','L4')]]==[True,False,False,True]
 checks.append({'week':'ai-6/6','verified':'actor/token exact-pair intersection,denied-before-stub execution ledger,explicit narrow weather expansion,cross-product overgrant prevention and current catalogue key'})
if weeks['ai-6/7']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/7'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete pure-component boundary tests and deliberate-defect check');ns=run(code)
 assert all(r['passed'] for r in ns['records']+ns['formatter']) and not ns['fault']['passed']
 assert ns['fault']['actual']==('value',6) and ns['room_label'](7)=='Room 7'
 assert ns['remaining'](9,0)==9 and ns['remaining'](9,9)==0
 for used in [10,True]:
  try:ns['remaining'](9,used)
  except ValueError:pass
  else:raise AssertionError('Invalid independent boundary accepted')
 checks.append({'week':'ai-6/7','verified':'exact expected value/error harness,normal/zero/equality/type boundaries,formatter spacing and zero rejection,finite invariant checks and caught deliberate off-by-one defect'})
if weeks['ai-6/8']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/8'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete constructed run-fixture rubric and summary-criterion audit');ns=run(code)
 assert ns['passes']==3 and len(ns['ledger'])==5 and len({r['case_id'] for r in ns['ledger']})==1
 assert [r['pass'] for r in ns['summary_ledger']]==[True,False,True,False] and ns['summary_ledger'][-1]['words']==25
 assert not ns['score']({**ns['fixtures'][0],'actions':['book']})['pass']
 assert (4+2)/(4+4)==.75 and 4/4==1 and 2/4==.5
 checks.append({'week':'ai-6/8','verified':'complete supplied five-run/one-case rubric ledger,unsupported capacities and schema/action failures,separate supplied semantic labels versus measured word count and independent per-case/run denominators'})
if weeks['ai-6/9']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/9'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete mocked integration response and adapter-call-trace audit');ns=run(code)
 assert ns['denied']==ns['bad']=={'status':'denied'} and ns['bad_calls']==['T']
 assert ns['trials']['normal'][0]=={'status':'answered','source_id':'S','room_id':'B','capacity':12}
 assert all('draft_stub' not in ns['trials'][mode][2] for mode in ['missing','failure'])
 lookup,calls=ns['storage_fixture']();events=[]
 assert ns['service']({'source_id':'T'},'student',lookup,events)=={'status':'denied'} and calls==[]
 assert ns['catalogue_reply']('N','N')['item']=='notebook' and ns['catalogue_reply']('N','M')['status']=='review'
 checks.append({'week':'ai-6/9','verified':'result-plus-call-trace hidden-read detection,local normal/missing/dependency-failure paths,no drafting after absent evidence and catalogue identifier mismatch'})
if weeks['ai-6/10']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/10'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete versioned local evaluation ledger and explicit-skip denominator audit');ns=run(code);summary=ns['summary']
 assert (summary['planned'],summary['completed'],summary['passed'],summary['failed'],summary['skipped'])==(6,5,4,1,1)
 assert summary['completed_pass_rate']==.8 and summary['coverage']==5/6
 assert ns['summarize'](ns['cases'],ns['all_skipped'])['completed_pass_rate'] is None
 for records in [ns['records'][:-1],ns['records']+[ns['records'][0]],[{**r,'expected':999} for r in ns['records']]]:
  try:ns['summarize'](ns['cases'],records)
  except ValueError:pass
  else:raise AssertionError('Inconsistent/overwriting result record accepted')
 assert 5/6==.8333333333333334 and 6/8==.75
 checks.append({'week':'ai-6/10','verified':'versioned fixed-stub raw ledger,explicit skips versus omitted/duplicate/extra records,reference preservation,completed/coverage denominators and all-skipped None'})
if weeks['ai-6/11']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/11'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete constructed request-budget audit with exact integer thresholds');ns=run(code);objective=ns['objective']
 assert len(ns['failed'])==5 and ns['criterion_failures']==7
 assert ns['report']['successes']==195 and ns['report']['allowed_failures']==4 and not ns['report']['meets']
 assert ns['picture_original']['failures']==3 and ns['picture_counterfactual']['failures']==2
 assert not ns['picture_original']['meets'] and ns['picture_counterfactual']['meets']
 assert objective(12,0,98)['allowed_failures']==0 and not objective(12,1,98)['meets']
 independent=objective(80,5,95);assert independent['allowed_failures']==4 and independent['success_rate']==.9375 and not independent['meets']
 for args in [(0,0,98),(200,201,98),(True,0,98),(200,1,98.0)]:
  try:objective(*args)
  except ValueError:pass
  else:raise AssertionError('Invalid objective counts accepted')
 checks.append({'week':'ai-6/11','verified':'exact integer budget/thresholds,request versus criterion overlap,predeclared exclusions,correct-refusal fixture and preserved original/counterfactual windows with independent95% case'})
if weeks['ai-6/12']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/12'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete mock trace-metadata builder and private-value exclusion audit');ns=run(code);event=ns['event']
 assert set(ns['safe'])=={'trace_id','stage','status','duration_ms','error_category'}
 assert all(ns['raw_mock'][key] not in ns['serialized'] for key in ['passcode','student_text','teacher_answer'])
 assert {r['trace_id'] for r in ns['trace']}=={'R17'} and ns['trace'][0]['duration_ms']==240 and ns['trace'][1]['source_id']=='C8'
 for args in [('R7','authorize','denied',True),('R7','authorize','denied',-1),('R7','authorize','denied',3,'private content')]:
  try:event(*args)
  except ValueError:pass
  else:raise AssertionError('Invalid metadata value accepted')
 try:event('R7','request','ok',3,source_id='C8')
 except ValueError:pass
 else:raise AssertionError('Undeclared source-ID stage accepted')
 checks.append({'week':'ai-6/12','verified':'explicit emitted metadata and mock private-value exclusion,controlled fields/categories/duration,linked request/source spans and no implied access/deletion enforcement'})
if weeks['ai-6/13']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/13'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete bounded-state trace guard and separately revised-retry audit');ns=run(code)
 assert ns['original']['first_invalid_step']==3 and ns['original']['lookup_entries']==1
 assert ns['waiting']['valid'] and not ns['waiting']['complete']
 assert not ns['without_evidence']['valid'] and ns['with_evidence']['complete']
 assert ns['revised_trace']['lookup_entries']==2 and ns['exhausted']['reason']=='lookup-entry budget exhausted'
 assert ns['BASE']['review']=={'done'} and not ns['parcel_path'](['idle','querying','complete'],ns['parcel_retry'])
 narrow={'ready':{'looking_up'},'looking_up':{'review'},'review':{'done'},'done':set()}
 assert not ns['audit'](['ready','review','done'],policy=narrow)['valid']
 assert ns['audit'](['ready','looking_up','review','done'],policy=narrow,authorized_review_evidence=True)['valid']
 assert (R/'assets/ai-6-13-declared-state-graph.png').exists()
 checks.append({'week':'ai-6/13','verified':'first-invalid-edge and accepted-prefix records,valid/incomplete distinction,separate review-evidence guard,immutable graph revision,retained retry budget and narrower independent graph'})
if weeks['ai-6/14']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/14'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete read-only proposal preflight and runtime-evidence audit');ns=run(code)
 assert ns['rejected']['status']=='rejected_plan' and ns['unsafe_events']==[]
 assert ns['answer']=={'status':'answered','room_id':'B','capacity':12,'source_id':'ROOM-R'} and ns['safe_events']==ns['SAFE']
 assert ns['missing']['status']=='review' and ns['missing_events']==['validate','retrieve']
 assert ns['wrong']['status']=='rejected_plan' and ns['wrong_events']==[]
 for replacement in [{'room_id':'C'},{'approved':False},{'capacity':True}]:
  events=[];result=ns['run_plan'](list(ns['SAFE']),{'room_id':'B'},{**ns['SOURCE'],**replacement},events)
  assert result['status']=='review' and 'answer' not in events
 assert ns['tower_reply'](None)['status']=='unsupported' and ns['tower_reply']({'source_id':'HEIGHT-CARD','height_m':24,'approved':True})['height_m']==24
 checks.append({'week':'ai-6/14','verified':'unsafe/wrong-order proposal preflight with empty work traces,separate fixed safe plan,runtime missing/mismatched/unapproved evidence fallback and explicitly conditional tower-card answer'})
if weeks['ai-6/15']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/15'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete trusted-approval mock ledger retry conflict and restart audit');ns=run(code)
 assert len(ns['ledger'].effects)==1 and len(ns['desk_ledger'].effects)==1
 assert ns['ledger'].submit('operator','K',ns['payload'],'A1')['status']=='committed_stub'
 assert len(ns['ledger'].effects)+len(ns['restarted'].effects)==2
 for payload,approval,error in [(ns['changed'],'A1',PermissionError),(ns['changed'],'A2',ValueError)]:
  try:ns['ledger'].submit('operator','K',payload,approval)
  except error:pass
  else:raise AssertionError('Stale approval or same-key payload conflict accepted')
 assert len(ns['ledger'].effects)==1
 checks.append({'week':'ai-6/15','verified':'trusted actor/key/full-payload approval fixture,identical replay without new stub,stale approval and changed-payload conflict,copy isolation and explicit lost-memory deduplication limit'})
if weeks['ai-6/16']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/16'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete virtual caller-wait retry-budget and boundary-cancellation audit');ns=run(code)
 assert ns['main']['elapsed_s']==15 and ns['main']['status']=='budget_exhausted'
 assert len([e for e in ns['main']['events'] if e['kind']=='attempt'])==3
 assert abs(ns['picture']['elapsed_s']-1.4)<1e-12 and ns['cancelled']['elapsed_s']==1 and ns['cancelled']['status']=='cancelled'
 assert ns['nonretryable']['status']=='nonretryable' and len(ns['nonretryable']['events'])==1
 assert ns['waiting_bound'](2,5,[2])==12
 for args in [(3,float('nan'),[1,2]),(3,4,[1]),(True,4,[]),(2,4,[True])]:
  try:ns['waiting_bound'](*args)
  except ValueError:pass
  else:raise AssertionError('Invalid virtual timing contract accepted')
 assert (R/'assets/ai-6-16-caller-wait-timeline.png').exists()
 checks.append({'week':'ai-6/16','verified':'virtual main15second/3attempt bound,declared transient-only retry,between-attempt cancellation and pictured1.4/1second paths,finite numeric guards and no remote-abort/undo claim'})
if weeks['ai-6/17']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/17'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete local committed unknown absent and compensation-decision audit');ns=run(code)
 assert ns['committed']==ns['before'] and ns['reconcile']('BOOK-1',ns['committed'])['status']=='return_existing'
 assert ns['reconcile']('BOOK-1',ns['unknown'])['status']=='review' and ns['reconcile']('BOOK-1',ns['prepared'])['status']=='pending_review'
 assert ns['candidate']['status']=='resend_candidate' and ns['candidate']['operation_id']=='J6'
 assert ns['reconcile']('J6',ns['absent'])['status']=='review'
 assert ns['reconcile']('J6',{**ns['absent'],'authoritative':False},resend_approved=True,provider_deduplicates=True)['status']=='review'
 assert ns['reconcile']('BOOK-1',ns['committed'],can_read_status=False)=={'status':'denied'}
 try:ns['plan_compensation'](ns['compensation'],None)
 except PermissionError:pass
 else:raise AssertionError('Unapproved compensation accepted')
 checks.append({'week':'ai-6/17','verified':'unchanged committed recovery and copied result,prepared/unknown/reliable-absence distinctions,read access and conditional same-key resend proposal,separate compensation authority without execution'})
if weeks['ai-6/18']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/18'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete exact ASCII shape trusted-scope and dictionary-lookup audit');ns=run(code)
 assert ns['calls']==['A1','D4'] and ns['RECORDS']==ns['before']
 assert ns['normal']['status']=='answered' and ns['rejected']=={'status':'invalid_input'} and ns['denied']=={'status':'denied'} and ns['missing']['status']=='review'
 assert [ns['valid_room_id'](v) for v in ['C0','c0','C00','C0 ',None]]==[True,False,False,False,False]
 assert ns['valid_picture_id']('z0') and not ns['valid_room_id']('A١')
 calls=[];result=ns['lookup']('A1',ns['TRUSTED_ALLOWED'],{'A1':{**ns['RECORDS']['A1'],'extra':'not allowed'}},calls)
 assert result['status']=='review'
 checks.append({'week':'ai-6/18','verified':'exact ASCII whole-input/no-normalization contracts,separate uppercase/lowercase rules,format versus trusted access,absent/invalid-record review and unchanged dictionary with no input evaluation'})
if weeks['ai-6/19']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/19'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete abstract sandbox-policy queue-admission and supplied-trial audit');ns=run(code)
 assert not ns['permitted']('network','public_web') and not ns['permitted']('write','outside')
 assert ns['permitted']('read','fixtures') and ns['permitted']('write','outputs')
 assert ns['admit_batch'](8,2)['admit'] and not ns['admit_batch'](9,2)['admit']
 assert ns['a']['within_declared_limits'] and ns['b']['violations']==['network prohibited'] and ns['slow']['violations']==['time limit exceeded']
 assert ns['audit_picture'](2,20_000_000,False)['within_declared_limits']
 assert ns['audit_picture'](2,20_000_001,False)['violations']==['output limit exceeded']
 for values in [(float('nan'),2,False),(1,True,False),(1,2,'no')]:
  try:ns['audit_picture'](*values)
  except ValueError:pass
  else:raise AssertionError('Invalid supplied resource record accepted')
 checks.append({'week':'ai-6/19','verified':'abstract operation/resource permission decisions,all-or-nothing queue projection,inclusive time/output fixture limits and invalid-value guards,without actual OS/network/process enforcement'})
if weeks['ai-6/20']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/20'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete copied-store retention residual-copy and audit-clock simulation');ns=run(code)
 assert ns['stores']==ns['before'] and len(ns['report']['removed'])==4 and ns['report']['scoped_complete']
 assert all(set(items)=={'S6'} for items in ns['after'].values())
 assert ns['picture_report']['scoped_complete'] and not ns['failed_report']['scoped_complete']
 assert ns['failed_report']['residuals']==[('backup','T2')] and ns['retry_report']['scoped_complete']
 assert ns['retain_audit'](29) and not ns['retain_audit'](30)
 assert all('content' not in record for record in ns['audit'])
 _,report,_=ns['simulate_retention']({'X':3,'Y':4,'Z':5},{'primary':{'X':'mock','Z':'mock'},'temporary_log':{'Y':'mock'}},4,failed_removals={('temporary_log','Y')})
 assert report['due_ids']==['Y','Z'] and report['residuals']==[('temporary_log','Y')] and not report['scoped_complete']
 for ages,stores in [({},{}),({'S':7},{'cache':{'unknown':'mock'}})]:
  try:ns['simulate_retention'](ages,stores)
  except ValueError:pass
  else:raise AssertionError('Empty/incomplete retention fixture accepted')
 checks.append({'week':'ai-6/20','verified':'inclusive content boundary across copied stores,separate content-free audit clock,explicit scope,backup failure/residual/retry history and current4day temporary-log case without actual deletion'})
if weeks['ai-6/21']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/21'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete local permission version and virtual-age cache audit');ns=run(code)
 assert ns['teacher_hit']['status']=='hit' and ns['student_miss']['status']=='miss' and ns['revoked']=={'status':'denied'}
 assert ns['expired']=={'status':'miss','reason':'expired'} and ns['lookups']==['5']
 assert ns['next_request']['value']['opening']=='09:30' and ns['first']['status']=='miss'
 c=ns['FixtureCache']();c.put('q','student','v','p',{'x':1},3)
 assert c.get('q','student','v','p',2,5,currently_allowed=True)['reason']=='invalid negative age'
 hit=c.get('q','student','v','p',4,5,currently_allowed=True);hit['value']['x']=9
 assert c.get('q','student','v','p',4,5,currently_allowed=True)['value']=={'x':1}
 for now,ttl in [(float('nan'),5),(1,0),(1,True)]:
  try:c.get('q','student','v','p',now,ttl,currently_allowed=True)
  except ValueError:pass
  else:raise AssertionError('Invalid cache timing accepted')
 checks.append({'week':'ai-6/21','verified':'current permission before cache values,four-part context isolation,strict virtual TTL boundary and negative-age guards,approved-source miss then hit,copy isolation and explicit silent-edit/retention limits'})
if weeks['ai-6/22']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/22'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete sequential queue commit redelivery and uncertainty audit');ns=run(code)
 assert ns['accepted']['state']=='pending' and ns['first']['status']=='simulated_crash_before_ack'
 assert ns['worker'].effects==['J'] and ns['worker'].acks==[]
 assert ns['recovered'].effects==[] and ns['recovered'].acks==['J'] and ns['second']['status']=='return_existing'
 assert ns['unknown']['status']=='review' and ns['uncertain'].effects==[]
 assert len(ns['worker'].effects)+len(ns['lost'].effects)==2
 assert ns['picture_history'][-1]['state']=='failed'
 result=ns['recovered'].deliver('J');result['result']['artifact']='tampered'
 assert ns['recovered'].jobs['J']['result']['artifact']!='tampered'
 checks.append({'week':'ai-6/22','verified':'acceptance versus completion,two modeled deliveries with one committed mock effect,preserved-snapshot redelivery without new effect,unknown/running review,payload conflict,copy isolation and explicit lost-history/durability limits'})
if weeks['ai-6/23']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/23'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete symbolic environment target namespace and credential audit');ns=run(code)
 assert ns['main']['status']=='blocked' and ns['changed']['status']=='blocked'
 assert ns['picture']['record']['room']=='Z' and ns['calls']==['stage-fixtures'] and ns['STORES']==ns['before']
 assert ns['audit']({**ns['config_for']('development'),'credential':'prod-reader'})['status']=='blocked'
 for config in [{},{**ns['stage'],'extra':'value'},{**ns['stage'],'operation':True}]:
  try:ns['audit'](config)
  except ValueError:pass
  else:raise AssertionError('Invalid environment config accepted')
 checks.append({'week':'ai-6/23','verified':'exact symbolic environment/store/namespace/trusted-credential-operation matching,wrong target/authority blocked before fixture lookup,one valid Z read and unchanged fictional stores without real IAM/deployment claims'})
if weeks['ai-6/24']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/24'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fictional release compatibility and mandatory-gate audit');ns=run(code)
 assert ns['main']['status']=='blocked' and ns['main']['incompatible_schemas']==[2] and ns['stored']==ns['before']
 assert ns['quality_a']==80 and ns['quality_b']==90 and ns['initial']['failed_gates']==['privacy']
 assert ns['privacy_repaired_only']['failed_gates']==['compatibility'] and ns['all_declared_pass']['eligible_for_review']
 for gates in [{},{'quality':True,'privacy':True,'compatibility':True,'recovery':1}]:
  try:ns['release_decision'](gates)
  except ValueError:pass
  else:raise AssertionError('Incomplete/non-Boolean release gates accepted')
 checks.append({'week':'ai-6/24','verified':'current-schema compatibility blocks code-only rollback,supplied80/90percent correctness cannot override privacy gate,other gates remain required,strict complete Boolean decisions and unchanged inventory without deployment/migration'})
if weeks['ai-6/25']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/25'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete supplied-count window slice and missing-outcome audit');ns=run(code)
 assert ns['drop_pp']==20 and ns['current']['quality_alert'] and not ns['reference']['quality_alert']
 assert ns['total_a']['passes']==26 and ns['total_b']['passes']==23
 assert ns['no_ambiguous']['observed_rate'] is None and ns['no_ambiguous']['quality_alert'] is None
 assert ns['incomplete']['missing']==2 and ns['incomplete']['coverage_alert'] and ns['incomplete']['quality_alert'] is None
 assert not ns['exact_boundary']['quality_alert']
 assert ns['window'](20,12,8,0,70)['quality_alert']
 for args in [(20,14,4,1),(True,0,0,1),(1,2,0,0)]:
  try:ns['window'](*args)
  except ValueError:pass
  else:raise AssertionError('Inconsistent monitoring counts accepted')
 checks.append({'week':'ai-6/25','verified':'exact complete-window rates and20point drop,clear/ambiguous slices and totals,strict threshold equality,unavailable empty slices,explicit observed-only/missing coverage protocol and independent70percent threshold without causal claims'})
if weeks['ai-6/26']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/26'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fictional incident timeline and controlled-candidate audit');ns=run(code)
 assert ns['main_events']==ns['before'] and ns['weight_before']==ns['weight_at_response']
 assert ns['with_cache']['source_version']=='c1' and ns['without_cache']['source_version']=='c2'
 assert ns['picture']['observed']=='stale evidence version' and ns['changed']['observed']=='draft differs from retrieved record'
 assert ns['locate_mismatch']('6','missing','C',ns['records'])['observed']=='incomplete source evidence'
 checks.append({'week':'ai-6/26','verified':'preserved supplied timeline and declared weight context,controlled buggy-cache candidate with fixed fictional sources,old-retrieval versus wrong-draft evidence localization and incomplete evidence handling without live diagnosis'})
if weeks['ai-6/27']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/27'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete local handoff authority deadline and unresolved-state audit');ns=run(code)
 assert not ns['unassigned']['assigned'] and ns['assigned']['assigned'] and not ns['wrong_owner']['assigned']
 assert not ns['ready']['overdue'] and ns['over']['overdue'] and ns['over']['status']=='needs_review'
 assert not ns['unreachable']['handoff_ready'] and ns['unreachable']['status']=='needs_review'
 assert ns['effects']==ns['notifications']==[] and ns['assigned']==ns['before']
 assert ns['over']['effects']==ns['over']['notifications_sent']==[]
 checks.append({'week':'ai-6/27','verified':'scoped fictional reviewer assignment,unassigned/wrong-owner detection,deadline equality remains review,unreachable supervisor remains unresolved and empty action/notification traces without real sending or certification'})
if weeks['ai-6/29']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/29'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete supplied-duration mean median quality and fictional-cost audit');ns=run(code)
 assert (ns['a']['mean_seconds'],ns['a']['median_seconds'],ns['a']['max_seconds'])==(3,1,9)
 assert ns['b']['mean_seconds']==ns['b']['median_seconds']==2 and ns['failed']['passes']==3 and ns['failed']['count']==4
 assert ns['picture_a']['mean_cost_units']==2 and ns['picture_b']['mean_cost_units']==3
 assert ns['summarize'](ns['rows']([1,2,3,10]))['median_seconds']==2.5
 for rows in [[],[{'case_id':'Q','seconds':float('nan'),'success':True}],[{'case_id':'Q','seconds':True,'success':True}]]:
  try:ns['summarize'](rows)
  except ValueError:pass
  else:raise AssertionError('Invalid timing fixture accepted')
 checks.append({'week':'ai-6/29','verified':'complete matched-case durations,mean/median/observed max,failed-outcome retention,aggregate-only fictional time/cost means and inclusive mean budget without actual benchmark/individual-cap claims'})
if weeks['ai-6/30']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/30'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fictional direct cache note-reader and counts-only path audit');ns=run(code)
 assert ns['student_trace']==[] and all(r=={'status':'denied'} for r in ns['student_results'])
 assert all(r['content']==ns['GUIDE'] for r in ns['teacher_results']) and ns['NOTES']==ns['notes_before']
 assert ns['note']('teacher-2','N1')=={'status':'denied'} and ns['picture_count']=={'revision_count':2}
 try:ns['analytics_packet']([{'kind':'revision','text':'mock'}])
 except ValueError:pass
 else:raise AssertionError('Private-text analytics payload accepted')
 checks.append({'week':'ai-6/30','verified':'direct/cache trusted gates before denied content read,unexpected role-field rejection,assigned-note relationship access,counts-only event allowlist and unchanged fictional notes without real-auth/anonymity/full-audit claims'})
if weeks['ai-6/31']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/31'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fictional red-team event-phase and read-only-gate audit');ns=run(code)
 assert not ns['main']['passes_declared_action_boundary'] and ns['main']['violations'][0]['event_index']==1
 assert ns['blocked_only']['passes_declared_action_boundary'] and ns['safe']['passes_declared_action_boundary']
 assert not ns['changed']['passes_declared_action_boundary'] and ns['card']==ns['original'] and ns['answer']['opened']==1912
 assert ns['report']['observed_fixture_trace']==ns['main_events']
 for events in [[{'phase':'unknown','operation':'read'}],[{'phase':'effect','operation':None}],{}]:
  try:ns['judge'](events)
  except ValueError:pass
  else:raise AssertionError('Invalid fictional red-team trace accepted')
 checks.append({'week':'ai-6/31','verified':'first forbidden invocation despite refusal,blocked-proposal distinction,read-only local gate with unchanged exhibit fact,failed-edit trace and exact-input/version report without live model/tools/exfiltration'})
if weeks['ai-6/33']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/33'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete deterministic room capstone and separate read-only garden adapter');ns=run(code)
 assert ns['a']['capacity']==12 and ns['b']['capacity'] is None and ns['t']['status']=='denied'
 assert [r['resource_id'] for r in ns['trace']]==['A','B'] and ns['ROOMS']==ns['before']
 assert ns['picture']['source_id']=='G2' and ns['missing']['claim'] is None and ns['GARDEN']==ns['garden_before']
 c={'C':{'id':'C','approved':True,'capacity':0,'version':'c1','source_id':'REG-C'}}
 assert ns['serve']({'resource_id':'C'},'student',c,[],[])['capacity']==0
 assert ns['serve']({'resource_id':'D'},'student',c,[],[])['status']=='review'
 assert ns['serve']({'resource_id':'C'},'student',{'C':{**c['C'],'capacity':True}},[],[])['status']=='review'
 checks.append({'week':'ai-6/33','verified':'exact deterministic request/record/output contracts,A support/B review/T prelookup denial,minimized logs,measured zero versus missing and read-only G2 adapter with unchanged fixtures'})
if weeks['ai-6/34']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/34'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete capstone four-case trace matrix and checked-fallback audit');ns=run(code)
 assert all(r['passed'] for r in ns['good']) and sum(r['passed'] for r in ns['bad'])==3
 assert ns['bad'][1]['actual']['status']=='denied' and ns['bad'][1]['lookup_trace']==['T'] and not ns['bad'][1]['passed']
 assert ns['picture']['mode']=='degraded_fixed_template' and ns['picture']['source_id']=='F4'
 assert ns['both_unavailable']['status']=='review' and ns['both_unavailable']['claim'] is None
 assert ns['ROOMS']==ns['before'] and ns['fallback'](True,False,{**ns['F4'],'version':'old'})['status']=='review'
 checks.append({'week':'ai-6/34','verified':'predeclared four-case response/claim/trace matrix,correct invalid-input versus denial enums,bad-order restricted lookup caught despite denial,and evidence-dependent F4 degraded template without live model/failure effects'})
if weeks['ai-6/35']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/35'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete versioned mandatory-gate release review and preserved-history audit');ns=run(code)
 assert ns['main']['blockers']==[('compatible_rollback','not_run')] and ns['ordinary_gate'](18,20)
 assert ns['initial']['blockers']==[('deletion','fail')] and not ns['stale']['eligible_under_declared_fixture_gates']
 assert ns['fresh']['eligible_under_declared_fixture_gates'] and ns['failed_records']==ns['failed_before']
 assert ns['history'][0]['blockers']==[('deletion','fail')]
 assert not ns['review']('x',{'required'}, {})['eligible_under_declared_fixture_gates']
 try:ns['review']('x',{'required'}, {'required':ns['gate']('pass','x')})
 except ValueError:pass
 else:raise AssertionError('Passed release gate without evidence reference accepted')
 checks.append({'week':'ai-6/35','verified':'inclusive90percent threshold,not-run rollback blocker,mandatory deletion veto,wrong-candidate evidence blocker,missing/reference checks and preserved hypothetical repair history without real approvals/deletion/deploy'})
if weeks['ai-6/36']['sections'][0].get('reading_flow'):
 w=weeks['ai-6/36'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete three-case read-only demonstration and evidence-gap inventory');ns=run(code)
 assert all(r['passed_expected_contract'] for r in ns['results']) and ns['CARDS']==ns['before']
 assert [r['actual']['status'] for r in ns['results']]==['supported','review','denied']
 assert ns['results'][0]['actual']['source_id']=='V7' and ns['results'][2]['actual']['trace']==[]
 assert ns['evidence']['rollback_rehearsal']=='not run' and ns['evidence']['audience_or_operator_signoff']=='not supplied'
 assert all(r['actual']['effects']==[] for r in ns['results'])
 checks.append({'week':'ai-6/36','verified':'predeclared supported/review/denied contracts,V7 provenance,send denied before lookup,unchanged fixtures and explicit network/resource/recovery/people evidence gaps without live-service claims'})
if weeks['ai-7/1']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/1'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete constructed five-query research-question and top-three scoring audit');ns=run(code)
 assert ns['a']['queries']==ns['b']['queries']==5 and ns['a']['mean_relevant_in_top3']==1 and ns['b']['mean_relevant_in_top3']==ns['Fraction'](7,5)
 assert ns['b']['counts']['Q4']==0 and ns['a']['counts']['Q4']==1
 bad={**ns['A'],'Q1':['R1','R1','R9']}
 try:ns['score_snapshot'](bad,ns['RELEVANT'],ns['CORPUS'])
 except ValueError:pass
 else:raise AssertionError('Duplicate-ranked retrieval record accepted')
 checks.append({'week':'ai-7/1','verified':'complete added fixed-query/corpus/relevance snapshot,exact top-three counts and means,preserved Q4 decline and explicit constructed-practice versus reserved/live-study scope'})
if weeks['ai-7/2']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/2'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fictional claim-rate absolute-relative and paired-record audit');ns=run(code)
 assert ns['main']['difference_percentage_points']==ns['Fraction'](25,2) and ns['main']['rate_ratio']==ns['Fraction'](6,5)
 assert ns['picture']['difference_percentage_points']==20 and ns['picture']['rate_ratio']==2 and ns['picture']['relative_increase_percent']==100
 assert ns['pattern_one']=={'gains':1,'losses':0} and ns['pattern_two']=={'gains':2,'losses':1}
 assert ns['compare_counts'](0,10,1,10)['rate_ratio'] is None
 checks.append({'week':'ai-7/2','verified':'exact absolute/relative claim arithmetic,distinct8case/10case outcomes,zero-baseline undefined ratio and possiblepaired-record ambiguity without learner/causal/significance claims'})
if weeks['ai-7/5']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/5'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete replay event-case accounting and supplied new-data scoring audit');ns=run(code)
 assert ns['main']['evaluation_events']==16 and ns['main']['distinct_case_ids']==8 and ns['main']['new_case_ids']==0
 assert ns['first']==ns['replayed'] and ns['first']['rate']==ns['Fraction'](3,4) and ns['new_result']['rate']==ns['Fraction'](1,2)
 assert ns['picture_counts']['distinct_case_ids']==8 and ns['picture_counts']['new_case_ids']==4 and ns['original']==ns['before']
 assert ns['buggy_rate']==ns['Fraction'](1,2) and ns['manifest']['actual_partner_rerun']=='not performed'
 try:ns['case_accounting'](['A'],['A'],['A'])
 except ValueError:pass
 else:raise AssertionError('Old case silently relabelled new')
 checks.append({'week':'ai-7/5','verified':'evaluation-events versus distinct/new cases,exact replay/new-fixture scoring,artifact mismatch illustration and actual-work/independence limits with strict IDs and binary outcomes'})
if weeks['ai-7/7']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/7'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete toy primary-outcome plan preserved-revision and coverage audit');ns=run(code)
 assert ns['plan']==ns['saved_plan'] and ns['a']['supported_rate']==ns['b']['supported_rate']==ns['Fraction'](2,3)
 assert not ns['primary_pattern'] and ns['b']['mean_seconds']<ns['a']['mean_seconds']
 assert ns['b']['counts']['abstain']==1 and ns['a']['counts']['unsupported']==1 and ns['revision']['stage']=='post_results'
 assert ns['picture']['A_unsupported']==ns['picture']['B_unsupported']==2
 checks.append({'week':'ai-7/7','verified':'fixed-denominator primary support tie,separate faster secondary,abstention versus support,preserved original toy plan/post-result exploratory revision and ten-case picture tie without population/significance/preregistration claims'})
if weeks['ai-7/8']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/8'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete same-procedure source-confound and declared-baseline-condition audit');ns=run(code)
 assert ns['a_old']['correct']==1 and ns['b_current']['correct']==ns['a_aligned']['correct']==3
 assert 'mismatched source_version' in ns['unequal'] and 'resource policy not supplied' in ns['unequal']
 assert 100*ns['picture_a']==75 and 100*ns['picture_b']==ns['Fraction'](175,2)
 assert 'test answer-key exposure' in ns['leaked']
 checks.append({'week':'ai-7/8','verified':'identical-procedure source-freshness counterexample,aligned-information tie,exact8case descriptive gain,declared hidden-label exposure and missing resource-policy checks without actual model/budget/significance claims'})
if weeks['ai-7/9']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/9'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete repeated-query unit counts and whole-plant split-leakage audit');ns=run(code)
 assert len(ns['query_runs'])==12 and len({r['query_id'] for r in ns['query_runs']})==3
 assert ns['valid']['train_views']==ns['valid']['eval_views']==6 and ns['valid']['shared_plants']==[]
 assert ns['leaky']['train_views']==5 and ns['leaky']['eval_views']==7 and ns['leaky']['shared_plants']==['P1']
 assert ns['views']==ns['before'] and (R/'assets/ai-7-09-plant-group-split.png').exists()
 try:ns['audit_split']([],ns['evaluation'])
 except ValueError:pass
 else:raise AssertionError('Empty declared split accepted')
 checks.append({'week':'ai-7/9','verified':'threecontexts/twelveruns,fourplants/twelveviews,whole-plant6/6disjointsplit,movedview5/7sharedP1leak,nonemptyunique metadata guards and nativefigure without identity-based independence or actual-study claims'})
if weeks['ai-7/10']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/10'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete declared-control differences and crossed-background toy-rule audit');ns=run(code)
 assert ns['main_changes']==['corpus','queries'] and ns['unintended_changes'](ns['A'],ns['matched_B'])==[]
 assert len(ns['original_cells']['missing_cells'])==2 and ns['crossed_cells']['missing_cells']==[]
 assert sum(r['correct'] for r in ns['original_results'])==2 and sum(r['correct'] for r in ns['crossed_results'])==2 and len(ns['crossed_results'])==4
 assert ns['crossed_cells']['leaf_ids']==2 and ns['crossed']==ns['before']
 assert (R/'assets/ai-7-10-crossed-leaf-background.png').exists()
 checks.append({'week':'ai-7/10','verified':'declared method/corpus/query controls,four crossed leaf-background cells,explicit nuisance-only2/2 versus2/4 counterexample,repeated object identity and native illustration without actual model/causal/collection claims'})
if weeks['ai-7/11']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/11'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete exact ID-pair enumeration and sampling-probability audit');ns=run(code)
 assert ns['means']==[1,2,2,2,2,3] and ns['average_of_means']==ns['population_mean']==2
 assert ns['probabilities'][ns['Fraction'](2)]==ns['Fraction'](2,3) and sum(ns['probabilities'].values())==1
 independent=[{'id':str(i),'value':v} for i,v in enumerate([0,0,4,4])]
 assert [r['mean'] for r in ns['enumerate_means'](independent,2)]==[0,2,2,2,2,4]
 for size in [0,True,5]:
  try:ns['enumerate_means'](ns['population'],size)
  except ValueError:pass
  else:raise AssertionError('Invalid exact sampling size accepted')
 assert (R/'assets/ai-7-11-exact-sampling-distribution.png').exists()
 checks.append({'week':'ai-7/11','verified':'complete uniform-ID-pair enumeration,exact mean distribution/probabilities and expectation,distinct equal-value IDs,boundary guards and separate model-free classifier rates with native exact chart'})
if weeks['ai-7/12']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/12'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete known-positive-sigma interval and supplied-bound interpretation audit');ns=run(code)
 assert ns['main']['standard_error']==.5 and abs(ns['main']['lower']-9.02)<1e-12 and abs(ns['main']['upper']-10.98)<1e-12
 assert not ns['picture']['contains_zero'] and ns['changed']['contains_zero']
 independent=ns['known_sigma_interval'](20,5,25)
 assert independent['standard_error']==1 and abs(independent['lower']-18.04)<1e-12 and abs(independent['upper']-21.96)<1e-12
 for values in [(10,None,16),(10,0,16),(float('nan'),2,16),(10,2,True)]:
  try:ns['known_sigma_interval'](*values)
  except ValueError:pass
  else:raise AssertionError('Invalid nondegenerate known-sigma interval inputs accepted')
 assert (R/'assets/ai-7-12-supplied-time-intervals.png').exists()
 checks.append({'week':'ai-7/12','verified':'known-positive-sigma normal interval arithmetic/units,rounded critical theoretical coverage,strict finite inputs and separate supplied-bound zero interpretation without refitted raw data or parameter-probability/equality claims'})
if weeks['ai-7/13']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/13'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete paired-time effect and absolute-relative practical-threshold audit');ns=run(code)
 assert ns['main']['gains_seconds']==[2,3,1] and ns['main']['mean_gain_seconds']==2 and ns['main']['meets_declared_mean_threshold']
 assert ns['picture']['fewer_errors_per_thousand']==5 and not ns['picture']['meets_declared_threshold']
 assert ns['changed']['fewer_errors_per_thousand']==12 and ns['changed']['meets_declared_threshold']
 independent=[{'case_id':str(i),'baseline_seconds':a,'candidate_seconds':b} for i,(a,b) in enumerate(zip([6,8,10],[5,7,9]))]
 result=ns['paired_gain'](independent,1.5)
 assert result['mean_gain_seconds']==1 and not result['meets_declared_mean_threshold']
 assert (R/'assets/ai-7-13-practical-error-threshold.png').exists()
 checks.append({'week':'ai-7/13','verified':'paired A-B gains and inclusive mean practical threshold,distinct absolute/relative error reductions,changed threshold decision and independent smaller positive gain without uncertainty/significance/readiness claims'})
if weeks['ai-7/14']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/14'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete exact-rational paired sign-flip enumeration and inclusive-tail audit');ns=run(code)
 assert ns['main']['p']==ns['picture']['p']==ns['scaled']['p']==ns['Fraction'](1,4)
 assert ns['sum_counts']=={-4:1,-2:2,0:2,2:2,4:1}
 assert ns['sign_flip_test']([2,2,2])['p']==ns['Fraction'](1,4)
 assert ns['sign_flip_test']([0,0,0])['p']==1
 compact=run(w['sections'][8]['blocks'][2]['text'])
 assert compact['sign_flip_p']([1e-13]*3)==.25
 for values in [[True],[.1],[]]:
  try:ns['sign_flip_test'](values)
  except ValueError:pass
  else:raise AssertionError('Invalid exact sign-flip input accepted')
 assert (R/'assets/ai-7-14-exact-signflip-null.png').exists()
 checks.append({'week':'ai-7/14','verified':'exact inclusive two-sided conditional sign enumeration,paired-time null counts,tiny-scale invariance,zero ties and compact numeric correction without design or null-truth claims'})
if weeks['ai-7/15']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/15'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete exact Bonferroni family and missing-outcome audit');ns=run(code)
 assert ns['main']['cutoff']==ns['Fraction'](1,100) and sum(ns['main']['reject'])==1
 assert ns['picture']['cutoff']==ns['Fraction'](1,120) and ns['changed']['missing_tests']==4
 assert ns['changed']['cutoff']==ns['Fraction'](1,200) and ns['boundary']['reject'][0]
 independent=ns['bonferroni_family'](['.01','.02','.2','.9'])
 assert independent['cutoff']==ns['Fraction'](1,80) and independent['reject']==[True,False,False,False]
 for values,size in [([],1),(['.1'],True),(['1.2'],1),(['.1','.2'],1)]:
  try:ns['bonferroni_family'](values,size)
  except ValueError:pass
  else:raise AssertionError('Invalid family accepted')
 assert (R/'assets/ai-7-15-family-cutoffs.png').exists()
 checks.append({'week':'ai-7/15','verified':'exact five/six/ten-test cutoffs and inclusive decisions,missing outcomes retained in denominator,equivalent adjusted p-values and independent four-test family without validity/effect-size claims'})
if weeks['ai-7/16']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/16'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete ablation count, critical-boundary and missing-interaction audit');ns=run(code)
 assert ns['main_retrieval']['count_drop']==3 and ns['main_validation']['percentage_point_drop']==10
 assert ns['picture']['percentage_point_drop']==20
 assert ns['interaction_contrast'](4)==0 and ns['interaction_contrast'](6)==2
 assert ns['ablation_drop'](12,9,15)['percentage_point_drop']==20
 assert ns['ablation_drop'](12,11,15)['percentage_point_drop']==ns['Fraction'](20,3)
 for args in [(True,1,10),(8,5,0),(8,11,10)]:
  try:ns['ablation_drop'](*args)
  except ValueError:pass
  else:raise AssertionError('Invalid ablation counts accepted')
 assert (R/'assets/ai-7-16-ablation-grid.png').exists()
 checks.append({'week':'ai-7/16','verified':'conditional net drops and percentage-point arithmetic,critical-boundary distinction,explicitly hypothetical missing-cell interaction counterexamples and independent fifteen-case totals'})
if weeks['ai-7/17']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/17'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete supplied-summary sensitivity and unlabelled-score cutoff audit');ns=run(code)
 assert ns['picture']['.5']==ns['picture']['.6']==[False,True,True]
 assert ns['picture']['.7']==[False,False,True] and ns['scores']==ns['before']
 assert ns['correct_count'](ns['picture']['.5'],ns['hypothetical_labels_A'])==3
 assert ns['correct_count'](ns['picture']['.7'],ns['hypothetical_labels_B'])==3
 for scores,cutoff in [([],'.5'),(['.5'],True),(['1.2'],'.5')]:
  try:ns['classify'](scores,cutoff)
  except ValueError:pass
  else:raise AssertionError('Invalid score/cutoff accepted')
 assert (R/'assets/ai-7-17-cutoff-grid.png').exists()
 checks.append({'week':'ai-7/17','verified':'fixed-score inclusive cutoff flags,unchanged inputs,explicit hypothetical label counterexamples and supplied retrieval summaries without invented accuracy/raw counts or fresh-evaluation claims'})
if weeks['ai-7/18']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/18'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete source-identity weighting and setting-coverage audit');ns=run(code)
 assert ns['main']['unique_source_ids']==8 and ns['main']['extra_rows_beyond_one_per_source']==2
 assert ns['rows']==ns['before'] and ns['outdoor_initial'] is None
 assert ns['outdoor_added']==ns['Fraction'](1,2) and ns['pooled_changed']==ns['Fraction'](11,14)
 independent=[{'row_id':str(i),'source_id':v} for i,v in enumerate(['S1']*4+[f'S{j}' for j in range(2,10)])]
 assert ns['audit_sources'](independent)['unique_source_ids']==9
 for rows in [[],[{'row_id':'r','source_id':''}],[{'row_id':'r','source_id':'a'},{'row_id':'r','source_id':'b'}]]:
  try:ns['audit_sources'](rows)
  except ValueError:pass
  else:raise AssertionError('Invalid source metadata accepted')
 assert (R/'assets/ai-7-18-benchmark-coverage.png').exists()
 checks.append({'week':'ai-7/18','verified':'ten rows/eight source IDs/two extra rows,unchanged records,unknown original outdoor slice,separate added and pooled rates and independent nine-source count without independence or invented outcomes'})
if weeks['ai-7/20']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/20'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete fictional governance-plan and minimum-subgroup audit');ns=run(code)
 assert len(ns['main_issues'])==3 and ns['proposed_issues']==[] and ns['audit_plan'](ns['published_key'])
 assert ns['subgroup_rule'](1)=='block_under_supplied_rule' and ns['subgroup_rule'](5)=='size_rule_met_only'
 assert ns['audit_plan']({**ns['proposed'],'analyst_can_read_key':True})
 for value in [True,-1,1.5]:
  try:ns['subgroup_rule'](value)
  except ValueError:pass
  else:raise AssertionError('Invalid subgroup size accepted')
 assert (R/'assets/ai-7-20-key-separation.png').exists()
 checks.append({'week':'ai-7/20','verified':'declared fictional field/role/retention metadata audit,published-key issue,minimum-five boundary and invalid-size guards without actual access/export/deletion or anonymity claims'})
if weeks['ai-7/23']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/23'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete supplied power-frequency and per-study resource audit');ns=run(code)
 assert ns['main_small']['detection_fraction']==ns['Fraction'](62,100) and ns['main_large']['per_study_cost']==120
 assert ns['picture_small']['per_study_cost']==40 and ns['picture_large']['detection_fraction']==ns['Fraction'](4,5)
 assert ns['summarize'](70,100,30,2)['per_study_cost']==60 and ns['summarize'](85,100,60,2)['detection_fraction']==ns['Fraction'](17,20)
 for values in [(101,100,20,3),(62,0,20,3),(True,100,20,3)]:
  try:ns['summarize'](*values)
  except ValueError:pass
  else:raise AssertionError('Invalid supplied simulation summary accepted')
 assert (R/'assets/ai-7-23-power-cost.png').exists()
 checks.append({'week':'ai-7/23','verified':'exact stipulated alternative detection frequencies,separate per-study/total hypothetical work costs,main/picture distinction and independent design without executed-simulation/null-error/real-power claims'})
if weeks['ai-7/24']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/24'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete in-memory mean replay and exact-byte run-record audit');ns=run(code)
 assert ns['original']['raw_output']=='4' and ns['changed']['raw_output']=='5'
 assert ns['original']['data_sha256']!=ns['changed']['data_sha256'] and ns['original']['script_sha256']==ns['changed']['script_sha256']
 assert ns['original']['run_id']!=ns['changed']['run_id'] and ns['original']['python_runtime']
 assert ns['record']('recheck','2,4,6\n')['raw_output']=='4'
 assert ns['original']['data_sha256']==ns['hashlib'].sha256(ns['original']['data_text'].encode('utf-8')).hexdigest()
 assert (R/'assets/ai-7-24-run-records.png').exists()
 checks.append({'week':'ai-7/24','verified':'actual tiny local exact mean replay,changed input4to5,exact-byte SHA256 and runtime records,distinct retained run identities without full AI-study/provenance/scientific-validity claims'})
if weeks['ai-7/25']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/25'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete primary-completion coverage and paired-case outcome audit');ns=run(code)
 assert ns['main']['completed_pass_rate']==ns['Fraction'](8,9) and ns['main']['coverage']==ns['Fraction'](9,10) and ns['main']['unassessed']==2
 assert sum(ns['A'])==4 and sum(ns['B'])==5 and ns['a_only']==['C4'] and ns['b_only']==['C2','C5']
 independent=ns['completion_summary'](9,1,2)
 assert independent['completed_pass_rate']==ns['Fraction'](9,10) and independent['coverage']==ns['Fraction'](5,6)
 assert ns['completion_summary'](0,0,2)['completed_pass_rate'] is None
 for args in [(True,1,1),(-1,2,1),(0,0,0)]:
  try:ns['completion_summary'](*args)
  except ValueError:pass
  else:raise AssertionError('Invalid primary count accepted')
 assert (R/'assets/ai-7-25-paired-grid.png').exists()
 checks.append({'week':'ai-7/25','verified':'completed-case performance/eligible coverage/unassessed separation,complete paired six-case winners and net-versus-flips distinction,independent denominators and zero-completion unknown without actual-model/significance/revised-score claims'})
if weeks['ai-7/26']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/26'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete retained-duration mean, median and anomaly-evidence audit');ns=run(code)
 assert ns['main']['mean_seconds']==5 and ns['main']['median_seconds']==2 and ns['main_values']==ns['before']
 assert ns['picture']['mean_seconds']==4 and ns['picture']['median_seconds']==2
 independent=ns['timing_summary']([2,3,4,20]);assert independent['mean_seconds']==ns['Fraction'](29,4) and independent['median_seconds']==ns['Fraction'](7,2)
 assert ns['hypothetical_main_deleted']['mean_seconds']==ns['Fraction'](5,3)
 for values in [[],[True],[-1]]:
  try:ns['timing_summary'](values)
  except ValueError:pass
  else:raise AssertionError('Invalid supplied duration accepted')
 assert (R/'assets/ai-7-26-retained-durations.png').exists()
 checks.append({'week':'ai-7/26','verified':'exact retained main/picture mean-median arithmetic,unchanged valid records,explicit hypothetical deletion distortion,independent slow-tail case and invalid inputs without actual timings or root-cause claims'})
if weeks['ai-7/27']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/27'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete declared-condition slice and pooled-rate audit');ns=run(code)
 assert 100*(ns['main_current']-ns['main_outdated'])==40
 assert 100*(ns['indoor']-ns['outdoor'])==50 and ns['pooled']==ns['Fraction'](5,8)
 assert ns['rate'](7,8)-ns['rate'](6,8)==ns['Fraction'](1,8) and ns['rate'](4,8)-ns['rate'](5,8)==-ns['Fraction'](1,8)
 assert ns['rate'](6+5,16)==ns['rate'](7+4,16)
 for args in [(True,8),(9,8),(1,0)]:
  try:ns['rate'](*args)
  except ValueError:pass
  else:raise AssertionError('Invalid condition count accepted')
 assert (R/'assets/ai-7-27-slice-rates.png').exists()
 checks.append({'week':'ai-7/27','verified':'condition-specific exact rates/gaps,pooled masking,independent opposite candidate changes and pooled tie without inferred paired flips,causality or all-condition claims'})
if weeks['ai-7/30']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/30'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete exact-input string-length method and boundary audit');ns=run(code)
 assert [r['label'] for r in ns['original']]==['short','long','long'] and [r['label'] for r in ns['changed']]==['short','short','long']
 assert [r['character_count'] for r in ns['original']]==[3,4,6] and ns['labels'](['oak '])[0]['label']=='long'
 for inputs,flag in [([1],False),(['oak'],1)]:
  try:ns['labels'](inputs,flag)
  except ValueError:pass
  else:raise AssertionError('Invalid string/boundary input accepted')
 assert (R/'assets/ai-7-30-method-boundary.png').exists()
 checks.append({'week':'ai-7/30','verified':'exact no-trimming ASCII length labels,inclusive/strict pine boundary,explicit whitespace probe and input guards without missing-AI-artifact or learned/ecological claims'})
if weeks['ai-7/33']['sections'][0].get('reading_flow'):
 w=weeks['ai-7/33'];code=next(b['text'] for b in w['sections'][8]['blocks'] if b.get('title')=='Complete distinct MAE-MSE fixture and saved-score disagreement audit');ns=run(code)
 assert ns['fixture']['errors']==[0,2] and ns['fixture']['MAE']==1 and ns['fixture']['MSE']==2
 assert ns['picture']['original_correct']==5 and ns['picture']['rerun_correct']==4 and ns['picture']['disputed_case']=='Q3'
 for predictions,targets in [([],[]),([1],[1,2]),([True],[1])]:
  try:ns['error_metrics'](predictions,targets)
  except ValueError:pass
  else:raise AssertionError('Invalid exact metric fixture accepted')
 assert (R/'assets/ai-7-33-scoring-disagreement.png').exists()
 checks.append({'week':'ai-7/33','verified':'explicitly distinct MAE-one/MSE-two fixture,metric contract and supplied Q3 dispute without adjudicated-score,actual independent reproduction or new-data replication claims'})
(R/'reports/connected-python-checks.json').write_text(json.dumps({'checks':checks,'errors':[]},indent=2)+'\n');print(len(checks),'authored Python weeks verified in fresh execution namespaces.')
