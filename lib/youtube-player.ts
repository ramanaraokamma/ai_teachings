export type YouTubeController={seekTo(seconds:number,allowSeekAhead:boolean):void;playVideo():void;destroy():void};
type PlayerOptions={events:{onReady(event:{target:YouTubeController}):void;onError():void}};
type YouTubeAPI={Player:new(element:HTMLIFrameElement,options:PlayerOptions)=>YouTubeController};
type YouTubeWindow=Window&{YT?:YouTubeAPI;onYouTubeIframeAPIReady?:()=>void};
let pending:Promise<YouTubeAPI>|null=null;
export function loadYouTubeAPI():Promise<YouTubeAPI>{
 const w=window as YouTubeWindow;
 if(w.YT?.Player)return Promise.resolve(w.YT);
 if(pending)return pending;
 pending=new Promise((resolve,reject)=>{
  const script=document.createElement('script');script.src='https://www.youtube.com/iframe_api';script.async=true;
  const previous=w.onYouTubeIframeAPIReady;
  const fail=()=>{clearTimeout(timer);script.remove();if(w.onYouTubeIframeAPIReady===ready)w.onYouTubeIframeAPIReady=previous;pending=null;reject(new Error('YouTube player could not load'));};
  const ready=()=>{try{previous?.();}finally{if(w.YT?.Player){clearTimeout(timer);resolve(w.YT);}}};
  const timer=setTimeout(fail,20000);w.onYouTubeIframeAPIReady=ready;script.onerror=fail;document.head.appendChild(script);
 });
 return pending;
}
export function youtubeEmbedURL(id:string,origin:string,start=0){
 if(!/^[A-Za-z0-9_-]{11}$/.test(id))throw new Error('Invalid YouTube video ID');
 const url=new URL(`https://www.youtube-nocookie.com/embed/${id}`);
 for(const [key,value] of Object.entries({enablejsapi:'1',origin,playsinline:'1',rel:'0',cc_lang_pref:'en',start:String(Math.max(0,Math.floor(start)))}))url.searchParams.set(key,value);
 return url.toString();
}
