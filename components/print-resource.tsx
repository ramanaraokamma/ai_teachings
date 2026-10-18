"use client";
import { Printer } from "lucide-react";
import { useEffect, useState } from "react";
export function PrintResource() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  useEffect(()=>{
    let opened:HTMLDetailsElement[]=[];
    const prepare=()=>{opened=Array.from(document.querySelectorAll<HTMLDetailsElement>('details.topic-solution:not([open]),[data-connected-reading] details:not([open])'));opened.forEach(d=>d.open=true);};
    const restore=()=>{opened.forEach(d=>d.open=false);opened=[];};
    const revealAnchor=()=>{const id=decodeURIComponent(location.hash.slice(1));if(!id)return;const target=document.getElementById(id);if(!target?.closest('[data-connected-reading]'))return;let parent=target.parentElement;while(parent){if(parent instanceof HTMLDetailsElement)parent.open=true;parent=parent.parentElement;}requestAnimationFrame(()=>target.scrollIntoView({block:'start'}));};
    window.addEventListener('hashchange',revealAnchor);revealAnchor();
    window.addEventListener('beforeprint',prepare);window.addEventListener('afterprint',restore);
    return()=>{window.removeEventListener('hashchange',revealAnchor);window.removeEventListener('beforeprint',prepare);window.removeEventListener('afterprint',restore);};
  },[]);
  async function print() {
    setBusy(true); setError(false);
    try {
      const images = Array.from(document.querySelectorAll<HTMLImageElement>(".lesson-reader-shell img"));
      await Promise.race([Promise.all(images.map(image => { image.loading = "eager"; return image.decode(); })), new Promise((_, reject) => setTimeout(() => reject(new Error("Image timeout")), 15000))]);
      window.print();
    } catch { setError(true); }
    finally { setBusy(false); }
  }
  return <><button type="button" className="resource-action" disabled={busy} onClick={print}><Printer aria-hidden="true" />{busy ? "Preparing illustrations…" : "Print this resource"}</button>{error && <span role="alert">A picture could not load. Sign in again if needed, then retry printing.</span>}</>;
}
