# Separate two-unit symmetry example, not the scalar-v training experiment.
# Parameters are in fixed order [u, v, a, b]. No random initialization is used here.
def output(params, x):
    u, v, a, b = params
    return a * max(0, u*x) + b * max(0, v*x)

def update(params, x, target, rate):
    u, v, a, b = params
    z1, z2 = u*x, v*x
    h1, h2 = max(0,z1), max(0,z2)
    residual = a*h1 + b*h2 - target
    # ReLU derivative convention at zero is 0 for this teaching program.
    gradients = [2*residual*a*x*(z1>0), 2*residual*b*x*(z2>0),
                 2*residual*h1, 2*residual*h2]
    new = [old-rate*g for old,g in zip(params,gradients)]
    return gradients, new, (output(new,x)-target)**2

old = [1.,1.,1.,1.]
gradients, new, loss = update(old, 1, 1, .1)
print('old [u,v,a,b]', old, 'output', output(old,1))
print('gradients', gradients)
print('new [u,v,a,b]', new)
print('new output/loss', round(output(new,1),6), round(loss,6))
print('identical units remain identical', new[0]==new[1] and new[2]==new[3])
print('all-zero start gradients', update([0.,0.,0.,0.],1,1,.1)[0])
print('hidden activations u1/v-1 at x1', [max(0,u*1) for u in [1,-1]])
print('hidden activations u1/v-1 at x-1', [max(0,u*(-1)) for u in [1,-1]])
# Numeric inputs and exactly four parameters assumed. This is one constructed update.
