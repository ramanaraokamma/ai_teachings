from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Answer the challenge from the evidence you have',ha='center',fontsize=19,weight='bold')
for x,title,value,detail in [(.06,'Camera A: tested','10 / 12 correct','≈83.333% on supplied photos'),(.54,'Camera B: original study','NO RECORDS','Do not promise an untested rate')]:
 ax.add_patch(FancyBboxPatch((x,.43),.4,.34,boxstyle='round,pad=0.012',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.2,.69,title,ha='center',fontsize=13,weight='bold');ax.text(x+.2,.58,value,ha='center',fontsize=20,color='#176b99',weight='bold');ax.text(x+.2,.48,detail,ha='center',fontsize=11)
ax.text(.5,.3,'Later one camera-B success: one demonstration, not broad reliability.',ha='center',fontsize=14,weight='bold')
ax.text(.5,.15,'Propose reserved camera-B cases, fixed scoring and recorded grouping.\nMark the proposed test as not run; keep original and demonstration records separate.',ha='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-35-evidence-boundary.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
