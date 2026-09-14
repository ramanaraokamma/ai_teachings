"use client";

import { useState } from "react";
import { Lightbulb, ScanLine, ArrowRight } from "lucide-react";
import { Slider } from "@/components/ui/slider";

export function SensorLab() {
  const [reading, setReading] = useState(18);
  const lampOn = reading < 30;
  return <section className="sensor-lab" aria-labelledby="sensor-lab-title">
    <div className="book-overline">MOVE • NOTICE • EXPLAIN</div><h3 id="sensor-lab-title">The sensor measures. The rule decides.</h3>
    <p>This classroom model uses a made-up light scale from 0 to 100. Change the reading and follow the two different jobs.</p>
    <div className="sensor-control"><label id="light-scale-label">Light reading: <strong>{reading}</strong></label><Slider aria-labelledby="light-scale-label" min={0} max={100} step={1} value={[reading]} onValueChange={v => setReading(v[0])} /><div className="scale-labels"><span>0 · darker</span><span>100 · brighter</span></div></div>
    <div className="sensor-demo-flow">
      <div className="sensor-demo-card"><ScanLine aria-hidden="true"/><small>1. SENSOR MESSAGE</small><div className="reading-bar"><i style={{height:`${reading}%`}} /></div><strong>{reading}</strong><p>A number describing light.</p></div>
      <ArrowRight className="sensor-flow-arrow" aria-hidden="true"/>
      <div className="sensor-demo-card"><small>2. FIXED RULE</small><code>IF reading &lt; 30<br/>THEN lamp ON<br/>ELSE lamp OFF</code><p>The rule checks the number.</p></div>
      <ArrowRight className="sensor-flow-arrow" aria-hidden="true"/>
      <div className={`sensor-demo-card lamp-${lampOn ? 'on' : 'off'}`}><Lightbulb aria-hidden="true"/><small>3. ACTION</small><strong aria-live="polite">Lamp {lampOn ? 'ON' : 'OFF'}</strong><p>The lamp follows the rule.</p></div>
    </div>
    <div className="book-discussion"><strong>Try 29, then 30.</strong><p>What changes? Which part measured the light, and which part chose the action?</p></div>
    <p className="sensor-boundary">This is fixed-rule automation. A sensor and a rule alone do not make a learned AI model.</p>
  </section>;
}
