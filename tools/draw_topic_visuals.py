"""Draw actual matrices, plots and weighted models from reviewed lesson values."""
from pathlib import Path
import json,math,html
import fitz
from draw_lesson_visuals import R,text,wrap,COLORS

def draw(a):
 v=a.get('mini_visual')
 if not v:return None
 out=[];w=1120;kind=v['kind']
 text(out,['AI ACADEMY  /  '+a['week'].upper()],52,54,22,'#356b7b',True)
 titlelines=wrap(v['title'],1016,38);y=text(out,titlelines,52,106,38,'#123c55',True)+35
 if kind=='bars':
  labels=v['labels'];values=v['values'];lo=min([0]+values);hi=max([0]+values);span=hi-lo or 1;x0=330;plotw=680
  unit=wrap(v.get('unit','Supplied toy values'),1016,26);y=text(out,unit,52,y,26)+22
  for label,value in zip(labels,values):
   label_lines=wrap(label,240,27);text(out,label_lines,52,y+30,27)
   zero=x0+(-lo/span)*plotw;end=x0+((value-lo)/span)*plotw
   out.append(f'<rect x="{min(zero,end)}" y="{y}" width="{max(abs(end-zero),3)}" height="50" rx="7" fill="#238a91"/>')
   out.append(f'<line x1="{zero}" y1="{y-8}" x2="{zero}" y2="{y+58}" stroke="#183249" stroke-width="2"/>')
   text(out,[str(value)],min(1015,end+12) if value>=0 else end-80,y+34,28,'#183249',True);y+=max(100,30+len(label_lines)*37)
  text(out,['Bar length shows the supplied value; the marked baseline is zero.'],52,y,25);y+=60
 elif kind=='grid':
  rows=v['cells'];labels=v.get('row_labels',[str(i+1) for i in range(len(rows))]);cols=v.get('column_labels',[str(i+1) for i in range(len(rows[0]))]);cw=760/len(cols);x0=290
  for j,label in enumerate(cols):text(out,wrap(label,cw-15,25),x0+j*cw+10,y,25,'#146b77',True)
  y+=90
  for i,row in enumerate(rows):
   text(out,wrap(labels[i],225,25),52,y+45,25,'#183249',True)
   for j,value in enumerate(row):
    fill='#e1eff4' if (i+j)%2 else '#c9e4e8';out.append(f'<rect x="{x0+j*cw}" y="{y}" width="{cw-5}" height="105" rx="8" fill="{fill}" stroke="#7ca9b8"/>')
    text(out,wrap(str(value),cw-25,31),x0+j*cw+16,y+59,31,'#183249',True)
   y+=118
  text(out,['Read a cell using both its row and column labels.'],52,y+25,25);y+=80
 elif kind=='scatter':
  points=v['points'];q=v.get('query');allpoints=points+([q] if q else []);xmin=min(p['x'] for p in allpoints)-1;xmax=max(p['x'] for p in allpoints)+1;ymin=min(p['y'] for p in allpoints)-1;ymax=max(p['y'] for p in allpoints)+1
  left=125;top=y+25;pw=830;ph=480
  scale=min(pw/(xmax-xmin),ph/(ymax-ymin));actualw=(xmax-xmin)*scale;actualh=(ymax-ymin)*scale;left+=(pw-actualw)/2;top+=(ph-actualh)/2;pw=actualw;ph=actualh
  X=lambda x:left+(x-xmin)*scale;Y=lambda value:top+ph-(value-ymin)*scale
  for i in range(6):
   xx=left+pw*i/5;yy=top+ph*i/5
   out.append(f'<path d="M{xx} {top} V{top+ph} M{left} {yy} H{left+pw}" stroke="#d0e0e8" stroke-width="1"/>')
   text(out,[f'{xmin+(xmax-xmin)*i/5:g}'],xx-20,top+ph+40,22);text(out,[f'{ymax-(ymax-ymin)*i/5:g}'],left-65,yy+8,22)
  out.append(f'<path d="M{left} {top} V{top+ph} H{left+pw}" fill="none" stroke="#42687b" stroke-width="3"/>')
  for i,p in enumerate(points):
   color=COLORS[i%len(COLORS)];out.append(f'<circle cx="{X(p["x"])}" cy="{Y(p["y"])}" r="12" fill="{color}"/>');text(out,[str(i+1)],X(p['x'])+18,Y(p['y'])-13,25,color,True)
  if q:
   x,yq=X(q['x']),Y(q['y']);out.append(f'<path d="M{x-13} {yq-13} L{x+13} {yq+13} M{x-13} {yq+13} L{x+13} {yq-13}" stroke="#a35d18" stroke-width="6"/>')
  y=top+ph+105;text(out,['Horizontal: '+v.get('x_label','first coordinate')+'; vertical: '+v.get('y_label','second coordinate')],left,y-20,24)
  for i,p in enumerate(points):y=text(out,wrap(f'{i+1}: {p["label"]} at ({p["x"]}, {p["y"]})',1016,25),52,y+20,25)
  if q:y=text(out,wrap(f'Cross: {q["label"]} at ({q["x"]}, {q["y"]})',1016,25),52,y+20,25)
  if v.get('metric'):y=text(out,wrap('Distance rule: '+v['metric'],1016,25),52,y+20,25)
  y+=45
 elif kind=='weights':
  terms=[x*weight for x,weight in zip(v['inputs'],v['weights'])];raw=sum(terms)+v['bias'];expected=max(0,raw) if v['activation']=='relu' else raw
  assert math.isclose(expected,v['output'],rel_tol=1e-8,abs_tol=1e-8),a['week']
  for x,weight,term in zip(v['inputs'],v['weights'],terms):
   out.append(f'<rect x="52" y="{y}" width="1016" height="82" rx="15" fill="#e1eff4"/>');text(out,[f'Input {x}  x  weight {weight}  =  {term:g}'],78,y+53,32,'#146b77',True);y+=105
  y=text(out,wrap(f'Add the products and bias {v["bias"]}: total = {raw:g}',1016,30),52,y+15,30)+20
  operation='Keep the total (identity)' if v['activation']=='identity' else 'ReLU: use max(0, total)'
  out.append(f'<rect x="52" y="{y}" width="1016" height="105" rx="18" fill="#fff3df"/>');text(out,[operation+f'  ->  output {v["output"]}'],78,y+62,30,'#875b22',True);y+=150
 else:raise ValueError('Unsupported mini_visual '+kind)
 height=int(y+30);svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="{height}" viewBox="0 0 1120 {height}"><rect width="1120" height="{height}" rx="25" fill="#f5f9fc"/>'+''.join(out)+'</svg>'
 stem='academy-detail-'+a['week'].replace('/','-');(R/'assets'/(stem+'.svg')).write_text(svg)
 with fitz.open(stream=svg.encode(),filetype='svg') as source:
  with fitz.open('pdf',source.convert_to_pdf()) as doc:doc[0].get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save(R/'assets'/(stem+'.png'))
 return {'week':a['week'],'kind':kind,'svg':'assets/'+stem+'.svg','png':'assets/'+stem+'.png','width':1120,'height':height}
if __name__=='__main__':
 rows=[row for p in sorted((R/'tools/lesson-upgrades').glob('*.json')) if p.name!='READY.json' for row in [draw(json.loads(p.read_text()))] if row]
 (R/'reports/topic-visual-assets.json').write_text(json.dumps(rows,indent=2));print('Drawn',len(rows),'topic-specific plots, grids and weighted models')
