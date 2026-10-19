from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'One agreement does not authorize every use',ha='center',fontsize=20,weight='bold')
ax.text(.5,.82,'Fictional adult drawing study: consent covers one pattern-recognition investigation',ha='center',fontsize=12)
for x,title,status,detail,color in [(.04,'Named investigation','WITHIN STATED SCOPE','Other review and handling\nconditions still apply','#157660'),(.36,'Public originals','EXCLUDED','Do not post drawings\nunder this agreement','#a34e32'),(.68,'Unrelated face study','EXCLUDED','A new request is not\nnew authorization','#a34e32')]:
 ax.add_patch(FancyBboxPatch((x,.34),.28,.35,boxstyle='round,pad=0.012',facecolor='white',edgecolor=color,linewidth=2));ax.text(x+.14,.61,title,ha='center',fontsize=12,weight='bold');ax.text(x+.14,.51,status,ha='center',fontsize=10,color=color,weight='bold');ax.text(x+.14,.4,detail,ha='center',fontsize=11)
ax.text(.5,.16,'Course activity: audit fictional proposals on paper; no recruitment or real data reuse.\nScope permission alone does not prove all ethical conditions are satisfied.',ha='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-19-purpose-map.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
