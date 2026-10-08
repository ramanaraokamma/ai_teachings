import data from "./classroom-data.json";
export type LessonRoute = {goals:string[]; flow:{title:string;section:number;task:string}[];visual_question:string;project:string;milestone:{title:string;task:string}};
export const classroom = data as {sequence:string[];levels:Record<string,{prerequisites:string;outcome:string;project:string}>;weeks:Record<string,LessonRoute>};
