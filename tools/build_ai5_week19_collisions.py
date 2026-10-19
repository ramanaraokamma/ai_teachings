from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(10.5,5),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
for ax,(name,w,h,col) in zip(axes,[('A',4,2,'#17628a'),('B',5,3,'#8b4a96')]):
 ax.add_patch(Rectangle((0,0),w,h,facecolor=col,alpha=.14,edgecolor='none'));ax.add_patch(Rectangle((0,0),w,h,fill=False,edgecolor=col,lw=3))
 ax.text(w/2,h/2,f'Area {w*h} cm²',ha='center',va='center',fontsize=15,color=col,bbox=dict(facecolor='white',edgecolor='none',alpha=.9))
 ax.set(xlim=(0,6),ylim=(0,4),xticks=range(7),yticks=range(5),xlabel='Width (cm)',ylabel='Height (cm)',title=f'{name}: input [{w}, {h}] → hidden [2, 0]')
 ax.set_aspect('equal');ax.grid(alpha=.22);ax.spines[['top','right']].set_visible(False)
fig.suptitle('Different rectangles. Same hidden vector. Different areas.',fontsize=16)
fig.supxlabel('h = [ReLU(width − height), ReLU(height − width)]\nBoth are wider: class 1. An area head seeing only the same h cannot return both 8 and 15.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-19-representation-collision.{ext}',bbox_inches='tight')
print('Saved scale-matched rectangle collision diagram.')
