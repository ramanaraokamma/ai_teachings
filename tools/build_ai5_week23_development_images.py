from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
cases=[('Train A',[[1,0],[0,0]],1),('Train B',[[1,0],[1,0]],1),('Train C',[[0,1],[0,0]],0),('Train D',[[0,1],[0,1]],0),('Validation E',[[0,0],[1,0]],1),('Validation F',[[0,0],[0,1]],0)]
fig,axes=plt.subplots(2,3,figsize=(10,6.6),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
for ax,(name,image,label) in zip(axes.flat,cases):
 for r,row in enumerate(image):
  for c,value in enumerate(row):
   ax.add_patch(Rectangle((c,r),1,1,facecolor='white' if value else '#153247',edgecolor='#a5b9ca',lw=1.5));ax.text(c+.5,r+.5,str(value),ha='center',va='center',fontsize=16,color='#153247' if value else 'white')
 d=image[0][0]+image[1][0]-image[0][1]-image[1][1]
 ax.set(xlim=(0,2),ylim=(2,0),xticks=[.5,1.5],yticks=[.5,1.5],xticklabels=['Left','Right'],yticklabels=['0','1'],ylabel='Row',title=f'{name}: d = {d}, class {label}');ax.set_aspect('equal')
 for spine in ax.spines.values():spine.set_color('#a55317' if name.startswith('Validation') else '#17628a');spine.set_linewidth(2)
fig.suptitle('Six complete development images; only the output scalar is trained',fontsize=15)
fig.supxlabel('Fixed kernel [[1, −1], [1, −1]] gives left-column sum minus right-column sum.\nClass 1 when d > 0; otherwise class 0. Training targets are +1 and −1 respectively.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-23-development-image-cards.{ext}',bbox_inches='tight')
print('Saved public A–F development images only; no final cases.')
