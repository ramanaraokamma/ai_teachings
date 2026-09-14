import {grade6Review} from '@/lib/grade6-review';
import {ResponseSpace} from '@/components/response-space';

export function ReadinessCheck({level,week}:{level:string;week:number}){
 const r=grade6Review(level,week);
 return <aside className="readiness-check" data-review-id={r.id}>
  <p className="review-eyebrow">RETRIEVE · CONNECT · EXPLAIN</p>
  <h2>Before you begin</h2><p>{r.recall}</p>
  <p>Explain this idea aloud or sketch an example before reading on. If it is unfamiliar, revisit the named lesson with your teacher.</p>
 </aside>;
}
export function TransferChallenge({level,week,teacher=false}:{level:string;week:number;teacher?:boolean}){
 const r=grade6Review(level,week);
 return <article className="transfer-challenge" data-transfer-id={r.id}>
  <header><p className="review-eyebrow">APPLY · JUSTIFY · CHECK THE LIMIT</p><h2>A new case to solve</h2></header>
  <p className="transfer-question">{r.task}</p>
  <p>Attempt this independently after the worked example. Show the steps and evidence that support your answer.</p>
  <ResponseSpace/>
  <details className="transfer-hint"><summary>Use a hint if you need one</summary><p>{r.hint}</p><p>Record that you used support; try a fresh case later without the hint.</p></details>
  <div className="transfer-self-check"><h3>Check your reasoning</h3><p>Did I answer each part, show my evidence or calculation, and avoid claiming more than the case establishes?</p><p>Attempt: independently / with a hint / with teacher support</p></div>
  {teacher&&<section className="transfer-answer" data-teacher-solution={r.id}><h3>Teacher solution and diagnostic notes</h3><p>{r.solution}</p><h4>Use this in two 45-minute sessions</h4><p>Session 1: retrieve prerequisites (5 min), explain with the weekly diagram (10), model the worked case (10), practise in pairs (15), check one explanation (5). Session 2: recall (5), run the supplied workbook case (15), attempt this transfer task (15), give feedback and identify a next step (10).</p><h4>Board plan and response to difficulty</h4><p>Draw three columns: given evidence, reasoning steps, conclusion and limit. Use the weekly diagram to model the original worked case. Keep this transfer solution covered until independent attempts are collected.</p><p>Support: read the task aloud, define its vocabulary and let students organise the given facts without supplying a conclusion. If a prerequisite is missing, return to the named lesson. Stretch: change one condition in this case, predict its effect and defend the change.</p><h4>Assess the evidence</h4><p>Check the result, reasoning and stated limit against the solution above. Record each as secure, developing or not yet, and record support used separately. A polished answer without a valid explanation is not independent mastery. After feedback, use a teacher-checked changed case for an uncoached retry.</p></section>}
 </article>;
}
