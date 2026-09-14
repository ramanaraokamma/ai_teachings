"use client";

import { useState } from "react";
import { Expand } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

export function LessonVisual({ src, alt, width, height }: { src: string; alt: string; width: number; height: number }) {
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  return <figure className="instruction-visual">
    {failed ? <div className="visual-recovery" role="status"><strong>This picture could not load.</strong><p>{alt}</p><button onClick={() => { setAttempt(attempt + 1); setFailed(false); }}>Try loading the picture again</button><p>If your session has ended, sign in again.</p></div> : <Dialog>
      <DialogTrigger asChild><button className="visual-expand" aria-label={`Enlarge illustration: ${alt}`}><img key={attempt} src={src + (attempt ? `?retry=${attempt}` : "")} alt={alt} width={width} height={height} loading="eager" decoding="async" onError={() => setFailed(true)} /><span className="visual-zoom-label"><Expand aria-hidden="true" /> Take a closer look</span></button></DialogTrigger>
      <DialogContent className="visual-dialog"><DialogTitle>Take a closer look</DialogTitle><DialogDescription>{alt}</DialogDescription><img src={src} alt={alt} /></DialogContent>
    </Dialog>}
    <figcaption>{alt}</figcaption>
  </figure>;
}
