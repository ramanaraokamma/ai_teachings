"""Native original/changed practical-effect comparison using supplied error counts."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,6.5));fig.patch.set_facecolor('white')
ax.bar([0,1],[5,12],width=.5,color=['#d9b385','#438ba5'],edgecolor='#365568',linewidth=1.5)
for x,gain in enumerate([5,12]):ax.text(x,gain+.5,f'{gain} fewer',ha='center',fontsize=22,weight='bold',color='#123c50')
ax.axhline(10,color='#68625b',linestyle='--',linewidth=2)
ax.text(.45,10.35,'minimum 10',ha='center',fontsize=17,color='#54504b')
ax.set(xlim=(-.55,1.55),ylim=(0,15),xticks=[0,1],xticklabels=['Original: B has 15 errors','Changed: B has 8 errors'],yticks=[0,5,10,15])
ax.set_ylabel('Fewer errors per 1,000 tasks',fontsize=20,labelpad=12);ax.tick_params(labelsize=17)
ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('Does the improvement meet\nthe declared practical target?',fontsize=25,weight='bold',color='#123c50',y=.98)
fig.text(.5,.78,'Baseline A has 20 errors per 1,000 tasks in both comparisons.',ha='center',fontsize=18,color='#345264')
fig.text(.5,.055,'Supplied counts and a declared threshold; no uncertainty estimated.',ha='center',fontsize=17,color='#345264')
fig.subplots_adjust(left=.15,right=.97,bottom=.20,top=.72)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-13-practical-error-threshold.{ext}',dpi=160,facecolor='white')
plt.close(fig)
