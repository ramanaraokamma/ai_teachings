"use client";
import { useId, useState } from "react";
export function ResponseSpace({label = "Your answer and reasoning", lines = 4}: {label?:string;lines?:number} = {}) {
  const id = useId();
  const [value, setValue] = useState("");
  return <div className="response-space interactive-response">
    <label htmlFor={id}>{label}</label>
    <textarea id={id} value={value} rows={Math.max(4, lines)} placeholder="Write your prediction, evidence or explanation…" onChange={event => { setValue(event.target.value); event.target.style.height = "auto"; event.target.style.height = `${event.target.scrollHeight}px`; }} />
    <small>Responses stay on this page until you leave or reload. Print to keep your work.</small>
    <pre className="print-answer" style={{minHeight:`${Math.max(4,lines)*1.6}rem`}}>{value || "\n\n\n"}</pre>
  </div>;
}
