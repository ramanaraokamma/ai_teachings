import youtubeLinks from "./youtube-videos.json";
import catalogue from "./lesson-videos.json";
export type VideoAsset = {key:string; bytes:number; sha256:string; mime:string; filename:string};
export type VideoChapter = {number:number; title:string; start:number; end:number; studentSections:number[]; workbookSections:number[]};
export type LessonVideo = {title:string; seconds:number; resolution:string; assets:Record<"video"|"captions"|"poster"|"transcript",VideoAsset>; chapters:VideoChapter[]};
export function getLessonVideo(level:string,week:string|number):LessonVideo|undefined {
 return (catalogue as Record<string,LessonVideo>)[`${level}/${week}`];
}

export function getYouTubeVideoID(level:string,week:string|number):string|undefined {
 return (youtubeLinks as Record<string,string>)[`${level}/${week}`] || undefined;
}
