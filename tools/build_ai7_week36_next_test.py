from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Defend a next test that distinguishes explanations',ha='center',fontsize=19,weight='bold')
for x,title,detail in [(.04,'Observed slices','Clear: 8/10 = 80%\nShaded: 4/10 = 40%\nCause not established'),(.36,'Proposed paired test','Same held-out objects\nBoth light conditions\nOne camera; fixed scoring'),(.68,'Evidence status','Proposed, not run\nNo new outcomes\nIndependence needs design')]:
 ax.add_patch(FancyBboxPatch((x,.34),.28,.43,boxstyle='round,pad=0.012',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.14,.67,title,ha='center',fontsize=13,weight='bold');ax.text(x+.14,.48,detail,ha='center',fontsize=11)
ax.text(.5,.16,'Changing camera as well as light reintroduces another explanation.\nA matched replay checks computation; it does not establish new-population or user benefits.',ha='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-36-next-test.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
