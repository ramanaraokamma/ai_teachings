"""Arithmetic on invented timing observations; this is not a benchmark."""
from math import isfinite
from statistics import median, mean

def timing_summary(seconds, count, method='median'):
    if type(count) is not int or count <= 0 or not seconds:
        raise ValueError('Need a positive integer count and timed passes')
    if any(not isfinite(t) or t <= 0 for t in seconds):
        raise ValueError('Times must be finite and positive')
    if method not in ('median','mean'):
        raise ValueError('Unknown summary method')
    duration = (median if method=='median' else mean)(seconds)
    return duration, 1000*duration/count, count/duration

def parameters(widths):
    if len(widths)<2 or any(type(n) is not int or n<=0 for n in widths):
        raise ValueError('Need at least two positive integer layer widths')
    weights=sum(m*n for m,n in zip(widths,widths[1:]))
    biases=sum(widths[1:])
    return weights,biases,weights+biases

a=timing_summary([2.0,2.2,1.8],100)
b=timing_summary([1.2,1.1,1.3],100)
def eligible(correct,count,ms,minimum_correct,maximum_ms):
    return correct>=minimum_correct and ms<=maximum_ms
assert a==(2.0,20.0,50.0) and b[:2]==(1.2,12.0)
assert eligible(92,100,a[1],91,25) and not eligible(90,100,b[1],91,25)
assert eligible(90,100,b[1],90,25)
print('Main median summaries: seconds, ms/example, examples/second',a,b)
print('Relative time reduction:',(a[1]-b[1])/a[1])
print('Relative throughput increase:',(b[2]-a[2])/a[2])
print('Timed passes per model: 3 × 100 = 300 prediction executions')
print('Plus warm-up: 100 more executions; quality sample remains 100 distinct cases')
w,bi,total=parameters([4,3,2])
assert (w,bi,total)==(18,5,23)
print('Dense weights, biases, total, raw bytes:',w,bi,total,total*4)
p=timing_summary([.32,.40,.48],40,'mean')
q=timing_summary([.20,.24,.28],40,'mean')
assert abs(p[1]-10)<1e-12 and abs(q[1]-6)<1e-12
print('Separate picture mean summaries:',p,q)
print('Picture quality:',38/40,36/40,'required:',.93)
# No peak memory, request latency, power or carbon measurements are supplied.
