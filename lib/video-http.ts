// R2 streams go straight to the response. Never buffer whole videos in Worker memory.
export type MediaAsset = {key:string; bytes:number; mime:string; filename:string};
export type VideoObject = {size:number; httpEtag:string; uploaded:Date; body:ReadableStream<Uint8Array>};
export type VideoBucket = {
 head(key:string):Promise<Omit<VideoObject,"body">|null>;
 get(key:string,options?:{range?:{offset:number;length:number}}):Promise<VideoObject|null>;
};
const privateHeaders={"Cache-Control":"private, no-store","Vary":"Cookie","X-Content-Type-Options":"nosniff"};
export function mediaError(message:string,status:number,extra:Record<string,string>={}) {return new Response(message,{status,headers:{...privateHeaders,...extra}});}
export function parseByteRange(value:string,size:number):{offset:number;length:number}|null {
 const match=/^bytes=(\d*)-(\d*)$/.exec(value);
 if(!match||(!match[1]&&!match[2])||size===0)return null;
 if(!match[1]){const suffix=Number(match[2]);if(!Number.isSafeInteger(suffix)||suffix<=0)return null;const length=Math.min(suffix,size);return {offset:size-length,length};}
 const start=Number(match[1]),end=match[2]?Math.min(Number(match[2]),size-1):size-1;
 if(!Number.isSafeInteger(start)||!Number.isSafeInteger(end)||start>=size||end<start)return null;
 return {offset:start,length:end-start+1};
}
export async function serveVideoAsset(request:Request,bucket:VideoBucket|undefined,asset:MediaAsset):Promise<Response>{
 if(!bucket)return mediaError("Video playback is not available yet.",503);
 const info=await bucket.head(asset.key);
 if(!info)return mediaError("Video resource is not available yet.",404);
 if(info.size!==asset.bytes)return mediaError("Video resource could not be verified.",503);
 const headers=new Headers({...privateHeaders,"Content-Type":asset.mime,"Accept-Ranges":"bytes","ETag":info.httpEtag,"Last-Modified":info.uploaded.toUTCString(),"Content-Disposition":`${asset.mime.startsWith('text/plain')?'attachment':'inline'}; filename="${asset.filename.replace(/[^a-zA-Z0-9_.-]/g,'_')}"`});
 if(request.headers.get('If-None-Match')?.split(',').map(x=>x.trim()).some(x=>x==='*'||x===info.httpEtag))return new Response(null,{status:304,headers});
 // HTTP Range applies to GET; HEAD reports full-object metadata without retrieving a body.
 let range:ReturnType<typeof parseByteRange>|undefined;
 let rawRange=request.method==='GET'?request.headers.get('Range'):null;
 const ifRange=request.headers.get('If-Range');
 if(rawRange&&ifRange){const date=Date.parse(ifRange);if(ifRange!==info.httpEtag&&(!Number.isFinite(date)||Math.floor(info.uploaded.getTime()/1000)>Math.floor(date/1000)))rawRange=null;}
 if(rawRange){range=parseByteRange(rawRange,info.size);if(!range)return mediaError('Requested range is not available.',416,{'Content-Range':`bytes */${info.size}`});}
 headers.set('Content-Length',String(range?range.length:info.size));
 if(range)headers.set('Content-Range',`bytes ${range.offset}-${range.offset+range.length-1}/${info.size}`);
 if(request.method==='HEAD')return new Response(null,{status:200,headers});
 const object=await bucket.get(asset.key,range?{range}:undefined);
 if(!object)return mediaError('Video resource is not available yet.',404);
 return new Response(object.body,{status:range?206:200,headers});
}
