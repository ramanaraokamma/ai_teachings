from connected_level_authoring import LevelAuthor,g,routes
a=LevelAuthor('ai-2/36');D=a.design
a.replace_text('on a reserved catalogue.','on a supplied practice catalogue.')
a.replace_text('Keep the reserved case distinct from practice demonstrations.','This pictured case is supported practice; keep the separately named independent activity task for a first attempt before feedback.')
D('sections',1,'Can you defend the result so a peer can reproduce it?','Show inputs, contract, validation, ranking, failures and limits together.',[g('Your learning goals',[1,2,3]),g('Recall reproducible evidence',[5,18],'prompts'),g('Your end goal',[20])])
D('sections',2,'Join each demonstration claim to its evidence','A working chooser does not by itself demonstrate educational benefit.',[g('The capstone handover contract',[11])])
D('sections',3,'Check report consistency without mistaking it for correctness','The small report script checks counts, not the winning recommendation.',[g('Predict and run the complete report check',[11],'example'),g('Trace the evidence needed beyond counts',[12,13,15]),g('Explain the deciding evidence',[17],'prompts')])
a.comparisons('Compare a defensible trace with a polished unsupported claim','A clear presentation keeps failures and missing evidence visible.')
p=a.add('sections',6,image=a.pic(2));ch=a.add('sections',6,image=a.pic(4))
code='''from collections import Counter

def book_report(raw, limit):
    if type(limit) is not int or limit < 0:
        return {'error':'invalid page limit'}
    names = Counter(r['id'] for r in raw if type(r) is dict
                    and type(r.get('id')) is str and r['id'])
    accepted, rejected = [], []
    for index, row in enumerate(raw,1):
        reason = None
        if type(row) is not dict:
            reason = 'not a record'
        elif type(row.get('id')) is not str or not row['id']:
            reason = 'invalid ID'
        elif names[row['id']] > 1:
            reason = 'duplicate ID'
        elif type(row.get('pages')) is not int or row['pages'] < 0:
            reason = 'invalid pages'
        elif type(row.get('interest')) is not int or not 0 <= row['interest'] <= 5:
            reason = 'invalid interest'
        elif type(row.get('illustrated')) is not bool:
            reason = 'invalid illustrated flag'
        if reason:
            rejected.append((index,reason))
        else:
            accepted.append(dict(row))
    eligible = [r for r in accepted if r['pages']<=limit]
    ranked = sorted(eligible, key=lambda r: (-(2*r['interest']+int(r['illustrated'])),r['id']))
    scores = [(r['id'],2*r['interest']+int(r['illustrated'])) for r in ranked]
    return dict(supplied=len(raw),accepted=len(accepted),rejected=rejected,
                eligible=len(eligible),ranked=scores,
                selected=scores[0][0] if scores else None,
                over_limit=[r['id'] for r in accepted if r['pages']>limit])

books = [dict(id='A',pages=120,interest=3,illustrated=True),
         dict(id='B',pages=100,interest=4,illustrated=False),
         dict(id='C',pages=121,interest=5,illustrated=True),
         dict(id='D',pages=90,interest='4',illustrated=True)]
original = book_report(books,120)
print(original)
# Explicitly supplied authorised toy-data correction; keep the original unchanged.
changed = [dict(r,interest=4) if r['id']=='D' else dict(r) for r in books]
print(book_report(changed,120))
assert book_report(list(reversed(books)),120)['ranked']==original['ranked']'''
ci=a.add('sections',6,image={'type':'code','language':'python','text':code,'title':'Complete pictured capstone book report'})
scope=a.add('sections',6,'The complete pictured implementation declares its missing schema details explicitly: nonempty unique IDs, exact integer nonnegative pages, exact integer interest0..5, Boolean illustrated; duplicate IDs are all rejected. It implements the supplied120-page limit and2interest+illustrated score with ID ties. These fields differ from the activity chooser’s fun/learning schema. The supplied correction to D is a new authorised fictional input version, not silent conversion of every text rating.')
D('sections',6,'Defend a complete book trace before presenting alone','The pictured catalogue is supported practice, not a fresh independent assessment.',[g('Name the evidence missing from a winner-only demo',[12],'prompts'),g('Read the separate book contract and rows',[16,18,19]),g('Trace validation, eligibility and ranking',[p,21,23]),g('Predict the explicit correction to D',[27],'prompts'),g('Check after predicting',[ch],'example',True),g('Read the complete implementation contract',[scope]),g('Run and inspect the complete pictured report',[ci]),g('Explain counts and remaining limits',[25,26],'prompts')])
err=a.add('sections',7,'Claim to repair: The report’s counts add up, so A must be the correct winner. Consistent counts can accompany the wrong score or tie rule. Show raw records, schema, exact limit, score formula, each eligible score and the tie policy before validating the selected item. The pictured book report selects B, while the small illustrative activity report says A; these are different records with different fields, not conflicting outputs for one case.')
D('sections',7,'Challenge a correct-looking report','Check the decision trace as well as the arithmetic of counts.',[g('Repair the consistency argument',[err],'example'),g('Propose a revealing audience question',[9],'prompts')])
D('sections',8,'Practise the evidence defence with less help','Retain the case version, failed checks and scope of the claim.',[g('Replace universal claims with tested behavior',[8]),g('Complete main W2',[9,10,11]),g('Repair a demo-based overclaim',[13,14,15],'prompts'),g('Explain the separate pictured report',[16,17,18],'prompts'),g('Reserve the independent activity case',[19])])
plan1=a.add('sections',9,'Expo rehearsal: use the complete pictured book program and its supplied rows. Predict the accepted/rejected/eligible counts, scores and winning ID before running. Record actual output only if run; otherwise label a paper trace. Show the supporting row for each claim. Reverse input order, trace no eligible rows with limit0, and inspect the explicit corrected-D version without overwriting original data.')
plan2=a.add('sections',9,'Prepare a reproducible handover: purpose and non-goals; raw fictional records/version; schema; source code and settings; exact run steps; expected and observed outputs; original failure and change log; regression coverage; and remaining limits. Ask a peer to reproduce the supported case from the bundle. A peer question after rehearsal is not automatically a fresh assessment; the teacher must withhold a separately checked new case until the independent attempt. Do not invent pupil work or claim learning benefit from the supplied toy outcomes.')
D('sections',9,'Rehearse a reproducible demonstration and handover','Use supplied local data; no accounts, publication or real learner profiles are required.',[g('Predict, run and explain the supplied report',[plan1],'steps'),g('Assemble and peer-check the evidence bundle',[plan2],'steps'),g('Keep the investigation record',[5,6,7,9])])
for r,n,i in [('sections',9,4),('teacher',4,5)]:a.fix(r,n,i,'Rehearse with the complete pictured book program and fictional rows, preserving expected/actual outputs and the handover bundle. Keep the independent activity task withheld for a first attempt. A familiar rehearsal case cannot establish fresh transfer.')
proj=a.add('sections',11,'Package the Transparent Book Recommender’s own schema, code, data, source-supported facts, test matrix, full ranking traces, no-match behavior, repair history and limitations. Label supplied classroom examples separately from work a learner actually completed. Provide local reproduction steps and record support used. A final showcase assesses the explanation and evidence for this bounded project; revisit other level concepts separately where readiness evidence is weak.')
D('sections',11,'Finish a project bundle someone else can check','A defensible handover includes the failures and evidence limits.',[g('This week’s concrete contribution',[proj,12]),g('Keep the checkpoint and human choice',[4,5,6,7,8,9,10])])
ref='Activity contract for this level: nonempty unique names; minutes exactint0..60;fun/learning exactint0..5; Boolean not integer; validate before selecting; eligibleminutes<=limit; score2fun+learning; highest score then ascending name; invalid rows retained with reasons; distinguish invalid request and no eligible option. Pictured book program uses different fields and score2interest+illustrated with ID ties.'
ix=a.add('sections',14,ref)
D('sections',14,'Try alone: defend the fresh activity report','Use this task’s activity contract rather than the pictured book formula.',[g('Independent records and standalone contract',[1,ix],'example'),g('Your first attempt and help record',[2,3,17]),g('Use feedback afterwards',[22])])
D('sections',16,'Finish: defend the decision and name the next evidence need','A completed expo does not establish mastery of every AI topic.',[g('Explain without notes',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
report=a.add('teacher',2,image=a.w['sections'][2]['blocks'][11]);tp=a.add('teacher',2,image=a.pic(2));bc=a.add('teacher',2,image={'type':'code','language':'python','text':code,'title':'Complete pictured capstone book report'})
D('teacher',2,'Model a reproducible defence rather than a winner-only demo','Keep illustrative activity report and supported book catalogue separate.',[g('State the handover purpose',[17]),g('Run the small count-consistency check',[report,18,23]),g('Read the pictured practice catalogue',[27,29,30]),g('Trace validation, filtering and scores',[tp,32,34]),g('Predict the authorised input correction',[38,39,40]),g('Run the complete pictured book program',[bc]),g('State evidence limits and preserve independent assessment',[36,42])])
extras={n:[a.add('workbook',n,ref)] for n in [12,13,14,16]};extras[4]=[a.add('workbook',4,ref)]
a.common('Defend a new activity case independently','Require a complete schema, filtering/score/tie trace, counts, reversed-order result and evidence limits.',[(12,'W1 · Assemble reproducible evidence','List inputs, contract, code, versions, results and failure history.'),(13,'W2 · Check report consistency','Reconcile supplied, accepted and rejected counts.'),(14,'W3 · Repair an educational-benefit claim','State the bounded software claim actually demonstrated.'),(16,'W5 · Name the next evidence need','Do not infer universal correctness or learning benefit from one pass.')], 'Picturedbooks4supplied,3accepted,Drejectedinteresttype;2eligibleA/B,Coverlimit;A7,B8→B. CorrectedDinterest4newversion4accepted,3eligible,D9wins. Reversalkeepsranking;limit0none. SmallillustrativereportA8countconsistentbutnotdecisionproof. IndependentactivityA/B8tieA,Cvalidbutoverlimit,Dinvalidfun;counts4/3/1/2. Reserve independentattempt;do notturnsupportedpictureintofreshassessment.',extras)
a.fix('teacher',6,13,'After Level2, continue to Level3: Generative AI Systems. Revisit the project’s explicit contracts, validation and reproducibility before starting Predictive and Generative AI in the next level; use recorded readiness and support evidence rather than expo polish as the progression decision.')
from connected_teacher_lab_keys import apply
apply(a,36)
from connected_paragraphs import format_additions
format_additions(a)
a.finish(routes(('Show the inputs. Trace the choice. Defend the evidence.','Present a reproducible bounded application with honest failures, support records and limitations.','Report consistency → full book trace → rehearsal and handover → independent activity defence.'),('Assess the explanation, trace and limits of the actual project.','Model supported examples, withhold the independent task, preserve support records and plan a delayed return.','Require enough evidence to reproduce the choice; keep software correctness separate from unmeasured learning benefit.'),('One connected capstone evidence record.','Assemble the bundle, reconcile counts, repair claims and name the next evidence need.','Retain data, contract, code version, full traces, tests, failures, support and unresolved limits.')))
