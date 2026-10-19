"""Native conditional sign-flip null distribution for the supplied paired picture."""
from pathlib import Path
from itertools import product
from collections import Counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
counts=Counter(sum(s*d for s,d in zip(signs,[1,2,1])) for signs in product((-1,1),repeat=3))
xs=sorted(counts)
fig,ax=plt.subplots(figsize=(10,6.4));fig.patch.set_facecolor('white')
ax.bar(xs,[counts[x]/8 for x in xs],width=1.05,color=['#b86644' if abs(x)>=4 else '#73a4bf' for x in xs],edgecolor='#385568',linewidth=1.5)
for x in xs:ax.text(x,counts[x]/8+.018,f'{counts[x]}/8',ha='center',fontsize=20,weight='bold',color='#123c50')
ax.set(xlim=(-5.1,5.1),ylim=(0,.36),xticks=xs,yticks=[0,.125,.25],yticklabels=['0','1/8','2/8'])
ax.set_xlabel('Signed sum of B − A differences (seconds)',fontsize=19,labelpad=13);ax.set_ylabel('Null probability',fontsize=20,labelpad=12)
ax.tick_params(labelsize=18);ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('Count both tails under the stated null.',fontsize=24,weight='bold',color='#123c50',y=.97)
fig.text(.5,.86,'Eight equally likely sign assignments · fixed magnitudes 1, 2, 1',ha='center',fontsize=18,color='#345264')
fig.text(.5,.77,'At least as extreme: −4 or +4 → 2/8 = 0.25',ha='center',fontsize=19,weight='bold',color='#854b35')
fig.text(.5,.055,'At alpha 0.05: do not reject. This does not prove zero effect.',ha='center',fontsize=17,color='#345264')
fig.subplots_adjust(left=.14,right=.97,bottom=.23,top=.69)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-14-exact-signflip-null.{ext}',dpi=160,facecolor='white')
plt.close(fig)
