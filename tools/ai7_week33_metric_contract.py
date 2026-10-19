"""A distinct numerical fixture demonstrating metric contracts, not a real reproduction."""
from fractions import Fraction

def error_metrics(predictions,targets):
 if not isinstance(predictions,(list,tuple)) or not isinstance(targets,(list,tuple)) or not predictions or len(predictions)!=len(targets):raise ValueError('same nonempty case lists required')
 if any(type(v) is not int for v in list(predictions)+list(targets)):raise ValueError('exact integer fixture values required')
 errors=[p-y for p,y in zip(predictions,targets)];n=len(errors)
 return {'errors':errors,'MAE':Fraction(sum(abs(e) for e in errors),n),'MSE':Fraction(sum(e*e for e in errors),n)}
# Added constructed fixture: original report supplies no numerical residuals.
fixture=error_metrics([1,3],[1,1])
assert fixture['errors']==[0,2] and fixture['MAE']==1 and fixture['MSE']==2
picture={'original_correct':5,'rerun_correct':4,'total':6,'disputed_case':'Q3','saved_file_available':'not verified by this program'}
assert Fraction(picture['original_correct']-picture['rerun_correct'],picture['total'])==Fraction(1,6)
print('Separate constructed metric fixture:',fixture)
print('Supplied six-case scoring disagreement:',picture)
print('Inspect saved Q3 output, reference label and rubric before adjudication. Do not choose the larger score or average incompatible scoring decisions.')
print('If the saved Q3 file is missing, exact verification of that case is unresolved. Record the missing artifact and any assistance; do not fabricate the file or a successful independent check.')
print('No other operator, new model output, full-study reproduction or new-data replication is executed here. This local fixture only demonstrates MAE versus MSE.')
