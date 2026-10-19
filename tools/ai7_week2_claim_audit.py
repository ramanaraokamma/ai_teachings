"""Exact arithmetic on fictional claim counts, not a study or statistical test."""
from fractions import Fraction

def proportion(passed,total):
 if type(passed) is not int or type(total) is not int or total<=0 or not 0<=passed<=total:
  raise ValueError('valid exact count and positive denominator required')
 return Fraction(passed,total)
def compare_counts(a_pass,a_total,b_pass,b_total):
 a=proportion(a_pass,a_total);b=proportion(b_pass,b_total)
 return {'baseline_rate':a,'new_rate':b,'difference_percentage_points':100*(b-a),
         'rate_ratio':b/a if a else None,'relative_increase_percent':100*(b-a)/a if a else None}
main=compare_counts(5,8,6,8)
picture=compare_counts(2,10,4,10)
assert main['baseline_rate']==Fraction(5,8) and main['new_rate']==Fraction(3,4)
assert main['difference_percentage_points']==Fraction(25,2) and main['rate_ratio']==Fraction(6,5)
assert picture['difference_percentage_points']==20 and picture['rate_ratio']==2 and picture['relative_increase_percent']==100
# Added possible paired records: both fit the same main aggregate counts.
a=[True,True,True,True,True,False,False,False]
b_one_gain=[True,True,True,True,True,True,False,False]
b_gain_and_loss=[True,True,True,True,False,True,True,False]
def paired_changes(a,b):
 if not a or len(a)!=len(b) or any(type(v) is not bool for v in a+b):raise ValueError('matched Boolean fixtures required')
 return {'gains':sum(not x and y for x,y in zip(a,b)),'losses':sum(x and not y for x,y in zip(a,b))}
pattern_one=paired_changes(a,b_one_gain);pattern_two=paired_changes(a,b_gain_and_loss)
assert sum(a)==5 and sum(b_one_gain)==sum(b_gain_and_loss)==6
assert pattern_one=={'gains':1,'losses':0} and pattern_two=={'gains':2,'losses':1}
assert compare_counts(0,10,1,10)['rate_ratio'] is None
print('Main supported-answer rates:',main,'62.5 percent versus 75 percent on eight supplied cases.')
print('Separate picture correctness rates:',picture,'20 percent versus 40 percent on ten supplied cases.')
print('Two added possible paired patterns with identical main totals:',pattern_one,pattern_two)
print('Aggregates do not reveal every case outcome, individual learning, causal effect or population uncertainty. These are constructed counts/possible records, not a real paper, model run or statistical significance test.')
