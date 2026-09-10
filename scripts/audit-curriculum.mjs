import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";

const data = JSON.parse(await readFile(new URL("../lib/academy-data.json", import.meta.url), "utf8"));
const art = await readdir(new URL("../public/academy-art/", import.meta.url));

assert.equal(data.version, "Curriculum 2.0 — Refined Edition");
assert.equal(data.levels.length, 4);
assert.equal(art.length, 144);

let weeks = 0;
let studentSections = 0;
let teacherSections = 0;
let workbookWeeks = 0;

for (const level of data.levels) {
  assert.equal(level.weeks.length, 36, `${level.code} must contain 36 weeks`);
  for (const [index, week] of level.weeks.entries()) {
    const number = index + 1;
    const codeLab = level.code === "AI-4" && [13, 22].includes(number);
    assert.equal(week.number, number);
    assert.equal(week.student.pages.length, codeLab ? 15 : 14, `${level.code} Week ${number} student sections`);
    assert.equal(week.teacher.pages.length, codeLab ? 7 : 6, `${level.code} Week ${number} teacher sections`);
    assert.ok(week.workbook.blocks.length >= 15, `${level.code} Week ${number} workbook content`);
    assert.match(week.hero, /^\/academy-art\/[a-f0-9]+\.(png|jpg|webp)$/);
    weeks += 1;
    studentSections += week.student.pages.length;
    teacherSections += week.teacher.pages.length;
    workbookWeeks += 1;
  }
}

const accessSource = await readFile(new URL("../lib/access.ts", import.meta.url), "utf8");
const accessRoute = await readFile(new URL("../app/api/access/route.ts", import.meta.url), "utf8");
assert.match(accessRoute, /httpOnly:\s*true/);
assert.match(accessSource, /STUDENT_PASSCODE/);
assert.match(accessSource, /TEACHER_PASSCODE/);
assert.doesNotMatch(accessSource, /student1234|teacher1234/);

console.log(JSON.stringify({ levels: 4, weeks, studentSections, teacherSections, workbookWeeks, heroes: art.length }));
