import {readingSegments,type ReadingPresentation} from "@/lib/reading-format";
export function FormattedReading({text,format}:{text:string;format:ReadingPresentation}) {
 if(format.kind==="section-label")return null;
 const rich=(value:string)=>readingSegments(value,format.emphasis).map((part,i)=>part.strong?<strong key={i}>{part.text}</strong>:part.text);
 if(format.kind==="eyebrow")return <p className="reading-eyebrow">{text}</p>;
 if(format.kind==="section-heading")return <><h2 className="reading-section-title">{text}</h2>{format.context&&<p className="reading-section-intro">{format.context}</p>}</>;
 if(format.kind==="checklist")return <div className="reading-block reading-checklist"><ul>{format.items?.map((item,i)=><li key={i}>{rich(item)}</li>)}</ul>{format.tail&&<p>{rich(format.tail)}</p>}</div>;
 const paragraphs=format.paragraphs||[text];
 const label=format.label;
 const content=<>{label&&<h3 className="reading-label">{label}</h3>}{format.context&&<p className="reading-context">{format.context}</p>}{paragraphs.map((value,i)=><p key={i}>{rich(value)}</p>)}</>;
 if(["concept","example","question","note","caution"].includes(format.kind))return <aside className={`reading-block reading-${format.kind}`}>{content}</aside>;
 return <div className={`reading-block reading-${format.kind}`}>{content}</div>;
}
