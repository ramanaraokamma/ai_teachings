import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAccess } from "@/lib/access";
import { PortalHeader } from "@/components/portal-header";
import { curriculumRoadmap, curriculumReleases } from "@/lib/curriculum-v3";
export const dynamic="force-dynamic";
export default async function CurriculumMap({params}:{params:Promise<{role:string}>}) {
 const {role}=await params;if(role!=="student"&&role!=="teacher")notFound();
 const sessionRole=await requireAccess(role);
 const count=Object.keys(curriculumReleases).length;
 return <main className="portal-page v3-map"><PortalHeader mode={role} sessionRole={sessionRole} edition="3"/>
  <header className="v3-intro"><p className="v3-kicker">Curriculum 3 · Starting in Grade 6</p><h1>Understand it. Test it. Explain it.</h1><p>A seven-level progression from evidence and representations to independent AI research. Each released week pairs an explanatory chapter, a practice workbook and a protected teacher guide, with matching Word and PDF editions.</p><p><strong>{count} of 252 weekly packages released.</strong> {count===252?"All seven levels have complete lesson, workbook and teacher-guide packages.":"The remaining weeks are a proposed sequence and are not yet available as rebuilt lessons."}</p><p>{curriculumRoadmap.placement}</p><Link href={`/learn/${role}`}>Open the existing four-level edition</Link></header>
  <section className="v3-levels" aria-label="Seven-level curriculum progression">{curriculumRoadmap.levels.map((level,index)=><article className="v3-level" key={level.slug}><header><p className="v3-kicker">Level {index+1} · Typical Grade {level.grade}</p><h2>{level.name}</h2><p><strong>Before starting</strong> {level.prerequisites}</p><p><strong>Evidence at the end</strong> {level.exitEvidence}</p></header><ol>{level.weeks.map((title,i)=>{const ready=Boolean(curriculumReleases[`${level.slug}/${i+1}`]);return <li key={title}><span className="v3-week-number">{String(i+1).padStart(2,"0")}</span>{ready?<Link href={`/learn/${role}/curriculum/${level.slug}/${i+1}`}>{title}<span className="v3-status">Released</span></Link>:<span>{title}<span className="v3-status v3-planned">Planned</span></span>}</li>})}</ol></article>)}</section>
 </main>;
}
