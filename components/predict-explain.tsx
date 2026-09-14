"use client";

import { useState, type ReactNode } from "react";
import { ResponseSpace } from "@/components/response-space";

export function PredictExplain({ children }: { children: ReactNode }) {
  const [open, setOpen] = useState(false);
  return <div className="predict-explain"><div className="prediction-prompt"><h3>Pause and make a prediction</h3><p>What do you think? Write or say your answer before you compare it with the worked explanation.</p><ResponseSpace /></div><button className="explanation-toggle" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? "Hide worked explanation" : "Compare with the worked explanation"}</button><div className="worked-reveal" hidden={!open}>{children}</div></div>;
}
