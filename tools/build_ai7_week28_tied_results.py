from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(11,6));fig.patch.set_facecolor('#f4f8fc')
for ax,count,total,title in [(axes[0],8,10,'Main support-pass count'),(axes[1],6,8,'Separate picture correctness')]:
 value=100*count/total;ax.bar(['A','B'],[value,value],color=['#176b99','#16836f'],width=.5);ax.set_ylim(0,100);ax.set_ylabel('Supplied pass/correct rate (%)');ax.set_title(title,fontsize=13,weight='bold');ax.spines[['top','right']].set_visible(False)
 for x in [0,1]:ax.text(x,value+2,f'{count}/{total} = {value:g}%',ha='center',fontsize=12,weight='bold')
fig.suptitle('Strict improvement was predicted; the supplied counts tie',fontsize=17,weight='bold')
fig.text(.08,.08,'Report the unmet prediction and preserve the original result.\nA tie is not an equivalence test; a later outcome-selected favorable task is exploratory evidence.',fontsize=12)
fig.subplots_adjust(left=.09,right=.95,bottom=.3,top=.8,wspace=.35)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-28-tied-results.{ext}',dpi=170,facecolor=fig.get_facecolor())
