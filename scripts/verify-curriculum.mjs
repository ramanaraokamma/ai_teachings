import assert from "node:assert/strict";
import { readFile, stat } from "node:fs/promises";
import { createDecipheriv } from "node:crypto";

const root = new URL("../", import.meta.url);
const read = path => readFile(new URL(path, root));
const data = JSON.parse(await read("lib/academy-data.json"));

for (const file of ["components/content-reader.tsx", "components/sensor-model.tsx", "components/lesson-visual.tsx", "content/programme.json"]) assert.ok((await stat(new URL(file, root))).size > 0, `Missing programme file: ${file}`);
const route = (await read("app/learn/[role]/[level]/[week]/page.tsx")).toString();
assert.match(route, /<ContentReader pages=\{week.student.pages\}/, "The week route must render every student section");
assert.match(route, /requireAccess\(role\)/, "Lesson access must remain protected");
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
  if (role === "student") assert.equal(manifest[id].role, "student", "Student content references a teacher resource");
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
assert.equal(data.version, "complete-programme-2026-10-07");
assert.deepEqual(data.levels.map(l=>l.slug), [...Array.from({length:7},(_,i)=>`ai-${i+1}`), "python-bridge"]);
let weeks = 0;
for (const level of data.levels) {
  const expected = level.slug === "python-bridge" ? 12 : 36;
  assert.deepEqual(level.weeks.map(w => w.number), Array.from({length:expected}, (_, i) => i + 1));
  for (const week of level.weeks) {
    weeks++;
    const id=`${level.slug}/${week.number}`;
    reference(week.hero, "student");
    assert.ok(week.student.pages.length >= 14, `Missing student sections: ${id}`);
    assert.ok(week.teacher.pages.length >= 6, `Missing teacher sections: ${id}`);
    for (const kind of ["student", "teacher"]) {
      const pages=week[kind].pages;
      assert.deepEqual(pages.map(p=>p.number),Array.from({length:pages.length},(_,i)=>i+1));
      for (const page of pages) {
        assert.ok(page.label?.trim() && page.blocks.length, `Empty section: ${id}/${kind}/${page.number}`);
        const count=walk(page.blocks,kind);
        if(kind === "student") visuals+=count;
      }
    }
    assert.ok(week.workbook.blocks.length, `Empty workbook: ${id}`);
    walk(week.workbook.blocks, "student");
    for (const kind of ["student", "teacher", "workbook"]) {
      const role=kind === "teacher" ? "teacher" : "student";
      for (const format of ["download", "pdf"]) {
        const rid=reference(week[kind][format],role);
        assert.equal(manifest[rid].role,role,"Download audience mismatch");
        assert.ok(manifest[rid].filename?.endsWith(format==='pdf'?'.pdf':'.docx'));
        downloads.add(rid);
      }
    }
  }
}
assert.equal(weeks,264);
assert.equal(downloads.size,1584);
for (const [id, metadata] of Object.entries(manifest)) {
  const path = `public/curriculum-blobs/${id}.bin`;
  assert.ok((await stat(new URL(path, root))).size > 28, `Empty resource: ${id}`);
  if (full) {
    const encrypted = await read(path);
    const decipher = createDecipheriv("aes-256-gcm", key, encrypted.subarray(0, 12));
    decipher.setAAD(Buffer.from(id));
    decipher.setAuthTag(encrypted.subarray(-16));
    const plain = Buffer.concat([decipher.update(encrypted.subarray(12, -16)), decipher.final()]);
    if (metadata.mime === "image/png") assert.equal(plain.subarray(0,8).toString("hex"), "89504e470d0a1a0a");
    if (metadata.mime === "application/pdf") assert.equal(plain.subarray(0,5).toString(), "%PDF-");
    else if (metadata.mime === "application/vnd.openxmlformats-officedocument.wordprocessingml.document") assert.equal(plain.subarray(0,2).toString(), "PK");
  }
}
console.log(`Curriculum verified: ${weeks} lessons, ${visuals} illustration placements, ${downloads.size} Word/PDF downloads, ${Object.keys(manifest).length} protected resources${full ? "; all resources decrypted successfully" : ""}.`);
