import "server-only";

import { env } from "cloudflare:workers";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";

import type { AcademyRole } from "./academy";

const COOKIE_NAME = "academy_access";
const SESSION_SECONDS = 60 * 60 * 10;

function runtimeValue(name: string): string {
  const value = (env as unknown as Record<string, string | undefined>)[name];
  if (!value) throw new Error(`Missing required runtime setting: ${name}`);
  return value;
}

function hex(bytes: ArrayBuffer): string {
  return Array.from(new Uint8Array(bytes), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

async function signature(payload: string): Promise<string> {
  const encoder = new TextEncoder();
  const key = await crypto.subtle.importKey("raw", encoder.encode(runtimeValue("ACADEMY_SESSION_SECRET")), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", key, encoder.encode(payload)));
}

function safeEqual(left: string, right: string): boolean {
  if (left.length !== right.length) return false;
  let difference = 0;
  for (let index = 0; index < left.length; index += 1) difference |= left.charCodeAt(index) ^ right.charCodeAt(index);
  return difference === 0;
}

export async function isCorrectPasscode(role: AcademyRole, passcode: string): Promise<boolean> {
  const expected = runtimeValue(role === "teacher" ? "TEACHER_PASSCODE" : "STUDENT_PASSCODE");
  return safeEqual(passcode, expected);
}

export async function createSession(role: AcademyRole): Promise<string> {
  const expires = Math.floor(Date.now() / 1000) + SESSION_SECONDS;
  const payload = `${role}.${expires}`;
  return `${payload}.${await signature(payload)}`;
}

export async function readSession(): Promise<AcademyRole | null> {
  const value = (await cookies()).get(COOKIE_NAME)?.value;
  if (!value) return null;
  const [role, expiresText, suppliedSignature, extra] = value.split(".");
  if (extra || (role !== "student" && role !== "teacher") || !expiresText || !suppliedSignature) return null;
  const expires = Number(expiresText);
  if (!Number.isFinite(expires) || expires <= Math.floor(Date.now() / 1000)) return null;
  const expected = await signature(`${role}.${expiresText}`);
  return safeEqual(suppliedSignature, expected) ? role : null;
}

export async function requireAccess(requestedRole: AcademyRole): Promise<AcademyRole> {
  const sessionRole = await readSession();
  const allowed = sessionRole === "teacher" || (sessionRole === "student" && requestedRole === "student");
  if (!allowed) redirect(`/?access=required&role=${requestedRole}`);
  return sessionRole;
}

export const sessionCookie = { name: COOKIE_NAME, maxAge: SESSION_SECONDS };
