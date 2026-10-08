"use client";
import { useEffect, useId, useState } from "react";
export function ResponseSpace({storageKey,prompt="Your answer and reasoning"}: {storageKey?:string;prompt?:string} = {}) {
  const id = useId();
  const [value, setValue] = useState("");
  const [saved, setSaved] = useState(true);
  const [activeKey,setActiveKey]=useState("");
  const [ready, setReady] = useState(false);
  const key = () => `academy-answer-v1:${window.location.pathname}:${new URLSearchParams(window.location.search).get("resource") || (window.location.pathname.includes("/teacher/") ? "guide" : "lesson")}:${storageKey || id}`;
  useEffect(() => {setActiveKey(key());try {setValue(localStorage.getItem(key()) || "");} catch {setSaved(false);}setReady(true);}, [id, storageKey, prompt]);
  return <div className="response-space interactive-response">
    <label htmlFor={id}>{prompt}</label>
    <textarea id={id} value={value} data-evidence-key={activeKey} data-evidence-prompt={prompt} disabled={!ready} rows={4} placeholder="Write your prediction, evidence or explanation…" onChange={event => { setValue(event.target.value); try {localStorage.setItem(key(),event.target.value);localStorage.setItem(`academy-answer-meta-v1:${key()}`,JSON.stringify({prompt,updatedAt:new Date().toISOString()}));setSaved(true);} catch {setSaved(false);}event.target.style.height = "auto"; event.target.style.height = `${event.target.scrollHeight}px`; }} />
    <small>{saved ? "Draft saved in this browser. Print or download your work for your portfolio. Use fictional data; clear drafts on a shared device." : "Browser storage is unavailable. Print to keep your work."}</small>
    <button type="button" onClick={() => {setValue("");try{localStorage.removeItem(key());localStorage.removeItem(`academy-answer-meta-v1:${key()}`);}catch{setSaved(false);}}}>Clear this draft</button>
    <pre className="print-answer">{value || "\n\n\n"}</pre>
  </div>;
}
