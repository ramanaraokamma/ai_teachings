export type Evidence = { key:string; role:string; week:string; resource:string; prompt:string; answer:string; updatedAt?:string };
export function identifyDraft(key:string) {
 const match=key.match(/^academy-answer-v1:\/learn\/(student|teacher)\/(ai-[1-7]|python-bridge)(?:\/(\d+))?:([^:]+):/);
 return match ? {role:match[1],week:`${match[2]}/${match[3]||'readiness'}`,resource:match[4]} : null;
}
export function collectEvidence(storage:Storage,role:string,week?:string):Evidence[] {
 const records:Evidence[]=[];
 for(let i=0;i<storage.length;i++) {const key=storage.key(i);if(!key)continue;const location=identifyDraft(key);if(!location||location.role!==role||(week&&location.week!==week))continue;const answer=storage.getItem(key)||'';if(!answer.trim())continue;
  let meta:{prompt?:string;updatedAt?:string}={};try{meta=JSON.parse(storage.getItem(`academy-answer-meta-v1:${key}`)||'{}');}catch{}
  const section=key.match(/section-(\d+)/)?.[1];records.push({key,...location,prompt:meta.prompt||`Saved ${location.resource} response${section?` in Section ${section}`:''}`,answer,updatedAt:meta.updatedAt});
 }
 return records.sort((a,b)=>a.week.localeCompare(b.week,undefined,{numeric:true})||a.key.localeCompare(b.key,undefined,{numeric:true}));
}
export function escapeHTML(text:string){return text.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));}
export function portfolioHTML(records:Evidence[],titles:Record<string,{title:string;project:string}>,date:string){
 return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>My AI Academy portfolio</title><style>body{max-width:900px;margin:auto;padding:24px;font:17px/1.65 system-ui;color:#183249}section{border-top:2px solid #9ab9c9;margin:24px 0;padding:18px 0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;background:#f1f6f9;padding:16px}h2,h3{break-after:avoid}@media print{body{padding:0;font-size:11pt}pre{background:white}}</style></head><body><h1>My AI Academy portfolio</h1><p>Exported ${escapeHTML(date)}. These are my recorded responses and evidence; they are not an automatic mastery score.</p>${records.map(r=>`<section><h2>${escapeHTML(titles[r.week]?.title||r.week)}</h2><p>Week: ${escapeHTML(r.week)} · Resource: ${escapeHTML(r.resource)}</p><p>Project: ${escapeHTML(titles[r.week]?.project||'Readiness and learning evidence')}</p><h3>${escapeHTML(r.prompt)}</h3><pre>${escapeHTML(r.answer)}</pre>${r.updatedAt?`<p>Last recorded: ${escapeHTML(r.updatedAt)}</p>`:''}</section>`).join('')}<p>Keep inputs, predictions, actual results, revisions and limitations together. Discuss your reasoning with your teacher.</p></body></html>`;
}
