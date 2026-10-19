from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
image=[[1,4,2,0],[3,2,5,1],[0,6,1,3],[2,4,2,7]]
maxima=[[4,5],[6,7]];means=[[2.5,2],[3,3.25]];colours=[['#e1eff8','#eee3f5'],['#e2f1e6','#faeddb']]
fig,axes=plt.subplots(1,3,figsize=(11,4.7),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
for ax,data,title,is_input in zip(axes,[image,maxima,means],['Input: 4 × 4','Max output: 2 × 2','Mean output: 2 × 2'],[True,False,False]):
 h,w=len(data),len(data[0])
 for r,row in enumerate(data):
  for c,value in enumerate(row):
   gr,gc=(r//2,c//2) if is_input else (r,c)
   ax.add_patch(Rectangle((c,r),1,1,facecolor=colours[gr][gc],edgecolor='#acbdcc',lw=1))
   ax.text(c+.5,r+.5,str(value),ha='center',va='center',fontsize=16)
 if is_input:
  for r in [0,2]:
   for c in [0,2]:ax.add_patch(Rectangle((c,r),2,2,fill=False,edgecolor='#274e67',lw=2.5))
 ax.set(xlim=(0,w),ylim=(h,0),xticks=[i+.5 for i in range(w)],yticks=[i+.5 for i in range(h)],xticklabels=range(w),yticklabels=range(h),xlabel='Column',ylabel='Row',title=title);ax.set_aspect('equal');ax.spines[:].set_visible(False)
fig.suptitle('Summarize each 2 × 2 region; keep its coarse position',fontsize=16)
fig.supxlabel('Stride 2 · no padding · complete windows · no learned weights\nColours mark window membership, not numeric intensity. Both summaries discard within-window detail.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-22-pooling-regions.{ext}',bbox_inches='tight')
print('Saved complete four-region max and mean pooling diagram.')
