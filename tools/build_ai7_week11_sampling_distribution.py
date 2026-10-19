"""Native exact probability figure for six uniformly chosen unordered ID pairs."""
from pathlib import Path
from itertools import combinations
from fractions import Fraction
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
values=[1,1,3,3];counts=Counter(Fraction(values[i]+values[j],2) for i,j in combinations(range(4),2))
fig,ax=plt.subplots(figsize=(10,6.2));fig.patch.set_facecolor('white')
ax.bar([1,2,3],[counts[Fraction(x)]/6 for x in [1,2,3]],width=.55,color=['#8bb5d4','#287b9d','#8bb5d4'],edgecolor='#234c65',linewidth=1.5)
for x in [1,2,3]:ax.text(x,counts[Fraction(x)]/6+.035,f'{counts[Fraction(x)]}/6 pairs',ha='center',fontsize=20,weight='bold',color='#123c50')
ax.set(xlim=(.4,3.6),ylim=(0,1),xticks=[1,2,3],yticks=[0,1/3,2/3,1],yticklabels=['0','1/3','2/3','1'])
ax.set_xlabel('Sample mean',fontsize=21,labelpad=12);ax.set_ylabel('Probability',fontsize=21,labelpad=12)
ax.tick_params(labelsize=18);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2);ax.set_axisbelow(True)
fig.suptitle('Different samples. Same population.',fontsize=25,weight='bold',color='#123c50',y=.97)
fig.text(.5,.88,'Values 1, 1, 3, 3 · choose two distinct IDs uniformly',ha='center',fontsize=19,color='#345264')
fig.text(.5,.065,'All six ID pairs are equally likely. Average of the six means = 2.',ha='center',fontsize=18,color='#345264')
fig.subplots_adjust(left=.13,right=.97,bottom=.23,top=.79)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-11-exact-sampling-distribution.{ext}',dpi=160,facecolor='white')
plt.close(fig)
