from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6.5));fig.patch.set_facecolor('#f4f8fc');ax.set_facecolor('#ffffff')
labels=['Five-test main family','Six-test picture family','Ten-test changed family']
y=[2,1,0];cutoffs=[.01,.05/6,.005]
ax.barh(y,cutoffs,height=.42,color=['#176b99','#168b75','#7756a5'])
for yy,x in zip(y,cutoffs):ax.text(x+.00015,yy,f'{x:.5f}'.rstrip('0'),va='center',fontsize=12,weight='bold')
ax.set_yticks(y,labels,fontsize=12);ax.set_xlim(0,.013);ax.set_xlabel('Bonferroni cutoff = family alpha 0.05 / number of tests',fontsize=11)
ax.set_xticks([0,.005,.01],['0','0.005','0.010']);ax.spines[['top','right']].set_visible(False)
ax.set_title('More declared tests → smaller per-test cutoff',fontsize=18,weight='bold',pad=22)
fig.text(.08,.07,'Reject a supplied valid test only when p ≤ its family cutoff, including equality.\nTen-test case: four p-values are missing; their decisions remain unknown.\nThese are decision boundaries, not effect sizes or measured false-positive rates.',fontsize=11,color='#26384b')
fig.subplots_adjust(left=.29,right=.93,top=.83,bottom=.25)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-15-family-cutoffs.{ext}',dpi=170,facecolor=fig.get_facecolor())
