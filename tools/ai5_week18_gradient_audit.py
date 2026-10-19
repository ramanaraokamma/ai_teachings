# Separate pictured diagnostic: y = 2a + 3c, target 4; not the dense layer.
def loss(a, c):
    return (2*a + 3*c - 4)**2

def partials(a, c, h=.1):
    if h <= 0:
        raise ValueError('Need positive finite-difference spacing')
    return [(loss(a+h,c)-loss(a-h,c))/(2*h),
            (loss(a,c+h)-loss(a,c-h))/(2*h)]

old = [1.,0.]
labels = ['a','c']
reported = [-12.,-8.]  # Correct length, wrong coordinate assignment.
checked = partials(*old)
formula = [-8.,-12.]
tolerance = 1e-6
for name, bad, numerical, correct in zip(labels,reported,checked,formula):
    print(name, 'reported/numerical/formula', bad, round(numerical,6), correct)
    print('reported entry agrees', abs(bad-numerical)<tolerance)
assert all(abs(n-f)<tolerance for n,f in zip(checked,formula))
new = [p-.01*g for p,g in zip(old,formula)]
print('correct new [a,c]', [round(p,6) for p in new])
print('prediction/loss', round(2*new[0]+3*new[1],6), round(loss(*new),6))
print('same gradient in [c,a] order', [formula[1],formula[0]])
# Finite numeric values assumed; these probes do not cross an activation corner.
