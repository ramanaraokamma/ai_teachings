from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Coded data: separate the key and restrict its readers',ha='center',fontsize=19,weight='bold')
for x,title,fields,reader in [(.07,'Analysis table','Participant code → task score','Declared analyst role'),(.55,'Identity key','Participant code → identity','Restricted withdrawal role only')]:
 ax.add_patch(FancyBboxPatch((x,.43),.37,.34,boxstyle='round,pad=0.015',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.185,.69,title,ha='center',fontsize=15,weight='bold');ax.text(x+.185,.58,fields,ha='center',fontsize=12);ax.text(x+.185,.48,reader,ha='center',fontsize=11)
ax.annotate('',xy=(.55,.6),xytext=(.44,.6),arrowprops={'arrowstyle':'<->','color':'#a34e32','lw':2});ax.text(.5,.36,'The shared code makes linking possible if the key is available.',ha='center',fontsize=12,color='#a34e32')
ax.text(.5,.2,'Publishing the key with the analysis breaks this separation.\nCoded does not mean anonymous; rare combinations may still identify people.\nThis is a fictional design diagram, not an implemented access-control system.',ha='center',fontsize=12)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-20-key-separation.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
