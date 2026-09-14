import {readFileSync, writeFileSync} from 'node:fs';
import assert from 'node:assert/strict';
const curriculum=JSON.parse(readFileSync('lib/academy-data.json','utf8'));
const kinds=new Set(['compare','flow','cycle','branch','trace','bars','groups','pixels','wave','split','fractions','matrix','tokens','context','spatial','checklist','residual','curve']);
const plans={};
const after=(blocks,heading)=>{
 const i=blocks.findIndex(b=>b.text===heading);
 assert.ok(i>=0,`Missing ${heading}`);
 return blocks.slice(i+1).find(b=>b.type==='paragraph')?.text??'';
};
for(const line of readFileSync('lib/topic-plans.txt','utf8').trim().split('\n')){
 const fields=line.split('|');assert.equal(fields.length,6,line);
 const [id,kind,title,rawItems,teach,misconception]=fields;
 assert.ok(!plans[id],`Duplicate ${id}`);assert.ok(kinds.has(kind),kind);
 const [slug,n]=id.split('/');const level=curriculum.levels.find(l=>l.slug===slug);const week=level?.weeks.find(w=>w.number===+n);
 assert.ok(week,`Unknown week ${id}`);
 const items=rawItems.split(';').map(s=>{const colon=s.indexOf(':');assert.ok(colon>0,s);return {label:s.slice(0,colon),value:s.slice(colon+1)};});
 assert.ok(items.length>0);
 if(['bars','groups','pixels','wave','split','context','matrix','residual','curve'].includes(kind))items.forEach(i=>assert.ok(Number.isFinite(Number(i.value))&&Number(i.value)>=0,`${id}: ${i.value}`));
 if(kind==='fractions')items.forEach(i=>{const [a,b]=i.value.split('/').map(Number);assert.ok(b>0&&a>=0&&a<=b,`${id}: invalid fraction`);});
 if(kind==='matrix')assert.equal(items.length,4);
 if(kind==='pixels'){assert.equal(items.length,4);items.forEach(i=>assert.ok(['0','1'].includes(i.value)));}
 const blocks=week.student.pages.find(p=>p.number===13).blocks;
 plans[id]={id,kind,title,items,teach,misconception,lesson:week.student.title,scenario:after(blocks,'The situation'),question:after(blocks,'The question'),explanation:after(blocks,'Worked explanation')};
}
for(const level of curriculum.levels)for(const week of level.weeks)assert.ok(plans[`${level.slug}/${week.number}`],`Missing ${level.slug}/${week.number}`);
assert.equal(Object.keys(plans).length,144);
writeFileSync('lib/topic-plans.json',JSON.stringify(plans,null,2)+'\n');
const rows=Object.values(plans).map(p=>`| ${p.id.split('/')[0].toUpperCase()} | ${p.id.split('/')[1]} | ${p.lesson.replace(/^Week \d+: /,'')} | ${p.kind} | ${p.title} |`);
writeFileSync('VISUAL_COVERAGE.md',`# All-level visual teaching coverage\n\nEdition: topic-studio-2026-09-14. All 144 weekly lessons have an individually authored diagram specification, a matching worked case, a misconception discussion and a teacher prompt. Existing student and teacher text, workbook missions and 292 protected DOCX downloads are retained. The DOCX files are the original editions; these improvements are to the website and printable HTML.\n\nDiagrams use exact HTML/SVG labels and quantities rather than generated text inside images. Existing weekly story art and vocabulary artwork remain available. Generic stage/case raster cards are replaced in the main reading flow; their source text is retained.\n\n| Level | Week | Concept | Visual form | Diagram |\n|---|---:|---|---|---|\n${rows.join('\n')}\n`);
console.log(`Compiled ${Object.keys(plans).length} individually specified visual lessons across ${curriculum.levels.length} levels.`);
