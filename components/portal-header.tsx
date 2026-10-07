import Link from "next/link";
import { BookOpen, GraduationCap, LogOut, Sparkles } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import type { AcademyRole } from "@/lib/academy";

export function PortalHeader({ mode, sessionRole, edition = "2.0" }: { mode: AcademyRole; sessionRole: AcademyRole; edition?: "2.0" | "3" }) {
  const suffix = edition === "3" ? "/curriculum" : "";
  return (
    <header className="portal-header">
      <Link href={`/learn/${mode}${suffix}`} className="brand" aria-label="AI Academy dashboard">
        <span className="brand-mark"><Sparkles aria-hidden="true" /></span>
        <span><strong>AI Academy</strong><small>Complete learning programme</small></span>
      </Link>
      <nav className="mode-nav" aria-label="Portal mode">
        <Badge className={`role-badge role-${mode}`}>
          {mode === "student" ? <GraduationCap aria-hidden="true" /> : <BookOpen aria-hidden="true" />}
          {mode === "student" ? "Student mode" : "Teacher mode"}
        </Badge>
        {sessionRole === "teacher" && (
          <Link className="mode-link" href={`/learn/${mode === "teacher" ? "student" : "teacher"}${suffix}`}>
            Open {mode === "teacher" ? "student" : "teacher"} view
          </Link>
        )}
        <form action="/api/logout" method="post">
          <Button variant="ghost" size="sm" type="submit" className="logout-button"><LogOut aria-hidden="true" /> Sign out</Button>
        </form>
      </nav>
    </header>
  );
}
