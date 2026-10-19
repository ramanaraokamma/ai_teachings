from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
records=[]
for rate in [.05,.2,.3,.4,.5]:
 v=0.;vs=[v]
 for _ in range(4):v=v-rate*5*(v-2);vs.append(v)
 records.append({'rate':rate,'v':vs,'mse':[2.5*(x-2)**2 for x in vs]})
fig,axes=plt.subplots(2,2,figsize=(11,7),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
styles=[('#17628a','o','-'),('#16754a','s','--'),('#8b4a96','^','-.'),('#a55317','D','--'),('#a52c38','x','-')]
for item,(col,marker,ls) in zip(records,styles):
 column=0 if item['rate']<.4 else 1
 for row,key in [(0,'v'),(1,'mse')]:axes[row,column].plot(range(5),item[key],color=col,marker=marker,ls=ls,lw=2,label=f"rate {item['rate']:g}")
for col in [0,1]:
 axes[0,col].axhline(2,color='#68798c',lw=1,alpha=.7);axes[0,col].set_ylabel('Parameter v')
 axes[1,col].set_ylabel('Training MSE');axes[1,col].set_xlabel('Updates completed · 0 is the starting state')
 for row in [0,1]:
  a=axes[row,col];a.set_xticks(range(5));a.grid(alpha=.16);a.spines[['top','right']].set_visible(False);a.legend(fontsize=9,frameon=False,loc='best')
axes[0,0].set_title('Approach or cross while shrinking');axes[0,1].set_title('Alternate without progress, or grow')
axes[1,0].set_title('Decreasing loss on this fixed objective');axes[1,1].set_title('Unchanged or increasing loss · different vertical scale')
fig.suptitle('Same start, same mean loss, four updates; only the rate changes',fontsize=15)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-14-controlled-rates.{ext}',bbox_inches='tight')
(R/'reports/ai-5-week14-curve-data.json').write_text(json.dumps({'objective':'2.5*(v-2)^2','gradient':'5*(v-2)','start':0,'updates':4,'records':records},indent=2)+'\n')
print('Saved complete controlled-rate parameter and loss curves.')
