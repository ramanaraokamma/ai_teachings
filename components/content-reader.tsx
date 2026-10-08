import { AlertTriangle, BookMarked, CheckCircle2, Lightbulb, MessageCircleQuestion, PencilLine } from "lucide-react";

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
  if (block.type === "sensor") return <SensorModel />;
  if (block.type === "diagram") return <figure className="content-table-wrap" tabIndex={0} aria-label={block.title || "Scrollable visual model"}><h3>{block.title || "Visual model"}</h3>{block.rows ? <table><thead><tr>{block.columns?.map((v,i)=><th key={i}>{v}</th>)}</tr></thead><tbody>{block.rows.map((row,i)=><tr key={i}>{row.map((v,j)=><td key={j}>{v}</td>)}</tr>)}</tbody></table> : <div>{block.values && <table><tbody>{block.values.map((row,i)=><tr key={i}>{row.map((value,j)=><td key={j} style={{background:value ? "#13243b" : "white",color:value ? "white" : "#13243b",textAlign:"center",width:48,height:48}}>{value}</td>)}</tr>)}</tbody></table>}{block.series && <CurvePlot series={block.series} xValues={block.xValues} axis={block.axis} xLabel={block.xLabel} max={block.max} />}{block.series && <table><caption>{block.xLabel} / {block.axis}</caption><thead><tr><th>Series</th>{block.xValues?.map(v=><th key={v}>{v}</th>)}</tr></thead><tbody>{block.series.map(series=><tr key={series.label}><th>{series.label}</th>{series.values.map((v,i)=><td key={i}>{v}</td>)}</tr>)}</tbody></table>}</div>}{block.key && <p>{block.key}</p>}{block.caption && <figcaption>{block.caption}</figcaption>}</figure>;
  if (block.type === "image") return <LessonVisual {...block} />;
  if (block.type === "gallery") return <div className="instruction-gallery">{block.cells.map((cell, i) => <div className="gallery-cell" key={i}>{cell.map((item,j) => <Block key={j} block={item} storageKey={`${storageKey}-cell-${i}-${j}`} />)}</div>)}</div>;
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

function PageBlocks({ page, responsePrefix }: { page: LessonPage; responsePrefix?:string }) {
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
  return (
    <div className="reader-layout">
      <aside className="reader-nav" aria-label="Lesson sections">
        <p className="reader-nav-title">In this resource</p>
        {sections.map((page) => <a key={page.number} href={`#section-${page.number}`}><span>{String(page.number).padStart(2, "0")}</span>{page.label.toLowerCase()}</a>)}
      </aside>
      <div className="reader-content">
        {sections.map((page) => (
          <article className="lesson-section" id={`section-${page.number}`} key={page.number}>
            <div className="section-kicker"><Badge variant="outline">Section {page.number}</Badge><span>{page.label}</span></div>
            <div className="section-blocks"><PageBlocks page={page} responsePrefix={responsePrefix} /></div>
          </article>
        ))}
      </div>
    </div>
  );
}
