"use client";
import {useEffect,useRef,useState} from "react";
import type {VideoChapter} from "@/lib/lesson-videos";
import {YouTubeLessonPlayer} from "@/components/youtube-lesson-player";
import type {YouTubeController} from "@/lib/youtube-player";
import {lessonVideoPath} from "@/lib/lesson-video-url";
type Props={level:string;week:number;title:string;seconds:number;bytes:number;chapters:VideoChapter[];teacher:boolean;resource:"lesson"|"guide";configured:boolean;youtubeId?:string};
function timestamp(seconds:number){return `${Math.floor(seconds/60)}:${String(Math.floor(seconds%60)).padStart(2,'0')}`;}
export function LessonVideoPlayer({level,week,title,seconds,bytes,chapters,teacher,resource,configured,youtubeId}:Props){
 const [loaded,setLoaded]=useState(false),[failed,setFailed]=useState(false);const player=useRef<HTMLVideoElement>(null);const pending=useRef<number|null>(null);const youtube=useRef<YouTubeController|null>(null);
 function revealSection(hash:string){
  if(!/^#section-\d+$/.test(hash))return;
  const section=document.getElementById(hash.slice(1));if(!section)return;
  for(let node:HTMLElement|null=section;node;node=node.parentElement)if(node instanceof HTMLDetailsElement)node.open=true;
  section.scrollIntoView({behavior:'smooth',block:'start'});
 }
 useEffect(()=>{const reveal=()=>revealSection(window.location.hash);const seek=(event:Event)=>{const time=(event as CustomEvent).detail;if(configured&&typeof time==='number'&&Number.isFinite(time)&&time>=0&&time<seconds)jump(time);};reveal();window.addEventListener('hashchange',reveal);document.addEventListener('academy-video-seek',seek);return()=>{window.removeEventListener('hashchange',reveal);document.removeEventListener('academy-video-seek',seek);};},[]);
 const base=(asset:string)=>lessonVideoPath(level,week,asset);
 function jump(time:number){pending.current=time;setFailed(false);setLoaded(true);if(youtubeId&&youtube.current){youtube.current.seekTo(time,true);youtube.current.playVideo();pending.current=null;}else if(player.current&&player.current.readyState>=1){player.current.currentTime=time;pending.current=null;player.current.play().catch(()=>{});}if(youtubeId)document.getElementById('week-video')?.scrollIntoView({behavior:'smooth',block:'start'});else player.current?.scrollIntoView({behavior:'smooth',block:'center'});}
 return <section className="classroom-panel week-video" id="week-video" aria-labelledby="week-video-title">
  <p className="week-video-eyebrow">Watch · pause · explain</p><h2 id="week-video-title">Watch this week’s lesson</h2>
  <p>{teacher?"Use this student-facing video to model the concept, pause for discussion and guide practice. The reserved assessment answer is kept separate.":"Follow one connected explanation, then pause to predict, write, draw and try the activities yourself."}</p>
  <p className="week-video-meta">{title} · {Math.ceil(seconds/60)} minutes{youtubeId?" · YouTube":configured?` · 1080p · ${Math.round(bytes/1024/1024)} MiB for the full video`:""}</p>
  {!configured?<p className="week-video-notice">The video for this week is coming soon. You can follow the complete written lesson below.</p>:<>
   {!loaded?<div className="week-video-start"><button type="button" onClick={()=>{setLoaded(true);setFailed(false);}}>Load this week’s video</button><p>The video loads only when you choose it. You can use captions and pause whenever you need more time.</p></div>:<>
    {youtubeId?<YouTubeLessonPlayer id={youtubeId} title={`${level.toUpperCase()} Week ${week}: ${title}`} startAt={pending.current??0} onReady={controller=>{youtube.current=controller;if(pending.current!==null){controller.seekTo(pending.current,true);controller.playVideo();pending.current=null;}}} onError={()=>setFailed(true)}/>:<video ref={player} controls playsInline preload="metadata" poster={base('poster')} src={base('video')} aria-label={`${level.toUpperCase()} Week ${week}: ${title}`} onLoadedMetadata={()=>{if(pending.current!==null&&player.current){player.current.currentTime=pending.current;pending.current=null;player.current.play().catch(()=>{});}}} onError={()=>setFailed(true)}>
     <track kind="captions" src={base('captions')} srcLang="en" label="English"/>
    </video>}
    {failed&&<p role="status">The video could not load. {youtubeId?<a href={`https://www.youtube.com/watch?v=${youtubeId}`} target="_blank" rel="noopener noreferrer">Open it on YouTube</a>:<button type="button" onClick={()=>{setFailed(false);player.current?.load();}}>Try again</button>}. You can continue with the written lesson below.</p>}
   </>}
   <details className="week-video-chapters"><summary>Choose a chapter or return to a written section</summary><ol>{chapters.map(c=><li key={c.number}><button type="button" onClick={()=>jump(c.start)}><span>{timestamp(c.start)}</span> {c.title.replace(/^\d+\s*·\s*/,'')}</button>{c.studentSections.length>0&&<a href={`${resource==='guide'?'?resource=lesson':''}#section-${c.studentSections[0]}`} onClick={()=>{if(resource==="lesson")revealSection(`#section-${c.studentSections[0]}`);}}>Read the matching section</a>}</li>)}</ol></details>
   {youtubeId?<p className="week-video-downloads"><a href={`https://www.youtube.com/watch?v=${youtubeId}`} target="_blank" rel="noopener noreferrer">Watch on YouTube</a></p>:<p className="week-video-downloads"><a href={base('transcript')}>Download transcript</a><a href={base('video')} download={`${level}-week-${week}.mp4`}>Download video ({Math.round(bytes/1024/1024)} MiB)</a></p>}
  </>}
  <p className="week-video-note">Synthetic teacher and learner voices. Keep your first independent attempt before feedback; watching the video alone does not demonstrate mastery.</p>
 </section>;
}
