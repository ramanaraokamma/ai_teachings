from connected_extended_authoring import ExtendedAuthor,g
from connected_level_authoring import routes
a=ExtendedAuthor('ai-2/33');D=a.design
# Correct stale topic links without changing the retained earlier examples.
a.replace_text('Week 24 selection function','selection function in this week’s lesson')
a.replace_text('Apply Week 24 selector','Apply this week’s selector')
a.replace_text('Week 24 selector','selector in this week’s lesson')
a.replace_text('block the ambiguous batch for review instead of arbitrarily keeping one','exclude every occurrence of each duplicated name, retain reasons and review the source instead of arbitrarily keeping one')
a.replace_text('Block the ambiguous batch and report duplicate names for correction.','Exclude every occurrence of each duplicated name and report the reasons for correction, following the frozen Week32 policy.')
D('sections',1,'Can another learner reproduce this recommendation?','Build the declared filter, score and tie policy, then compare expected and actual results.',[g('Your learning goals',[1,2,3]),g('Recall a hard constraint',[5,18],'prompts'),g('Your end goal',[23]),g('Pipeline extension · Name the stages',[20,21],'reference',True)])
D('sections',2,'Implement a deterministic baseline','Filtering, scoring and ties must follow the frozen contract.',[g('The main activity-selector contract',[11]),g('Pipeline extension · Validate before selection',[13],'reference',True)])
D('sections',3,'Trace the best-so-far item through complete code','The compact selector assumes its inputs have already passed validation.',[g('Predict and run the complete activity example',[11],'example'),g('Trace equal scores and the name tie',[12,13,15]),g('Explain the deciding step',[23],'prompts'),g('Pipeline extension · Complete single-row validator',[17,18,19,21],'reference',True)])
a.comparisons('Compare eligibility, ranking and no-match behavior','A high score cannot repair a failed hard constraint.')
p=a.add('sections',6,image=a.pic(2));ch=a.add('sections',6,image=a.pic(4))
bookcode='''def choose_book(rows, subject, max_pages):
    # Inputs are supplied, validated fictional rows with unique IDs.
    eligible = [r for r in rows if r['subject'] == subject and r['pages'] <= max_pages]
    ranked = sorted(eligible, key=lambda r: (-(2*int(r['illustrated']) + int(r['comic'])), r['id']))
    return [(r['id'], 2*int(r['illustrated']) + int(r['comic'])) for r in ranked]

books = [dict(id='A',subject='animal',pages=90,illustrated=True,comic=False),
         dict(id='B',subject='animal',pages=70,illustrated=False,comic=True),
         dict(id='C',subject='space',pages=60,illustrated=True,comic=True),
         dict(id='D',subject='animal',pages=80,illustrated=True,comic=True)]
print(choose_book(books, 'animal', 90))
changed = [dict(r, pages=91) if r['id']=='D' else dict(r) for r in books]
print(choose_book(changed, 'animal', 90))
print(choose_book(books, 'animal', 50))'''
bc=a.add('sections',6,image={'type':'code','language':'python','text':bookcode,'title':'Complete pictured book ranking'})
D('sections',6,'Test the activity selector, then a separate book ranking','The book example uses illustrated/comic scores and ID ties, not activity fields.',[g('Predict activity order reversal and limit8',[12],'prompts'),g('Read the separate animal-book request and rows',[18,20,21]),g('Trace eligibility before preference scores',[p,24,26]),g('Predict D at91pages',[30],'prompts'),g('Check after predicting',[ch],'example',True),g('Run the complete pictured book ranking',[bc]),g('Explain why fewer pages alone does not win',[28,29],'prompts'),g('Pipeline extension · Predict valid boundary fields',[14],'reference',True)])
err=a.add('sections',7,'Claim to repair: The last tied activity should replace the current best. In the main activity contract, equal scores use ascending name, so A wins over B in either order. Compare that with the separate independent task’s shorter-page tie rule only when you reach that task. Do not silently substitute one policy for another. Test reversed order and no eligible items after repairing order dependence.')
D('sections',7,'Repair an order-dependent tie','Use the declared policy rather than whichever row happens to be last.',[g('Find the first policy mismatch',[err],'example'),g('Propose a case that would reveal it',[9],'prompts')])
D('sections',8,'Practise a no-match trace with less help','A schema rejection, an ineligible item and no eligible result are different outcomes.',[g('Repair an incorrect tied update',[8]),g('Complete main W2 using the original activity list',[11,12,13]),g('Repair an overclaim before discussion',[15,16,17],'prompts'),g('Explain the separate pictured ranking',[20,21,22],'prompts'),g('Keep independent work separate',[23]),g('Pipeline extension · Send only accepted rows to selection',[10,19],'reference',True)])
full='''from collections import Counter

def pipeline(raw, limit):
    if type(limit) is not int or not 0 <= limit <= 60:
        return {'error': 'invalid request'}
    names = Counter(r['name'] for r in raw if type(r) is dict
                    and type(r.get('name')) is str and r['name'])
    accepted, rejected = [], []
    for index, row in enumerate(raw, 1):
        reason = None
        if type(row) is not dict:
            reason = 'not a record'
        elif type(row.get('name')) is not str or not row['name']:
            reason = 'invalid name'
        elif names[row['name']] > 1:
            reason = 'duplicate name'
        else:
            for key, maximum in [('minutes',60),('fun',5),('learning',5)]:
                value = row.get(key)
                if type(value) is not int or not 0 <= value <= maximum:
                    reason = 'invalid ' + key
                    break
        if reason:
            rejected.append((index, reason))
        else:
            accepted.append(dict(row))
    eligible = [r for r in accepted if r['minutes'] <= limit]
    ranked = sorted(eligible, key=lambda r: (-(2*r['fun']+r['learning']),r['name']))
    scores = [(r['name'],2*r['fun']+r['learning']) for r in ranked]
    return {'winner': scores[0][0] if scores else None, 'ranked': scores,
            'accepted': len(accepted), 'rejected': rejected,
            'ineligible': [r['name'] for r in accepted if r['minutes']>limit]}

raw = [dict(name='A',minutes=20,fun=3,learning=2),
       dict(name='B',minutes=21,fun=5,learning=5),
       dict(name='C',minutes=12,fun=2,learning=4),
       dict(name='D',minutes=10,fun='4',learning=2)]
print(pipeline(raw,20))
print(pipeline(list(reversed(raw)),20)['ranked'])
print(pipeline(raw,0)['winner'])
print(pipeline(raw,True))'''
fc=a.add('sections',9,image={'type':'code','language':'python','text':full,'title':'Complete validation-to-ranking activity pipeline'})
l1=a.add('sections',9,'Predict before running: A and C score8 and qualify at20minutes; B is valid but too long; D fails the fun type. Expected accepted3of4, rejected row4, ineligibleB, ranked[(A,8),(C,8)], winnerA. Reverse the input to check the same ranking; rejection row numbers then refer to the new input order. Limit0 produces no eligible option; Boolean True is an invalid request, not a1-minute request.')
l2=a.add('sections',9,'Use this complete local pipeline for the investigation. Compare each output with your frozen Week32 expectations. Add duplicate copies of A: every A occurrence must be rejected under the planned duplicate policy, with C still eligible. Add a missing field, a Boolean rating, an empty list and a duration exactly20. Preserve original rows and rejection reasons. For the separate book example, run the supplied full ranking and changed-D case. Do not describe a written score rule as a trained model or its outputs as real learner preferences. Reserve the mystery-book independent task for its first attempt.')
D('sections',9,'Run a complete validation-to-ranking pipeline','Inspect accepted, rejected, ineligible and ranked records separately.',[g('The complete standalone implementation',[fc]),g('Predict the supplied results',[l1],'example'),g('Test boundaries and preserve evidence',[l2],'steps'),g('Keep expected and actual results',[5,6,7,9])])
for r,n,i in [('sections',9,4),('teacher',4,5)]:a.fix(r,n,i,'Run the supplied complete activity pipeline and pictured book ranking on fictional local records. Hand-check scores, reverse order, test duplicates and invalid fields, and compare a valid no-match result with an invalid request. No live learner profile is required.')
proj=a.add('sections',11,'Keep the implemented baseline with its schema and versioned score/tie contract, complete ranked output, exclusion reasons and acceptance results. The activity pipeline and book chooser illustrate separate schemas; use the book contract for the recommender project. Show a no-eligible-option result without relaxing a hard constraint. Preserve the human decision owner and state that written preference weights are neither learned preferences nor proof of learning benefit.')
D('sections',11,'Save a baseline that can be inspected and rerun','Keep the full trace beside the selected result.',[g('This week’s concrete contribution',[proj,12]),g('Keep the checkpoint and human choice',[4,5,6,7,8,9,10])])
note=a.add('sections',14,'This mystery-book assessment has its own score and tie policy: use the supplied mystery/page requirements,3genre+2illustration points and shorter-page tie. Do not reuse the worked activity name tie or animal-book ID tie. The supplied rows are fictional and complete for this comparison; no live lookup or new preference estimate is required.')
D('sections',14,'Try alone: rank the fresh mystery-book catalogue','Filter first and follow this task’s own stated tie policy.',[g('The independent records and policy',[1,note],'example'),g('Your first attempt and help record',[2,3,17]),g('Use feedback afterwards',[22])])
D('sections',16,'Finish: explain eligibility, score and tie separately','Show why the result follows from this contract and these inputs.',[g('Explain without notes',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
main=a.add('teacher',2,image=a.w['sections'][2]['blocks'][11]);vc=a.add('teacher',2,image=a.w['sections'][2]['blocks'][17]);tp=a.add('teacher',2,image=a.pic(2));bk=a.add('teacher',2,image={'type':'code','language':'python','text':bookcode,'title':'Complete pictured book ranking'})
D('teacher',2,'Model the activity state trace and separate book ranking','Keep schemas, scores and tie rules labelled.',[g('State main assumptions',[17]),g('Run and trace the activity selector',[main,18,27]),g('Read the separate animal-book dataset',[31,33,34]),g('Trace the book ranking and exclusions',[tp,37,39]),g('Predict the changed-D result',[43,44,45]),g('Run the complete pictured book code',[bk]),g('Explain the picture’s limits',[41,47]),g('Pipeline extension · Validate each row before selection',[22,vc,23,24],'reference',True)])
ref='Main activity example: B(fun3,learning2,minutes10), A(2,4,9), limit10; score2fun+learning; equal scores8 use ascending name. Both orders selectA;limit8or emptyinput returnsNone. Full pipeline uses exact integer ranges, rejects every duplicate-name occurrence and reports invalid rows separately from ineligible rows. Separate animal-book picture uses illustrated/comic points and ID ties; independent mystery task has its own shorter-page tie.'
extras={n:[a.add('workbook',n,ref)] for n in [12,13,14,16]};extras[4]=[a.add('workbook',4,a.w['sections'][13]['blocks'][note]['text'])]
a.records('Rank the new mystery catalogue independently','Use the selected independent book task’s exact constraints, score and shorter-page tie.',[(12,'W1 · Trace the main activity tie','Explain the best-so-far change using the written policy.'),(13,'W2 · Handle no match','Trace an empty list and the main example under limit8.'),(14,'W3 · Repair order dependence','Declare the correct tie policy and rerun both orders.'),(16,'W5 · Explain the additional activity practice','Keep the supplied X/Y/Z practice distinct from the selected book assessment.')], 'MainactivityA/B scores8 tieA;limit8None. Fullpipeline acceptsA/B/C, rejectsDtextfun;Bvalidbutineligible;A/Cscore8tieA. Reversedrankunchanged;zero limitNone;Trueinvalid;duplicatedAallreject,Ccanwin. BookpictureA2,B1,D3,Cexcludedsubject;D91excludedthenA2wins. Selectedindependentmystery:Delengthfail,Fgenrefail;E3,G5,H5;Hshorter90beatsG95. X/Y/Zisadditionalactivitypractice,nottheselectedassessment.','Building the data pipeline',extras)
a.fix('teacher',6,12,'Selected independent mystery task: D fails length, F fails subject; E scores3 and G/H5; H wins the shorter-page tie90<95. Require the filtering and score trace. Fresh book retry: requestanimal,max80pages; score2illustrated+1comic,tieID; J animal80 plaincomic, K animal70 illustratedprose, L space60 illustratedcomic. Expected J1,K2;Lexcluded;Kselected. Collect before feedback and record support used. The older X/Y/Z activity task remains additional practice with its own key.')
a.fix('teacher',6,13,'Next is Week34: Test Diverse Users. Reuse the implemented baseline, contract, complete traces and expected outputs when auditing cases and failure conditions.')
o=routes(('Validate. Filter. Score. Apply the declared tie.','Build a reproducible baseline with complete local code and explicit exclusions.','Compact selector → state trace → separate book ranking → complete pipeline → independent catalogue.'),('Teach the code together with its assumptions and tests.','Run all supplied code, keep policies separate and assess the selected mystery-book case before feedback.','Require rejected versus ineligible counts and a tie explanation tied to the current task.'),('One connected implementation record, with a validation extension.','Trace the selector, handle no match, repair ties and explain practice before the independent catalogue.','Retain code version, accepted/rejected rows, ranked output, expected results and limitations.'))
v=list(o['workbook']);mainorder=[1,12,13,14,16,4,9,22,10];v[3]=mainorder+[i for i in range(1,27) if i not in mainorder];v[4]=[('Recall',1),('Trace',12),('No match',13),('Repair ties',14),('Explain',16),('Try alone',4)];o['workbook']=tuple(v)
from connected_teacher_lab_keys import apply
apply(a,33)
a.finish(o)
