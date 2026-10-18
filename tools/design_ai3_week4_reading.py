from connected_extended_authoring import ExtendedAuthor,g
from connected_level_authoring import routes
from connected_paragraphs import format_additions
a=ExtendedAuthor('ai-3/4');D=a.design
D('sections',1,'How does the same draw change under a different distribution?','Trace sampling boundaries and positive temperature without claiming factual accuracy.',[g('Your learning goals',[1,2,3]),g('Recall greedy versus whole paths',[5,17],'prompts'),g('Your end goal',[22]),g('Attention extension · Permitted normalised weights',[19,20],'reference',True)])
D('sections',2,'Define sampling intervals before selecting a token','The left endpoint belongs to the interval; the right endpoint does not.',[g('The complete red/blue/green distribution and interval contract',[11]),g('Separate repeated frequencies from a single trace',[12]),g('Attention extension · Scores, scale and stable softmax',[14,15],'reference',True)])
D('sections',3,'Calculate the positive-temperature transformation','For this half-temperature example, square then normalise.',[g('The stated formula and exact adjusted probabilities',[11]),g('Compare the original and adjusted tables',[12]),g('Trace the same draw under both distributions',[13]),g('Explain the deciding evidence',[19],'prompts'),g('Attention extension · Query/key/value roles and exact ratio',[15,16,17],'reference',True)])
a.comparisons('Compare changed intervals with unchanged factual evidence','A more concentrated distribution is not a source of new truth.')
p=a.add('sections',6,image=a.pic(2));ch=a.add('sections',6,image=a.pic(4))
D('sections',6,'Explain the temperature limit, then a separate two-token picture','Keep the three-colour and A/B distributions distinct.',[g('Compare positive temperatures without changing rank',[12]),g('Reject substituting zero into this formula',[13]),g('Read the separate two-token distribution and draw',[20,22,23]),g('Trace squared weights and exact intervals',[p,26,28]),g('Predict the changed draw0.97',[32],'prompts'),g('Check after predicting',[ch],'example',True),g('Explain remaining probability and truth limits',[30,31],'prompts'),g('Attention extension · Equal scores and masks',[15,16],'reference',True)])
err=a.add('sections',7,'Claim to repair: Lower temperature made red more likely, so red is more accurate. The operation transforms probabilities and sampling intervals. It does not supply evidence about the actual colour. A highly consistent wrong token remains wrong. In the two-token picture B retains probability1/17 at T=0.5; less likely is not impossible, and u=0.97 still selects B.')
D('sections',7,'Separate consistency from correctness','Inspect factual support with its own reference rather than inferring it from concentration.',[g('Repair the lower-temperature truth claim',[err],'example'),g('Design a revealing fixed-draw comparison',[9],'prompts')])
D('sections',8,'Practise exact boundary draws with less help','Keep exact fractions when a draw lies near an endpoint.',[g('Read and trace the three supplied draws',[8,9],'prompts'),g('Complete main temperature W2',[13,14,15]),g('Repair sampling means equal chances',[17,18,19],'prompts'),g('Explain the separate A/B picture',[22,23,24],'prompts'),g('Keep independent work separate',[25]),g('Attention extension · Stable common-shift calculation',[11,12,21],'reference',True)])
code='''from fractions import Fraction as F

def half_temperature(p):
    if not p or any(x<=0 for x in p) or sum(p)!=1:
        raise ValueError('positive probabilities summing to one required')
    weights = [x*x for x in p]
    return [x/sum(weights) for x in weights]

def sample(p,u):
    if not p or any(x<0 for x in p) or sum(p)!=1 or not 0<=u<1:
        raise ValueError('invalid distribution or draw')
    cumulative=F(0)
    for index,probability in enumerate(p):
        cumulative+=probability
        if u<cumulative:
            return index
    raise AssertionError('complete exact distribution must select an interval')

labels=['red','blue','green']
p=[F(6,10),F(3,10),F(1,10)]
q=half_temperature(p)
print('T=0.5:',q)
for u in [F(2,10),F(6,10),F(9,10)]:
    print(u,labels[sample(p,u)],labels[sample(q,u)])
draws=[F(1,10),F(4,10),F(7,10),F(85,100),F(97,100)]
for name,distribution in [('T=1',p),('T=0.5',q)]:
    outputs=[labels[sample(distribution,u)] for u in draws]
    print(name,outputs,{label:outputs.count(label) for label in labels})'''
ci=a.add('sections',9,image={'type':'code','language':'python','text':code,'title':'Complete exact half-temperature and cumulative-interval simulation'})
l1=a.add('sections',9,'Complete controlled paper/local experiment: fixed prefix Next colour:, token order red/blue/green, original distribution0.6/0.3/0.1, draws0.1,0.4,0.7,0.85,0.97. Compare T=1 and the stated T=0.5 transformation using the same draws. Predict all outputs and category counts, then run the supplied program or make an explicitly labelled paper trace. These are paired deterministic traces of recorded draws, not five new random trials or actual language-model stories.')
l2=a.add('sections',9,'For a separate factual check, supplied fictional reference R says the current flag is blue. Score each generated colour label against that reference. Both five-draw traces have two blue outputs, even though the adjusted distribution produces red more often. The experiment demonstrates changed sampling behavior and a distinction between consistency and reference agreement; it does not establish an optimal model setting, general factual accuracy or educational benefit. Keep the independent A/B/C table withheld.')
D('sections',9,'Run a complete fixed-draw comparison','Hold prompt, candidates and draws fixed while changing the stated distribution transformation.',[g('Predict the controlled setup',[l1],'steps'),g('Run the complete exact-arithmetic simulation',[ci]),g('Compare consistency with separate supplied evidence',[l2],'steps'),g('Keep the investigation record',[5,6,7,9])])
for r,n,i in [('sections',9,4),('teacher',4,5)]:a.fix(r,n,i,'Use the supplied fixed prefix, three-colour table and five recorded draws with the complete local simulation. Compare output counts and agreement with fictional blue-flag reference R separately. These are toy paired traces, not actual prompt runs, stories or model-quality measurements.')
proj=a.add('sections',11,'For the Verified Study Buddy, record generation settings and keep unrelated settings fixed during a comparison. Evaluate supported facts, response format and task usefulness separately from output similarity. A lower-variability policy may be a hypothesis for a structured task, but the project must test its own criteria; temperature alone does not verify factual claims. The classroom simulation supplies no recommendation about a deployed service’s best settings.')
D('sections',11,'Treat a generation setting as a policy to evaluate','Keep the source checks regardless of observed variability.',[g('This week’s concrete contribution',[proj,12]),g('Keep the checkpoint and human choice',[4,5,6,7,8,9,10])])
ix=a.add('sections',14,'Use exact fractions for squared weights and cumulative boundaries. Intervals are left-inclusive,right-exclusive in A,B,C order. Zero temperature is outside the stated formula. The task provides no factual reference for these labels, so explain the procedural comparison without calling either output true.')
D('sections',14,'Try alone: transform the fresh A/B/C table','Trace both distributions before interpreting the result.',[g('Independent table and scope',[1,ix],'example'),g('Your first attempt and help record',[2,3,17]),g('Use feedback afterwards',[22])])
D('sections',16,'Finish: explain the interval, transformation and truth boundary','A fixed-draw trace makes the numerical decision reproducible.',[g('Explain without notes',[0,1],'prompts'),g('Plan a changed-case return',[2,3])])
tp=a.add('teacher',2,image=a.pic(2));table=a.add('teacher',2,image=a.w['sections'][2]['blocks'][12]);att=a.add('teacher',2,image=a.w['sections'][2]['blocks'][15])
D('teacher',2,'Model exact sampling before discussing variability','Keep the main three-colour table, pictured A/B table and attention scores separate.',[g('State half-open intervals and repeated-draw scope',[17,18]),g('Calculate the half-temperature probabilities',[19,table]),g('Distinguish positive transformation and zero policy',[29,30]),g('Read the separate two-token picture',[34,36,37]),g('Trace its normalisation and same draw',[tp,40,42]),g('Predict u0.97',[46,47,48]),g('State what remains unproven',[44,50]),g('Attention extension · Stable softmax and weighted values',[23,24,att,25,26],'reference',True)])
ref='Main table order red,blue,green with probabilities0.6,0.3,0.1. Intervals[0,0.6),[0.6,0.9),[0.9,1). T=0.5 squares and normalises:18/23,9/46,1/46; boundaries18/23,45/46,1. Separate pictured A/B probabilities0.8/0.2 become16/17,1/17. Do not substitute those boundaries into the main table.'
extras={n:[a.add('workbook',n,ref)] for n in [12,13,14,16]};extras[4]=[a.add('workbook',4,a.w['sections'][13]['blocks'][ix]['text'])]
a.records('Sample a new table independently','Require exact adjusted probabilities, interval endpoints and a separate factual-evidence limit.',[(12,'W1 · Trace interval boundaries','Reject the draw1 under the stated half-open contract.'),(13,'W2 · Compute the adjusted table','Square, total and normalise with exact fractions.'),(14,'W3 · Compare a fixed draw','Do not infer factual improvement from a changed token.'),(16,'W5 · Specify a controlled experiment','Fix task, model conditions and evaluation criteria before comparison.')], 'Main adjusted probabilities18/23,9/46,1/46; recorded0.2/0.6/0.9 give red/blue/green atT1 and red/red/blue atThalf. Five paired draws give red,red,blue,blue,green versus red,red,red,blue,blue; blue-reference agreement2/5 in each. Separate A/B u0.85 switchesBtoA;u0.97Bboth;Bnotimpossible. Attention weights1/4,3/4 output5;maskBoutput2; equal-score2Doutput[1,2]; common shift preserves ratios. Independent table probabilities25/38,9/38,4/38 and boundaries25/38,34/38; reserve its first attempt.','A small attention calculation',extras)
for n in [17,18,19,21]:
 b=a.add('workbook',n,'Attention extension reference: q=[1],keys[0],[ln(3)],values[2],[6],width1. Scores0,ln(3); stable softmax subtracts their maximum before exponentiation. For the separate equal-score example q=[1,1],keys[1,0],[0,1],values[2,0],[0,4],divide scores bysqrt(2). Mask before normalisation; reject incompatible key/query widths. These weights do not verify source truth.')
 D('workbook',n,'Extension · '+a.w['workbook'][n-1]['title'],'Use the declared dimensions, values and score procedure beside this task.',[g('Contract, question and response',[b]+list(range(len(a.original['workbook'][n-1]['blocks']))),'prompts')],True)
a.fix('teacher',6,13,'Next is Week5: Prompt as a Contract. Carry forward controlled conditions, explicit output rules and separate evidence criteria before comparing prompt specifications.')
o=routes(('Fix the draw. Transform the table. Check the interval.','Compare positive-temperature sampling without mistaking consistency for factual correctness.','Interval contract → exact transformation → two-token picture → paired traces → independent table.'),('Teach the numerical mechanism and evidence boundary together.','Use exact fractions and complete draw records, preserve the attention extension and collect the fresh table before feedback.','Ask which inputs changed, which stayed fixed and which factual reference was actually supplied.'),('One connected sampling record, with a small attention extension.','Trace boundaries, calculate probabilities, compare a draw and specify a fair experiment.','Retain token order, exact intervals, draws, transformations, outcomes and separate reference checks.'))
v=list(o['workbook']);main=[1,12,13,14,16,4,9,22,10];v[3]=main+[i for i in range(1,27) if i not in main];v[4]=[('Recall',1),('Intervals',12),('Temperature',13),('Fixed draw',14),('Experiment',16),('Try alone',4)];o['workbook']=tuple(v)
format_additions(a);a.finish(o)
