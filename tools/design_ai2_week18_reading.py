from connected_level_authoring import LevelAuthor,g,routes
a=LevelAuthor('ai-2/18');D=a.design
D('sections',1,'How can zero be valid while a missing value is not?','Use the written type and range rules instead of a truthiness shortcut.',[g('Your learning goals',[1,2,3]),g('Recall text versus integer',[5,18],'prompts'),g('Your end goal',[20])])
meaning=a.add('sections',2,'Each duration row is one fictional activity session. This contract checks only the minutes field: an exact integer 0–60 inclusive. A missing field or explicit None means unknown here. A type or range rejection means this version cannot use the record for its numeric summary; preserve the row for review. Acceptance does not prove that the measurement is true.')
D('sections',2,'State the duration contract before filtering','Keep recorded zero, absent values and invalid values distinct.',[g('The activity-log problem',[11]),g('Row meaning, units and review scope',[meaning])])
syntax=a.add('sections',3,'get reads the minutes field without raising an error when the key is absent. The word and short-circuits: Python checks the exact type first and only tests the numeric bounds if that check succeeds. Thus None and text never reach a numeric comparison. type(value) is int also rejects Boolean True and False; arithmetic compatibility is not the same as this declared input contract.')
D('sections',3,'Trace the complete five-record filter','Keep source order, accepted values and rejected count visible.',[g('Predict and run the supplied script',[11],'example'),g('Explain get, append and the type-first condition',[syntax,13]),g('Match each raw value to the contract',[12,15]),g('Point to the deciding check',[17],'prompts')])
a.comparisons('Compare a valid boundary with an unknown value','Do not turn a rejected record into a guessed zero.')
p=a.add('sections',6,image=a.pic(2));ch=a.add('sections',6,image=a.pic(4))
countcode='''rows = [{"count": 0}, {"count": 4}, {},
        {"count": "4"}, {"count": True}, {"count": 9}]
accepted = []
review = []
for number, row in enumerate(rows, 1):
    value = row.get("count")
    if value is None:
        reason = "unknown count"
    elif type(value) is not int:
        reason = "count is not an exact integer"
    elif not 0 <= value <= 8:
        reason = "count outside 0 through 8"
    else:
        accepted.append(value)
        continue
    review.append((number, row.copy(), reason))
print(accepted)
print(len(review))'''
cc=a.add('sections',6,image={'type':'code','title':'Separate stock-count validator with retained reasons · Python3','text':countcode})
D('sections',6,'Extend the duration cases, then use a separate stock contract','Duration maximum60 and stock maximum 8 belong to different tasks.',[g('Predict the two added duration cases',[12],'prompts'),g('State the separate stock-count rule',[16,18,19]),g('Trace the pictured exact-type and range checks',[p,23]),g('Run the complete stock validator and retain reasons',[cc],'example'),g('Predict one authorised text conversion',[27],'prompts'),g('Check after predicting',[ch],'example',True),g('Explain Boolean rejection and the truth limit',[26,25],'prompts')])
D('sections',7,'Report what filtering leaves out','A statistic on accepted rows does not describe every supplied session.',[g('Keep the five-row coverage statement',[8]),g('Explain why2/5 belongs in the report',[9],'prompts')])
D('sections',8,'Replace if value with the explicit contract','Truthiness cannot distinguish allowed zero from invalid text.',[g('Expose both sides of the shortcut error',[8]),g('Trace the standalone W2 cases',[10,11,12]),g('Challenge successful run proves the conclusion',[14,15],'prompts'),g('Explain the separate stock Boolean case',[17,19])])
full='''rows = [{"minutes": 0}, {}, {"minutes": 12},
        {"minutes": -1}, {"minutes": None},
        {"minutes": 60}, {"minutes": "5"}, {"minutes": True}]
accepted = []
review = []
for number, row in enumerate(rows, 1):
    value = row.get("minutes")
    if value is None:
        reason = "unknown duration"
    elif type(value) is not int:
        reason = "duration is not an exact integer"
    elif not 0 <= value <= 60:
        reason = "duration outside 0 through 60"
    else:
        accepted.append(value)
        continue
    review.append((number, row.copy(), reason))
print(accepted)
print(len(review))'''
fc=a.add('sections',9,image={'type':'code','title':'Extended duration audit with retained review rows · Python3','text':full})
lab=a.add('sections',9,'Use the extended eight-record duration program supplied here. Before executing, record raw value, acceptance/review decision and first failing reason for each numbered row. The original five records accept2/5; adding60 and text"5" gives3/7; adding Boolean True gives3/8. Preserve those populations separately. Predict the accepted list and review count, then execute or label a paper trace. Inspect review to see retained row copies and reasons: unknown, non-integer or out of range. continue moves to the next row after a valid append; a rejected row reaches review.append. No source record is overwritten and no missing value is invented. Reserve the 0–10 independent count filter for W4.')
policies=a.add('sections',9,'Optional recommender policy extension, using fictional scenarios: P1 has an unrecorded length preference; P2 has a missing page count required by a hard limit; P3 has unknown stock; P4 has a reader-confirmed no preference. Compare asking for missing evidence, abstaining from the decision that needs it, and a declared configured fallback. State what remains unknown and any user effort; do not invent a reader reply or present a default as a measurement. P4 is a known preference statement, not missing data. These policy choices are separate from the numeric filter and cannot change an unknown measurement into observed zero.')
D('sections',9,'Audit eight supplied records and preserve every review reason','Distinguish baseline coverage from the expanded investigation.',[g('The complete extended duration program',[fc],'example'),g('Predict, trace, inspect and report coverage',[lab],'steps'),g('Keep the evidence and explain the limit',[5,6,7,9]),g('Optional policy extension · Four supplied scenarios',[policies],'reference',True)])
for r,n,i in [('sections',9,4),('teacher',4,5)]:a.fix(r,n,i,'Use the supplied extended eight-record duration audit for the main investigation. Retain accepted values and rejected row copies with reasons. The four explicitly supplied fictional recommender scenarios are an optional ask/abstain/fallback extension, not missing activity-log measurements.')
proj=a.add('sections',11,'For the fictional recommender, keep stock 0, missing stock and a reader-confirmed no preference as different states. Validate numeric fields against their own contract; do not silently convert text or fill unknown values. A partial score must disclose unknown components rather than claim a complete score. Record accepted and reviewed case counts, reasons, the chosen policy and the human next step. Use fictional profiles; do not ask real learners for extra personal information for this exercise.')
D('sections',11,'Keep numeric validation separate from preference policy','Defaults and confirmed preferences need honest labels.',[g('This week’s concrete portfolio contribution',[proj,12]),g('Keep the checkpoint and human choices visible',[4,5,6,7,8,9,10])])
policy=a.add('sections',14,'For this independent filter require exact Python int values, excluding Booleans, and inclusive bounds 0–10. Keep source order. Missing values are reviewed rather than imputed. The prompt’s row keys must be quoted when writing executable Python; this task uses a different field and maximum from the worked duration and stock cases.')
D('sections',14,'Try alone: implement the new 0–10 count contract','Write the new filter before consulting the key.',[g('The independent row list and question',[1],'example'),g('The exact-type and bounds policy',[policy]),g('Your first attempt and support record',[2,3,17]),g('Use feedback after the attempt',[22])])
D('sections',16,'Finish: explain a valid zero and an unavailable observation','State the contract, review reason and remaining coverage limit.',[g('Explain without notes',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
code=a.add('teacher',2,image=a.w['sections'][2]['blocks'][11]);ct=a.add('teacher',2,image={'type':'code','title':'Separate stock-count validator with retained reasons · Python3','text':countcode});tp=a.add('teacher',2,image=a.pic(2))
D('teacher',2,'Teach the type-first condition and preserved review records','Keep duration, stock and independent count contracts distinct.',[g('State the duration schema and supply its complete script',[17,code],'example'),g('Explain get, append and exact type',[18]),g('Collect the added 60/text 5 prediction',[23],'prompts'),g('State the separate stock schema and all its rows',[27,29,30]),g('Trace the Boolean and range decisions',[tp,34]),g('Run the complete stock reason-recording script',[ct],'example'),g('Predict and check an authorised conversion',[38,39,40]),g('Limit the inference and elicit picture reasoning',[36,25,42])])
ref='Duration reference: exact Python int, minutes 0–60 inclusive; None or absent minutes is unknown, and Boolean is not a count. Original rows in order:0,absent,12,-1,None. W2 supplies a separate four-value list. The original filter accepts2/5; the extended lab adds60,text"5",True and accepts3/8. Do not mix the separate stock maximum 8 or independent maximum 10 into this duration rule.'
extras={n:[a.add('workbook',n,ref)] for n in [12,13,14,16]};extras[4]=[a.add('workbook',4,'Independent policy: exact int only, inclusive count bounds 0–10; preserve input order and hold missing/type/range failures for review. Quote dictionary keys in Python.')]
a.common('Validate independently','Use an exact type and explicit bounds, preserve zero, retain review reasons and report the population that remains.',[(12,'W1 · Distinguish zero, absent and None','Explain what is measured and what is unknown.'),(13,'W2 · Trace four supplied durations','Keep exact type, range, order and rejection count.'),(14,'W3 · Repair a truthiness condition','Give a valid zero and invalid nonempty-text counterexample.'),(16,'W5 · Report rejected-record coverage','Use the original five-record population in this question.')], 'Original duration script accepts[0,12],rejects3 of5. Adding60 and text"5" gives[0,12,60],rejects4 of7; addingTrue gives the same list,rejects5 of8. Extended review IDs are2unknown,4range,5unknown,7type,8type. Separate stock accepts[0,4],rejects4; authorised conversion of text4 adds another4 and leaves3 rejected. get alone does not distinguish absent versus explicit None, which are both unknown under this schema. Exact type rejects Booleans; neither validation nor a configured policy establishes truth of a measurement. Reserve the 0–10 independent task for W4.',extras)
D('teacher',5,'Assess the selected independent count filter','Keep this key until after the first individual attempt.',[g('Selected W4 and checked key',[32,34],'example'),g('Judge implementation, trace and limits',[35,36]),g('Give one repair action',[38]),g('W1 zero/unknown key',[16,17]),g('W2 four-duration key',[19,20,21]),g('W3 condition-repair key',[23,24]),g('W5 coverage key',[29,30])])
a.fix('teacher',6,13,'Next is Week 19: Sampling and Representation. Carry forward supplied, accepted and reviewed counts; filtering can change which cases remain represented even when every retained value passes its contract.')
o=routes(('Read the contract. Keep zero. Preserve unknowns and reasons.','Validate missing, typed and bounded values without inventing measurements or hiding excluded cases.','Duration filter → separate stock contract → expanded reason audit → independent new bounds.'),('Teach validation as a declared decision with inspectable evidence.','Supply complete scripts and row populations, distinguish policy from measurement and reserve the new count filter for assessment.','Ask for raw value, exact type, bound, outcome, reason and coverage before accepting a report.'),('One connected missing-data validation record.','Distinguish zero and unknown, trace filtering, repair truthiness and explain which sessions are excluded.','Retain original rows, accepted order, review reasons, field-specific bounds and reported denominators.'))
a.finish(o)
