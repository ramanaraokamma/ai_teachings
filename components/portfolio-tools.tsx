"use client";
import {useState} from "react";
import {collectEvidence,identifyDraft,portfolioHTML,type Evidence} from "@/lib/learning/portfolio";
import {ResponseSpace} from "@/components/response-space";
export function PortfolioTools({role,week,titles}:{role:string;week?:string;titles:Record<string,{title:string;project:string}>}){
 const [status,setStatus]=useState('');
 function download(format:'html'|'json'){
  let evidence:Evidence[]=[];try{evidence=collectEvidence(localStorage,role,week);}catch{}
  const merged=new Map(evidence.map(e=>[e.key,e]));
  document.querySelectorAll<HTMLTextAreaElement>('textarea[data-evidence-key]').forEach(area=>{const key=area.dataset.evidenceKey||'';const info=identifyDraft(key);if(info?.role===role&&(!week||info.week===week)){if(area.value.trim())merged.set(key,{key,...info,prompt:area.dataset.evidencePrompt||'My reasoning',answer:area.value,updatedAt:new Date().toISOString()});else merged.delete(key);}});
  evidence=[...merged.values()];if(!evidence.length){setStatus('Write an answer or project reflection first, then download your completed work.');return;}
  const date=new Date().toISOString();const content=format==='html'?portfolioHTML(evidence,titles,date):JSON.stringify({version:1,exportedAt:date,role,evidence:evidence.map(({key,...record})=>({...record,...titles[record.week]}))},null,2);
  const url=URL.createObjectURL(new Blob([content],{type:format==='html'?'text/html;charset=utf-8':'application/json'}));const link=document.createElement('a');link.href=url;link.download=`ai-academy-${role}-${week?.replace('/','-')||'portfolio'}.${format}`;link.click();setTimeout(()=>URL.revokeObjectURL(url),1000);setStatus(`Downloaded ${evidence.length} recorded responses. Open the HTML file to read or print your portfolio.`);
 }
 return <section className="classroom-panel portfolio-tools"><h2>{week?'Keep this week’s completed work':'Your completed-work portfolio'}</h2><p>Download your own answers and project reflections. The HTML copy is readable offline and printable; the JSON copy keeps a structured record.</p>{week&&<details><summary>Add project evidence and reflection</summary>{['The input, test or code I used','My prediction, actual result and what I changed','My explanation, remaining limit and next useful test'].map((prompt,i)=><div key={prompt}><h3>{prompt}</h3><ResponseSpace prompt={prompt} storageKey={`${week}-portfolio-${i}`}/></div>)}</details>}<div className="learning-actions"><button type="button" onClick={()=>download('html')}>Download completed work (.html)</button><button type="button" onClick={()=>download('json')}>Download evidence (.json)</button></div><p role="status" aria-live="polite">{status}</p></section>;
}
