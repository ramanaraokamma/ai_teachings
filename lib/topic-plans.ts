import 'server-only';
import data from './topic-plans.json';
export type TopicPlan={id:string;kind:string;title:string;items:{label:string;value:string}[];teach:string;misconception:string;lesson:string;scenario:string;question:string;explanation:string};
export function topicPlan(level:string,week:number):TopicPlan {
 const plan=(data as Record<string,TopicPlan>)[`${level}/${week}`];
 if(!plan)throw new Error(`Missing visual teaching plan: ${level}/${week}`);
 return plan;
}
