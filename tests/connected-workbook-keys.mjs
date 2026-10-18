import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
const data=JSON.parse(await fs.readFile('lib/academy-data.json','utf8'));let weeks=0,responses=0;
for(const level of data.levels)for(const week of level.weeks){
 if(!week.workbook.pages)continue;
 const fields=week.workbook.pages.flatMap(p=>p.blocks.filter(b=>b.type==='response'));
 const keys=fields.map(b=>b.responseStorageSuffix);
 assert.ok(keys.every(Boolean));assert.equal(new Set(keys).size,keys.length,`${level.slug}/${week.number}: response keys collide`);
 if(level.slug==='ai-2'&&week.number===5){assert.equal(week.workbook.pages[11].blocks[1].responseStorageSuffix,'section-1-block-48');assert.equal(fields.filter(b=>b.reading_addition).length,4);}
 weeks++;responses+=keys.length;
}
console.log(`${responses} response keys across ${weeks} authored workbooks are unique; original Week 5 range answers retain their key.`);
