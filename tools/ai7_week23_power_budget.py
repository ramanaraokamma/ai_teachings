"""Summarize stipulated alternative-model simulation counts; do not simulate trials."""
from fractions import Fraction

def summarize(detections,trials,n,cost_per_unit):
 if any(type(x) is not int for x in (detections,trials,n,cost_per_unit)) or trials<1 or n<1 or cost_per_unit<1 or not 0<=detections<=trials:
  raise ValueError('valid integer trial counts, sample size and positive unit cost required')
 return {'detection_fraction':Fraction(detections,trials),'per_study_cost':n*cost_per_unit,
         'stated_simulation_work_cost':trials*n*cost_per_unit}
main_small=summarize(62,100,20,3);main_large=summarize(83,100,40,3)
picture_small=summarize(60,100,20,2);picture_large=summarize(80,100,40,2)
assert main_small['per_study_cost']==60 and main_large['per_study_cost']==120
assert 100*(main_large['detection_fraction']-main_small['detection_fraction'])==21
assert picture_small['per_study_cost']==40 and picture_large['per_study_cost']==80
assert picture_large['detection_fraction']-picture_small['detection_fraction']==Fraction(1,5)
print('Main summaries:',main_small,main_large)
print('Separate picture summaries:',picture_small,picture_large)
print('Per-study cost differs from total hypothetical work across 100 simulation trials; the latter is arithmetic, not measured compute or billing.')
print('These are supplied finite-trial detection frequencies under a fixed alternative, not executed simulations, exact known power or guaranteed real-study success.')
print('No null trials are supplied: false-positive rate is unknown. Changed effect/variability requires new model-specific planning; no new detection frequency is invented.')
