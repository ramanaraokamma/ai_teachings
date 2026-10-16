"""Learner-safe index of week-specific outcomes and worked pictures."""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1];D=json.loads((R/'content/programme.json').read_text());e=html.escape
if not D.get('pictorial_case_design'):raise SystemExit('Integrate reviewed cases first')
body='<main><header class="hero"><p class="kicker">AI Academy · Discover, build and explain</p><h1>Explore AI through clear examples and pictures</h1><p>Each lesson now has a six-picture concept journey, a learning goal, a changed condition and questions to explain. Your full lesson and project stay connected.</p></header><div class="actions"><a href="START_HERE.html">Programme home</a><a href="student/index.html">Complete student lessons</a><a href="student/LEARNING_GUIDE.html">How to learn</a></div><nav class="contents">'+''.join(f'<a href="#level-{l["number"]}">Level {l["number"]}: {e(l["name"])}</a>' for l in D['levels'])+'<a href="#bridge">Python readiness</a></nav>'
groups=[]
for level in D['levels']:
 groups.append((f'level-{level["number"]}',[w for w in D['weeks'] if w['level']==level['number']]))
 if level['number']==3:groups.append(('bridge',D['python_bridge']))
for label,group in groups:
 heading='Python readiness' if label=='bridge' else 'Level '+str(group[0]['level'])+': '+D['levels'][group[0]['level']-1]['name']
 body+='<section class="chapter" id="'+label+'"><h2>'+e(heading)+'</h2><div class="week-grid">'
 for w in group:
  a=w['pictorial_case'];stem=('bridge-' if w['id'].startswith('python') else f"ai-{w['level']}-")+f"week-{w['week']:02}"
  image=(w.get('graphic_story',[{},{}])[1].get('asset') or ('academy-detail-' if a.get('mini_visual') else 'academy-visual-')+w['id'].replace('/','-'))+'.png'
  body+='<article class="week-card"><p class="kicker">Week '+str(w['week'])+'</p><h3>'+e(w['title'])+'</h3><p>'+e(a['outcome'])+'</p><details><summary>Preview the worked picture</summary><img loading="lazy" src="assets/'+image+'" alt="'+e(w['graphic_story'][1]['alt'] if w.get('graphic_story') else a.get('mini_visual',{}).get('title',a['title']))+'" style="width:100%;height:auto"></details><p>'+e(a['scenario'])+'</p><p><a href="student/'+stem+'.html#section-'+str(next(i+1 for i,s in enumerate(w['sections']) if s['title']=='Visual concept journey'))+'">Open the lesson and six-picture journey</a> · <a href="workbook/'+stem+'.html">Practise in your workbook</a></p></article>'
 body+='</div></section>'
body+='<footer>Worked pictures support practice. Attempt the separate independent case before feedback, and record any help.</footer></main>'
(R/'PICTORIAL_LESSONS.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Academy · Pictorial lessons</title><link rel="stylesheet" href="assets/programme.css"></head><body>'+body+'</body></html>')
