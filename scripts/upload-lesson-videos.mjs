/** Upload prepared objects to R2 only with --execute. Credentials stay in Wrangler's login/environment. */
import {readFile,stat,writeFile,mkdir} from 'node:fs/promises';
import {createReadStream} from 'node:fs';
import {createHash} from 'node:crypto';
import {resolve,relative,sep,dirname} from 'node:path';
import {spawn} from 'node:child_process';
const args=process.argv.slice(2),value=(flag,fallback)=>{const i=args.indexOf(flag);return i<0?fallback:args[i+1];};
const root=resolve(value('--root','.')),planFile=resolve(value('--plan','outputs/video-publishing/upload-plan.json')),bucket=value('--bucket','ai-teachings-videos'),execute=args.includes('--execute');
if(!/^[a-z0-9][a-z0-9-]{1,61}[a-z0-9]$/.test(bucket))throw Error('Invalid R2 bucket name');
const plan=JSON.parse(await readFile(planFile,'utf8')),wrangler=resolve('node_modules/.bin/wrangler');
const stateFile=resolve('outputs/video-publishing',`uploaded-${bucket}.json`);let completed={};try{completed=JSON.parse(await readFile(stateFile,'utf8'));}catch(e){if(e.code!=='ENOENT')throw e;}
const hash=async file=>{const h=createHash('sha256');for await(const chunk of createReadStream(file))h.update(chunk);return h.digest('hex');};
let bytes=0,pending=0;
for(const object of plan.objects){
 const source=resolve(root,object.source),rel=relative(root,source);
 if(rel.startsWith('..'+sep)||rel==='..')throw Error('Source outside selected root');
 if((await stat(source)).size!==object.bytes)throw Error(`Wrong file size: ${source}. If this is an LFS archive, run git lfs pull first.`);
 bytes+=object.bytes;
 if(completed[object.key]===object.sha256)continue;
 pending++;
 if(!execute)continue;
 if(await hash(source)!==object.sha256)throw Error(`Checksum mismatch: ${source}`);
 console.log(`Uploading ${pending}: ${object.key}`);
 await new Promise((res,rej)=>{const child=spawn(wrangler,['r2','object','put',`${bucket}/${object.key}`,'--file',source,'--content-type',object.mime,'--cache-control','private, no-store','--remote'],{stdio:'inherit'});child.on('error',rej);child.on('exit',code=>code===0?res():rej(Error(`Wrangler exited ${code}`)));});
 completed[object.key]=object.sha256;await mkdir(dirname(stateFile),{recursive:true});await writeFile(stateFile+'.tmp',JSON.stringify(completed,null,2)+'\n');const {rename}=await import('node:fs/promises');await rename(stateFile+'.tmp',stateFile);
}
console.log(`${execute?'Upload finished':'DRY RUN — nothing uploaded'}: ${plan.videos} videos, ${plan.objects.length} objects, ${(bytes/1024**3).toFixed(2)} GiB; ${pending} ${execute?'uploaded':'pending'}.`);
if(!execute)console.log('Add --execute after creating the private R2 bucket and authenticating Wrangler. No video files are copied into public/ or dist/.');
