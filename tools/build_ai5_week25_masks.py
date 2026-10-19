from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10.5,5.7),dpi=145,layout='constrained');fig.patch.set_facecolor('#f5f8fc');ax.set(xlim=(0,8.2),ylim=(-.6,6.8));ax.axis('off')
rows=[('Position',6.1,['0','1','2','3']),('Event token',5.1,['GO','STOP','PAD','PAD']),('Token ID',4.15,['2','4','0','0']),('Mask',3.2,['1 · real','1 · real','0 · padding','0 · padding']),('Sensor value',1.7,['0 · measured','4','0 · padding','0 · padding']),('Same mask',.75,['1 · real','1 · real','0 · padding','0 · padding'])]
for name,y,values in rows:
 ax.text(.1,y+.25,name,ha='left',va='center',fontsize=12)
 for i,value in enumerate(values):
  x=2.1+1.5*i;bg='#e1eff8' if i<2 else '#e8edf1';edge='#17628a' if i<2 else '#8b9ba9'
  if name=='Sensor value' and i==0:bg='#e1f1e5';edge='#16754a'
  ax.add_patch(FancyBboxPatch((x,y),1.37,.57,boxstyle='round,pad=.03',facecolor=bg,edgecolor=edge,lw=1.5));ax.text(x+.685,y+.285,value,ha='center',va='center',fontsize=11)
fig.suptitle('Use the mask to keep real positions, including measured zero',fontsize=15)
fig.supxlabel('Event IDs name symbols; the final real event is at position 1.\nSensor masked mean = (0 + 4) / 2 = 2. Both measurements count, including zero.',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-5-25-real-position-masks.{ext}',bbox_inches='tight')
print('Saved aligned event/ID/mask and measured-zero diagram.')
