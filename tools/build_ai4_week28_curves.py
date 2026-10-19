"""Standalone teaching plots from declared synthetic learning-curve records."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
data={
 'p':{'training_mean':[7,7,7],'validation_repeats':[[7,9,8],[7,9,8],[7,9,8]]},
 'q':{'training_mean':[1,1,1],'validation_repeats':[[8,10,9],[7,9,8],[7,9,8]]},
 'r':{'training_mean':[1,2,3],'validation_repeats':[[7,9,8],[5,7,6],[4,6,5]]}}
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':15,'axes.titlesize':22,'axes.labelsize':17,'xtick.labelsize':14,'ytick.labelsize':14})
for case,record in data.items():
 x=[10,20,40];repeats=record['validation_repeats'];means=[sum(v)/len(v) for v in repeats];low=[min(v) for v in repeats];high=[max(v) for v in repeats]
 fig,ax=plt.subplots(figsize=(10,6.5),dpi=120);fig.patch.set_facecolor('#f5f9fc');ax.set_facecolor('white')
 ax.fill_between(x,low,high,color='#b64d0a',alpha=.13,label='Observed min–max of 3 validation runs')
 ax.plot(x,record['training_mean'],'o-',color='#087e8b',lw=3,markersize=8,label='Training MAE (supplied mean)')
 ax.plot(x,means,'s-',color='#a23c00',lw=3,markersize=8,label='Validation MAE (mean of 3 runs)')
 ax.axhline(3,color='#424b53',lw=1.5,linestyle='--',label='Declared classroom reference: 3 cm')
 ax.set(xlim=(7,43),ylim=(0,11),xticks=x,yticks=[0,2,4,6,8,10],xlabel='Training rows (source groups kept separate)',ylabel='Mean absolute error (cm)',title=f'Case {case.upper()} · What does this pattern suggest?')
 ax.grid(alpha=.2);ax.legend(loc='upper center',bbox_to_anchor=(.5,-.21),fontsize=12,frameon=False,ncol=2)
 fig.text(.5,.018,'Synthetic supplied records · Same validation protocol · A pattern is not a proven cause',ha='center',fontsize=12,color='#344b5d')
 fig.subplots_adjust(left=.11,right=.97,top=.89,bottom=.30)
 fig.canvas.draw();renderer=fig.canvas.get_renderer();bounds=fig.bbox
 bad=[]
 for artist in [ax.title,ax.xaxis.label,ax.yaxis.label,ax.get_legend(),*ax.get_xticklabels(),*ax.get_yticklabels(),*fig.texts]:
  box=artist.get_window_extent(renderer)
  if box.x0<-.5 or box.y0<-.5 or box.x1>bounds.width+.5 or box.y1>bounds.height+.5:bad.append(str(artist))
 assert not bad,bad
 stem=R/f'assets/ai-4-28-learning-curve-{case}'
 fig.savefig(str(stem)+'.png',facecolor=fig.get_facecolor());fig.savefig(str(stem)+'.svg',facecolor=fig.get_facecolor());plt.close(fig)
(R/'reports/ai-4-week28-curve-data.json').write_text(json.dumps({'sizes':[10,20,40],'unit':'cm','status':'synthetic supplied records, not executed model training','cases':data},indent=2)+'\n')
print('Rendered 3 standalone learning-curve figures; labels/legend bounds checked.')
