import Link from "next/link";
import coverage from "@/curriculum-v3/edition-coverage.json";
import { getChapter } from "@/lib/curriculum-v3";
import { ArrowLeft, ArrowRight, BookOpen, ClipboardCheck, GraduationCap, Image as ImageIcon, Lightbulb } from "lucide-react";
import { notFound } from "next/navigation";

import { ContentReader } from "@/components/content-reader";
import { TransferChallenge } from "@/components/grade6-learning";
import { VisualLessonBook, TeacherVisualBoard, WorkbookTrace, lessonIdea } from "@/components/visual-lesson-book";
import { PortalHeader } from "@/components/portal-header";
import { PrintResource } from "@/components/print-resource";
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
  const matched = coverage.find(row => row.legacy === `${levelSlug}/${week.number}`);
  if (!matched) notFound();
  const [currentLevel, currentWeek] = matched.destination.split("/");
  const current = getChapter(currentLevel, currentWeek);
  if (!current) notFound();
  const currentPath = `/learn/${role}/curriculum/${matched.destination}`;
  const allowedResources: Resource[] = role === "teacher" ? ["guide", "lesson", "workbook"] : ["lesson", "workbook"];
  const requested = query.resource as Resource | undefined;
  if (requested && !allowedResources.includes(requested)) notFound();
  const resource = requested && allowedResources.includes(requested) ? requested : allowedResources[0];
  const title = resource === "guide" ? week.teacher.title : resource === "workbook" ? week.workbook.title : week.student.title;
  return (
    <main className={`portal-page lesson-page level-${level.slug} accent-${level.accent}`}>
      <PortalHeader mode={role} sessionRole={sessionRole} edition="3" />
      <section className="lesson-hero">
        <div className="lesson-breadcrumbs"><Link href={currentPath}><ArrowLeft aria-hidden="true" /> Back to {matched.destinationTitle}</Link><span>/</span><span>Optional topic practice</span></div>
        <div className={`lesson-hero-grid ${resource === "lesson" ? "book-title-grid" : ""}`}>
          <div className="lesson-title"><div><Badge>Additional practice</Badge></div><h1>{titleWithoutWeek(title)}</h1><p>{resource === "guide" ? "Teacher-ready background, explanations, lesson flow, interventions, and assessment evidence." : resource === "workbook" ? "A focused practice mission for recording reasoning and demonstrating mastery." : "A complete illustrated lesson with explanations, worked examples, activities, responsibility checks, and mastery proof."}</p></div>
          {resource !== "lesson" && week.hero && <figure className="lesson-art"><img src={week.hero} alt={`Concept illustration for ${titleWithoutWeek(week.student.title)}`} /><figcaption><ImageIcon aria-hidden="true" /> Week {week.number} concept visual</figcaption></figure>}
        </div>
        {resource === "lesson" && <p className="lesson-core-idea"><Lightbulb aria-hidden="true"/>{lessonIdea(week)}</p>}
        <nav className="resource-nav" aria-label="Week resources">
          {role === "teacher" && <Link className={resource === "guide" ? "active" : ""} href="?resource=guide"><ClipboardCheck aria-hidden="true" /><span>Teacher guide<small>{week.teacher.pages.length} sections</small></span></Link>}
          <Link className={resource === "lesson" ? "active" : ""} href="?resource=lesson"><BookOpen aria-hidden="true" /><span>Student lesson<small>{week.student.pages.length} sections</small></span></Link>
          <Link className={resource === "workbook" ? "active" : ""} href="?resource=workbook"><GraduationCap aria-hidden="true" /><span>Workbook practice<small>Weekly mission</small></span></Link>
        </nav>
        <div className="resource-actions">
          <a className="resource-action" href={resource === "guide" ? week.teacher.download : resource === "workbook" ? week.workbook.download : week.student.download}>Download editable original {resource === "workbook" ? "36-week workbook" : resource === "guide" ? "teacher guide" : "student booklet"} (.docx)</a>
          <PrintResource />
        </div>
        <p className="legacy-download-note">This retained practice uses an earlier worked case. Its original Word download excludes the added transfer challenge and visual teaching refinements; print this page to include them. Follow the current lesson’s prerequisites and sequence.</p>
      </section>
      <section className="lesson-reader-shell">
        <aside className="readiness-check" data-review-id={`${level.slug}/${week.number}`}><h2>Before you begin</h2><p>{current.chapter.prerequisite.prompt}</p><p>Try the current lesson first, then use this case to practise the same topic with different evidence.</p></aside>
        {resource === "guide" && <><TeacherVisualBoard week={week} level={level.slug}/><ContentReader pages={week.teacher.pages} /></>}
        {resource === "lesson" && <VisualLessonBook week={week} level={level.slug} />}
        {resource === "workbook" && <><WorkbookTrace level={level.slug} week={week.number}/><ContentReader workbookBlocks={week.workbook.blocks} /></>}
        <TransferChallenge level={level.slug} week={week.number} teacher={resource === "guide" && role === "teacher"}/>
      </section>
      <nav className="week-pagination" aria-label="Return to current learning path"><Link href={`${currentPath}?resource=${resource}`}>← Back to {matched.destinationTitle}</Link><Link href={`/learn/${role}`}>All seven levels</Link></nav>
    </main>
  );
}
