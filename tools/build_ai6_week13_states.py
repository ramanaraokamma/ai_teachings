from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,FancyArrowPatch,Circle
root=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(12,5),layout='constrained')
ax.set(xlim=(0,10.3),ylim=(-.25,4.1));ax.axis('off')
for name,x,y,color in [('ready',1.1,2.3,'#dceef7'),('looking_up',4.1,2.3,'#cfe9ed'),('review',6.1,.8,'#fae8b7')]:
 ax.add_patch(FancyBboxPatch((x-.9,y-.36),1.8,.72,boxstyle='round,pad=.07',facecolor=color,edgecolor='#254557',linewidth=1.5))
 ax.text(x,y,name,ha='center',va='center',fontsize=13,weight='bold')
for radius in [.48,.41]:ax.add_patch(Circle((9.1,2.3),radius,facecolor='#dceedd',edgecolor='#31593a',linewidth=1.5))
ax.text(9.1,2.3,'done',ha='center',va='center',fontsize=13,weight='bold')
for start,end in [((2.1,2.3),(3.1,2.3)),((5.1,2.3),(8.6,2.3)),((4.6,1.9),(5.6,1.2)),((7.1,1.1),(8.7,1.95))]:
 ax.add_patch(FancyArrowPatch(start,end,arrowstyle='-|>',mutation_scale=18,color='#254557',linewidth=1.7))
ax.text(2.6,2.57,'start lookup',ha='center',fontsize=10)
ax.text(6.8,2.57,'finish lookup',ha='center',fontsize=10)
ax.text(4.7,1.4,'needs review',ha='center',fontsize=10)
ax.text(8.3,.65,'authorized review\nevidence required',ha='center',fontsize=10)
ax.text(9.1,3.0,'terminal',ha='center',fontsize=10,color='#31593a')
ax.text(5.1,3.45,'Separate budget: at most 2 lookup-state entries\nA budget does not create a missing retry arrow.',ha='center',fontsize=11,bbox={'facecolor':'#f3f5f7','edgecolor':'#b6c1c9','boxstyle':'round,pad=.5'})
ax.text(5.1,-.02,'Original graph: review → looking_up is forbidden; done has no outgoing transition.',ha='center',fontsize=11,color='#9b3838')
fig.suptitle('Follow only the declared state transitions',fontsize=17,weight='bold')
for ext in ['png','svg']:fig.savefig(root/'assets'/f'ai-6-13-declared-state-graph.{ext}',dpi=180)
