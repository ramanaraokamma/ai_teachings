"""Space newly authored prose and number-heavy table cells; preserve source blocks."""
import re

def prose(text):
 text=re.sub(r'([,;])(?=\S)',r'\1 ',text)
 text=re.sub(r'\b([a-z]{3,}|MAE|MSE|RMSE|SSE|TP|FP|FN|TN)(?=\d)',r'\1 ',text)
 text=re.sub(r'(?<=\d)(?=[a-z]{3,})',' ',text)
 text=re.sub(r'(?<=\d)(?=(?:cm|mm|m)\b)',' ',text)
 return text

def space_additions(a):
 for role in ['sections','teacher','workbook']:
  for section in a.w[role]:
   for b in section['blocks']:
    if b.get('reading_addition')!=a.tag:continue
    if b['type']=='paragraph':
     b['text']=prose(b['text'])
     if b.get('presentation',{}).get('paragraphs'):b['presentation']['paragraphs']=[b['text']]
    elif b['type']=='table':
     b['rows']=[[prose(cell) if isinstance(cell,str) else cell for cell in row] for row in b['rows']]
