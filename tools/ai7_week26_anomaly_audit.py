"""Describe supplied valid durations without erasing inconvenient observations."""
from fractions import Fraction

def timing_summary(values):
 if not isinstance(values,(list,tuple)) or not values or any(type(v) is not int or v<0 for v in values):raise ValueError('nonempty nonnegative integer durations required')
 ordered=sorted(values);n=len(values)
 middle=Fraction(ordered[n//2]) if n%2 else Fraction(ordered[n//2-1]+ordered[n//2],2)
 return {'count':n,'mean_seconds':Fraction(sum(values),n),'median_seconds':middle}
main_values=[1,2,2,15];before=main_values[:];main=timing_summary(main_values)
picture_values=[2,2,2,10];picture=timing_summary(picture_values)
# Wrong-deletion illustration only, never replaces either retained record.
hypothetical_main_deleted=timing_summary(main_values[:-1])
hypothetical_picture_deleted=timing_summary(picture_values[:-1])
assert main['mean_seconds']==5 and main['median_seconds']==2 and main_values==before
assert picture['mean_seconds']==4 and picture['median_seconds']==2
print('Retained main valid durations:',main_values,main)
print('Retained separate picture durations:',picture_values,picture,'fourth trace logs a source timeout')
print('Illustrative wrong deletion would change main mean to',hypothetical_main_deleted['mean_seconds'],'and picture mean to',hypothetical_picture_deleted['mean_seconds'])
print('These deletion summaries demonstrate distortion only; original valid observations and the planned timeout inclusion are retained.')
print('A timeout log is a recorded event, not a complete root-cause diagnosis. A genuine measurement correction needs evidence and provenance, not dislike of an outcome.')
print('No response is timed, no timeout is generated, and no causal explanation or population tail estimate is established.')
