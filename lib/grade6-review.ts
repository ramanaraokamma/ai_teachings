import 'server-only';
import data from './grade6-review.json';
export type Grade6Review={id:string;recall:string;task:string;hint:string;solution:string};
export function grade6Review(level:string,week:number):Grade6Review{
 const result=(data as Record<string,Grade6Review>)[`${level}/${week}`];
 if(!result)throw new Error(`Missing Grade 6 review: ${level}/${week}`);
 return result;
}
