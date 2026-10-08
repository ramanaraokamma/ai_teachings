import type { LessonRoute as Route } from "@/lib/classroom";
export function LessonRoute({ route }: {route:Route}) {
 return <section className="classroom-panel" aria-label="Your lesson route"><h2>Your lesson route</h2><p>Read, explain, practise and apply. Your teacher can spread this week across several classes.</p><ol className="lesson-route">{route.flow.map((step)=><li key={step.title}><a href={`#section-${step.section}`}><strong>{step.title}</strong><span>{step.task}</span></a></li>)}</ol><details><summary>What I will be able to explain</summary><ul>{route.goals.map(g=><li key={g}>{g}</li>)}</ul></details><p><strong>Project milestone: {route.milestone.title}.</strong> {route.milestone.task}</p></section>;
}
