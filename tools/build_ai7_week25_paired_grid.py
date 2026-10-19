from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,8);ax.set_ylim(0,4);ax.axis('off')
ax.text(4,3.7,'Frozen six-case results: the paired pattern matters',ha='center',fontsize=19,weight='bold')
for j in range(6):ax.text(j+1.8,3.05,f'C{j+1}',ha='center',fontsize=12,weight='bold')
for i,(label,values) in enumerate([('A: 4 / 6',[1,0,1,1,0,1]),('B: 5 / 6',[1,1,1,0,1,1])]):
 y=2.45-i*.7;ax.text(1,y,label,ha='right',va='center',fontsize=13,weight='bold')
 for j,v in enumerate(values):
  ax.add_patch(Rectangle((j+1.45,y-.23),.7,.46,facecolor='#d7efe7' if v else '#f3ded7',edgecolor='#668095'));ax.text(j+1.8,y,'1' if v else '0',ha='center',va='center',fontsize=14)
ax.text(4,.85,'B-only correct: C2 and C5     •     A-only correct: C4\nNet gain: one correct; three case outcomes differ.',ha='center',fontsize=13)
ax.text(4,.3,'1 = correct, 0 = incorrect. Supplied fictional results, not an actual model run.\nTuning on C4 turns a revised same-set score into development evidence.',ha='center',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-25-paired-grid.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
