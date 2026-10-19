"""Descriptive ablation arithmetic on supplied summaries; no real AI actions."""
from fractions import Fraction

def ablation_drop(full, removed, total):
 if any(type(x) is not int for x in (full,removed,total)) or total<=0 or not 0<=full<=total or not 0<=removed<=total:
  raise ValueError('require integer counts within a positive common denominator')
 return {'count_drop':full-removed,'percentage_point_drop':100*Fraction(full-removed,total)}
main_retrieval=ablation_drop(8,5,10)
main_validation=ablation_drop(8,7,10)
picture=ablation_drop(8,6,10)
assert main_retrieval['count_drop']==3 and main_validation['count_drop']==1
assert picture['percentage_point_drop']==20
# Two possible joint-removal outcomes, neither supplied by the actual exercise.
# Full R+V = 8; R only = 7; V only = 5. Neither component = unknown.
def interaction_contrast(neither):
 if type(neither) is not int or not 0<=neither<=10:raise ValueError('invalid hypothetical count')
 return 8-7-5+neither
assert interaction_contrast(4)==0 and interaction_contrast(6)==2
print('Main retrieval removal:',main_retrieval)
print('Main validation removal:',main_validation)
print('Separate filter picture:',picture)
print('Main no-validation condition also permits a stipulated unauthorized action; a one-pass drop does not make that boundary unimportant.')
print('Joint-removal outcome is UNKNOWN. Hypothetical neither counts 4 versus 6 give interaction contrasts 0 versus 2; these are counterexamples, not observations.')
print('Counts give net changes, not the identities of changed cases. No model, study, external action, significance test or universal causal attribution is performed.')
