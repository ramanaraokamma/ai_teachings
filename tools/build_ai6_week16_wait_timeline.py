from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(12,5.5),gridspec_kw={'width_ratios':[1.4,1]},layout='constrained')
ax=axes[0]
for start,width,color,label in [(0,4,'#197b91','Attempt 1\n4 s'),(4,1,'#b8c1ca','1 s'),(5,4,'#197b91','Attempt 2\n4 s'),(9,2,'#b8c1ca','2 s'),(11,4,'#197b91','Attempt 3\n4 s')]:
 ax.broken_barh([(start,width)],(.7,.6),facecolors=color,edgecolors='white',linewidth=1.5)
 ax.text(start+width/2,1,label,ha='center',va='center',fontsize=15,color='white' if color=='#197b91' else '#172d39')
ax.set(xlim=(-.2,15.6),ylim=(0,2),yticks=[],xticks=[0,4,5,9,11,15],xlabel='Modeled caller waiting + retry gaps (seconds)',title='Main budget: 3 × 4 + 1 + 2 = 15 seconds')
ax.text(7.5,.35,'Blue: capped caller waits • grey: retry gaps\nFourth attempt is outside the declared budget.',ha='center',va='center',fontsize=13)
ax.spines[['top','right','left']].set_visible(False)
ax=axes[1]
for y in [1.25,.35]:ax.broken_barh([(0,1)],(y,.4),facecolors='#c78823',edgecolors='white')
ax.broken_barh([(1,.4)],(1.25,.4),facecolors='#3a8567',edgecolors='white')
ax.text(.5,1.45,'timeout: 1 s',ha='center',va='center',color='white',fontsize=13)
ax.text(1.2,1.45,'0.4 s',ha='center',va='center',color='white',fontsize=12)
ax.text(.5,.55,'timeout: 1 s',ha='center',va='center',color='white',fontsize=13)
ax.plot([1],[.55],marker='x',color='#b83c3c',markersize=14,markeredgewidth=3)
ax.text(1.06,.55,'cancel:\nno retry',va='center',fontsize=13,color='#a12d2d')
ax.set(xlim=(-.05,1.8),ylim=(0,2),yticks=[],xticks=[0,1,1.4],xlabel='Separate pictured waiting model (seconds)',title='Picture: 1.4 s without cancellation')
ax.text(.7,1.83,'Same timeout; cancellation changes the next step',ha='center',fontsize=13)
ax.spines[['top','right','left']].set_visible(False)
fig.suptitle('A wait cap, a retry budget and cancellation\nare separate controls',fontsize=17,weight='bold')
fig.supxlabel('Constructed virtual timelines; overhead excluded; no real clock or network runs.\nA caller timeout does not prove that remote work stopped.',fontsize=11)
for ext in ['png','svg']:fig.savefig(root/'assets'/f'ai-6-16-caller-wait-timeline.{ext}',dpi=180)
