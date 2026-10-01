const fs=require('node:fs');const path=require('node:path');
const sharp=require(process.env.ACADEMY_NODE_PACKAGES+'/sharp');
const dir=path.resolve(process.argv[2]||'work/v3-diagrams');fs.mkdirSync(dir,{recursive:true});
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&apos;'}[c]));
const wrap=(s,n)=>{const lines=[];let line='';for(const w of s.split(' ')){if((line+' '+w).trim().length>n&&line){lines.push(line);line=w;}else line=(line+' '+w).trim();}if(line)lines.push(line);return lines;};
function text(s,x,y,n=25,size=22){return wrap(s,n).map((l,i)=>`<text x="${x}" y="${y+i*(size+7)}" font-size="${size}">${esc(l)}</text>`).join('');}
function render(d){
 let body='',height=500;
 if(d.kind==='lanes'){
  const rowHeights=d.rows.map(r=>Math.max(...r.map(c=>wrap(c,25).length))*29+35);height=80+rowHeights.reduce((n,h)=>n+h+18,0);
  d.columns.forEach((c,i)=>{body+=text(c,18+i*320,34,26,21);});let y=62;
  d.rows.forEach((row,r)=>{const h=rowHeights[r];row.forEach((c,i)=>{const x=8+i*320;body+=`<rect x="${x}" y="${y}" width="294" height="${h}" rx="8" fill="${i===1?'#e7f0fa':'#fff'}" stroke="#536c83"/>`+text(c,x+14,y+31);if(i<2)body+=`<path d="M${x+299} ${y+h/2} h16 m-6 -6 l6 6 -6 6" fill="none" stroke="#17324f" stroke-width="2"/>`;});y+=h+18;});
 }else if(d.kind==='grid'){
  const cell=72;const rows=d.values.length,cols=d.values[0].length;height=Math.max(380,rows*cell+130);
  d.values.forEach((row,r)=>row.forEach((v,c)=>{body+=`<rect x="${40+c*cell}" y="${55+r*cell}" width="${cell}" height="${cell}" fill="${v?'#17324f':'#fff'}" stroke="#536c83"/><text x="${76+c*cell}" y="${98+r*cell}" text-anchor="middle" fill="${v?'#fff':'#17324f'}" font-size="26">${v}</text>`;}));
  d.values.forEach((row,r)=>{body+=text(`Row ${r+1}: [${row.join(', ')}]`,cols*cell+90,86+r*58,38,22);});body+=text(d.key||'0 is white and 1 is black',40,rows*cell+98,60,21);
 }else if(d.kind==='bars'){
  height=90+d.items.length*95;body+=text(d.axis,20,30,70,22);
  d.items.forEach(([label,value],i)=>{const y=68+i*95;body+=text(label,20,y,21,20);body+=`<rect x="270" y="${y-25}" width="600" height="35" fill="#edf1f5"/><rect x="270" y="${y-25}" width="${600*value/d.max}" height="35" fill="#315f87"/><text x="885" y="${y+1}" font-size="22">${value}</text>`;});body+=text(`Shared scale from 0 to ${d.max}`,270,height-15,55,20);
 }else if(d.kind==='curves'){
  height=420;
  const left=100,right=875,top=85,bottom=335;
  const xs=d.xValues;
  if(xs.length<2||d.max<=0||d.series.some(s=>s.values.length!==xs.length||s.values.some(v=>!Number.isFinite(v)||v<0||v>d.max)))throw new Error('Invalid curve data');
  const px=i=>left+i*(right-left)/(xs.length-1),py=v=>bottom-v*(bottom-top)/d.max;
  body+=text(d.axis,left,28,55,22);
  for(let i=0;i<=4;i++){
   const v=d.max*i/4,y=py(v);
   body+=`<path d="M${left} ${y} H${right}" stroke="#d4dde5"/><text x="${left-15}" y="${y+7}" text-anchor="end" font-size="20">${v}</text>`;
  }
  body+=`<path d="M${left} ${top} V${bottom} H${right}" fill="none" stroke="#17324f" stroke-width="2"/>`;
  xs.forEach((x,i)=>{body+=`<text x="${px(i)}" y="${bottom+30}" text-anchor="middle" font-size="21">${esc(x)}</text>`;});
  body+=text(d.xLabel,360,405,40,22);
  d.series.forEach((s,j)=>{
   const color=j===0?'#17324f':'#a44818';
   body+=`<path d="${s.values.map((v,i)=>`${i?'L':'M'}${px(i)} ${py(v)}`).join(' ')}" fill="none" stroke="${color}" stroke-width="4" ${j?'stroke-dasharray="10 6"':''}/>`;
   s.values.forEach((v,i)=>{body+=j?`<rect x="${px(i)-5}" y="${py(v)-5}" width="10" height="10" fill="${color}"/>`:`<circle cx="${px(i)}" cy="${py(v)}" r="5" fill="${color}"/>`;});
   const lx=left+j*385;
   body+=`<path d="M${lx} 55 h40" stroke="${color}" stroke-width="4" ${j?'stroke-dasharray="10 6"':''}/>`+text(s.label,lx+50,62,30,21);
  });
 }else throw new Error('Unknown diagram '+d.kind);
 return `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="${height}" viewBox="0 0 960 ${height}" role="img" aria-label="${esc(d.title)}"><rect width="960" height="${height}" fill="white"/><g font-family="Arial,sans-serif" fill="#17324f">${body}</g></svg>`;
}
(async()=>{for(const name of fs.readdirSync('curriculum-v3').filter(n=>/^ai-.*\.json$/.test(n))){const w=JSON.parse(fs.readFileSync('curriculum-v3/'+name));let index=0;for(const s of w.lesson)for(const b of s.blocks)if(b.type==='diagram'){const stem=`${w.level}-week-${String(w.week).padStart(2,'0')}-diagram-${++index}`;const svg=render(b);fs.writeFileSync(path.join(dir,stem+'.svg'),svg);await sharp(Buffer.from(svg),{density:160}).png().toFile(path.join(dir,stem+'.png'));}}})().catch(e=>{console.error(e);process.exit(1)});
