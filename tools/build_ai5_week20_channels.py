from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
R=Path(__file__).resolve().parents[1]
image=[[[255,0,0],[0,255,0]],[[0,0,255],[255,255,255]]]
fig,axes=plt.subplots(1,4,figsize=(12,4.2),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc')
for panel,ax in enumerate(axes):
 for row in range(2):
  for col in range(2):
   raw=image[row][col]
   if panel==0:rgb=tuple(v/255 for v in raw);label='['+', '.join(map(str,raw))+']'
   else:
    c=panel-1;rgb=tuple(raw[c]/255 if j==c else 0 for j in range(3));label=str(raw[c])
   ax.add_patch(Rectangle((col,row),1,1,facecolor=rgb,edgecolor='#8894a3',lw=1.5))
   bright=.2126*rgb[0]+.7152*rgb[1]+.0722*rgb[2]
   ax.text(col+.5,row+.5,label,ha='center',va='center',fontsize=10.5,color='black' if bright>.18 else 'white')
 ax.set(xlim=(0,2),ylim=(2,0),xticks=[.5,1.5],yticks=[.5,1.5],xticklabels=['0','1'],yticklabels=['0','1'],xlabel='Column k',ylabel='Row r');ax.set_aspect('equal');ax.spines[:].set_visible(False)
axes[0].set_title('RGB pixels · HWC');axes[1].set_title('Red plane · c = 0');axes[2].set_title('Green plane · c = 1');axes[3].set_title('Blue plane · c = 2')
fig.suptitle('One image. Three channel planes. Same pixel values.',fontsize=16)
fig.supxlabel('HWC shape 2 × 2 × 3 → CHW shape 3 × 2 × 2\nPreserve each value: HWC[r][k][c] = CHW[c][r][k]. Zero-based row, column and channel indices.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-20-rgb-channel-planes.{ext}',bbox_inches='tight')
print('Saved pixel-labelled RGB and channel-plane diagram.')
