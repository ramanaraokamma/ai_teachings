from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,6));fig.patch.set_facecolor('#f4f8fc');ax.set_facecolor('white')
values=[87.5,37.5,62.5];labels=['Indoor\n7 / 8','Outdoor shade\n3 / 8','Pooled\n10 / 16']
ax.bar(labels,values,color=['#176b99','#b35e43','#74879a'],width=.55);ax.set_ylim(0,100);ax.set_ylabel('Correct on the supplied cases (%)');ax.set_title('The pooled score hides a weaker condition',fontsize=19,weight='bold',pad=20);ax.spines[['top','right']].set_visible(False)
for i,v in enumerate(values):ax.text(i,v+2,f'{v}%',ha='center',fontsize=13,weight='bold')
fig.text(.1,.07,'Same frozen model and rubric stipulated. Slice gap: 50 percentage points.\nEight cases per slice do not establish cause, stable population rates or all-condition robustness.',fontsize=11)
fig.subplots_adjust(left=.12,right=.95,bottom=.3,top=.82)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-27-slice-rates.{ext}',dpi=170,facecolor=fig.get_facecolor())
