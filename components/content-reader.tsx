import { AlertTriangle, BookMarked, CheckCircle2, Lightbulb, MessageCircleQuestion, PencilLine } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { ContentBlock, LessonPage } from "@/lib/academy";
import { ResponseSpace } from "@/components/response-space";
import { LessonVisual } from "@/components/lesson-visual";
import { LearningStages } from "@/components/learning-stages";
import { PredictExplain } from "@/components/predict-explain";

const calloutIcon = { idea: Lightbulb, think: MessageCircleQuestion, caution: AlertTriangle, teacher: BookMarked, answer: CheckCircle2 };

export function ContentBlockView({ block }: { block: ContentBlock }) {
  if (block.type === "image") return <LessonVisual {...block} />;
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

const Block = ContentBlockView;

function PageBlocks({ page }: { page: LessonPage }) {
  const explanation = page.number === 13 ? page.blocks.findIndex(b => b.type === "subheading" && /worked explanation/i.test(b.text)) : -1;
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
  return <>{grouped.map((block, index) => <Block key={index} block={block} />)}{explanation >= 0 && <PredictExplain>{page.blocks.slice(explanation).map((block, index) => <Block key={index} block={block} />)}</PredictExplain>}</>;
}

const stageNames: Record<string, string[]> = { ai1: ["Look", "Learn", "Try", "Show"], ai2: ["Notice", "Trace", "Test", "Explain"], ai3: ["Explore", "Create", "Verify", "Defend"], ai4: ["Frame", "Model", "Evaluate", "Defend"] };
const stageHints: Record<string, string[]> = {
  ai1: ["Look closely. What do you notice in the pictures? Learn the new words together.", "Follow the pictures and talk through what happens. Predict before revealing the explanation.", "Try the activity with a partner or grown-up. Mistakes help you find what to change.", "Use a fresh example. Show your thinking with a drawing, words, or a demonstration."],
  ai2: ["Spot the important details and name the idea you will investigate.", "Trace each step. Compare cases and explain why the results differ.", "Run the activity, record evidence, and repair a mistake.", "Solve a new case independently and explain the evidence for your decision."],
  ai3: ["Identify the system's purpose, inputs, and limits.", "Follow the mechanism and predict the outcome before examining a worked case.", "Test the workflow, verify the evidence, and diagnose its failure modes.", "Apply the idea independently and defend your choices and limitations."],
  ai4: ["Define the learning problem and the evidence needed to investigate it.", "Trace the model or calculation and explain the assumptions in the worked example.", "Run an experiment, record results, and diagnose errors using evidence.", "Evaluate a fresh case, document limitations, and connect the result to your capstone."]
};

export function ContentReader({ pages, workbookBlocks, level }: { pages?: LessonPage[]; workbookBlocks?: ContentBlock[]; level?: string }) {
  const sections = pages ?? [{ number: 1, label: "WORKBOOK PRACTICE", blocks: workbookBlocks ?? [] }];
  const article = (page: LessonPage) => <article className={`lesson-section section-page-${page.number}`} id={`section-${page.number}`} key={page.number}><div className="section-kicker"><Badge variant="outline">Section {page.number}</Badge><span>{page.label}</span></div><div className="section-blocks"><PageBlocks page={page} /></div></article>;
  if (level && pages) {
    const key = level.replace(/-/g, "");
    const order = [[1,2,5], [3,4,6,13], [8,9,7], [14,12,10,11,15]];
    return <LearningStages stages={order.map((numbers, i) => ({ title: (stageNames[key] ?? stageNames.ai1)[i], hint: (stageHints[key] ?? stageHints.ai1)[i], content: <div className="reader-content">{numbers.map(n => pages.find(p => p.number === n)).filter((p): p is LessonPage => Boolean(p)).map(article)}</div> }))} />;
  }
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
