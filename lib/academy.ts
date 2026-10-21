import "server-only";
import type {ReadingPresentation,ReadingFlow} from "./reading-format";

import academyData from "./academy-index.json";

export type AcademyRole = "student" | "teacher";

export type ContentBlock = (
  | { type: "sensor"; title: string }
  | { type: "diagram"; kind: string; max?:number; title?: string; columns?: string[]; rows?: string[][]; values?: number[][]; series?: {label: string; values: number[]}[]; xValues?: number[]; axis?: string; xLabel?: string; key?: string; caption?: string }
  | { type: "image"; src: string; alt: string; width: number; height: number; graphic_journey?: boolean }
  | { type: "gallery"; cells: ContentBlock[][]; layout?: "reading-cards" }
  | { type: "title" | "heading" | "subheading" | "paragraph" | "step" | "code" | "response"; text: string }
  | { type: "list"; marker: "bullet" | "number"; text: string }
  | { type: "callout"; tone: "idea" | "think" | "caution" | "teacher" | "answer"; text: string }
  | { type: "table"; rows: string[][] }) & {presentation?:ReadingPresentation;responseStorageSuffix?:string};

export type LessonPage = { number: number; label: string; intro?:string; flow?:ReadingFlow; blocks: ContentBlock[] };

export type Week = {
  number: number;
  phase: number;
  hero: string | null;
  student: { title: string; pages: LessonPage[]; download: string; pdf: string };
  teacher: { title: string; pages: LessonPage[]; download: string; pdf: string };
  workbook: { title: string; pages?:LessonPage[]; blocks: ContentBlock[]; download: string; pdf: string };
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

// Called only after the page has checked the user's session. No lesson content is public JSON.
export async function loadWeekContent(week: Week): Promise<Week> {
  const { env } = await import("cloudflare:workers");
  const { resourceKey } = await import("./resource-key");
  const id = (week as Week & {contentId:string}).contentId;
  if (!/^[a-f0-9]{64}$/.test(id)) throw new Error("Invalid lesson asset reference");
  const assets = (env as unknown as {ASSETS:{fetch(request:Request):Promise<Response>}}).ASSETS;
  const response = await assets.fetch(new Request(`https://academy.internal/lesson-blobs/${id}.bin`));
  if (!response.ok) throw new Error("Lesson content unavailable");
  const bytes = new Uint8Array(await response.arrayBuffer());
  const key = await crypto.subtle.importKey("raw",Uint8Array.from(atob(resourceKey),c=>c.charCodeAt(0)),"AES-GCM",false,["decrypt"]);
  const plain = await crypto.subtle.decrypt({name:"AES-GCM",iv:bytes.slice(0,12),additionalData:new TextEncoder().encode(id)},key,bytes.slice(12));
  const content = JSON.parse(new TextDecoder().decode(plain)) as Week;
  if(content.number!==week.number) throw new Error("Lesson content mismatch");
  return content;
}
