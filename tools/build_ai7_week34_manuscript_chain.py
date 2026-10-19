from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Every manuscript view must preserve the same result',ha='center',fontsize=19,weight='bold')
for x,title,detail in [(.04,'Raw result','18 passes\n2 failures\n20 evaluated'),(.36,'Figure and table','Show all twenty\nKeep both failures\n18 / 20 = 90%'),(.68,'Abstract claim','90% on this set\nNot 100%\nAttach the scope')]:
 ax.add_patch(FancyBboxPatch((x,.35),.28,.42,boxstyle='round,pad=0.012',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.14,.67,title,ha='center',fontsize=14,weight='bold');ax.text(x+.14,.49,detail,ha='center',fontsize=13)
ax.text(.5,.15,'Link each statement to the actual run/artifact; do not hide failures to protect a headline.\nSeparate picture: ten indoor photos come from five plants with two views each.',ha='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-34-manuscript-chain.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
