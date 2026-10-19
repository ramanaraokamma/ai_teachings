from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(12,4.7),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
a=axes[0];xs=[i/50 for i in range(251)];a.plot(xs,[(x-2)**2 for x in xs],color='#17628a',lw=3,label='L(w) = (w − 2)²')
a.plot([.4,1.6],[2.2,-.2],color='#a55317',ls='--',lw=2,label='Local tangent at w = 1: slope −2')
for x,y,label,off in [(1,1,'Start (1, 1)',(-65,18)),(1.1,.81,'Small increase: L(1.1) = 0.81',(25,35)),(2,0,'Minimum (2, 0)',(0,15)),(4,4,'Large increase: L(4) = 4',(-130,18))]:
 a.scatter(x,y,s=45,color='#17628a',zorder=4);a.annotate(label,(x,y),xytext=off,textcoords='offset points',fontsize=9,arrowprops={'arrowstyle':'-','color':'#68798c'})
a.set(xlim=(0,5),ylim=(-.5,9.5),xlabel='Parameter w',ylabel='Loss L(w)',title='A negative local slope is not a safe jump size');a.legend(loc='upper left',fontsize=9,frameon=False)
a=axes[1];xs=[-1.4+i/100 for i in range(281)];a.plot(xs,[(x*x-1)**2 for x in xs],color='#8b4a96',lw=3,label='F(w) = (w² − 1)²');a.plot([-.45,.45],[1,1],color='#a55317',ls='--',lw=2,label='Flat tangent at w = 0')
a.scatter([0,.1,-1,1],[1,.9801,0,0],color='#8b4a96',s=45,zorder=4);a.annotate('F(0) = 1; local slope 0',(0,1),xytext=(-85,30),textcoords='offset points',fontsize=10);a.annotate('F(0.1) = 0.9801 < 1',(.1,.9801),xytext=(28,-45),textcoords='offset points',fontsize=10,arrowprops={'arrowstyle':'-','color':'#68798c'})
a.set(xlim=(-1.4,1.4),ylim=(-.1,1.5),xlabel='Parameter w',ylabel='Loss F(w)',title='Zero local slope does not prove a minimum');a.legend(loc='lower center',fontsize=9,frameon=False)
for a in axes:a.grid(alpha=.16);a.spines[['top','right']].set_visible(False)
fig.suptitle('Read a local direction clue; then check the new loss.',fontsize=16)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-09-local-slope-limits.{ext}',bbox_inches='tight')
print('Saved local slope and zero-slope counterexample graphs.')
