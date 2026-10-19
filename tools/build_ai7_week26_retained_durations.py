from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=Path(__file__).resolve().parents[1]
fig,axes=plt.subplots(2,1,figsize=(11,6));fig.patch.set_facecolor('#f4f8fc')
for ax,values,title,mean in [(axes[0],[1,2,2,15],'Main: all four traces stipulated valid',5),(axes[1],[2,2,2,10],'Separate picture: fourth trace logs a source timeout',4)]:
 ax.scatter(values,[.7,.6,.8,.7],s=130,c=['#176b99']*3+['#b35e43']);ax.axvline(mean,color='#16836f',linestyle='--',label=f'Mean = {mean} s');ax.axvline(2,color='#7756a5',linestyle=':',label='Median = 2 s');ax.set_xlim(0,16);ax.set_ylim(.35,1.05);ax.set_yticks([]);ax.set_title(title,fontsize=12,weight='bold');ax.set_xlabel('Supplied duration (seconds)');ax.legend(loc='upper center',ncol=2,fontsize=10);ax.spines[['top','right','left']].set_visible(False)
fig.suptitle('Investigate a slow valid case; keep it in the planned analysis',fontsize=16,weight='bold')
fig.text(.09,.04,'Vertical offsets separate overlapping dots; they carry no measurement. No actual timings were run.\nThe timeout event does not establish every underlying cause; a proposed explanation still needs a test.',fontsize=10)
fig.subplots_adjust(left=.08,right=.95,bottom=.2,top=.82,hspace=.65)
for ext in ['png','svg']:fig.savefig(R/f'assets/ai-7-26-retained-durations.{ext}',dpi=170,facecolor=fig.get_facecolor())
