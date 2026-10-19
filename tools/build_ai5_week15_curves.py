from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
values=[0,1,1.5,1.75,1.875];train=[2.5*(v-2)**2 for v in values];valid=[12.5*(v-1.5)**2 for v in values]
fig,axes=plt.subplots(1,2,figsize=(11.5,4.8),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
for ax,start in zip(axes,[0,1]):
 xs=list(range(start,5));ax.plot(xs,train[start:],marker='o',lw=2.5,color='#17628a',label='Training MSE · 2 fixed pairs');ax.plot(xs,valid[start:],marker='s',lw=2.5,ls='--',color='#a55317',label='Validation MSE · 2 fixed pairs')
 ax.axvline(2,color='#68798c',ls=':',lw=1.5);ax.set(xlabel='Saved checkpoint · updates completed',ylabel='Ordinary MSE',xticks=xs);ax.grid(alpha=.16);ax.spines[['top','right']].set_visible(False);ax.legend(fontsize=9,frameon=False,loc='upper right')
axes[0].set_title('All five saved states, including the start');axes[1].set_title('Same records, zoom to checkpoints 1–4')
axes[1].annotate('Choose checkpoint 2\nRestore v = 1.5\nValidation MSE = 0',(2,0),xytext=(20,105),textcoords='offset points',fontsize=10,arrowprops={'arrowstyle':'-','color':'#68798c'})
fig.suptitle('Evaluate both splits at the same saved state; select with validation',fontsize=15)
fig.supxlabel('Constructed target rules differ between these tiny splits. These are development results, not a final evaluation.',fontsize=10)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-15-checkpoint-curves.{ext}',bbox_inches='tight')
(R/'reports/ai-5-week15-curve-data.json').write_text(json.dumps({'checkpoints':values,'train':train,'validation':valid,'selected_index':2},indent=2)+'\n')
print('Saved complete checkpoint curves and labelled zoom.')
