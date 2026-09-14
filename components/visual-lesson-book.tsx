import { ArrowRight, BookOpen, Camera, CheckCircle2, Cpu, FlaskConical, Lightbulb, Mic, MoveDown, PencilLine, ScanLine, Thermometer, Waypoints } from "lucide-react";
import type { ContentBlock, LessonPage, Week } from "@/lib/academy";
import { ContentBlockView } from "@/components/content-reader";
import { LessonVisual } from "@/components/lesson-visual";
import { ResponseSpace } from "@/components/response-space";
import { SensorLab } from "@/components/sensor-lab";
import { TopicDiagram, MisconceptionRepair, WorkedCaseStudio, TopicTeacherPrompt, TopicWorkbookPrompt } from "@/components/topic-studio";

type Picture = Extract<ContentBlock, { type: "image" }>;
const isPicture = (block: ContentBlock): block is Picture => block.type === "image";
const labels = ["", "Your mission", "Notice the evidence", "See how it works", "Compare the cases", "Words that unlock the idea", "Follow a worked example", "Find and repair a mistake", "Practise together", "Run the investigation", "Build your understanding", "Connect your project", "Show what you know", "Study a complete case", "Try a new case independently", "Code and experiment"];
const prompts = ["", "What will you be able to explain?", "Point to the clues before making a claim.", "Follow what changes at each stage.", "What stays the same? What changes?", "Use the word to explain a fresh example.", "Connect every step to its evidence.", "Find the cause, then choose one repair.", "Explain your thinking to a partner.", "Predict first. Record what actually happens.", "Use a fresh example as you climb.", "Keep evidence for your design decision.", "Make your reasoning visible.", "Read the situation, predict, then compare.", "Complete this after the worked example.", "Keep your code and evidence together."];
const icons = [BookOpen, BookOpen, ScanLine, Waypoints, CheckCircle2, Lightbulb, Waypoints, PencilLine, PencilLine, FlaskConical, MoveDown, Cpu, CheckCircle2, BookOpen, PencilLine, Cpu];

export function lessonIdea(week: Week): string {
  const blocks = week.student.pages[0].blocks;
  const title = blocks.findIndex(b => "text" in b && /^Week\s+\d+/i.test(b.text));
  const idea = blocks.slice(title + 1).find(b => b.type === "paragraph" && b.text.trim());
  return idea && "text" in idea ? idea.text : week.student.title;
}

export function NativeMechanism({ week, level }: { week: Week; level: string }) {
  return <TopicDiagram week={week.number} level={level}/>;
}

function LegacyMechanism({ week, level }: { week: Week; level: string }) {
  const mechanism = week.student.pages.find(p => p.number === 3)?.blocks ?? [];
  const explicit = mechanism.flatMap(b => {
    if (!("text" in b)) return [];
    const m = b.text.match(/^(INPUT|PROCESS|OUTPUT|QUESTION|MODEL IDEA|PROOF NEEDED)\s{2,}([\s\S]+)/);
    return m ? [{ label: m[1], text: m[2] }] : [];
  });
  const reasoning = (week.student.pages.find(p => p.number === 6)?.blocks ?? []).flatMap(b => {
    if (!("text" in b)) return [];
    const m = b.text.match(/^(?:STEP\s+\d+\s*(?:—\s*\w+)?\s+|\d+\.\s+)([\s\S]+)/);
    return m ? [{ label: `STEP`, text: m[1] }] : [];
  });
  const nodes = explicit.length >= 3 ? explicit : reasoning;
  return <figure className="native-mechanism" data-native-diagram="mechanism"><figcaption><Waypoints aria-hidden="true"/><span>{explicit.length >= 3 ? "Follow the idea" : "Follow the worked reasoning"}</span></figcaption><ol className={`mechanism-nodes nodes-${nodes.length}`}>{nodes.map((node,i) => <li key={i}><span className="mechanism-index">{i+1}</span><h3>{node.label === "STEP" ? `Reasoning step ${i+1}` : node.label.toLowerCase()}</h3><p>{node.text}</p>{i < nodes.length-1 && <ArrowRight className="mechanism-arrow" aria-hidden="true"/>}</li>)}</ol><p className="mechanism-question">{level === "ai-1" ? "Can you point to each step and explain it in your own words?" : "Which assumption, input, or step could change the conclusion?"}</p></figure>;
}

function SensorConnections() {
  const examples = [{Icon:Camera,name:"Camera",signal:"Light",data:"Pixel values",limit:"A later process may label a cat."},{Icon:Mic,name:"Microphone",signal:"Sound vibrations",data:"Sound samples",limit:"A later process may recognize words."},{Icon:Thermometer,name:"Temperature sensor",signal:"Temperature",data:"A reading such as 22 °C",limit:"A person or rule decides what to do."}];
  return <div className="sensor-connections" data-native-diagram="sensor-matching">{examples.map(({Icon,...item})=><div key={item.name}><Icon aria-hidden="true"/><h3>{item.name}</h3><p>{item.signal}</p><MoveDown aria-hidden="true"/><strong>{item.data}</strong><p>{item.limit}</p></div>)}</div>;
}

function VisualPage({ page, week, level }: { page: LessonPage; week: Week; level: string }) {
  if(page.number===13) return <WorkedCaseStudio level={level} week={week.number}/>;
  const pictures = page.blocks.filter(isPicture);
  const table = page.blocks.find(b => b.type === "table");
  const cards = page.number === 5 && pictures.length === 4;
  const flow = page.number === 3 && pictures.length === 3;
  const steps = (page.number === 6 || page.number === 9 || page.number === 10) ? page.blocks.filter(b => "text" in b && /^(?:STEP\s+\d+|\d+[. •]|RECALL\s|EXPLAIN\s|TRACE\s|DIAGNOSE\s|TRANSFER\s|CREATE\s|DEFEND\s|DEFINE\s|CALCULATE\s|IMPROVE\s)/.test(b.text)) : [];
  const caseText = page.number === 4 ? page.blocks.filter(b => "text" in b && /^(?:CASE [1-4]\s|NORMAL\s{2}|BOUNDARY\s{2}|MISSING\s{2}|SHIFTED\s{2})/.test(b.text)) : [];
  const skip = new Set<ContentBlock>();
  // Keep story and vocabulary art. Replace generic raster stage/case cards
  // with topic diagrams while retaining all original explanatory text.
  if(page.number!==1 && page.number!==5) pictures.forEach(b=>skip.add(b));
  if (cards || flow) pictures.forEach(b => skip.add(b));
  if (page.number === 5 && cards && table) skip.add(table);
  if (page.number===4) caseText.forEach(b => skip.add(b));
  const firstHeading = page.blocks.findIndex(b => b.type === "title" || b.type === "heading");
  // Replace repeated document mastheads with a consistent book chapter heading.
  const introCount = page.number <= 12 ? (firstHeading >= 0 ? firstHeading + 1 : 2) : 1;
  const content = page.blocks.filter((b,i) => i >= introCount && !skip.has(b) && !("text" in b && b.text.trim() === "↓"));
  const lead = content[0]?.type === "paragraph" ? content.shift() : undefined;
  return <>
    {lead && <ContentBlockView block={lead}/>}
    {page.number === 3 && <NativeMechanism week={week} level={level}/>}
    {page.number===4 && <div className="topic-case-comparison" data-topic-panel="case-comparison">{(caseText.length===4?caseText:week.student.pages.find(p=>p.number===14)?.blocks.filter((b,i)=>i===2)??[]).map((b,i)=><section key={i}><span className="topic-kicker">{caseText.length===4?`CASE ${i+1}`:'TRANSFER TO A NEW CASE'}</span><p>{'text' in b?b.text:''}</p><ResponseSpace/></section>)}</div>}
    {page.number===7 && <MisconceptionRepair level={level} week={week.number}/>}
    {page.number === 3 && level === "ai-1" && week.number === 3 && <><SensorConnections/><SensorLab/></>}
    {cards && <div className={`book-visual-cards ${page.number===5 ? 'vocabulary-cards' : 'comparison-cards'}`}>{pictures.map((picture,i) => {
      const row = page.number===5 && table?.type==='table' ? table.rows[i+1] : undefined;
      const headers = table?.type==='table' ? table.rows[0] : [];
      const paired = caseText.length===4 ? caseText[i] : undefined;
      return <section className="book-visual-card" key={picture.src}><div className="book-card-number">{page.number===5 ? 'WORD' : 'CASE'} {i+1}</div>{page.number===5 && <LessonVisual {...picture}/>} {paired && 'text' in paired && <p className="case-evidence">{paired.text}</p>}{row && <><h3>{row[0]}</h3>{row.slice(1).map((cell,j)=><div className="vocabulary-use" key={j}><strong>{headers[j+1]}</strong>{cell ? <p>{cell}</p> : <ResponseSpace/>}</div>)}</>}</section>;
    })}</div>}
    {content.map((b,i)=> steps.includes(b) ? (b===steps[0] ? <ol key={i} className={`reasoning-path ${page.number===10 ? 'mastery-path' : ''}`}>{steps.map((step,j)=><li key={j}><span>{j+1}</span><p>{"text" in step ? step.text.replace(/^(?:STEP\s+\d+\s*|\d+[. •]\s*)/, "") : ""}</p></li>)}</ol> : null) : <ContentBlockView key={i} block={b}/>)}
  </>;
}

export function TeacherVisualBoard({ week, level }: { week: Week; level: string }) {
  return <section className="teacher-visual-board"><div className="book-overline">BOARD PLAN • MODEL • DISCUSS</div><h2>Teach the idea visually</h2><p className="board-big-idea">{lessonIdea(week)}</p><NativeMechanism week={week} level={level}/><TopicTeacherPrompt level={level} week={week.number}/></section>;
}

export function WorkbookTrace({ level, week }: { level: string; week:number }) {
  const labels = level==='ai-4' ? ['Data and question', 'Model or calculation', 'Evidence and limitation'] : ['Input or starting information', 'Steps or process', 'Output and evidence'];
  return <TopicWorkbookPrompt level={level} week={week}/>;
}

export function VisualLessonBook({ week, level }: { week: Week; level: string }) {
  // Read the concrete worked case before guided practice and independent assessment.
  const order=[1,2,3,4,5,13,6,7,8,9,10,11,12,14,15];
  const sections = [...week.student.pages].sort((a,b)=>order.indexOf(a.number)-order.indexOf(b.number));
  return <div className="visual-lesson-book" data-edition="grade6-entry-2026-09-14">
    <nav className="book-contents" aria-label="Lesson book chapters"><strong><BookOpen aria-hidden="true"/> In this lesson</strong><div>{sections.map((p,index)=><a href={`#section-${p.number}`} key={p.number}><span>{String(index+1).padStart(2,'0')}</span>{labels[p.number]}</a>)}</div></nav>
    <div className="book-pages">{sections.map((page,index)=>{ const Icon=icons[page.number]??BookOpen;return <article className={`book-chapter chapter-${page.number}`} id={`section-${page.number}`} key={page.number}>
      <header className="book-chapter-heading"><span className="chapter-number">{String(index+1).padStart(2,'0')}</span><div><p className="book-overline"><Icon aria-hidden="true"/> {page.number <= 5 ? "DISCOVER" : page.number <= 7 || page.number===13 ? "UNDERSTAND" : page.number <= 11 ? "PRACTISE" : "APPLY"}</p><h2>{labels[page.number]??page.label}</h2><p>{prompts[page.number]}</p></div></header>
      <div className="book-chapter-content"><VisualPage page={page} week={week} level={level}/></div>
    </article>})}</div>
  </div>;
}
