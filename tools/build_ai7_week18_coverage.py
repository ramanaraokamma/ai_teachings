from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.axis('off')
ax.text(.5,.94,'Benchmark coverage: keep the setting visible',ha='center',fontsize=20,weight='bold')
for x,title,value,detail in [(.06,'Indoor benchmark','9 / 10 = 90%','Clean indoor photos\nObserved supplied slice'),(.54,'Outdoor shade: initial','NOT MEASURED','Zero outdoor cases\nUnknown is not zero accuracy')]:
 ax.add_patch(FancyBboxPatch((x,.48),.4,.3,boxstyle='round,pad=0.015',facecolor='white',edgecolor='#326c91',linewidth=2));ax.text(x+.2,.72,title,ha='center',fontsize=13,weight='bold');ax.text(x+.2,.62,value,ha='center',fontsize=19,color='#176b99',weight='bold');ax.text(x+.2,.53,detail,ha='center',fontsize=11)
ax.text(.5,.36,'Changed scenario: four reserved outdoor cases supplied',ha='center',fontsize=14,weight='bold')
ax.text(.5,.25,'Outdoor: 2 / 4 = 50%     •     Pooled: 11 / 14 ≈ 78.6%',ha='center',fontsize=15,color='#176b99')
ax.text(.5,.1,'The pooled rate is not the outdoor rate. Neither small slice guarantees future performance.\nAll counts are supplied teaching examples; no model or new photo collection was run.',ha='center',fontsize=11)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-18-benchmark-coverage.{ext}',dpi=170,facecolor=fig.get_facecolor(),bbox_inches='tight')
