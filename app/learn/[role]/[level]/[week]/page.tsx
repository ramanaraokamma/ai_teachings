import Link from "next/link";
import { ArrowLeft, ArrowRight, BookOpen, ClipboardCheck, GraduationCap, Image as ImageIcon } from "lucide-react";
import { notFound } from "next/navigation";

import { ContentReader } from "@/components/content-reader";
import { PortalHeader } from "@/components/portal-header";
import { Badge } from "@/components/ui/badge";
import { requireAccess } from "@/lib/access";
import { getLevel, getWeek, titleWithoutWeek, type AcademyRole } from "@/lib/academy";

export const dynamic = "force-dynamic";

type Resource = "lesson" | "guide" | "workbook";

export default async function WeekPage({ params, searchParams }: { params: Promise<{ role: string; level: string; week: string }>; searchParams: Promise<{ resource?: string }> }) {
  const [{ role: rawRole, level: levelSlug, week: weekParam }, query] = await Promise.all([params, searchParams]);
  if (rawRole !== "student" && rawRole !== "teacher") notFound();
  const role = rawRole as AcademyRole;
  const level = getLevel(levelSlug);
  const week = level ? getWeek(level, weekParam) : undefined;
  if (!level || !week) notFound();
  const sessionRole = await requireAccess(role);
  const allowedResources: Resource[] = role === "teacher" ? ["guide", "lesson", "workbook"] : ["lesson", "workbook"];
  const requested = query.resource as Resource | undefined;
  const resource = requested && allowedResources.includes(requested) ? requested : allowedResources[0];
  const title = resource === "guide" ? week.teacher.title : resource === "workbook" ? week.workbook.title : week.student.title;
  const previous = week.number > 1 ? week.number - 1 : null;
  const next = week.number < 36 ? week.number + 1 : null;
  return (
    <main className={`portal-page lesson-page accent-${level.accent}`}>
      <PortalHeader mode={role} sessionRole={sessionRole} />
      <section className="lesson-hero">
        <div className="lesson-breadcrumbs"><Link href={`/learn/${role}/${level.slug}`}><ArrowLeft aria-hidden="true" /> {level.code} {level.name}</Link><span>/</span><span>Week {week.number}</span></div>
        <div className="lesson-hero-grid">
          <div className="lesson-title"><div><Badge>{level.code}</Badge><Badge variant="outline">Week {String(week.number).padStart(2, "0")} of 36</Badge></div><h1>{titleWithoutWeek(title)}</h1><p>{resource === "guide" ? "Teacher-ready background, explanations, lesson flow, interventions, and assessment evidence." : resource === "workbook" ? "A focused practice mission for recording reasoning and demonstrating mastery." : "A complete illustrated lesson with explanations, worked examples, activities, responsibility checks, and mastery proof."}</p></div>
          {week.hero && <figure className="lesson-art"><img src={week.hero} alt={`Concept illustration for ${titleWithoutWeek(week.student.title)}`} /><figcaption><ImageIcon aria-hidden="true" /> Week {week.number} concept visual</figcaption></figure>}
        </div>
        <nav className="resource-nav" aria-label="Week resources">
          {role === "teacher" && <Link className={resource === "guide" ? "active" : ""} href="?resource=guide"><ClipboardCheck aria-hidden="true" /><span>Teacher guide<small>{week.teacher.pages.length} sections</small></span></Link>}
          <Link className={resource === "lesson" ? "active" : ""} href="?resource=lesson"><BookOpen aria-hidden="true" /><span>Student lesson<small>{week.student.pages.length} sections</small></span></Link>
          <Link className={resource === "workbook" ? "active" : ""} href="?resource=workbook"><GraduationCap aria-hidden="true" /><span>Workbook practice<small>Weekly mission</small></span></Link>
        </nav>
      </section>
      <section className="lesson-reader-shell">
        {resource === "guide" && <ContentReader pages={week.teacher.pages} />}
        {resource === "lesson" && <ContentReader pages={week.student.pages} />}
        {resource === "workbook" && <ContentReader workbookBlocks={week.workbook.blocks} />}
      </section>
      <nav className="week-pagination" aria-label="Adjacent weeks">
        {previous ? <Link href={`/learn/${role}/${level.slug}/${previous}?resource=${resource}`}><ArrowLeft aria-hidden="true" /><span><small>Previous</small>Week {previous}</span></Link> : <span />}
        <Link className="all-weeks" href={`/learn/${role}/${level.slug}`}>All 36 weeks</Link>
        {next ? <Link href={`/learn/${role}/${level.slug}/${next}?resource=${resource}`}><span><small>Next</small>Week {next}</span><ArrowRight aria-hidden="true" /></Link> : <span />}
      </nav>
    </main>
  );
}
