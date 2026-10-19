from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(11,6));fig.patch.set_facecolor('#f4f8fc');ax.axis('off')
ax.set_title('Method details decide the boundary case',fontsize=21,weight='bold',pad=25)
t=ax.table(cellText=[['oak','3','short','short'],['pine','4','long','short ← changes'],['willow','6','long','long']],colLabels=['Exact input','Characters','Length ≥ 4','Length > 4'],cellLoc='center',loc='center',bbox=[.06,.32,.88,.5]);t.auto_set_font_size(False);t.set_fontsize(14)
for (row,col),cell in t.get_celld().items():cell.set_edgecolor('#668095');cell.set_facecolor('#d7e8f1' if row==0 else '#ffffff')
fig.text(.1,.12,'No whitespace trimming. The rule, input and inclusive/strict boundary must be recorded.\n“Long” is a toy string label, not an ecological category or a learned-model result.',fontsize=12)
fig.subplots_adjust(top=.8,bottom=.1)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-30-method-boundary.{ext}',dpi=170,facecolor=fig.get_facecolor())
