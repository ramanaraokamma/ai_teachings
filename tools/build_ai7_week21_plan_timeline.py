from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Preserve the plan and make later changes visible',ha='center',fontsize=19,weight='bold')
items=[(.04,'BEFORE RESULTS','Plan v1','All 20 cases included\nOutcome and rule recorded'),(.36,'AFTER RESULTS','Proposed exclusion','Four failures removed\nReason: graph looks worse'),(.68,'HONEST REPORT','Keep both records','Original denominator: 20\nRevision disclosed separately')]
for x,stage,title,detail in items:
 ax.add_patch(FancyBboxPatch((x,.36),.28,.4,boxstyle='round,pad=0.012',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.14,.69,stage,ha='center',fontsize=10,weight='bold',color='#176b99');ax.text(x+.14,.58,title,ha='center',fontsize=13,weight='bold');ax.text(x+.14,.45,detail,ha='center',fontsize=11)
for x in [.325,.645]:ax.annotate('',xy=(x+.025,.55),xytext=(x-.005,.55),arrowprops={'arrowstyle':'->','color':'#326c91','lw':2})
ax.text(.5,.18,'The other sixteen outcomes are not supplied: do not assume sixteen passes.\nA version label or timestamp alone does not prove when a plan was fixed.',ha='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-21-plan-timeline.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
