from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,6),dpi=150,layout='constrained');fig.patch.set_facecolor('#f5f8fc');ax.set_facecolor('white')
x=[1,2,3,4,5];ax.plot(x,[2*t-3 for t in x],color='#17628a',lw=3,label='Original b = −3: height = 2 × width − 3')
ax.plot(x,[2*t-1 for t in x],color='#a55317',lw=3,ls='--',label='Changed b = −1: height = 2 × width − 1')
for name,px,py in [('Boundary',2,1),('Boundary',3,3),('Boundary',4,5)]:
 ax.scatter(px,py,color='#17628a',s=55,zorder=4);ax.annotate(f'{name} ({px}, {py})',(px,py),xytext=(7,-19),textcoords='offset points',fontsize=10)
ax.scatter([4,4],[4,6],s=80,color=['#16754a','#a52c38'],marker='s',zorder=4)
ax.annotate('(4, 4): z = 1 → class 1',(4,4),xytext=(8,-28),textcoords='offset points',fontsize=10)
ax.annotate('(4, 6): z = −1 → class 0',(4,6),xytext=(-205,4),textcoords='offset points',fontsize=10)
ax.add_patch(FancyArrowPatch((3,3.2),(3,4.8),arrowstyle='<->',mutation_scale=15,color='#a55317',lw=2))
ax.text(3.12,4,'Same slope 2\nBoundary rises 2 cm',fontsize=10,va='center',bbox=dict(facecolor='white',edgecolor='#d6dee8',pad=4))
ax.text(1.08,8.2,'For b = −3:\nclass 0 ABOVE the solid line\nclass 1 ON or BELOW it',fontsize=11,bbox=dict(facecolor='#edf3f8',edgecolor='none',pad=8))
ax.set(xlim=(1,5.2),ylim=(0,10),xlabel='Width (cm) · horizontal coordinate',ylabel='Height (cm) · vertical coordinate',title='Bias moves the boundary; the weights keep its slope')
ax.legend(loc='upper left',bbox_to_anchor=(0,-.16),frameon=False,fontsize=10);ax.grid(alpha=.18);ax.spines[['top','right']].set_visible(False)
ax.text(.5,-.32,'Declared toy rule: z = 2 × width − height + b; class 1 when z ≥ 0. Supplied parameters; no training.',ha='center',fontsize=9,transform=ax.transAxes)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-03-bias-boundary.{ext}',bbox_inches='tight')
print('Saved labelled original/changed boundary plot.')
