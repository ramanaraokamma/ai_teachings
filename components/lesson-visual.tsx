"use client";

import { useState } from "react";
import { Expand } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

export function LessonVisual({ src, alt, width, height, graphic_journey }: { src: string; alt: string; width: number; height: number; graphic_journey?: boolean }) {
  const [failed, setFailed] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [readLabels, setReadLabels] = useState(Boolean(graphic_journey));
  return <figure className="instruction-visual">
    {failed ? <div className="visual-recovery" role="status"><strong>This picture could not load.</strong><p>{alt}</p><button onClick={() => { setAttempt(attempt + 1); setFailed(false); }}>Try loading the picture again</button><p>If your session has ended, sign in again.</p></div> : <Dialog>
      <DialogTrigger asChild><button className="visual-expand" aria-label={`Take a closer look: ${alt}`}><img key={attempt} src={src + (attempt ? `?retry=${attempt}` : "")} alt={alt} width={width} height={height} loading="eager" decoding="async" onError={() => setFailed(true)} /><span className="visual-zoom-label"><Expand aria-hidden="true" /> Take a closer look</span></button></DialogTrigger>
      <DialogContent className="visual-dialog"><DialogTitle>Take a closer look</DialogTitle><DialogDescription>Fit the whole picture, or choose Read labels and scroll to explore the details.</DialogDescription><div className="visual-view-controls"><button type="button" aria-pressed={!readLabels} onClick={() => setReadLabels(false)}>Fit whole picture</button><button type="button" aria-pressed={readLabels} onClick={() => setReadLabels(true)}>Read labels</button></div><div className={`visual-detail-scroll ${readLabels ? "read-labels" : "fit-picture"}`} tabIndex={0} role="group" aria-label="Scrollable enlarged lesson graphic"><img src={src} alt={alt} /></div></DialogContent>
    </Dialog>}
    <figcaption>{graphic_journey ? "Follow the labels and arrows. Read the explanation below." : alt}</figcaption>
  </figure>;
}
