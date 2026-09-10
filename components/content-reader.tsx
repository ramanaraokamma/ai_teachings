import { AlertTriangle, BookMarked, CheckCircle2, Lightbulb, MessageCircleQuestion, PencilLine } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { ContentBlock, LessonPage } from "@/lib/academy";
import { ResponseSpace } from "@/components/response-space";

const calloutIcon = { idea: Lightbulb, think: MessageCircleQuestion, caution: AlertTriangle, teacher: BookMarked, answer: CheckCircle2 };

function Block({ block }: { block: ContentBlock }) {
  if (block.type === "image") return <figure className="instruction-visual"><img src={block.src} alt={block.alt} width={block.width} height={block.height} loading="lazy" decoding="async" /><figcaption>{block.alt}</figcaption></figure>;
  if (block.type === "gallery") return <div className="instruction-gallery">{block.cells.map((cell, i) => <div className="gallery-cell" key={i}>{cell.map((item,j) => <Block key={j} block={item} />)}</div>)}</div>;
  if (block.type === "title") return <h2 className="content-title">{block.text}</h2>;
  if (block.type === "heading") return <h2 className="content-heading">{block.text}</h2>;
  if (block.type === "subheading") return <h3 className="content-subheading">{block.text}</h3>;
  if (block.type === "code") return <pre className="code-block"><code>{block.text}</code></pre>;
  if (block.type === "step") return <div className="step-block">{block.text}</div>;
  if (block.type === "response") return <ResponseSpace />;
  if (block.type === "list") return <div className={`content-list list-${block.marker}`}><span aria-hidden="true">{block.marker === "number" ? "→" : "•"}</span><p>{block.text}</p></div>;
  if (block.type === "callout") {
    const Icon = calloutIcon[block.tone];
    return <aside className={`callout callout-${block.tone}`}><Icon aria-hidden="true" /><p>{block.text}</p></aside>;
  }
  if (block.type === "table") {
    const [head, ...rows] = block.rows;
    return (
      <div className="content-table-wrap">
        <Table>
          <TableHeader><TableRow>{head.map((cell, index) => <TableHead key={index}>{cell}</TableHead>)}</TableRow></TableHeader>
          <TableBody>{rows.map((row, rowIndex) => <TableRow key={rowIndex}>{row.map((cell, cellIndex) => <TableCell key={cellIndex}>{cell}</TableCell>)}</TableRow>)}</TableBody>
        </Table>
      </div>
    );
  }
  return <p className="content-paragraph">{"text" in block ? block.text : ""}</p>;
}

export function ContentReader({ pages, workbookBlocks }: { pages?: LessonPage[]; workbookBlocks?: ContentBlock[] }) {
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
            <div className="section-blocks">{page.blocks.map((block, index) => <Block key={`${page.number}-${index}`} block={block} />)}</div>
          </article>
        ))}
      </div>
    </div>
  );
}
