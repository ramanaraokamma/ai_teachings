import Link from "next/link";
import { ArrowLeft, ArrowRight, Award, BookOpen, ClipboardList } from "lucide-react";
import { notFound } from "next/navigation";

import { PortalHeader } from "@/components/portal-header";
import { Badge } from "@/components/ui/badge";
import { requireAccess } from "@/lib/access";
import { getLevel, titleWithoutWeek, type AcademyRole } from "@/lib/academy";

import { classroom } from "@/lib/classroom";
import { PythonReadiness } from "@/components/python-readiness";

export const dynamic = "force-dynamic";

export default async function LevelPage({ params }: { params: Promise<{ role: string; level: string }> }) {
  const { role: rawRole, level: levelSlug } = await params;
  if (rawRole !== "student" && rawRole !== "teacher") notFound();
  const role = rawRole as AcademyRole;
  const level = getLevel(levelSlug);
  if (!level) notFound();
  const sessionRole = await requireAccess(role);
  return (
    <main className={`portal-page accent-${level.accent}`}>
      <PortalHeader mode={role} sessionRole={sessionRole} />
      <section className="level-hero" id="main-content" tabIndex={-1}>
        <Link href={`/learn/${role}`} className="back-link"><ArrowLeft aria-hidden="true" /> All levels</Link>
        <div className="level-hero-main"><div><Badge>{level.ages}</Badge><p>{level.code}</p><h1>{level.name}</h1><span>{level.summary}</span></div><div className="capstone-card"><Award aria-hidden="true" /><small>Final capstone</small><strong>{level.capstone}</strong><span>Built across the final phase</span></div></div>
        <div className="phase-track" aria-label="Curriculum phases">{level.phases.map((phase) => <a href={`#phase-${phase.number}`} key={phase.number}><i>{phase.number}</i><span><strong>{phase.name}</strong><small>Weeks {phase.weeks}</small></span></a>)}</div>
      </section>
      <section className="classroom-panel"><h2>Before you start</h2><p>{classroom.levels[level.slug].prerequisites}</p><h3>What you will be able to do</h3><p>{classroom.levels[level.slug].outcome}</p><p><strong>Your project:</strong> {classroom.levels[level.slug].project}. Keep each week’s inputs, predictions, test results and revisions in one portfolio.</p></section>
      {(level.slug === "python-bridge" || level.slug === "ai-4") && <PythonReadiness />}
      <div className="weeks-shell">
        {level.phases.map((phase) => (
          <section className="phase-section" id={`phase-${phase.number}`} key={phase.number}>
            <div className="phase-heading"><span>Phase {phase.number}</span><div><h2>{phase.name}</h2><p>Weeks {phase.weeks}</p></div></div>
            <div className="week-grid">
              {level.weeks.filter((week) => week.phase === phase.number).map((week) => (
                <Link href={`/learn/${role}/${level.slug}/${week.number}`} className="week-card" key={week.number}>
                  {week.hero && <img className="week-card-image" src={week.hero} alt={`Illustration for ${titleWithoutWeek(week.student.title)}`} width={420} height={170} loading="lazy" decoding="async" />}
                  <div className="week-card-meta"><span>Week {String(week.number).padStart(2, "0")}</span><Badge variant="outline">Phase {week.phase}</Badge></div>
                  <h3>{titleWithoutWeek(week.student.title)}</h3>
                  {role === "teacher" && <p className="teacher-week-title">Guide: {titleWithoutWeek(week.teacher.title)}</p>}
                  <div className="resource-counts"><span><BookOpen aria-hidden="true" /> Lesson</span><span><ClipboardList aria-hidden="true" /> Workbook</span>{role === "teacher" && <span>Teacher guide</span>}</div>
                  <div className="open-week"><span>Open week</span><ArrowRight aria-hidden="true" /></div>
                </Link>
              ))}
            </div>
          </section>
        ))}
      </div>
    </main>
  );
}
