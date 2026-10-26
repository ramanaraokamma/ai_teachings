"use client";

import {ResponseSpace} from "@/components/response-space";

type CheckpointProps = {week:string;title:string;teacher:boolean;workedExample?:number};

export function LearningCheckpoint({week,title,teacher,workedExample}:CheckpointProps){
 return <section data-connected-reading className="classroom-panel learning-checkpoint" aria-labelledby="learning-checkpoint-title">
  <p className="checkpoint-eyebrow">{teacher?"Observe, then choose the next step":"Pause · explain · choose your next step"}</p>
  <h2 id="learning-checkpoint-title">{teacher?"Check understanding, beyond the right answer":"What can you explain now?"}</h2>
  <p>{teacher?`Use these three checks after teaching “${title}”. Let the learner answer before you offer a hint. Record what they said or did, and the support they needed.`:`Think back to “${title}”. Try these checks from memory first. Then reopen the lesson and improve anything you missed.`}</p>
  <ol className="checkpoint-route">
   <li><strong>Explain the idea</strong><p>{teacher?"Ask for an explanation in the learner’s own words. Listen for how the parts connect, rather than a copied definition.":"How does the main idea work? Explain it to someone who has not taken this lesson. Name the parts and how they connect."}</p></li>
   <li><strong>Trace an example</strong><p>{teacher?"Ask the learner to walk through one example step by step. Change one detail and ask which step or result would change, and why.":"Choose one lesson example. What happens first, next and last? Change one detail: which step or result might change, and why?"}</p></li>
   <li><strong>Find a limit</strong><p>{teacher?"Ask when the approach could fail or need more information. Look for a specific limitation and a useful check.":"When might this idea fail or need more information? Give a specific case and say what you would check before trusting the result."}</p></li>
  </ol>
  <details className="checkpoint-notes"><summary>{teacher?"Record observations and plan the next lesson":"Save your explanation and next step"}</summary>
   <div className="checkpoint-notes-body">
    <ResponseSpace storageKey={`${week}-checkpoint-explanation`} prompt={teacher?"Evidence: what did the learner explain, trace or question? Record the task and any hints or support used. Use a fictional learner code.":"My explanation: how does the idea work? Trace one example, then describe a limit and what you would check."}/>
    <ResponseSpace storageKey={`${week}-checkpoint-next-step`} prompt={teacher?"Next teaching step: which part needs another model, guided practice or a fresh independent case? What evidence will you look for?":"My next step: what is still unclear? Name one part to revisit, one question to ask, or one new example to try."}/>
   </div>
  </details>
  <div className="checkpoint-next"><strong>Choose what helps next</strong><ul>
   <li>{teacher?"If the explanation is incomplete, model the missing connection and ask the learner to explain a changed example.":"If you are unsure, reopen a worked example and explain each step aloud."}{workedExample&&<> <a href={`#section-${workedExample}`}>Revisit the worked example</a>.</>}</li>
   <li>{teacher?"If the learner succeeds with hints, remove one hint and try another example.":"If you needed hints, try a different example with one less hint."}</li>
   <li>{teacher?"If the learner can explain, trace and identify a limit, use the reserved independent case and the teacher assessment criteria.":"If you can explain all three, try the lesson’s independent case and ask your teacher for feedback."}</li>
  </ul></div>
  <p className="checkpoint-note">{teacher?"Keep the reserved assessment answer private. These observations guide teaching; they do not automatically establish mastery.":"This reflection is practice, not a grade. Save your reasoning and use feedback to decide what to practise next."}</p>
 </section>;
}
