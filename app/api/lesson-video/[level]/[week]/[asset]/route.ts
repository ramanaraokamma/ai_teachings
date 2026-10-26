import {env} from "cloudflare:workers";
import {readSession} from "@/lib/access";
import {getLessonVideo,type LessonVideo} from "@/lib/lesson-videos";
import {serveVideoAsset,mediaError,type VideoBucket} from "@/lib/video-http";
export const dynamic="force-dynamic";
type Context={params:Promise<{level:string;week:string;asset:string}>};
async function serve(request:Request,{params}:Context){
 // The existing signed student/teacher session protects every video, caption and poster.
 if(!await readSession())return mediaError('Sign in to view this lesson video.',401);
 const {level,week,asset}=await params;
 if(!/^(ai-1|ai-2)$/.test(level)||!/^([1-9]|[12]\d|3[0-6])$/.test(week))return mediaError('Video unavailable.',404);
 const video=getLessonVideo(level,week);
 if(!video||!Object.hasOwn(video.assets,asset))return mediaError('Video unavailable.',404);
 const bucket=(env as unknown as {LESSON_VIDEOS?:VideoBucket}).LESSON_VIDEOS;
 try{return await serveVideoAsset(request,bucket,video.assets[asset as keyof LessonVideo['assets']]);}
 catch{return mediaError('Video playback is temporarily unavailable.',503);}
}
export const GET=serve;
export const HEAD=serve;
