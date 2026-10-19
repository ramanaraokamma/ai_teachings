from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(11,6));fig.patch.set_facecolor('#f4f8fc')
for ax,values,title,unit,limit in [(axes[0],[62,83],'Supplied detection frequency','Detections per 100 alternative trials',100),(axes[1],[60,120],'Per-study resource cost','Credits: independent units × 3',140)]:
 ax.bar(['n = 20','n = 40'],values,color=['#176b99','#16836f'],width=.5);ax.set_ylim(0,limit);ax.set_title(title,fontsize=14,weight='bold');ax.set_ylabel(unit,fontsize=11);ax.spines[['top','right']].set_visible(False)
 for x,v in enumerate(values):ax.text(x,v+limit*.025,str(v),ha='center',fontsize=13,weight='bold')
fig.suptitle('Main example: detection estimates and cost are different quantities',fontsize=16,weight='bold')
fig.text(.09,.08,'Observed difference: 21 percentage points; extra per-study cost: 60 credits.\nCounts are stipulated, not simulated here. Null error is unmeasured; real-study power is not guaranteed.',fontsize=11)
fig.subplots_adjust(left=.09,right=.95,bottom=.29,top=.8,wspace=.35)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-23-power-cost.{ext}',dpi=170,facecolor=fig.get_facecolor())
