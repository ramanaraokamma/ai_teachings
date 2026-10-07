import "server-only";

import academyData from "./academy-data.json";

export type AcademyRole = "student" | "teacher";

export type ContentBlock =
  | { type: "sensor"; title: string }
  | { type: "diagram"; kind: string; title?: string; columns?: string[]; rows?: string[][]; values?: number[][]; series?: {label: string; values: number[]}[]; xValues?: number[]; axis?: string; xLabel?: string; key?: string; caption?: string }
  | { type: "image"; src: string; alt: string; width: number; height: number }
  | { type: "gallery"; cells: ContentBlock[][] }
  | { type: "title" | "heading" | "subheading" | "paragraph" | "step" | "code" | "response"; text: string }
  | { type: "list"; marker: "bullet" | "number"; text: string }
  | { type: "callout"; tone: "idea" | "think" | "caution" | "teacher" | "answer"; text: string }
  | { type: "table"; rows: string[][] };

export type LessonPage = { number: number; label: string; blocks: ContentBlock[] };

export type Week = {
  number: number;
  phase: number;
  hero: string | null;
  student: { title: string; pages: LessonPage[]; download: string; pdf: string };
  teacher: { title: string; pages: LessonPage[]; download: string; pdf: string };
  workbook: { title: string; blocks: ContentBlock[]; download: string; pdf: string };
};

export type Level = {
  slug: string;
  code: string;
  name: string;
  ages: string;
  accent: "sky" | "violet" | "amber" | "emerald";
  summary: string;
  capstone: string;
  focus: string[];
  phases: { number: number; name: string; weeks: string }[];
  weeks: Week[];
};

type AcademyData = { version: string; levels: Level[] };

export const academy = academyData as unknown as AcademyData;
export const levels = academy.levels;

export function getLevel(slug: string): Level | undefined {
  return levels.find((level) => level.slug === slug);
}

export function getWeek(level: Level, weekNumber: string | number): Week | undefined {
  const value = Number(weekNumber);
  return Number.isInteger(value) ? level.weeks.find((week) => week.number === value) : undefined;
}

export function titleWithoutWeek(title: string): string {
  return title.replace(/^Week\s+\d+\s*:\s*/i, "").trim();
}

export function learningKind(week: number): string {
  if (week <= 6) return "Discover";
  if (week <= 12) return "Practice";
  if (week <= 18) return "Investigate";
  if (week <= 24) return "Evaluate";
  if (week <= 30) return "Design";
  return "Capstone";
}
