// Keep curriculum text out of Worker JavaScript; only the navigation index is bundled.
import {readFile,writeFile,mkdir,readdir,unlink} from 'node:fs/promises';
import {createHash,createCipheriv,randomBytes} from 'node:crypto';
const root=new URL('../',import.meta.url);
const data=JSON.parse(await readFile(new URL('lib/academy-data.json',root),'utf8'));
const keySource=await readFile(new URL('lib/resource-key.ts',root),'utf8');
const key=Buffer.from(keySource.match(/resourceKey\s*=\s*"([^"]+)"/)[1],'base64');
const dir=new URL('public/lesson-blobs/',root);await mkdir(dir,{recursive:true});
const used=new Set();
for(const level of data.levels)for(let i=0;i<level.weeks.length;i++){
 const week=level.weeks[i];const bytes=Buffer.from(JSON.stringify(week));
 const id=createHash('sha256').update(bytes).digest('hex');const filename=`${id}.bin`;used.add(filename);
 let existing;try{existing=await readFile(new URL(filename,dir));}catch{}
 if(!existing){const iv=randomBytes(12);const cipher=createCipheriv('aes-256-gcm',key,iv);cipher.setAAD(Buffer.from(id));await writeFile(new URL(filename,dir),Buffer.concat([iv,cipher.update(bytes),cipher.final(),cipher.getAuthTag()]));}
 const summary={...week,contentId:id};
 for(const role of ['student','teacher','workbook'])summary[role]={...week[role],pages:[],...(role==='workbook'?{blocks:[]}: {})};
 level.weeks[i]=summary;
}
for(const file of await readdir(dir))if(file.endsWith('.bin')&&!used.has(file))await unlink(new URL(file,dir));
await writeFile(new URL('lib/academy-index.json',root),JSON.stringify(data));
console.log(`Prepared ${used.size} encrypted weekly lesson assets and lightweight navigation index.`);
