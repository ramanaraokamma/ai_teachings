from connected_level_authoring import LevelAuthor,g,routes
a=LevelAuthor('ai-2/22');D=a.design
D('sections',1,'Which stored examples vote, and under which tie rule?','Order by distance before selecting neighbours or looking at query references.',[g('Your learning goals',[1,2,3]),g('Recall a stored tree before comparing methods',[5,18],'prompts'),g('Your end goal',[20])])
D('sections',2,'Store labelled training examples and declare the method','IDs identify rows and break distance ties; they are not measured features.',[g('The nearest-neighbour prediction idea',[11]),g('The complete five-row training pool',[12,13],'example'),g('Distance, k and the predefined ID rule',[14])])
D('sections',3,'Trace sorting, selection and voting in complete Python','Keep the labels out of distance calculation.',[g('Predict and execute the single-query script',[11],'example'),g('Read tuple sorting and the first-three slice',[12]),g('Explain what changes for k=1',[13]),g('Check the script’s declared assumptions',[14]),g('Point to the deciding step',[16],'prompts')])
a.comparisons('Compare a distance tie with a vote','A reproducible tie policy is not evidence that the chosen label is true.')
p=a.add('sections',6,image=a.pic(2));ch=a.add('sections',6,image=a.pic(4))
D('sections',6,'Explain the centimetre query, then a separate book-format example','The two training pools have different readings and category names.',[g('Trace the main query’s first three neighbours',[12,13]),g('Compare k=1 and k=3 before discussing',[14],'prompts'),g('Keep vote share distinct from a calibrated probability',[15]),g('Read the separate four-book pool and tie rules',[19,21,22]),g('Trace the book-query order and predictions',[p,27]),g('Predict the moved book query',[31],'prompts'),g('Check after predicting',[ch],'example',True),g('Explain disagreement and the representation limit',[30,29],'prompts')])
D('sections',7,'A query must not bring its answer into the training pool','An exact feature match does not certify a true label.',[g('Retain feature-scale and split limits',[8,9]),g('Challenge a self-neighbour perfect score',[10],'prompts')])
D('sections',8,'Score the frozen method on all three supplied validation queries','Keep the baseline on the same references.',[g('Read the query references and selected IDs',[8]),g('Compare the training-majority baseline and preserve the final test',[9]),g('Practise the neighbour/tie rules in W2',[11,12,13]),g('Repair the negative-distance misconception',[15,16],'prompts'),g('Explain the separate book k disagreement',[18,20])])
full='''train = [("A", 2, "blocked"), ("B", 4, "clear"),
         ("C", 8, "clear"), ("D", 10, "blocked"),
         ("E", 12, "clear")]
def predict(query, k):
    ranked = sorted((abs(x - query), item_id, label)
                    for item_id, x, label in train)
    near = ranked[:k]
    labels = [row[2] for row in near]
    prediction = "clear"
    if labels.count("blocked") > labels.count("clear"):
        prediction = "blocked"
    return [row[1] for row in near], prediction
for k in [1, 3]:
    print("query3", k, predict(3, k))
validation = [(3, "blocked"), (9, "blocked"), (11, "clear")]
training_labels = [row[2] for row in train]
baseline = "clear"
if training_labels.count("blocked") > training_labels.count("clear"):
    baseline = "blocked"
correct = baseline_correct = 0
for query, reference in validation:
    ids, prediction = predict(query, 3)
    print(query, ids, prediction, reference)
    correct += prediction == reference
    baseline_correct += baseline == reference
print("validation", correct, len(validation))
print("baseline", baseline, baseline_correct, len(validation))'''
ci=a.add('sections',9,image={'type':'code','title':'Complete neighbour and frozen-validation comparison · Python3','text':full})
lab=a.add('sections',9,'Use only the supplied five training rows. Predict all five distances for query3, then selected IDs and labels under k1 and k3. Keep the distance/ID rule unchanged. Next predict all selected IDs for validation queries3,9,11 using k3, before comparing with their supplied references. Run the complete program or label a paper trace. The function receives query and k, not the query reference; the reference is used only after prediction for scoring. Its declared contract requires unique IDs, numeric readings, allowed clear/blocked labels and1<=k<=training count; this teaching code does not implement those validations. Retain each error, selected IDs, settings and training-majority baseline result. Record any later k search as development and preserve a final test. Reserve the new P–T pool for independent W4.')
D('sections',9,'Audit the complete stored-pool prediction and validation process','Do not invent training examples or add validation answers to the pool.',[g('The runnable unchanged-training comparison',[ci],'example'),g('Predict, order, vote, score and preserve',[lab],'steps'),g('Keep the evidence and scope',[5,6,7,9])])
for r,n,i in [('sections',9,4),('teacher',4,5)]:a.fix(r,n,i,'Use the supplied five-row training pool, query3 and the three validation records. Record distances, selected IDs, k, votes and predefined ties; compare the frozen k3 method and training-majority baseline without adding query answers to training.')
proj=a.add('sections',11,'For the fictional recommender, identify the stored training examples, selected features, distance, k and tie policies before explaining a neighbour-based prediction. Keep the new case’s label out of the stored pool. Retain neighbour IDs and distances so a human can inspect the evidence. Liked neighbours and vote fractions do not guarantee a good recommendation or a probability of enjoyment; validate any hard requirements separately.')
D('sections',11,'Keep neighbour evidence beside the recommender result','Explain why those examples were close and which information was unavailable.',[g('This week’s concrete contribution',[proj,12]),g('Keep the checkpoint and human decision',[4,5,6,7,8,9,10])])
rule=a.add('sections',14,'Use numeric absolute distance in centimetres, unique training IDs, distance then alphabetical-ID ordering, and unweighted selected-label votes. Predict before comparing with validation references. The stated binary k1/k3 votes cannot tie; distance ties still require the ID policy. Choose the baseline from the new training labels, not validation answers.')
D('sections',14,'Try alone: use the new P–T training pool','Keep its query and validation records separate from the worked pool.',[g('The independent training and validation brief',[1],'example'),g('Method and tie policy',[rule]),g('Your first attempt and support record',[2,3,17]),g('Use feedback after the attempt',[22])])
D('sections',16,'Finish: explain the stored evidence and the prediction limit','State distance, neighbour IDs, k, ties and the reference-free prediction path.',[g('Explain without notes',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
code=a.add('teacher',2,image=a.w['sections'][2]['blocks'][11]);tc=a.add('teacher',2,image={'type':'code','title':'Complete neighbour and frozen-validation comparison · Python3','text':full});tp=a.add('teacher',2,image=a.pic(2))
D('teacher',2,'Teach order, selection and voting before scoring','Supply complete programs and keep the book pool distinct.',[g('Introduce stored training and the full numeric pool',[17,18,19]),g('Trace the single-query program',[code,20,21,22],'example'),g('Collect the main k comparison and probability limit',[27,28,29,30]),g('Show the full validation and baseline program',[tc],'example'),g('Read the separate four-book pool',[34,36,37]),g('Trace the book-query order and k choices',[tp,42,44]),g('Move only the book query',[46,47,48]),g('Elicit the picture explanation',[32,50])])
ref='Worked training A2 blocked,B4 clear,C8 clear,D10 blocked,E12 clear; unitscm. Distance is absolute difference, distance ties sort alphabetically by ID. Compare k1/k3; k3 votes by majority of stored labels. Worked validation queries/references:(3,blocked),(9,blocked),(11,clear). The baseline is training-majority clear. The separate compact/extended book pool has different rows and is not used for this validation.'
extras={n:[a.add('workbook',n,ref)] for n in [12,13,14,16]};extras[4]=[a.add('workbook',4,'Use the new P–T training pool supplied in W4. Distance is absolute gap, equal distances use alphabetical ID order and k3 votes use the three stored labels; do not add validation references to training.')]
a.common('Find neighbours independently','Keep training storage, numeric distance, k, tie policies and reference-free prediction explicit before evaluation.',[(12,'W1 · Calculate all five feature distances','Labels do not affect the numeric gap.'),(13,'W2 · Apply k and the declared distance tie-break','Changing the number of voters can change the prediction.'),(14,'W3 · Keep query answers out of the pool','Use all three supplied validation records and the same baseline.'),(16,'W5 · Limit a vote fraction and an exact match','Neither establishes calibrated correctness or full suitability.')], 'Query3 distances1,1,5,7,9; k1 selectsA blocked, k3 selectsA/B/C clear. Validation triples areA/B/C,C/D/E,D/E/C; all predictclear, matching only the third reference:1/3. Training-majority clear also1/3. The separate book query7 givesB/C/A/D, k1extended,k3compact; query9 givesC/B/D/A,k1compact,k3extended. These pools and labels are different. Never add query references before prediction, and do not call2/3 votes a calibrated probability. Reserve P–T for independent W4.',extras)
a.replace_text('as in Week 6.','as in Week 11.')
a.replace_text('Next week we will address scaling and learn any scaling values from training data only.','Any learned scaling values must come from training only. Next is Week23, Recommendation Scores; retain explicit feature and weighting choices rather than treating raw closeness as objective quality.')
a.fix('teacher',6,13,'Next is Week23: Recommendation Scores. Carry forward feature definitions, training-only evidence, distance and tie policies when contrasting a nearest-neighbour prediction with a declared recommendation score.')
o=routes(('Measure the gaps. Select the neighbours. Vote before scoring.','Use stored examples under declared k and tie rules without leaking query answers into prediction.','Training pool → numeric ordering → k comparison → frozen validation and baseline.'),('Teach a neighbour classifier as an inspectable reference-free prediction path.','Supply complete scripts and validation records, separate the book example and reserve the new pool for assessment.','Require neighbour IDs, distances, votes and settings beside the prediction and score.'),('One connected nearest-neighbour record.','Measure distances, apply k/ties, preserve split independence and limit vote/probability claims.','Retain training rows, query values, selected IDs, predictions, references and baseline separately.'))
a.finish(o)
