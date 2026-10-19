from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
x=[[1,2,0],[0,1,3],[2,0,1]];k=[[1,-1],[0,1]]
fig,axes=plt.subplots(2,2,figsize=(9.5,7.8),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
for ax,(sr,sc) in zip(axes.flat,[(0,0),(0,1),(1,0),(1,1)]):
 products=[]
 for r in range(3):
  for c in range(3):
   inside=sr<=r<sr+2 and sc<=c<sc+2
   ax.add_patch(Rectangle((c,r),1,1,facecolor='#e9f3ff' if inside else '#f3f5f8',edgecolor='#b9c7d6',lw=1))
   if inside:
    weight=k[r-sr][c-sc];label=f'{x[r][c]} × {weight}';products.append(x[r][c]*weight);colour='#9a263c' if weight<0 else '#143f62'
   else:label=str(x[r][c]);colour='#68798c'
   ax.text(c+.5,r+.5,label,ha='center',va='center',fontsize=12,color=colour)
 ax.add_patch(Rectangle((sc,sr),2,2,fill=False,edgecolor='#17628a',lw=3))
 ax.set(xlim=(0,3),ylim=(3,0),xticks=[.5,1.5,2.5],yticks=[.5,1.5,2.5],xticklabels=['0','1','2'],yticklabels=['0','1','2'],xlabel='Column',ylabel='Row',title=f'Window start ({sr}, {sc}) → output {sum(products)}')
 ax.set_aspect('equal');ax.spines[:].set_visible(False)
 ax.text(.5,-.25,'Products '+str(products)+'; sum '+str(sum(products)),transform=ax.transAxes,ha='center',fontsize=10)
fig.suptitle('Reuse the same unflipped kernel [[1, −1], [0, 1]]\nStride 1 · no padding · bias 0',fontsize=15)
fig.supxlabel('Four valid windows → feature map [[0, 5], [−1, −1]]\n4 shared weights; 16 products. Highlighted cells show value × matching weight.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-21-local-window-products.{ext}',bbox_inches='tight')
print('Saved all four labelled local windows and product sums.')
