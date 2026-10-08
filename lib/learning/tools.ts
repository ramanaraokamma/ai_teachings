export type PracticeQuestion={id:string;prompt:string;hint:string;choices:{text:string;correct:boolean;feedback:string}[]};
export type Repair={week:string;title:string;goal:string;task:string;section:number};
export type LearningTools={scenario:string;questions:PracticeQuestion[];repairs:Repair[];labs:{title:string;code:string}[];limits:string};
