"use client";

export function CurvePlot({series,xValues,xLabel,axis,max}:{series:{label:string;values:number[]}[];xValues?:number[];xLabel?:string;axis?:string;max?:number}) {
 const xs=xValues || series[0]?.values.map((_,i)=>i) || [];const ys=series.flatMap(s=>s.values);if(!xs.length||!ys.length)return null;
 const minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(0,...ys),maxY=Math.max(max||0,...ys);
 const px=(x:number)=>65+(x-minX)/(maxX-minX||1)*600;const py=(y:number)=>290-(y-minY)/(maxY-minY||1)*240;
 const colors=['#12648a','#a33e10','#6844a5','#267641'];
 return <svg className="curve-plot" viewBox="0 0 720 360" role="img" aria-label={`${axis||"Value"} by ${xLabel||"checkpoint"}. Exact values follow in the table.`}><title>{`${axis || "Value"} by ${xLabel || "checkpoint"}`}</title><path d="M65 45 V290 H665" fill="none" stroke="#425b70" strokeWidth="2"/>{[minY,maxY].map((v,i)=><text key={i} x="55" y={py(v)+5} textAnchor="end" fontSize="13">{v}</text>)}{xs.map((v,i)=><text key={i} x={px(v)} y="310" textAnchor="middle" fontSize="12">{v}</text>)}{series.map((s,i)=><g key={s.label}><polyline points={s.values.map((v,j)=>`${px(xs[j]??j)},${py(v)}`).join(' ')} fill="none" stroke={colors[i%4]} strokeWidth="3" strokeDasharray={i%2?'7 4':undefined}/>{s.values.map((v,j)=>(i%2 ? <rect key={j} x={px(xs[j]??j)-4} y={py(v)-4} width="8" height="8" fill={colors[i%4]}/> : <circle key={j} cx={px(xs[j]??j)} cy={py(v)} r="4" fill={colors[i%4]}/>))}<text x={80+i*210} y="25" fill={colors[i%4]} fontSize="13">{s.label}</text></g>)}<text x="360" y="343" textAnchor="middle" fontSize="14">{xLabel}</text><text x="18" y="180" transform="rotate(-90 18 180)" textAnchor="middle" fontSize="14">{axis}</text></svg>;
}
