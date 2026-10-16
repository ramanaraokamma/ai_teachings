export type ReadingPresentation = {
  kind: "body" | "eyebrow" | "concept" | "example" | "question" | "note" | "caution" | "step" | "definition" | "check" | "section-label" | "section-heading" | "checklist";
  label?: string;
  context?:string;
  items?:string[];
  tail?:string;
  paragraphs?: string[];
  emphasis?: string[];
};

export function readingSegments(text:string,terms:string[] = []) {
 const escaped=[...terms].sort((a,b)=>b.length-a.length).map(s=>s.replace(/[.*+?^${}()|[\]\\]/g,"\\$&"));
 if(!escaped.length)return [{text,strong:false}];
 const pattern=new RegExp(`(${escaped.join("|")})`,"gi");
 return text.split(pattern).filter(Boolean).map(part=>({text:part,strong:terms.some(term=>term.toLowerCase()===part.toLowerCase())}));
}
