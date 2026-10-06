import assert from "node:assert/strict";
import { readFile, stat } from "node:fs/promises";
import {readResource} from './resource-storage.mjs';

const root = new URL("../", import.meta.url);
const read = path => readFile(new URL(path, root));
const data = JSON.parse(await read("lib/academy-data.json"));
const review=JSON.parse(await read('lib/grade6-review.json'));
for (const file of ["components/visual-lesson-book.tsx", "components/sensor-lab.tsx", "components/lesson-visual.tsx", "app/lesson-book.css", "PACKAGE_EDITION.txt"]) assert.ok((await stat(new URL(file, root))).size > 0, `Missing visual book file: ${file}`);
assert.match((await read("app/learn/[role]/[level]/[week]/page.tsx")).toString(), /<VisualLessonBook/, "The week route must render the complete illustrated lesson book");
const manifest = JSON.parse(await read("lib/resource-manifest.json"));
const keySource = (await read("lib/resource-key.ts")).toString();
const keyMatch = keySource.match(/["']([A-Za-z0-9+/]{43}=)["']/);
assert.ok(keyMatch, "The curriculum encryption key is missing. Restore the complete source package.");
const key = Buffer.from(keyMatch[1], "base64");
const full = process.argv.includes("--decrypt");
let visuals = 0;
const downloads = new Set();
function reference(url, role) {
  const id = url?.match(/^\/api\/resource\/([a-f0-9]{64})$/)?.[1];
  assert.ok(id && manifest[id], `Missing curriculum resource: ${url}`);
  if (role === "student") assert.equal(manifest[id].role, "student", "Student page references a teacher resource");
  return id;
}
function walk(blocks, role) {
  let images = 0;
  for (const block of blocks) {
    if (block.type === "image") { reference(block.src, role); assert.ok(block.alt?.trim()); images++; }
    if (block.type === "gallery") for (const cell of block.cells) images += walk(cell, role);
  }
  return images;
}
assert.equal(data.levels.length, 4);
for (const level of data.levels) {
  assert.deepEqual(level.weeks.map(w => w.number), Array.from({length:36}, (_, i) => i + 1));
  for (const week of level.weeks) {
    const id=`${level.slug}/${week.number}`;
    assert.ok(review[id]?.recall&&review[id]?.task&&review[id]?.hint&&review[id]?.solution,`Incomplete Grade 6 teaching set: ${id}`);
    for(const block of week.student.pages.find(p=>p.number===5).blocks){
      if(block.type==='table')for(const row of block.rows.slice(1))assert.ok(row[1]?.trim(),`Undefined vocabulary: ${id}: ${row[0]}`);
    }
    reference(week.hero, "student");
    let count = 0;
    for (const p of week.student.pages) count += walk(p.blocks, "student");
    assert.equal(count, 20, `${level.code} week ${week.number} must include all 20 instructional visuals`);
    assert.ok(week.student.pages.every(p => p.number >= 1 && p.number <= 15), "Update the guided lesson stages to include new pages");
    const mechanism = week.student.pages.find(p=>p.number===3).blocks.filter(b=>b.text && /^(INPUT|PROCESS|OUTPUT|QUESTION|MODEL IDEA|PROOF NEEDED)\s{2,}/s.test(b.text));
    const reasoning = week.student.pages.find(p=>p.number===6).blocks.filter(b=>b.text && /^(?:STEP\s+\d+\s*(?:—\s*\w+)?\s+|\d+\.\s+)/s.test(b.text));
    assert.ok(mechanism.length >= 3 || reasoning.length >= 3, `${level.code} week ${week.number} needs a complete native teaching diagram`);
    visuals += count;
    for (const p of week.teacher.pages) walk(p.blocks, "teacher");
    walk(week.workbook.blocks, "student");
    for (const kind of ["student", "teacher", "workbook"]) downloads.add(reference(week[kind].download, kind === "teacher" ? "teacher" : "student"));
  }
}
assert.equal(downloads.size, 292);
for (const [id, metadata] of Object.entries(manifest)) {
  const path = `public/curriculum-blobs/${id}.bin`;
  assert.ok((await stat(new URL(path, root))).size > 28, `Empty resource: ${id}`);
  if (full) {
    const plain = await readResource(id,metadata,key,read);
    if (metadata.mime === "image/png") assert.equal(plain.subarray(0,8).toString("hex"), "89504e470d0a1a0a");
    if (metadata.mime === "application/pdf") assert.equal(plain.subarray(0,5).toString(), "%PDF-");
    else if (metadata.filename) assert.equal(plain.subarray(0,2).toString(), "PK");
  }
}
console.log(`Curriculum verified: 144 weeks, ${visuals} illustration placements, ${downloads.size} Word downloads, ${Object.keys(manifest).length} protected resources${full ? "; all resources decrypted successfully" : ""}.`);
