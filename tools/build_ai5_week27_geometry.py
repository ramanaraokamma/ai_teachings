from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from math import sqrt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(1,2,figsize=(11,6),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
raw={'Q':(3,4),'A':(6,8),'B':(3,0),'C':(-3,-4)};col={'Q':'#183249','A':'#17628a','B':'#16754a','C':'#a52c38'}
a=axes[0]
for name in ['A','B','C','Q']:
 x,y=raw[name]
 a.annotate('',(x,y),(0,0),arrowprops=dict(arrowstyle='->',color=col[name],lw=2.2,ls='--' if name=='Q' else '-'))
 a.scatter(x,y,color=col[name],marker='*' if name=='Q' else 'o',s=125 if name=='Q' else 60,zorder=4)
 offsets={'Q':(-70,10),'A':(-78,12),'B':(10,-18),'C':(10,10)}
 a.annotate(f'{name} [{x}, {y}]',(x,y),xytext=offsets[name],textcoords='offset points',fontsize=11,color=col[name])
a.set(xlim=(-4.5,7.6),ylim=(-5.3,9.8),title='Raw coordinates: B is nearest to query Q')
a=axes[1];unit={n:(x/sqrt(x*x+y*y),y/sqrt(x*x+y*y)) for n,(x,y) in raw.items()}
a.add_patch(Circle((0,0),1,fill=False,ls=':',lw=1.2,edgecolor='#93a4b2'))
for name in ['A','B','C']:
 x,y=unit[name];a.annotate('',(x,y),(0,0),arrowprops=dict(arrowstyle='->',color=col[name],lw=2.2));a.scatter(x,y,color=col[name],s=60,zorder=4)
a.scatter(*unit['Q'],color=col['Q'],marker='*',s=150,zorder=5)
a.annotate('Q and A [0.6, 0.8]',unit['Q'],xytext=(-138,17),textcoords='offset points',fontsize=11,bbox=dict(facecolor='white',edgecolor='none',pad=2))
a.annotate('B [1, 0]',unit['B'],xytext=(-40,-25),textcoords='offset points',fontsize=11,color=col['B'])
a.annotate('C [−0.6, −0.8]',unit['C'],xytext=(12,-14),textcoords='offset points',fontsize=11,color=col['C'])
a.set(xlim=(-1.35,1.35),ylim=(-1.4,1.5),title='Normalize both sides: A coincides with Q')
for a in axes:
 a.set_aspect('equal');a.axhline(0,color='#a8b7c3',lw=.7);a.axvline(0,color='#a8b7c3',lw=.7);a.grid(alpha=.14);a.set_xlabel('Coordinate 1');a.set_ylabel('Coordinate 2');a.spines[['top','right']].set_visible(False)
fig.suptitle('Length and direction answer different comparison questions',fontsize=16)
fig.supxlabel('Raw squared distances Q→A/B/C: 25, 16, 100. Cosines: 1, 0.6, −1.\nUnit-vector squared distances: 0, 0.8, 4 = 2 − 2 × cosine. These toy coordinates do not prove meaning.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-27-raw-unit-vector-geometry.{ext}',bbox_inches='tight')
print('Saved equal-aspect raw and normalized vector diagrams.')
