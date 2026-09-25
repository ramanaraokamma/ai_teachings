import Link from "next/link";
import { ArrowRight, Award, BookOpenCheck, Layers3, Route } from "lucide-react";
import { notFound } from "next/navigation";

import { PortalHeader } from "@/components/portal-header";
import { Badge } from "@/components/ui/badge";
import { requireAccess } from "@/lib/access";
import { levels, type AcademyRole } from "@/lib/academy";

export const dynamic = "force-dynamic";

export default async function RoleDashboard({ params }: { params: Promise<{ role: string }> }) {
  const { role: rawRole } = await params;
  if (rawRole !== "student" && rawRole !== "teacher") notFound();
  const role = rawRole as AcademyRole;
  const sessionRole = await requireAccess(role);
  return (
    <main className="portal-page">
      <PortalHeader mode={role} sessionRole={sessionRole} />
      <section className="v3-release-callout"><h2>The new seven-level curriculum</h2><p>Start with the rebuilt Grade 6 foundation unit, with matching student lessons, workbooks, teacher guides and printable downloads. Later weeks remain clearly marked as planned.</p><Link href={`/learn/${role}/curriculum`}>Open Curriculum 3 and its release map →</Link></section>
      <section className="dashboard-hero">
        <div><Badge variant="outline">{role === "student" ? "Your learning map" : "Your teaching studio"}</Badge><h1>{role === "student" ? "Choose a level. Start the next idea." : "Plan the lesson. Teach the idea. Check mastery."}</h1><p>{role === "student" ? "Every level is a 36-week path with explanations, visual models, practice, challenges, and a capstone." : "Open any level to see its 36-week sequence, teacher guide, student lesson, and workbook practice together."}</p></div>
        <div className="dashboard-stat"><strong>4</strong><span>existing levels</span><i /><strong>144</strong><span>weeks of learning</span></div>
      </section>
      <section className="level-grid" aria-label="AI Academy levels">
        {levels.map((level, index) => (
          <Link href={`/learn/${role}/${level.slug}`} className={`level-card accent-${level.accent}`} key={level.slug}>
            <div className="level-card-top"><span className="level-number">0{index + 1}</span><Badge>{level.ages}</Badge></div>
            <div><p className="level-code">{level.code}</p><h2>{level.name}</h2><p>{level.summary}</p></div>
            <div className="focus-list">{level.focus.map((focus) => <span key={focus}>{focus}</span>)}</div>
            <div className="capstone-line"><Award aria-hidden="true" /><span><small>Capstone</small>{level.capstone}</span></div>
            <div className="level-enter"><span>Open {role === "student" ? "level" : "teaching plan"}</span><ArrowRight aria-hidden="true" /></div>
          </Link>
        ))}
      </section>
      <section className="journey-note">
        <div><Route aria-hidden="true" /><span><strong>One coherent pathway</strong><small>Concepts build from level to level without skipping the foundations.</small></span></div>
        <div><Layers3 aria-hidden="true" /><span><strong>36 weeks per level</strong><small>Six focused phases lead toward a substantial final project.</small></span></div>
        <div><BookOpenCheck aria-hidden="true" /><span><strong>Evidence every week</strong><small>Learning is demonstrated through explanation, practice, and testing.</small></span></div>
      </section>
    </main>
  );
}
