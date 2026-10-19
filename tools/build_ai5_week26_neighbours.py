from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(8,6.8),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
query=(1,0)
items=[('GO',(2,0),1,'#17628a',(12,-5)),('TURN',(1,1),1,'#16754a',(10,12)),('WAIT',(0,1),2,'#8b4a96',(-85,-30)),('STOP',(0,2),5,'#a55317',(-88,10))]
for name,(x,y),distance,col,off in items:
 ax.plot([1,x],[0,y],color=col if distance==1 else '#bac7d1',lw=2 if distance==1 else 1.2,ls='-' if distance==1 else '--');ax.scatter(x,y,s=90,color=col,zorder=4)
 ax.annotate(f'{name} ({x}, {y})\nd² = {distance}',(x,y),xytext=off,textcoords='offset points',fontsize=11,color=col)
ax.scatter([0,-1],[0,-1],color='#728493',marker='x',s=75,zorder=4);ax.annotate('PAD (0, 0)\nexcluded candidate',(0,0),xytext=(-95,-35),textcoords='offset points',fontsize=10,color='#596d7e');ax.annotate('UNK (−1, −1)\nexcluded candidate',(-1,-1),xytext=(10,-20),textcoords='offset points',fontsize=10,color='#596d7e')
ax.scatter(*query,s=180,color='#183249',marker='*',zorder=5);ax.annotate('Query (1, 0)',query,xytext=(12,-38),textcoords='offset points',fontsize=11)
ax.add_patch(Circle(query,1,fill=False,ls=':',lw=1.5,edgecolor='#68798c'))
ax.set(xlim=(-1.4,2.9),ylim=(-1.45,2.65),xlabel='Toy embedding coordinate 1',ylabel='Toy embedding coordinate 2',title='Query [1, 0]: GO and TURN tie among declared candidates')
ax.set_aspect('equal');ax.set_xticks([-1,0,1,2]);ax.set_yticks([-1,0,1,2]);ax.grid(alpha=.16);ax.spines[['top','right']].set_visible(False)
fig.supxlabel('Squared distance = sum of squared coordinate differences. Dotted circle marks d² = 1.\nPAD is equally close but excluded by policy. Constructed geometry alone does not prove meaning.',fontsize=10)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-26-embedding-neighbour-tie.{ext}',bbox_inches='tight')
print('Saved labelled candidate/tie geometry with excluded reserved entries.')
