"use client";
import { useId, useState } from "react";
export function ResponseSpace() {
  const id = useId();
  const [value, setValue] = useState("");
  return <div className="response-space interactive-response">
    <label htmlFor={id}>Your answer and reasoning</label>
    <textarea id={id} value={value} rows={4} placeholder="Write your prediction, evidence or explanation…" onChange={event => { setValue(event.target.value); event.target.style.height = "auto"; event.target.style.height = `${event.target.scrollHeight}px`; }} />
    <small>Responses stay on this page until you leave or reload. Print to keep your work.</small>
    <pre className="print-answer">{value || "\n\n\n"}</pre>
  </div>;
}
