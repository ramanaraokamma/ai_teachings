from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'A scoring disagreement needs the record and rubric',ha='center',fontsize=19,weight='bold')
for x,title,value in [(.07,'Original supplied score','5 / 6'),(.55,'Rerun supplied score','4 / 6')]:
 ax.add_patch(FancyBboxPatch((x,.47),.37,.28,boxstyle='round,pad=0.012',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.185,.67,title,ha='center',fontsize=13,weight='bold');ax.text(x+.185,.55,value,ha='center',fontsize=27,color='#176b99',weight='bold')
ax.text(.5,.35,'Only disputed scoring case: Q3',ha='center',fontsize=17,weight='bold')
ax.text(.5,.2,'Inspect saved output + reference label + scoring rule.\nIf Q3’s saved file is missing, verification remains unresolved.\nNo new model outputs are generated; this is not new-data replication.',ha='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-33-scoring-disagreement.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
