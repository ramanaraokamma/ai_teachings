import Link from "next/link";
import { notFound } from "next/navigation";
import { requireAccess } from "@/lib/access";
import { PortalHeader } from "@/components/portal-header";
import { PrintResource } from "@/components/print-resource";
import { getChapter, curriculumReleases, curriculumRoadmap } from "@/lib/curriculum-v3";
export const dynamic="force-dynamic";
function ResponseSpace({label,lines,id}:{label:string;lines:number;id:string}) {return <div className="v3-response"><p id={id}>{label}</p><div className="v3-writing-space" aria-labelledby={id} style={{minHeight:`${lines*1.6}rem`}}><span className="v3-screen-note">Write in your notebook or download the workbook.</span>{Array.from({length:lines},(_,i)=><div className="v3-writing-line" aria-hidden="true" key={i}/>)}</div></div>;}
function Table({headers,rows}:{headers:string[];rows:string[][]}) {return <div className="v3-table-scroll"><table><thead><tr>{headers.map(h=><th scope="col" key={h}>{h}</th>)}</tr></thead><tbody>{rows.map((row,i)=><tr key={i}>{row.map((v,j)=><td key={j}>{v}</td>)}</tr>)}</tbody></table></div>;}
export default async function ChapterPage({params,searchParams}:{params:Promise<{role:string;level:string;week:string}>;searchParams:Promise<{resource?:string}>}) {
 const [{role,level,week},query]=await Promise.all([params,searchParams]);
 if(role!=="student"&&role!=="teacher")notFound();
 const sessionRole=await requireAccess(role);
 const found=getChapter(level,week);if(!found)notFound();
 const {chapter:c,release}=found;
 const resource=query.resource??(role==="teacher"?"guide":"lesson");
 if(!["lesson","workbook","guide"].includes(resource)||(resource==="guide"&&role!=="teacher"))notFound();
 const label=resource==="guide"?"Teacher guide":resource==="workbook"?"Workbook":"Student lesson";
 const levelInfo=curriculumRoadmap.levels.find(item=>item.slug===level)!;
 const t=c.teacher;let diagramIndex=0;
 const base=`/learn/${role}/curriculum/${level}/${week}`;
 return <main className="portal-page v3-page"><PortalHeader mode={role} sessionRole={sessionRole} edition="3"/>
 <header className="v3-chapter-header"><Link className="v3-back" href={`/learn/${role}/curriculum`}>← Seven-level learning map</Link><p className="v3-kicker">Curriculum 3 · {level.toUpperCase().replace("-"," ")} {levelInfo.name} · Grade {levelInfo.grade} · Week {week} · {label}</p><h1>{c.title}</h1><p className="v3-duration">Two 45-minute sessions · Paper activities included</p>
 <nav className="v3-resource-nav" aria-label="Chapter resources">{["lesson","workbook",...(role==="teacher"?["guide"]:[])].map(r=><Link key={r} aria-current={resource===r?"page":undefined} href={`${base}?resource=${r}`}>{r==="lesson"?"Student lesson":r==="guide"?"Teacher guide":"Workbook"}</Link>)}</nav>
 <div className="resource-actions"><a className="resource-action" href={`/api/resource/${release.documents[`${resource}.docx`].id}`}>Download matching Word edition</a><a className="resource-action" href={`/api/resource/${release.documents[`${resource}.pdf`].id}`}>Download print-ready PDF</a><PrintResource/></div></header>
 <article className="v3-chapter lesson-reader-shell" data-curriculum="3" data-resource={resource} data-source-hash={release.sourceHash}>
 {resource==="lesson"&&<><section className="v3-chapter-section"><h2>What you will learn</h2><ul>{c.goals.map(g=><li key={g}>{g}</li>)}</ul><h3>Recall before reading</h3><p>{c.prerequisite.prompt}</p></section>{c.lesson.map((s,i)=><section className="v3-chapter-section" key={s.title}><p className="v3-kicker">Read and reason · {i+1} of {c.lesson.length}</p><h2>{s.title}</h2>{s.blocks.map((b,j)=>{
 if(b.type==="paragraph")return <p key={j}>{b.text}</p>;
 if(b.type==="code")return <pre className="v3-code" key={j} aria-label={b.title??"Python code"}><code>{b.text}</code></pre>;
 if(b.type==="table")return <Table key={j} headers={b.headers!} rows={b.rows!}/>;
 if(b.type==="response")return <ResponseSpace key={j} id={b.id!} label={b.label!} lines={b.lines!}/>;
 if(b.type==="diagram"){const image=release.diagrams[diagramIndex++];return <figure key={j}><h3>{b.title}</h3><img src={`/api/resource/${image.id}`} alt={b.title} loading="eager"/><figcaption>{b.caption}</figcaption><details className="v3-diagram-description"><summary>Read the diagram as text</summary>{b.rows?<Table headers={b.columns!} rows={b.rows}/>:b.values?<><p>{b.key}</p><ol>{b.values.map((row,r)=><li key={r}>Row {r+1}: {row.join(", ")}</li>)}</ol></>:<p>{b.caption}</p>}</details></figure>;}
 return null;
 })}</section>)}<section className="v3-chapter-section"><h2>Words to use accurately</h2><Table headers={["Word","Meaning"]} rows={c.vocabulary}/></section></>}
 {resource==="workbook"&&<><p>Write your name and date. Complete the supported tasks first. Attempt the new case independently and record any help you use. Your teacher has the answer explanations.</p>{c.workbook.map(task=><section className="v3-chapter-section" key={task.id}><h2>{task.id} {task.title}</h2><p>{task.prompt}</p><ResponseSpace id={task.id} label="My reasoning and evidence" lines={task.lines}/></section>)}<p>Support used: None / Hint / Teacher explanation</p></>}
 {resource==="guide"&&<><section className="v3-chapter-section"><h2>Teacher background</h2><p>{t.background}</p><h3>Learning outcomes</h3><ul>{c.goals.map(g=><li key={g}>{g}</li>)}</ul><h3>Preparation</h3><ul>{t.materials.map(m=><li key={m}>{m}</li>)}</ul><h3>Prerequisite check and answer</h3><p>{c.prerequisite.prompt}</p><p>{c.prerequisite.answer}</p></section><section className="v3-chapter-section"><h2>Teaching sequence</h2>{t.sessions.map(([title,body])=><div key={title}><h3>{title}</h3><p>{body}</p></div>)}</section><section className="v3-chapter-section" data-teacher-answers="true"><h2>Solutions to student chapter questions</h2><p>{t.guidedAnswer}</p><h2>Workbook answer explanations</h2>{c.workbook.map(task=><div key={task.id}><h3>{task.id} {task.title}</h3><p>{task.answer}</p></div>)}</section><section className="v3-chapter-section"><h2>Respond to misconceptions</h2>{t.misconceptions.map(([title,body])=><div key={title}><h3>{title}</h3><p>{body}</p></div>)}<h2>Assess independent understanding</h2><p>{t.assessment}</p><h2>Support and extension</h2><p>{t.support}</p><h2>Connect to the next week</h2><p>{t.next}</p></section></>}
 </article><nav className="v3-pagination" aria-label="Adjacent released chapters">{curriculumReleases[`${level}/${c.week-1}`]&&<Link href={`/learn/${role}/curriculum/${level}/${c.week-1}?resource=${resource}`}>← Week {c.week-1}</Link>}<Link href={`/learn/${role}/curriculum`}>All planned and released weeks</Link>{curriculumReleases[`${level}/${c.week+1}`]&&<Link href={`/learn/${role}/curriculum/${level}/${c.week+1}?resource=${resource}`}>Week {c.week+1} →</Link>}</nav></main>;
}
