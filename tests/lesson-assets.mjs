import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {createDecipheriv,createHash} from 'node:crypto';
const source=JSON.parse(await readFile('lib/academy-data.json','utf8'));
const index=JSON.parse(await readFile('lib/academy-index.json','utf8'));
const key=Buffer.from((await readFile('lib/resource-key.ts','utf8')).match(/resourceKey\s*=\s*"([^"]+)"/)[1],'base64');
let count=0;
for(const [li,level] of source.levels.entries())for(const [wi,week] of level.weeks.entries()){
 const entry=index.levels[li].weeks[wi];
 const bytes=await readFile(`public/lesson-blobs/${entry.contentId}.bin`);
 const cipher=createDecipheriv('aes-256-gcm',key,bytes.subarray(0,12));
 cipher.setAAD(Buffer.from(entry.contentId));cipher.setAuthTag(bytes.subarray(-16));
 const plain=Buffer.concat([cipher.update(bytes.subarray(12,-16)),cipher.final()]);
 assert.equal(createHash('sha256').update(plain).digest('hex'),entry.contentId);
 assert.deepEqual(JSON.parse(plain),week,`${level.slug}/${week.number} content changed`);
 for(const role of ['student','teacher','workbook'])assert.equal(entry[role].pages.length,0);
 count++;
}
assert.equal(count,264);
console.log(`${count} encrypted weeks match every original student, teacher and workbook field.`);
