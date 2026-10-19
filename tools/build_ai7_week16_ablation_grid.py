from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,7));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Ablation contributions depend on what remains',ha='center',fontsize=20,weight='bold')
for x,y,title,score,detail in [(.08,.52,'Retrieval ON · Validation ON','8 / 10','Full system'),(.55,.52,'Retrieval OFF · Validation ON','5 / 10','Retrieval removal: net drop 3'),(.08,.18,'Retrieval ON · Validation OFF','7 / 10','Validation removal: net drop 1\nUnauthorized action stipulated'),(.55,.18,'Retrieval OFF · Validation OFF','UNKNOWN','Joint removal was not supplied')]:
 ax.add_patch(FancyBboxPatch((x,y),.37,.25,boxstyle='round,pad=0.015',facecolor='#ffffff',edgecolor='#326c91',linewidth=2))
 ax.text(x+.185,y+.19,title,ha='center',fontsize=11,weight='bold');ax.text(x+.185,y+.115,score,ha='center',fontsize=24,color='#176b99',weight='bold');ax.text(x+.185,y+.035,detail,ha='center',fontsize=10,va='center')
ax.text(.5,.07,'Same ten cases and scoring; other settings held fixed by the constructed exercise.\nThe unknown cell prevents calculating the interaction; net counts do not identify case flips.',ha='center',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-16-ablation-grid.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
