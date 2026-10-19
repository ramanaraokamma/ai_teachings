from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(11,6));fig.patch.set_facecolor('#f4f8fc')
for ax,values,title in [(axes[0],[8,9],'Main supplied pass counts'),(axes[1],[9,10],'Separate supported-answer counts')]:
 ax.bar(['A','B'],values,color=['#176b99','#16836f'],width=.5);ax.set_ylim(0,12);ax.set_ylabel('Count out of 12 fixed cases/questions');ax.set_title(title,fontsize=13,weight='bold');ax.spines[['top','right']].set_visible(False)
 for x,v in enumerate(values):ax.text(x,v+.3,f'{v}/12',ha='center',fontsize=13,weight='bold')
fig.suptitle('Describe the measured outcome before making a broader claim',fontsize=17,weight='bold')
fig.text(.08,.08,'Each comparison differs by one of twelve cases, about 8.333 percentage points.\nNo user learning or timings were measured. The two scenarios have different supplied outcomes.',fontsize=11)
fig.subplots_adjust(left=.09,right=.95,bottom=.3,top=.8,wspace=.35)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-31-scoped-results.{ext}',dpi=170,facecolor=fig.get_facecolor())
