from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,3,figsize=(12,4.1),dpi=140,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
xs=[-4+i/40 for i in range(321)]
functions=[('Identity: a = z',lambda z:z,'#17628a'),('ReLU: a = max(0, z)',lambda z:max(0,z),'#16754a'),('Sigmoid: a = 1 / (1 + exp(−z))',lambda z:1/(1+math.exp(-z)),'#8b4a96')]
for ax,(title,f,col) in zip(axes,functions):
 ax.plot(xs,[f(z) for z in xs],lw=3,color=col);ax.axvline(0,color='#8c98a8',lw=.8);ax.axhline(0,color='#8c98a8',lw=.8)
 for z in [-2,0,2]:
  y=f(z);ax.scatter(z,y,color=col,s=45,zorder=4);label=f'({z}, {round(y,4):g})';ax.annotate(label,(z,y),xytext=(3,12 if z!=2 else -20),textcoords='offset points',fontsize=9)
 ax.set(title=title,xlabel='Incoming score z',ylabel='Activation a',xlim=(-4,4));ax.grid(alpha=.15);ax.spines[['top','right']].set_visible(False)
axes[0].set_ylim(-4.5,4.5);axes[1].set_ylim(-.5,4.5);axes[2].set_ylim(-.12,1.14);axes[2].axhline(.5,color='#8b4a96',ls='--',lw=1)
fig.suptitle('Same incoming scores. Different fixed transformations.',fontsize=16)
fig.supxlabel('These are arithmetic functions. A class rule and probability interpretation need separate definitions and evidence.',fontsize=10)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-04-activation-curves.{ext}',bbox_inches='tight')
print('Saved three labelled activation plots.')
