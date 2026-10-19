from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,Circle
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Repair the unit assumption, not just the wording',ha='center',fontsize=19,weight='bold')
for x,plant in [(.07,'P1'),(.55,'P2')]:
 ax.add_patch(FancyBboxPatch((x,.4),.37,.35,boxstyle='round,pad=0.012',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.185,.68,f'Plant {plant}',ha='center',fontsize=15,weight='bold')
 for j in range(4):
  cx=x+.055+j*.085;ax.add_patch(Circle((cx,.54),.032,color='#d7e8f1',ec='#326c91'));ax.text(cx,.54,f'V{j+1}',ha='center',va='center',fontsize=10)
 ax.text(x+.185,.44,'Four views of one plant',ha='center',fontsize=11)
ax.text(.5,.25,'Eight photos → two distinct plant identities',ha='center',fontsize=17,weight='bold',color='#176b99')
ax.text(.5,.12,'Revisit grouping, split roles and uncertainty assumptions; no outcome counts are supplied.\nTwo IDs do not prove independent sampling. Changing labels alone cannot fix the analysis.',ha='center',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-32-review-units.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
