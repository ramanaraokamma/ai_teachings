from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
cases=[('Original',[[1,0],[0,0]],'#17628a'),('Swap rows · vertical flip',[[0,0],[1,0]],'#16754a'),('Swap columns · horizontal flip',[[0,1],[0,0]],'#a55317')]
fig,axes=plt.subplots(1,3,figsize=(10.5,4.6),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
for ax,(name,image,col) in zip(axes,cases):
 for r,row in enumerate(image):
  for c,v in enumerate(row):
   ax.add_patch(Rectangle((c,r),1,1,facecolor='white' if v else '#153247',edgecolor='#a5b9ca',lw=1.5));ax.text(c+.5,r+.5,str(v),ha='center',va='center',fontsize=18,color='#153247' if v else 'white')
 d=image[0][0]+image[1][0]-image[0][1]-image[1][1]
 ax.set(xlim=(0,2),ylim=(2,0),xticks=[.5,1.5],yticks=[.5,1.5],xticklabels=['Left','Right'],yticklabels=['0','1'],ylabel='Row',title=f'{name}\nd = {d}; class {int(d>0)}');ax.set_aspect('equal')
 for spine in ax.spines.values():spine.set_color(col);spine.set_linewidth(2)
fig.suptitle('Check the task label before copying it to a transformed image',fontsize=15)
fig.supxlabel('Task: class 1 only when left-column sum > right-column sum.\nRow swaps preserve this rule. Column swaps negate d; ties remain class 0 rather than being complemented.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-24-transform-label-rules.{ext}',bbox_inches='tight')
print('Saved explicit row/column transform and target diagram.')
