"""Keep appended explanations in short paragraphs without changing their wording."""
import re
def format_additions(a,limit=420):
 for role in ['sections','teacher','workbook']:
  for section in a.w[role]:
   for block in section['blocks']:
    if block.get('reading_addition')!=a.tag or block['type']!='paragraph':continue
    text=block['text'];parts=[];part=''
    for sentence in re.split(r'(?<=[.!?])\s+',text):
     if part and len(part)+len(sentence)+1>limit:
      parts.append(part);part=''
     part+=(' ' if part else '')+sentence
    if part:parts.append(part)
    assert ' '.join(parts)==text
    block.setdefault('presentation',{})['paragraphs']=parts
