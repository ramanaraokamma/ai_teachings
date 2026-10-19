from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(12,5),layout='constrained')
colors=['#197b91','#d9a441']
for ax,title,counts,correct in zip(axes,['Development: 82 / 100 correct','New use: 58 / 100 correct'],[[80,20],[20,80]],[[72,10],[18,40]]):
 for j,(n,k,c) in enumerate(zip(counts,correct,colors)):
  ax.bar(j,k,color=c,width=.6,label='Correct' if j==0 else None)
  ax.bar(j,n-k,bottom=k,color=c,alpha=.25,width=.6,hatch='///',edgecolor=c)
  ax.text(j,k/2,f'{k} correct',ha='center',va='center',color='white',weight='bold')
  ax.text(j,n+2,f'{n} cases',ha='center')
 ax.set(title=title,ylim=(0,91),ylabel='Number of cases',xticks=[0,1],xticklabels=['Clear: 90% correct','Dim: 50% correct'])
 ax.spines[['top','right']].set_visible(False)
fig.suptitle('Same group accuracy, different group sizes',fontsize=17,weight='bold')
fig.supxlabel('Constructed audit counts • solid = correct • pale hatched = incorrect • fixed model and preprocessing',fontsize=10)
for ext in ['png','svg']:fig.savefig(root/'assets'/f'ai-5-30-group-mix-counts.{ext}',dpi=180)
