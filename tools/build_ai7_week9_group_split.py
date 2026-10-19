"""Native plant-ID grouping figure; all view markers are fictional metadata."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,6.2));fig.patch.set_facecolor('white');ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
ax.text(.5,.96,'Four plants. Twelve photo views.',ha='center',va='top',fontsize=24,weight='bold',color='#123c50')
ax.text(.5,.86,'Keep every view of a plant in the same split.',ha='center',fontsize=18,color='#345264')
for x,title,plants,color in [(.04,'TRAIN · 6 views',['P1','P2'],'#dff0e5'),(.54,'EVALUATE · 6 views',['P3','P4'],'#e3edf9')]:
 ax.add_patch(FancyBboxPatch((x,.25),.42,.53,boxstyle='round,pad=.012',facecolor=color,edgecolor='#537080',linewidth=1.5))
 ax.text(x+.21,.70,title,ha='center',fontsize=20,weight='bold',color='#123c50')
 for y,plant in zip([.54,.37],plants):
  ax.text(x+.06,y,plant,ha='center',va='center',fontsize=24,weight='bold',color='#123c50')
  for i in range(3):
   xx=x+.16+i*.085
   ax.add_patch(Circle((xx,y),.032,facecolor='white',edgecolor='#345264',linewidth=1.4))
   ax.text(xx,y,str(i+1),ha='center',va='center',fontsize=17,color='#123c50')
ax.text(.5,.15,'Each numbered marker is one view, not a new plant.',ha='center',fontsize=18,color='#345264')
ax.text(.5,.065,'No shared plant IDs across splits.\nStatistical independence still needs a justified study design.',ha='center',va='center',fontsize=17,color='#345264')
fig.subplots_adjust(left=.01,right=.99,bottom=.01,top=.99)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-09-plant-group-split.{ext}',dpi=160,facecolor='white')
plt.close(fig)
