"""Code-native crossed-condition illustration, not collected plant photos."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch,Ellipse
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,7));fig.patch.set_facecolor('white');ax.set(xlim=(0,1),ylim=(0,1));ax.axis('off')
ax.text(.5,.97,'Cross leaf condition with background.',ha='center',va='top',fontsize=24,weight='bold',color='#123c50')
for x,paper in [(.38,'White paper'),(.77,'Blue paper')]:ax.text(x,.84,paper,ha='center',fontsize=21,weight='bold',color='#123c50')
for y,leaf,condition in [(.63,'H1','Healthy'),(.32,'S1','Spotted')]:
 ax.text(.035,y,condition+'\n'+leaf,ha='left',va='center',fontsize=21,weight='bold',color='#123c50')
 for x,color in [(.38,'#ffffff'),(.77,'#a7cee8')]:
  ax.add_patch(FancyBboxPatch((x-.15,y-.13),.30,.26,boxstyle='round,pad=.01',facecolor=color,edgecolor='#537080',linewidth=1.7))
  ax.add_patch(Ellipse((x,y),.17,.13,angle=25,facecolor='#62a45d',edgecolor='#28603b',linewidth=2))
  ax.plot([x-.07,x+.07],[y-.035,y+.035],color='#28603b',linewidth=2)
  if condition=='Spotted':
   for dx,dy in [(-.032,.02),(.025,.025),(.015,-.025)]:ax.add_patch(Ellipse((x+dx,y+dy),.026,.026,facecolor='#875738',edgecolor='#70442d'))
ax.text(.5,.13,'Same leaf ID in each row; only the background changes.',ha='center',fontsize=18,color='#345264')
ax.text(.5,.055,'Illustrated design: not collected photos or model predictions.',ha='center',fontsize=17,color='#345264')
fig.subplots_adjust(left=.01,right=.99,bottom=.01,top=.99)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-10-crossed-leaf-background.{ext}',dpi=160,facecolor='white')
plt.close(fig)
