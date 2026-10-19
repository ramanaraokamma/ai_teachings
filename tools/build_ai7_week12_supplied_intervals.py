"""Plot supplied difference intervals, without inferring unavailable raw data."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,6));fig.patch.set_facecolor('white')
for y,lower,upper,color in [(1.65,-1.4,-.2,'#287b9d'),(.65,-1.4,.3,'#bd762d')]:
 ax.hlines(y,lower,upper,color=color,linewidth=5);ax.vlines([lower,upper],y-.08,y+.08,color=color,linewidth=3)
 ax.plot(-.8,y,'o',color='#163c50',markersize=11)
 ax.text(lower,y+.18,f'{lower:g}',ha='center',fontsize=18,color='#163c50');ax.text(upper,y+.18,f'{upper:g}',ha='center',fontsize=18,color='#163c50')
 ax.text(-.8,y-.25,'estimate −0.8',ha='center',fontsize=17,color='#163c50')
ax.axvline(0,color='#6b7076',linestyle='--',linewidth=2)
ax.text(0,2.13,'0',ha='center',fontsize=20,weight='bold',color='#444a50')
ax.set(xlim=(-1.65,.6),ylim=(.12,2.28),yticks=[.65,1.65],yticklabels=['Changed\nsupplied','Original\nsupplied'],xticks=[-1.5,-1,-.5,0,.5])
ax.set_xlabel('Mean time difference B − A (seconds)',fontsize=20,labelpad=13)
ax.tick_params(labelsize=17);ax.spines[['top','right','left']].set_visible(False);ax.tick_params(axis='y',length=0)
fig.suptitle('Does the supplied interval include zero?',fontsize=24,weight='bold',color='#123c50',y=.97)
fig.text(.5,.865,'Assume the study’s 95% interval method is appropriate.',ha='center',fontsize=18,color='#345264')
fig.text(.5,.055,'Intervals are supplied, not fitted here. Zero inside does not prove equality.',ha='center',fontsize=16,color='#345264')
fig.subplots_adjust(left=.22,right=.97,bottom=.23,top=.78)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-12-supplied-time-intervals.{ext}',dpi=160,facecolor='white')
plt.close(fig)
