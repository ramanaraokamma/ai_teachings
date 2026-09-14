"use client";

import { useRef, useState, type ReactNode } from "react";
import { ArrowRight, Eye, Lightbulb, FlaskConical, Flag } from "lucide-react";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

const icons = [Eye, Lightbulb, FlaskConical, Flag];
export function LearningStages({ stages }: { stages: { title: string; hint: string; content: ReactNode }[] }) {
  const [active, setActive] = useState("0");
  const root = useRef<HTMLDivElement>(null);
  function next(index: number) {
    setActive(String(index));
    root.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    requestAnimationFrame(() => root.current?.querySelector<HTMLButtonElement>(`[data-stage="${index}"]`)?.focus({ preventScroll: true }));
  }
  return <div ref={root} className="learning-journey">
    <div className="journey-intro"><span className="eyebrow">YOUR LEARNING PATH</span><h2>One idea. Four ways to understand it.</h2><p>Explore the pictures, explain the idea, test it, then show your own reasoning. You can return to any step.</p></div>
    <Tabs value={active} onValueChange={setActive}>
      <TabsList className="journey-tabs" aria-label="Learning steps">{stages.map((stage, i) => { const Icon = icons[i]; return <TabsTrigger data-stage={i} key={i} value={String(i)}><Icon aria-hidden="true" /><span><small>Step {i + 1}</small>{stage.title}</span></TabsTrigger>; })}</TabsList>
      {stages.map((stage, i) => <TabsContent forceMount className="journey-panel" value={String(i)} key={i}>
        <div className="stage-purpose"><strong>{stage.title}</strong><p>{stage.hint}</p></div>
        {stage.content}
        {i < stages.length - 1 && <button className="journey-next" onClick={() => next(i + 1)}>Next: {stages[i + 1].title}<ArrowRight aria-hidden="true" /></button>}
      </TabsContent>)}
    </Tabs>
  </div>;
}
