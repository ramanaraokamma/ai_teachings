import fs from 'node:fs';
import path from 'node:path';
import {createHash,createCipheriv,randomBytes} from 'node:crypto';
const source=process.argv.includes('--root')?'.':(process.argv.slice(2).find(arg=>!arg.startsWith('--'))||'outputs/ai-academy-complete-programme');
if(!fs.existsSync(path.join(source,'content/programme.json')))throw Error('Complete programme source missing');
// Keep the complete offline edition at repository root, outside public assets.
if(!process.argv.includes('--root'))for(const item of fs.readdirSync(source)){
 if(['README.md','CLOUDFLARE_DEPLOYMENT.md'].includes(item))continue;
 fs.cpSync(path.join(source,item),item,{recursive:true});
}
const programme=JSON.parse(fs.readFileSync('content/programme.json'));
const key=Buffer.from(fs.readFileSync('lib/resource-key.ts','utf8').match(/resourceKey = "([^"]+)"/)[1],'base64');
const manifest={}; const blobs='public/curriculum-blobs';
fs.mkdirSync(blobs,{recursive:true});
function resource(file,role='student',download=false){
 const bytes=fs.readFileSync(file),ext=path.extname(file);
 const id=createHash('sha256').update(role+'\0'+file+'\0').update(bytes).digest('hex');
 if(!manifest[id]){if(!fs.existsSync(`${blobs}/${id}.bin`)){const iv=randomBytes(12),cipher=createCipheriv('aes-256-gcm',key,iv);cipher.setAAD(Buffer.from(id));fs.writeFileSync(`${blobs}/${id}.bin`,Buffer.concat([iv,cipher.update(bytes),cipher.final(),cipher.getAuthTag()]));}
 manifest[id]={mime:ext==='.png'?'image/png':ext==='.svg'?'image/svg+xml':ext==='.pdf'?'application/pdf':'application/vnd.openxmlformats-officedocument.wordprocessingml.document',role,filename:download?path.basename(file):null};}
 return `/api/resource/${id}`;
}
function blocks(items){return items.map(b=>{
 if(b.type==='image')return {...b,src:resource(`assets/${b.src.split('/').pop()}.png`),height:b.height||600};
 if(b.type==='gallery')return {...b,cells:b.cells.map(blocks)};
 if(b.type==='response')return {...b,text:b.label||b.text||'Explain your thinking.'};
 if(b.type==='callout')return {...b,tone:b.tone||'idea'};
 if(b.type==='diagram')return b;
 if(b.type==='sensor')return b;
 return b;
});}
const pages=sections=>sections.map((s,i)=>({number:i+1,label:s.title,blocks:blocks(s.blocks)}));
function week(w){const stem=w.id.startsWith('python-bridge')?`bridge-week-${String(w.week).padStart(2,'0')}`:`ai-${w.level}-week-${String(w.week).padStart(2,'0')}`;
 const result={number:w.week,phase:Math.ceil(w.week/6),hero:resource(`assets/academy-visual-${w.id.replace('/','-')}.png`)};
 for(const role of ['student','teacher','workbook']){result[role]={title:`Week ${w.week}: ${w.title}`,download:resource(`downloads/${role}/${stem}.docx`,role==='teacher'?'teacher':'student',true),pdf:resource(`downloads/${role}/${stem}.pdf`,role==='teacher'?'teacher':'student',true)};
 if(role==='workbook')result[role].blocks=w.workbook.flatMap(s=>[{type:'heading',text:s.title},...blocks(s.blocks)]);
 else result[role].pages=pages(role==='student'?w.sections:w.teacher);}
 return result;
}
const phases=['Discover','Practice','Investigate','Evaluate','Design','Capstone'];
const levels=programme.levels.map(l=>({slug:`ai-${l.number}`,code:`AI-${l.number}`,name:l.name,ages:`Grade ${l.grade}`,accent:['sky','violet','amber','emerald'][(l.number-1)%4],summary:l.prerequisites,capstone:l.project,focus:['Explain','Build','Test responsibly'],phases:phases.map((name,i)=>({number:i+1,name,weeks:`${i*6+1}–${i*6+6}`})),weeks:programme.weeks.filter(w=>w.level===l.number).map(week)}));
levels.splice(3,0,{slug:'python-bridge',code:'Python',name:'Python Readiness Bridge',ages:'12 preparation lessons',accent:'sky',summary:'After Level 3, prepare for Level 4 Machine Learning. Skip only when you can independently demonstrate the Python readiness skills.',capstone:'Explain, trace and test Python code',focus:['Trace','Debug','Test'],phases:phases.slice(0,2).map((name,i)=>({number:i+1,name,weeks:`${i*6+1}–${i*6+6}`})),weeks:programme.python_bridge.map(week)});
for(const file of fs.readdirSync(blobs))if(file.endsWith('.bin')&&!manifest[file.slice(0,-4)])fs.unlinkSync(path.join(blobs,file));
fs.writeFileSync('lib/academy-data.json',JSON.stringify({version:'complete-programme-2026-10-07',levels}));fs.writeFileSync('lib/resource-manifest.json',JSON.stringify(manifest));
console.log(`Imported ${levels.reduce((n,l)=>n+l.weeks.length,0)} lessons; ${Object.keys(manifest).length} encrypted resources.`);
