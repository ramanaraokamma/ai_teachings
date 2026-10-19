from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,ax=plt.subplots(figsize=(10,6));fig.patch.set_facecolor('#f4f8fc');ax.set_facecolor('white')
ax.barh(['Disagree','Agree'],[1,3],color=['#b35e43','#16836f'],height=.5)
for y,x in enumerate([1,3]):ax.text(x+.06,y,f'{x} of 4',va='center',fontsize=13,weight='bold')
ax.set_xlim(0,4);ax.set_xticks(range(5));ax.set_xlabel('Practice answers scored by both reviewers',fontsize=12);ax.set_title('Pilot agreement: 3 / 4 = 75%',fontsize=20,weight='bold',pad=20);ax.spines[['top','right']].set_visible(False)
fig.text(.1,.09,'One disagreement can reveal a rubric problem; its cause is not supplied.\nThese four revised practice answers are development evidence, not untouched final cases.\nAgreement is not correctness or a long-run reliability estimate.',fontsize=11)
fig.subplots_adjust(left=.17,right=.92,bottom=.3,top=.83)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-22-pilot-agreement.{ext}',dpi=170,facecolor=fig.get_facecolor())
