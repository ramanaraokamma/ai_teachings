"use client";
export function VideoSectionLink({start}:{start:number}){
 return <a className="section-video-link" href="#week-video" onClick={()=>document.dispatchEvent(new CustomEvent('academy-video-seek',{detail:start}))}>Watch this section in the video</a>;
}
