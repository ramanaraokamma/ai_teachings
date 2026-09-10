import { NextResponse } from "next/server";

import { createSession, isCorrectPasscode, sessionCookie } from "@/lib/access";
import type { AcademyRole } from "@/lib/academy";

export async function POST(request: Request) {
  const origin = request.headers.get("origin");
  if (origin && origin !== new URL(request.url).origin) return new Response("Invalid origin.", { status: 403 });
  const form = await request.formData();
  const requestedRole = String(form.get("role") ?? "");
  const role: AcademyRole | null = requestedRole === "student" || requestedRole === "teacher" ? requestedRole : null;
  const passcode = String(form.get("passcode") ?? "");
  if (!role || !(await isCorrectPasscode(role, passcode))) {
    const target = new URL("/", request.url);
    target.searchParams.set("access", "incorrect");
    if (role) target.searchParams.set("role", role);
    return NextResponse.redirect(target, 303);
  }
  const response = NextResponse.redirect(new URL(`/learn/${role}`, request.url), 303);
  response.cookies.set(sessionCookie.name, await createSession(role), { httpOnly: true, secure: true, sameSite: "lax", path: "/", maxAge: sessionCookie.maxAge });
  response.headers.set("Cache-Control", "no-store");
  return response;
}
