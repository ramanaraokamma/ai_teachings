import assert from 'node:assert/strict';import fs from 'node:fs';
const tools=JSON.parse(fs.readFileSync('lib/learning-tools.json'));let event;const messages=[];globalThis.self={postMessage:m=>{event=m;messages.push(m);}};
await import('../public/python-lab-worker.mjs');assert.equal(event.type,'ready');assert.equal(event.version,'314.0.7');
const results=[];
for(const [week,value] of Object.entries(tools))for(const [index,lab] of value.labs.entries()){
 await self.onmessage({data:{type:'run',code:lab.code}});assert.equal(event.type,'result');const intended=week==='python-bridge/7'&&lab.code.trim()==='counts = [4, 7, 4]\nprint(counts[3])';const okay=intended?event.error.includes('IndexError'):!event.error;results.push({week,index,expected_error:intended,passed:okay,stdout:event.stdout,error:event.error});assert.ok(okay,`${week}/${index}: ${event.error}`);
}
await self.onmessage({data:{type:'run',code:'print(7 * 3)'}});assert.equal(event.stdout,'21');
await self.onmessage({data:{type:'run',code:'print(items[2])'}});assert.ok(event.error.includes('NameError'));
await self.onmessage({data:{type:'run',code:'print(open("durations.txt").read().splitlines())'}});assert.equal(event.stdout,"['12', '8']");
const pilot=JSON.parse(fs.readFileSync('lib/pilot-data.json'));const branch=pilot.find(t=>t.id==='python-bridge/5');let branchChecks=0;
for(const [phase,checks] of Object.entries({baseline:[[20,'off'],[19,'on'],[101,'invalid']],post:[[30,'off'],[29,'on'],[-1,'invalid']],delayed:[[24,'on'],[25,'off'],[100,'off'],[101,'invalid'],[-1,'invalid']]}))for(const [reading,want] of checks){const source=branch[phase].code.replace(/reading = [-0-9]+/,`reading = ${reading}`);await self.onmessage({data:{type:'run',code:source}});assert.equal(event.stdout,want);assert.equal(event.error,'');branchChecks++;}
fs.writeFileSync('reports/python-lab-validation.json',JSON.stringify({runtime:'314.0.7',examples:results.length,pilot_branch_checks:branchChecks,errors:results.filter(r=>!r.passed),results},null,2));console.log(`${results.length} supported Python examples executed in the vendored runtime.`);
