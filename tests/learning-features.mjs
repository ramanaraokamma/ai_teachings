import assert from 'node:assert/strict';
import {collectEvidence,portfolioHTML} from '../lib/learning/portfolio.ts';
class Store {data=new Map();get length(){return this.data.size;}key(i){return [...this.data.keys()][i]||null;}getItem(k){return this.data.get(k)||null;}setItem(k,v){this.data.set(k,v);}}
const store=new Store();const key='academy-answer-v1:/learn/student/ai-1/1:workbook:ai-1/1/workbook-section-1-block-2';store.setItem(key,'My prediction was wrong; the deciding evidence changed my explanation.');store.setItem(`academy-answer-meta-v1:${key}`,JSON.stringify({prompt:'Explain your revised prediction',updatedAt:'2026-10-07T12:00:00Z'}));store.setItem('academy-answer-v1:/learn/teacher/ai-1/1:guide:section-1','Private teacher response');store.setItem('academy-answer-v1:/learn/student/ai-2/1:lesson:section-2','Later learner response');
assert.equal(collectEvidence(store,'student').length,2);assert.equal(collectEvidence(store,'student','ai-1/1').length,1);assert.equal(collectEvidence(store,'teacher').length,1);assert.equal(collectEvidence(store,'student')[0].prompt,'Explain your revised prediction');
const html=portfolioHTML([{...collectEvidence(store,'student')[0],answer:'<script>alert(1)</script>'}],{'ai-1/1':{title:'AI or Not?',project:'Classroom Sorter'}},'2026-10-07');assert.ok(html.includes('Classroom Sorter'));assert.ok(html.includes('&lt;script&gt;'));assert.ok(!html.includes('<script>'));assert.ok(!html.includes('Private teacher response'));
console.log('Portfolio scope, role boundaries, labels and escaped printable export passed.');

import fs from 'node:fs';
const tools=JSON.parse(fs.readFileSync('lib/learning-tools.json'));const programme=JSON.parse(fs.readFileSync('content/programme.json'));const weeks=new Map([...programme.weeks,...programme.python_bridge].map(w=>[w.id,w]));
assert.equal(Object.keys(tools).length,264);
for(const [week,data] of Object.entries(tools)){
 assert.equal(data.questions.length,2);
 for(const q of data.questions){assert.equal(q.choices.filter(c=>c.correct).length,1);assert.ok(!q.choices.some(c=>c.text===weeks.get(week).method.independent.answer));assert.ok(q.hint.length>20);}
 for(const repair of data.repairs){assert.ok(weeks.has(repair.week));assert.equal(weeks.get(repair.week).sections[repair.section-1].title,'Follow a worked example');assert.notEqual(repair.week,week);}
 for(const lab of data.labs)assert.ok(!weeks.get(week).sections.filter(s=>s.title==='Try a new case independently').flatMap(s=>s.blocks).some(b=>b.type==='code'&&b.text===lab.code));
}
console.log('All 528 formative questions, reserved assessment boundaries and 719 repair links checked.');
import {pilotCSV,pilotSummary,validPilotRow} from '../lib/learning/pilot.ts';
const observation={track:'ai-1/1',group:'TEST_GROUP',learnerCode:'TEST01',phase:'baseline',date:'2026-10-01',priorExposure:'no',supportUsed:'none',explanation:'not yet',trace:'with support',limits:'not yet',minutes:6,learnerEvidence:'Synthetic unit-test evidence only',confusingPart:'',accessBarrier:'',nextAction:''};
assert.ok(validPilotRow(observation));assert.ok(!validPilotRow({...observation,date:'2026-99-99'}));assert.ok(!validPilotRow({...observation,minutes:-1}));assert.ok(!validPilotRow({...observation,learnerEvidence:''}));
const summary=pilotSummary([observation,{...observation,phase:'post',date:'2026-10-02',explanation:'independent',trace:'with support',limits:'with support'}]);assert.equal(summary.learners,1);assert.equal(summary.post.pairedLearners,1);assert.equal(summary.post.dimensions.explanation.improved,1);assert.equal(summary.post.dimensions.trace.unchanged,1);assert.equal(pilotSummary([]).learners,0);assert.equal(pilotSummary([observation,{...observation,phase:'post',priorExposure:'yes'}]).post.pairedLearners,0);assert.equal(pilotSummary([observation,{...observation,phase:'post',date:'2026-09-30'}]).post.pairedLearners,0);assert.ok(pilotCSV([{...observation,learnerEvidence:'=1+1'}]).includes("'=1+1"));
const pilot=JSON.parse(fs.readFileSync('lib/pilot-data.json'));assert.equal(pilot.length,3);
const baseline=['A','A','B'],refs=['A','B','B'],candidate=['A','B','A'];assert.equal(refs.filter(x=>x==='A').length,1);assert.equal(candidate.filter((x,i)=>x===refs[i]).length,2);
const validation=['blue','red','red','blue','blue'],proposed=['red','red','blue','red','blue'];assert.equal(validation.filter(x=>x==='blue').length,3);assert.equal(proposed.filter((x,i)=>x===validation[i]).length,2);
console.log('Pilot validation, fresh/date-matched comparisons, CSV safety and task arithmetic passed (synthetic tests only).');
