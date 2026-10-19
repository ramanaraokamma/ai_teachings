from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(11,6));fig.patch.set_facecolor('#f4f8fc')
for ax,values,title,unit,limit,labels in [(axes[0],[80,82],'Main supplied rates','Supplied rate (%)',100,['A: 80%','B: 82%']),(axes[1],[6,8],'Separate ten-case picture','Correct cases out of 10',10,['A: 6/10','B: 8/10'])]:
 ax.bar(labels,values,color=['#176b99','#16836f'],width=.5);ax.set_ylim(0,limit);ax.set_ylabel(unit);ax.set_title(title,fontsize=14,weight='bold');ax.spines[['top','right']].set_visible(False)
 for x,v in enumerate(values):ax.text(x,v+limit*.025,str(v),ha='center',fontsize=13,weight='bold')
fig.suptitle('Use labelled scales that preserve the comparison',fontsize=19,weight='bold')
fig.text(.08,.08,'Main difference: 2 percentage points; underlying case counts are not supplied.\nPicture difference: 2 correct out of 10 = 20 percentage points. No uncertainty bounds are supplied.',fontsize=11)
fig.subplots_adjust(left=.09,right=.95,bottom=.3,top=.8,wspace=.35)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-29-honest-axes.{ext}',dpi=170,facecolor=fig.get_facecolor())
