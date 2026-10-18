import { AlertTriangle, BookMarked, CheckCircle2, Lightbulb, MessageCircleQuestion, PencilLine } from "lucide-react";

import { FormattedReading } from "@/components/formatted-reading";
import { SensorModel } from "@/components/sensor-model";
import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { ContentBlock, LessonPage } from "@/lib/academy";
import { ResponseSpace } from "@/components/response-space";
import { LessonVisual } from "@/components/lesson-visual";
import { PredictExplain } from "@/components/predict-explain";

import { CurvePlot } from "@/components/curve-plot";

const calloutIcon = { idea: Lightbulb, think: MessageCircleQuestion, caution: AlertTriangle, teacher: BookMarked, answer: CheckCircle2 };

export function ContentBlockView({ block, storageKey }: { block: ContentBlock; storageKey?:string }) {
  if (block.presentation && "text" in block) return <FormattedReading text={block.text} format={block.presentation} />;
  if (block.type === "sensor") return <SensorModel />;
  if (block.type === "diagram") return <figure className="content-table-wrap" tabIndex={0} aria-label={block.title || "Scrollable visual model"}><h3>{block.title || "Visual model"}</h3>{block.rows ? <table><thead><tr>{block.columns?.map((v,i)=><th key={i}>{v}</th>)}</tr></thead><tbody>{block.rows.map((row,i)=><tr key={i}>{row.map((v,j)=><td key={j}>{v}</td>)}</tr>)}</tbody></table> : <div>{block.values && <table><tbody>{block.values.map((row,i)=><tr key={i}>{row.map((value,j)=><td key={j} style={{background:value ? "#13243b" : "white",color:value ? "white" : "#13243b",textAlign:"center",width:48,height:48}}>{value}</td>)}</tr>)}</tbody></table>}{block.series && <CurvePlot series={block.series} xValues={block.xValues} axis={block.axis} xLabel={block.xLabel} max={block.max} />}{block.series && <table><caption>{block.xLabel} / {block.axis}</caption><thead><tr><th>Series</th>{block.xValues?.map(v=><th key={v}>{v}</th>)}</tr></thead><tbody>{block.series.map(series=><tr key={series.label}><th>{series.label}</th>{series.values.map((v,i)=><td key={i}>{v}</td>)}</tr>)}</tbody></table>}</div>}{block.key && <p>{block.key}</p>}{block.caption && <figcaption>{block.caption}</figcaption>}</figure>;
  if (block.type === "image") return <LessonVisual {...block} />;
  if (block.type === "gallery") return <div className={`instruction-gallery ${block.layout === "reading-cards" ? "reading-cards" : ""}`}>{block.cells.map((cell, i) => <div className="gallery-cell" key={i}>{cell.map((item,j) => <Block key={j} block={item} storageKey={`${storageKey}-cell-${i}-${j}`} />)}</div>)}</div>;
  if (block.type === "title") return <h2 className="content-title">{block.text}</h2>;
  if (block.type === "heading") return <h2 className="content-heading">{block.text}</h2>;
  if (block.type === "subheading") return <h3 id={(block as {anchor?: string}).anchor} className="content-subheading">{block.text}</h3>;
  if (block.type === "code") return <pre className="code-block" tabIndex={0} aria-label="Python code example"><code>{block.text}</code></pre>;
  if (block.type === "step") return <div className="step-block">{block.text}</div>;
  if (block.type === "response") return <div><p>{block.text}</p><ResponseSpace storageKey={storageKey} prompt={block.text} /></div>;
  if (block.type === "list") return <div className={`content-list list-${block.marker}`}><span aria-hidden="true">{block.marker === "number" ? "→" : "•"}</span><p>{block.text}</p></div>;
  if (block.type === "callout") {
    const Icon = calloutIcon[block.tone] || Lightbulb;
    return <aside className={`callout callout-${block.tone}`}><Icon aria-hidden="true" /><p>{block.text}</p></aside>;
  }
  if (block.type === "table") {
    const [head, ...rows] = block.rows;
    return (
      <div className="content-table-wrap">
        <Table aria-label={head.join(" · ")}>
          <TableHeader><TableRow>{head.map((cell, index) => <TableHead key={index}>{cell}</TableHead>)}</TableRow></TableHeader>
          <TableBody>{rows.map((row, rowIndex) => <TableRow key={rowIndex}>{row.map((cell, cellIndex) => <TableCell key={cellIndex}>{cell}</TableCell>)}</TableRow>)}</TableBody>
        </Table>
      </div>
    );
  }
  return <p className="content-paragraph">{"text" in block ? block.text : ""}</p>;
}

const Block = ContentBlockView;

function FlowPageBlocks({page,responsePrefix}:{page:LessonPage;responsePrefix?:string}) {
 const show=(index:number,card=false)=>{
  const source=page.blocks[index];
  const block=source.presentation && "text" in source && !["checklist","definition"].includes(source.presentation.kind)
   ? {...source,presentation:{...source.presentation,kind:"body" as const,label:undefined,context:undefined}} : source;
  return <div className="flow-item" key={index}>{card&&source.presentation?.label&&<h4 className="flow-card-title">{source.presentation.label}</h4>}{source.presentation?.context&&<p className="flow-note">{source.presentation.context}</p>}<Block block={block} storageKey={source.responseStorageSuffix?`${responsePrefix || "resource"}-${source.responseStorageSuffix}`:`${responsePrefix || "resource"}-section-${page.number}-block-${index}`} /></div>;
 };
 return <>{page.flow!.groups.map((group,n)=>{
  const list=group.kind==="steps"||group.kind==="prompts";
  const textIndices=group.indices.filter(i=>["paragraph","step","list"].includes(page.blocks[i].type));
  const otherIndices=group.indices.filter(i=>!textIndices.includes(i));
  const items=list?<>{group.kind==="steps"?<ol className="flow-list flow-steps">{textIndices.map(i=><li key={i}>{show(i)}</li>)}</ol>:<ul className="flow-list">{textIndices.map(i=><li key={i}>{show(i)}</li>)}</ul>}{otherIndices.map(i=>show(i))}</>:<div className={group.kind==="cards"?"flow-card-grid":"flow-prose"}>{group.indices.map(i=>show(i,group.kind==="cards"))}</div>;
  const body=<>{group.note&&<p className="flow-note">{group.note}</p>}{items}</>;
  return group.collapsed?<details className="flow-reference" key={n}><summary>{group.title}</summary><div className="flow-reference-body">{body}</div></details>:<section className={`flow-chunk flow-${group.kind||"text"}`} key={n}><h3 className="flow-chunk-title">{group.title}</h3>{body}</section>;
 })}</>;
}

function PageBlocks({ page, responsePrefix }: { page: LessonPage; responsePrefix?:string }) {
  if(page.flow)return <FlowPageBlocks page={page} responsePrefix={responsePrefix} />;
  const explanation = page.blocks.findIndex(b => b.type === "subheading" && /^worked explanation$/i.test(b.text));
  const end = explanation >= 0 ? page.blocks.findIndex((b,i) => i > explanation && b.type === "subheading") : -1;
  const blocks = explanation >= 0 ? page.blocks.slice(0, explanation) : page.blocks;
  const grouped: ContentBlock[] = [];
  for (let i = 0; i < blocks.length; i++) {
    if (blocks[i].type === "image" && blocks[i + 1]?.type === "image") {
      const cells: ContentBlock[][] = [];
      while (blocks[i]?.type === "image") cells.push([blocks[i++]]);
      i--;
      grouped.push({ type: "gallery", cells });
    } else grouped.push(blocks[i]);
  }
  return <>{grouped.map((block, index) => <Block key={index} block={block} storageKey={`${responsePrefix || "resource"}-section-${page.number}-block-${index}`} />)}{explanation >= 0 && <PredictExplain storageKey={`${responsePrefix || "resource"}-prediction-${page.number}`}>{page.blocks.slice(explanation, end >= 0 ? end : undefined).map((block, index) => <Block key={index} block={block} storageKey={`${responsePrefix || "resource"}-section-${page.number}-explanation-${index}`} />)}</PredictExplain>}{end >= 0 && page.blocks.slice(end).map((block,index)=><Block key={`after-${index}`} block={block} storageKey={`${responsePrefix || "resource"}-section-${page.number}-block-${end+index}`}/>)}</>;
}

export function ContentReader({ pages, workbookBlocks, responsePrefix }: { pages?: LessonPage[]; workbookBlocks?: ContentBlock[]; responsePrefix?:string }) {
  const sections = pages ?? [{ number: 1, label: "WORKBOOK PRACTICE", blocks: workbookBlocks ?? [] }];
  const overview=sections[0]?.flow?.overview;
  const ordered=overview?overview.order.map(number=>sections.find(p=>p.number===number)!).filter(Boolean):sections;
  const main=ordered.filter(p=>!p.flow?.optional),reference=ordered.filter(p=>p.flow?.optional);
  const article=(page:LessonPage)=><article className={`lesson-section ${page.flow?"flow-section":""}`} id={`section-${page.number}`} key={page.number}>
    <div className="section-kicker"><Badge variant="outline">{page.flow?(page.flow.optional?"Reference & extra practice":"Main lesson"): `Section ${page.number}`}</Badge><span>{page.flow?`Section ${page.number}`:page.label}</span></div>
    <h2 className="reading-section-title">{page.flow?.title||page.label}</h2>
    {(page.flow?.purpose||page.intro)&&<p className="reading-section-intro">{page.flow?.purpose||page.intro}</p>}
    <div className="section-blocks"><PageBlocks page={page} responsePrefix={responsePrefix} /></div>
  </article>;
  return <div className={`reader-layout ${sections.some(page=>(page.intro || page.blocks.some(block=>block.presentation))) ? "reading-edition" : ""} ${overview?"connected-reading":""}`} data-connected-reading={overview?true:undefined}>
    <aside className="reader-nav" aria-label="Lesson sections">
      <p className="reader-nav-title">{overview?"Your main route":"In this resource"}</p>
      {main.map((page,index)=><a key={page.number} href={`#section-${page.number}`}><span>{String(overview?index+1:page.number).padStart(2,"0")}</span>{page.flow?.title||page.label.toLowerCase()}</a>)}
      {reference.length>0&&<a href="#reading-reference-bank">Reference & extra practice ({reference.length})</a>}
    </aside>
    <div className="reader-content">
      {overview&&<section className="flow-overview" aria-label="This week as a whole"><p className="flow-kicker">THE CONNECTED WEEK</p><h2>{overview.title}</h2><p>{overview.lead}</p><nav className="flow-route" aria-label="Six steps through the week">{overview.route.map((step,i)=><a href={`#section-${step.section}`} key={i}><span>{i+1}</span>{step.label}</a>)}</nav><p className="flow-outcome"><strong>Keep one habit:</strong> {overview.outcome}</p></section>}
      {main.map(article)}
      {reference.length>0&&<section className="flow-reference-bank" id="reading-reference-bank"><h2>Reference & extra practice</h2><p>Choose what helps you. Alternative copies and previously discussed cases are not additional independent assessments.</p>{reference.map(page=><details className="flow-reference flow-reference-section" key={page.number}><summary>{page.flow?.title||page.label}</summary>{article(page)}</details>)}</section>}
    </div>
  </div>;
}
