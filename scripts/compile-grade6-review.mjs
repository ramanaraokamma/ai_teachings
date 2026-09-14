import {readFileSync, writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';

const data=JSON.parse(readFileSync('lib/academy-data.json','utf8'));
const lines=path=>readFileSync(path,'utf8').split('\n').filter(s=>s.trim()&&!s.startsWith('#'));
const definitions=Object.fromEntries(lines('lib/vocabulary-definitions.txt').map(line=>{
 const [term,definition,...extra]=line.split('|');
 assert.ok(term&&definition&&!extra.length,`Malformed definition: ${term}`);
 return [term,definition];
}));
const review={};
for(const line of lines('lib/grade6-review.txt')){
 const [id,recall,task,hint,solution,...extra]=line.split('|');
 assert.ok(id&&recall&&task&&hint&&solution&&!extra.length,`Malformed review: ${id}`);
 assert.ok(!review[id],`Duplicate review: ${id}`);
 review[id]={id,recall,task,hint,solution};
}
const names=['Foundations','Algorithms & Data','Generative AI Systems','Machine Learning'];
const summaries=[
 'Start in Grade 6: explain representations, rules, learning and uncertainty, then defend a tested classroom prototype.',
 'Build on foundations: trace algorithms, organise data, compare predictions and implement a reproducible recommender.',
 'Build on algorithms and data: investigate generation, retrieval, verification and bounded tools, then evaluate a grounded assistant.',
 'Build on data and programming readiness: fit and compare small models, examine errors and defend an evaluated ML project.'
];
let defined=0;
for(const [index,level] of data.levels.entries()){
 level.name=names[index];
 level.ages=`Typical entry: Grade ${6+index}`;
 level.summary=summaries[index];
 for(const week of level.weeks){
  const id=`${level.slug}/${week.number}`;
  assert.ok(review[id],`Missing review: ${id}`);
  const target=review[id].task;
  const replaceAfter=(blocks,heading)=>{
   const index=blocks.findIndex(b=>b.text===heading);
   if(index>=0){const next=blocks.slice(index+1).find(b=>b.type==='paragraph');if(next)next.text=target;}
  };
  replaceAfter(week.workbook.blocks,'Your learning target');
  replaceAfter(week.teacher.pages[0].blocks,'What the learner must demonstrate');
  const mission=week.student.pages[0].blocks.find(b=>b.type==='callout'&&/MISSION|LEARNING TARGET/.test(b.text));
  if(mission)mission.text=`LEARNING TARGET  ${target}`;
  const oldNames=['Explorer','Thinker','Creator','ML Builder'];
  const refreshText=blocks=>{for(const b of blocks){
   if(b.type==='gallery')b.cells.forEach(refreshText);
   if(b.type==='image')b.alt=b.alt.replace('Child-friendly story illustration','Concept illustration');
   if(typeof b.text==='string'){
    b.text=b.text.replace(/Explorer name:/g,'Learner name:');
    for(let n=0;n<4;n++)b.text=b.text.replaceAll(`AI-${n+1} ${oldNames[n]}`,`AI-${n+1} ${names[n]}`);
    b.text=b.text.replace('Curriculum 2.0 refined edition','Grade 6 entry edition');
   }
  }};
  week.student.pages.forEach(p=>refreshText(p.blocks));
  week.teacher.pages.forEach(p=>refreshText(p.blocks));refreshText(week.workbook.blocks);
  if(level.slug==='ai-4'&&[13,22].includes(week.number)){
   const file=week.number===13?'threshold_classifier':'linear_regression';
   const code=readFileSync(`examples/${file}.py`,'utf8');
   for(const role of ['student','teacher'])for(const page of week[role].pages){
    // The converter flattened original Python paragraphs; preserve one canonical runnable block.
    const start=page.blocks.findIndex(b=>(b.type==='paragraph'&&b.text.startsWith('train = ['))||b.type==='code'&&b.text.includes('train = [('));
    if(start>=0){
     if(page.blocks[start].type==='code')page.blocks[start].text=code;
     else {
      const end=page.blocks.findIndex((b,i)=>i>=start&&b.text?.startsWith('print('));
      assert.ok(end>=start,`Incomplete code: ${id}`);
      page.blocks.splice(start,end-start+1,{type:'code',text:code});
     }
    }
   }
   if(week.number===22){
    const page=week.student.pages.find(p=>p.number===15);
    if(!page.blocks.some(b=>b.text==='Math bridge: fitting the line')){
     page.blocks.splice(2,0,
      {type:'subheading',text:'Math bridge: fitting the line'},
      {type:'paragraph',text:'A straight line predicts y = slope × x + intercept. Slope is the change in predicted height for one extra week; intercept is the prediction at x=0, which may lie outside the measured ages. You need means, subtraction, multiplication and squared numbers for this example; calculus is not required.'},
      {type:'table',rows:[['x (weeks)','y (cm)','x − mean x','y − mean y','Product','Squared x difference'],['1','3','−1','−2','2','1'],['2','5','0','0','0','0'],['3','7','1','2','2','1']]},
      {type:'paragraph',text:'Mean x=2 and mean y=5. Add the product column: 4. Add squared x differences: 2. Slope=4/2=2 cm per week. Intercept=5−2×2=1 cm. This least-squares formula chooses the line minimising squared training errors when the x values are not all identical. Compare its held-out error with a baseline; a good training fit alone is insufficient.'}
     );
    }
   }
  }
  // Fill meanings, but preserve intentionally empty student example/response cells.
  const vocabulary=week.student.pages.find(p=>p.number===5).blocks.filter(b=>b.type==='table');
  for(const table of vocabulary)for(const row of table.rows.slice(1)){
   if(!row[1]?.trim()||[1,2].includes(index)&&definitions[row[0]]){
    assert.ok(definitions[row[0]],`Missing definition: ${id}: ${row[0]}`);
    if(!row[1]?.trim())defined++;
    row[1]=definitions[row[0]];
   }
  }
  const meanings=new Map(vocabulary.flatMap(t=>t.rows.slice(1).map(r=>[r[0],r[1]])));
  for(const page of week.teacher.pages)for(const block of page.blocks){
   if(block.type==='table'&&/Term|Word/i.test(block.rows[0]?.[0]??'')){
    for(const row of block.rows.slice(1))if(meanings.has(row[0]))row[1]=meanings.get(row[0]);
   }
  }
 }
}
assert.equal(Object.keys(review).length,data.levels.reduce((n,l)=>n+l.weeks.length,0));
// Keep the source edition identifier: protected original DOCX resources still use it.
writeFileSync('lib/academy-data.json',JSON.stringify(data)+'\n');
writeFileSync('lib/grade6-review.json',JSON.stringify(review,null,2)+'\n');
const rows=data.levels.flatMap(level=>level.weeks.map(week=>{
 const r=review[`${level.slug}/${week.number}`];
 return `| ${level.code} | ${week.number} | ${week.student.title.replace(/^Week \d+: /,'')} | ${r.recall} | ${r.task} |`;
}));
writeFileSync('GRADE6_REVIEW.md',`# Grade 6 entry redesign — review register\n\nAll 144 existing weeks have a prerequisite retrieval prompt, a fresh transfer task, a hint and a teacher solution. The four existing levels retain their topic order and protected resource routes. Typical grades 6–9 guide presentation; they are not age gates or validated placement decisions. The proposed seven-level replacement from prior planning is not represented as completed curriculum.\n\nStudent and teacher vocabulary meanings are now populated consistently. The new tasks require reasoning beyond the original early-years examples. Original DOCX downloads remain identified as the prior edition; current lessons, workbooks and guides are available through the portal's print action.\n\n## Review boundaries\n\nThis register records an editorial review of the weekly concepts, prerequisite sequence, worked-case explanations and transfer assessment. Structural checks inspect every student, teacher and workbook resource. It is not a claim that every legacy paragraph was rewritten or that classroom learning outcomes have been validated. Browser and print checks are reported separately in the validation report.\n\n## Design references\n\n[AI4K12 grade-band charts](https://ai4k12.org/gradeband-progression-charts/) provide a broad K–12 progression; [UNESCO's student framework](https://www.unesco.org/en/articles/ai-competency-framework-students?hub=66973) combines human-centred, ethical, technical and design competencies. These are reference points, not certification or a completed standards alignment. [scikit-learn's common pitfalls](https://scikit-learn.org/1.8/common_pitfalls.html) informs the separation of fitting, validation and final testing.\n\n| Level | Week | Existing concept | Prerequisite retrieval | New transfer assessment |\n|---|---:|---|---|---|\n${rows.join('\n')}\n`);
console.log(`Grade 6 review: ${rows.length} weeks, ${Object.keys(definitions).length} definitions available, ${defined} empty student meanings filled.`);
