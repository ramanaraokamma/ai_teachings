from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,4);ax.set_ylim(0,4.3);ax.axis('off')
ax.text(2,4,'Same scores, different decisions',ha='center',fontsize=20,weight='bold')
for j,s in enumerate(['0.4','0.6','0.8']):ax.text(j+1.5,3.35,f'Score {s}',ha='center',fontsize=13,weight='bold')
for i,c in enumerate([.5,.7,.6]):
 y=2.65-i*.7;ax.text(.9,y,f'Cutoff {c}',ha='right',va='center',fontsize=12)
 for j,s in enumerate([.4,.6,.8]):
  positive=s>=c;ax.add_patch(Rectangle((j+1.1,y-.23),.8,.46,facecolor='#d7efe7' if positive else '#e7ebf1',edgecolor='#668095'))
  ax.text(j+1.5,y,'Positive' if positive else 'Negative',ha='center',va='center',fontsize=11)
ax.text(2,.35,'Rule: score ≥ cutoff, including equality.\nNo reference labels are supplied, so this grid cannot show accuracy\nor identify the best cutoff.',ha='center',va='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-17-cutoff-grid.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
