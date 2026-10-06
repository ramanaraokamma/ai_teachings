import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAccess } from "@/lib/access";
import { PortalHeader } from "@/components/portal-header";
import { curriculumRoadmap, curriculumReleases } from "@/lib/curriculum-v3";
export const dynamic="force-dynamic";
export default async function CurriculumMap({params}:{params:Promise<{role:string;level?:string}>}) {
 const {role,level:levelSlug}=await params;if(role!=="student"&&role!=="teacher")notFound();
 const sessionRole=await requireAccess(role);
 const selectedLevels=levelSlug?curriculumRoadmap.levels.filter(level=>level.slug===levelSlug):curriculumRoadmap.levels;
 if(!selectedLevels.length)notFound();
 const count=Object.keys(curriculumReleases).length;
 return <main className="portal-page v3-map"><PortalHeader mode={role} sessionRole={sessionRole} edition="3"/>
  <header className="v3-intro"><p className="v3-kicker">AI Academy · Grades 6–12</p><h1>Understand it. Test it. Explain it.</h1><p>A seven-level progression from evidence and representations to independent AI research. Each released week pairs an explanatory chapter, a practice workbook and a protected teacher guide, with matching Word and PDF editions.</p><p><strong>{count} of 252 weeks ready to learn.</strong> {count===252?"All seven levels include student lessons, workbook practice, teacher guides and printable downloads.":"The remaining weeks are a proposed sequence and are not yet available as rebuilt lessons."}</p><p>{curriculumRoadmap.placement}</p>{levelSlug&&<Link href={`/learn/${role}`}>← All seven levels</Link>}</header>
  {!levelSlug&&<nav className="v3-level-picker" aria-label="Choose your level">{curriculumRoadmap.levels.map(level=><Link key={level.slug} href={`/learn/${role}/${level.slug}`}><span>Grade {level.grade} · {level.slug.toUpperCase()}</span><strong>{level.name}</strong><small>36 weeks · Lessons, practice and {role==="teacher"?"teaching guides":"worked examples"}</small></Link>)}</nav>}
  <section className="v3-levels" aria-label="Seven-level curriculum progression">{selectedLevels.map((level,index)=><article className="v3-level" key={level.slug}><header><p className="v3-kicker">Level {Number(level.slug.slice(3))} · Typical Grade {level.grade}</p><h2>{level.name}</h2><p><strong>Before starting</strong> {level.prerequisites}</p><p><strong>Evidence at the end</strong> {level.exitEvidence}</p></header><ol>{level.weeks.map((title,i)=>{const ready=Boolean(curriculumReleases[`${level.slug}/${i+1}`]);return <li key={title}><span className="v3-week-number">{String(i+1).padStart(2,"0")}</span>{ready?<Link href={`/learn/${role}/curriculum/${level.slug}/${i+1}`}>{title}<span className="v3-status">Released</span></Link>:<span>{title}<span className="v3-status v3-planned">Planned</span></span>}</li>})}</ol></article>)}</section>
 </main>;
}
