"use client";
import {useEffect,useState} from "react";
const key="academy-progress-v1";
type RecordItem={visited?:boolean;complete?:boolean};
export function LearningProgress({id,role}:{id?:string;role:string}) {
 const [records,setRecords]=useState<Record<string,RecordItem>>({});const [ready,setReady]=useState(false);const [saved,setSaved]=useState(true);
 useEffect(()=>{try{const value=JSON.parse(localStorage.getItem(`${key}-${role}`)||"{}");setRecords(value&&typeof value==="object"&&!Array.isArray(value)?value:{});}catch{setSaved(false);}setReady(true);},[role]);
 function mark(complete:boolean){if(!id)return;const updated={...records,[id]:{visited:true,complete}};setRecords(updated);try{localStorage.setItem(`${key}-${role}`,JSON.stringify(updated));setSaved(true);}catch{setSaved(false);}}
 const done=Object.values(records).filter(v=>v?.complete).length;
 const latest=Object.entries(records).filter(([,v])=>v?.complete).at(-1)?.[0];
 return <div className="learning-progress"><strong>{done} weeks marked {role==="teacher"?"reviewed":"practised"}</strong>{id&&<label><input type="checkbox" disabled={!ready} checked={Boolean(records[id]?.complete)} onChange={e=>mark(e.target.checked)}/>{role==="teacher"?"I reviewed this week’s teaching materials":"I practised this week and saved my evidence"}</label>}<small>{saved?"Progress stays in this browser. A tick records practice; your explanation and evidence show understanding.":"This browser could not save progress. Keep a printed or downloaded record."}</small>{!id&&latest&&<a href={`/learn/${role}/${latest}`}>Return to your latest recorded week</a>}{!id&&done>0&&<ul>{Object.entries(records).filter(([,v])=>v?.complete).map(([week])=><li key={week}><a href={`/learn/${role}/${week}`}>{week.replace("/"," · Week ")}</a></li>)}</ul>}</div>;
}
