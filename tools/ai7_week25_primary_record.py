"""Analyze stipulated primary-study records; no actual model experiment."""
from fractions import Fraction

def completion_summary(passes,failures,unassessed):
 values=(passes,failures,unassessed)
 if any(type(x) is not int or x<0 for x in values) or sum(values)==0:raise ValueError('nonnegative integer counts and positive eligible total required')
 completed=passes+failures;eligible=completed+unassessed
 return {'passes':passes,'failures':failures,'unassessed':unassessed,'completed':completed,'eligible':eligible,
         'completed_pass_rate':Fraction(passes,completed) if completed else None,
         'coverage':Fraction(completed,eligible)}
main=completion_summary(16,2,2)
assert main['completed_pass_rate']==Fraction(8,9) and main['coverage']==Fraction(9,10)
A=[1,0,1,1,0,1];B=[1,1,1,0,1,1]
paired=[{'case_id':f'C{i+1}','A':a,'B':b,'B_minus_A':b-a} for i,(a,b) in enumerate(zip(A,B))]
a_only=[r['case_id'] for r in paired if r['A']==1 and r['B']==0]
b_only=[r['case_id'] for r in paired if r['A']==0 and r['B']==1]
assert sum(A)==4 and sum(B)==5 and a_only==['C4'] and b_only==['C2','C5']
assert completion_summary(0,0,2)['completed_pass_rate'] is None
print('Main supplied completion summary:',main)
print('Separate frozen six-case picture:',paired)
print('A-only correct:',a_only,'B-only correct:',b_only,'net B-A:',sum(B)-sum(A))
print('Net one extra correct is not one changed case: three paired cases differ. Unassessed cases remain unknown.')
print('A version tuned after inspecting C4 is a post-inspection revision. Same-set rescoring is development evidence; its new outputs are not supplied.')
print('No model is run, no outage is induced, no significance or population advantage is established, and a revised score is not invented.')
