"use client";
import {useEffect,useRef} from "react";
import {loadYouTubeAPI,youtubeEmbedURL,type YouTubeController} from "@/lib/youtube-player";
type Props={id:string;title:string;startAt:number;onReady(player:YouTubeController):void;onError():void};
export function YouTubeLessonPlayer({id,title,startAt,onReady,onError}:Props){
 const host=useRef<HTMLDivElement>(null);
 useEffect(()=>{
  let cancelled=false,controller:YouTubeController|undefined;
  // React owns the host; YouTube owns its children, including teardown.
  const frame=document.createElement('iframe');frame.src=youtubeEmbedURL(id,window.location.origin,startAt);frame.title=title;frame.allow='autoplay; encrypted-media; picture-in-picture; fullscreen';frame.allowFullscreen=true;frame.referrerPolicy='strict-origin-when-cross-origin';frame.className='week-youtube-frame';
  host.current?.appendChild(frame);
  loadYouTubeAPI().then(api=>{if(cancelled)return;controller=new api.Player(frame,{events:{onReady:event=>{if(!cancelled)onReady(event.target);},onError:()=>{if(!cancelled)onError();}}});}).catch(()=>{if(!cancelled)onError();});
  return()=>{cancelled=true;controller?.destroy();frame.remove();};
 },[id]);
 return <div className="week-youtube-player" ref={host}/>;
}
