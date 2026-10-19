from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'A result needs its complete run record',ha='center',fontsize=20,weight='bold')
for y,label,data,total,result in [(.57,'Original run','2, 4, 6','12','4'),(.27,'Changed run','2, 4, 9','15','5')]:
 ax.text(.04,y+.09,label,fontsize=12,weight='bold')
 for x,title,value in [(.24,'Exact input',data),(.49,'Sum ÷ count',total+' ÷ 3'),(.74,'Mean output',result)]:
  ax.add_patch(FancyBboxPatch((x,y),.2,.23,boxstyle='round,pad=0.01',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.1,y+.16,title,ha='center',fontsize=11);ax.text(x+.1,y+.065,value,ha='center',fontsize=17,weight='bold',color='#176b99')
ax.text(.5,.1,'Retain both: run ID, input bytes/hash, script/version, runtime, metric and raw output.\nA seed or output screenshot alone is insufficient; a hash is not proof of scientific correctness.',ha='center',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-24-run-records.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
