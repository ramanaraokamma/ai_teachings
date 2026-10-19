from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
root=Path(__file__).resolve().parents[1]
x=np.linspace(-2.5,6.5,181)
fig,ax=plt.subplots(figsize=(10,5),layout='constrained')
ax.plot(x,2*x,'--',color='#7552a0',label='Supplied target relationship y = 2x')
ax.plot(x,np.maximum(0,2*x),color='#197b91',linewidth=2.5,label='Frozen candidate: ReLU(2x)')
ax.plot(x,np.maximum(0,x),color='#c78823',label='Baseline: ReLU(x)')
for name,v in [('F1',5),('F2',6),('F3',-1),('F4',-2)]:
 ax.scatter(v,2*v,color='#7552a0',zorder=5)
 ax.annotate(name,(v,2*v),xytext=(5,-17 if v<0 else 7),textcoords='offset points')
 if v<0:
  ax.plot([v,v],[2*v,0],color='#c54949',linewidth=2)
  ax.scatter(v,0,color='#197b91',zorder=5)
ax.axhline(0,color='#999',linewidth=.7);ax.axvline(0,color='#999',linewidth=.7)
ax.set(xlabel='Input x',ylabel='Prediction or supplied target y',title='A nonnegative output cannot represent a negative target',xlim=(-2.6,6.6),ylim=(-6.5,14))
ax.legend(loc='upper left',fontsize=9)
ax.spines[['top','right']].set_visible(False)
fig.supxlabel('Constructed four-case evaluation • red gaps mark the two negative-target errors • changing the output requires a new version',fontsize=9)
for ext in ['png','svg']:fig.savefig(root/'assets'/f'ai-5-35-nonnegative-output-limit.{ext}',dpi=180)
