"""Draw labelled vector mechanisms and portable high-resolution teaching images."""
from pathlib import Path
import html,json,re,unicodedata
import fitz
R=Path(__file__).resolve().parents[1];font=fitz.Font('helv')
COLORS=['#147d87','#35699d','#946528','#7155a0','#327650']
ICONS={
'book':'<path d="M12 19 Q31 12 46 21 Q64 12 82 19 V74 Q64 66 46 77 Q30 66 12 74 Z"/><path d="M46 21 V77 M21 31 L36 34 M56 33 L73 30 M21 43 L36 46 M56 45 L73 42"/>',
'sensor':'<circle cx="47" cy="47" r="12"/><path d="M25 25 Q6 47 25 69 M69 25 Q88 47 69 69 M34 34 Q23 47 34 60 M60 34 Q71 47 60 60"/>',
'rule':'<path d="M47 10 V25 M47 25 L29 44 L47 63 L65 44 Z M29 44 H12 V79 M65 44 H82 V79"/><circle cx="12" cy="82" r="5"/><circle cx="82" cy="82" r="5"/>',
'data':'<rect x="12" y="14" width="70" height="65" rx="6"/><path d="M12 35 H82 M12 56 H82 M36 14 V79 M59 14 V79"/>',
'model':'<circle cx="17" cy="25" r="8"/><circle cx="17" cy="70" r="8"/><circle cx="48" cy="47" r="10"/><circle cx="79" cy="25" r="8"/><circle cx="79" cy="70" r="8"/><path d="M24 30 L39 41 M24 65 L39 53 M57 41 L72 30 M57 53 L72 65"/>',
'person':'<circle cx="47" cy="24" r="12"/><path d="M47 36 V63 M23 51 L47 40 L71 51 M47 63 L29 83 M47 63 L65 83"/>',
'check':'<rect x="13" y="13" width="68" height="68" rx="12"/><path d="M27 47 L41 61 L69 31"/>',
'chart':'<path d="M12 13 V81 H85 M25 76 V57 H39 V76 M45 76 V37 H59 V76 M65 76 V20 H79 V76"/>',
'code':'<path d="M31 20 L9 47 L31 74 M63 20 L85 47 L63 74 M55 14 L39 80"/>',
'shield':'<path d="M47 9 L81 22 V46 Q79 72 47 86 Q15 72 13 46 V22 Z"/><rect x="33" y="39" width="28" height="24" rx="3"/><path d="M38 39 V31 Q47 17 56 31 V39"/>',
'question':'<circle cx="47" cy="47" r="36"/><path d="M31 33 Q34 17 51 22 Q72 30 56 45 Q47 51 47 60"/><circle cx="47" cy="72" r="2"/>',
'output':'<rect x="39" y="17" width="43" height="61" rx="7"/><path d="M10 47 H62 M48 33 L62 47 L48 61"/>',
'experiment':'<path d="M25 12 H46 M29 12 V44 L12 77 Q9 83 17 84 H54 Q62 83 59 77 L42 44 V12 M19 64 H52 M65 20 H83 M68 20 V68 Q75 88 80 68 V20 M69 55 H79"/>',
'network':'<circle cx="15" cy="20" r="7"/><circle cx="15" cy="73" r="7"/><circle cx="47" cy="20" r="7"/><circle cx="47" cy="47" r="7"/><circle cx="47" cy="73" r="7"/><circle cx="79" cy="47" r="8"/><path d="M22 20 H40 M22 20 L40 47 M22 20 L40 73 M22 73 L40 20 M22 73 L40 47 M22 73 H40 M54 20 L71 42 M54 47 H71 M54 73 L71 52"/>',
'clock':'<circle cx="47" cy="47" r="35"/><path d="M47 21 V47 L65 59 M47 13 V18 M47 76 V81 M13 47 H18 M76 47 H81"/>'}
def safe(text):
 return unicodedata.normalize('NFKC',str(text)).translate(str.maketrans({'→':' -> ','←':' <- ','≥':'>=','≤':'<=','−':'-','×':' x ','÷':' / ','–':'-','—':'-','“':'"','”':'"','‘':"'",'’':"'"}))
def wrap(text,width,size):
 lines=[]
 for para in safe(text).splitlines():
  line=''
  for word in para.split():
   trial=(line+' '+word).strip()
   if line and font.text_length(trial,fontsize=size)>width:lines.append(line);line=word
   else:line=trial
  lines.append(line)
 return lines

def text(svg,lines,x,y,size,color='#183249',bold=False):
 for line in lines:
  svg.append(f'<text x="{x}" y="{y}" font-family="Helvetica,Arial,sans-serif" font-size="{size}"'+(' font-weight="bold"' if bold else '')+f' fill="{color}">{html.escape(line)}</text>');y+=size*1.35
 return y

def draw(a):
 width=1120;parts=[]
 parts.append('<rect x="0" y="0" width="1120" height="HEIGHT" rx="28" fill="#edf5f8"/>')
 y=text(parts,['AI ACADEMY  /  '+a['week'].upper()],52,57,22,'#356b7b',True)
 y=text(parts,wrap(a['title'],1016,40),52,y+18,40,'#123c55',True)+24
 parts.append(f'<rect x="52" y="{y-8}" width="1016" height="100" rx="18" fill="#ffffff" stroke="#c4dbe5"/>')
 text(parts,['Start with the supplied facts'],76,y+28,27,'#146b77',True)
 text(parts,['Follow each arrow. Ask which fact allows the next step.'],76,y+65,25)
 y+=130
 for i,s in enumerate(a['steps']):
  color=COLORS[i%len(COLORS)];details=wrap(s['detail'],780,30);label=wrap(s['label'],780,32)
  height=max(150,36+len(label)*42+len(details)*40)
  parts.append(f'<rect x="52" y="{y}" width="1016" height="{height}" rx="20" fill="#ffffff" stroke="#bed5df" stroke-width="2"/>')
  parts.append(f'<rect x="52" y="{y}" width="10" height="{height}" rx="5" fill="{color}"/>')
  parts.append(f'<circle cx="131" cy="{y+height/2}" r="54" fill="{color}" opacity=".10"/>')
  parts.append(f'<g transform="translate(84,{y+height/2-47})" fill="none" stroke="{color}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">{ICONS[s["icon"]]}</g>')
  yy=text(parts,[str(i+1)+'. '+line if j==0 else line for j,line in enumerate(label)],216,y+43,32,color,True)
  text(parts,details,216,yy+8,30)
  y+=height
  if i<len(a['steps'])-1:
   parts.append(f'<path d="M560 {y+7} V{y+27} M550 {y+19} L560 {y+29} L570 {y+19}" fill="none" stroke="#638796" stroke-width="4" stroke-linecap="round"/>');y+=37
 y+=25
 change=a['counterfactual'];change_lines=wrap(change['change'],960,27)
 height=70+len(change_lines)*37
 parts.append(f'<rect x="52" y="{y}" width="1016" height="{height}" rx="18" fill="#fff3df" stroke="#dfb569"/>')
 yy=text(parts,['CHANGE ONE THING'],76,y+40,26,'#875b22',True);text(parts,change_lines,76,yy+10,27)
 y+=height+34
 text(parts,['Explain the changed result using the matching lesson.'],52,y,24,'#466378');y+=48
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="'+str(int(y))+'" viewBox="0 0 1120 '+str(int(y))+'">'+''.join(parts).replace('HEIGHT',str(int(y)))+'</svg>'
 stem='academy-visual-'+a['week'].replace('/','-');(R/'assets'/(stem+'.svg')).write_text(svg)
 with fitz.open(stream=svg.encode(),filetype='svg') as source:
  with fitz.open('pdf',source.convert_to_pdf()) as doc:doc[0].get_pixmap(matrix=fitz.Matrix(1.35,1.35)).save(R/'assets'/(stem+'.png'))
 return {'week':a['week'],'svg':'assets/'+stem+'.svg','png':'assets/'+stem+'.png','width':1120,'height':int(y),'steps':len(a['steps'])}
if __name__=='__main__':
 rows=[]
 for path in sorted((R/'tools/lesson-upgrades').glob('*.json')):
  if path.name=='READY.json':continue
  rows.append(draw(json.loads(path.read_text())))
 (R/'reports/pictorial-assets.json').write_text(json.dumps(rows,indent=2));print('Drawn',len(rows),'topic-specific vector diagrams and matching PNGs')
