"""Plain-text-preserving presentation shared by HTML and document exports."""
import re,html
from pathlib import Path
def segments(text,terms):
 if not terms:return [(text,False)]
 pattern='('+'|'.join(re.escape(t) for t in sorted(terms,key=len,reverse=True))+')';keys={t.casefold() for t in terms}
 return [(part,part.casefold() in keys) for part in re.split(pattern,text,flags=re.I) if part]
def formatted_html(b):
 f=b.get('presentation')
 if not f:return None
 if f['kind']=='section-label':return ''
 if f['kind']=='checklist':return '<div class="reading-block reading-checklist"><ul>'+''.join('<li>'+html.escape(item)+'</li>' for item in f['items'])+'</ul><p>'+html.escape(f['tail'])+'</p></div>'
 if f['kind']=='eyebrow':return '<p class="reading-eyebrow">'+html.escape(b['text'])+'</p>'
 title='<h3 class="reading-label">'+html.escape(f['label'])+'</h3>' if f.get('label') else ''
 paragraphs=''.join('<p>'+''.join(('<strong>'+html.escape(part)+'</strong>') if strong else html.escape(part) for part,strong in segments(text,f.get('emphasis',[])))+'</p>' for text in f.get('paragraphs',[b['text']]))
 context='<p class="reading-context">'+html.escape(f['context'])+'</p>' if f.get('context') else ''
 return '<div class="reading-block reading-'+f['kind']+'">'+title+context+paragraphs+'</div>'
CSS='''
.reading-block{max-width:72ch;margin:1.15rem 0;color:#203c4f;font-size:1rem;line-height:1.85}.reading-block p{margin:.65rem 0}.reading-block strong{color:#123c51;font-weight:750}.reading-label{font-size:1.1rem;line-height:1.45;font-weight:750;margin:0 0 .8rem;color:#173e54}.reading-eyebrow{margin:1.5rem 0 .5rem;color:#476176;font-size:.75rem;font-weight:750;letter-spacing:.12em}.reading-concept,.reading-example,.reading-question,.reading-note,.reading-caution,.reading-definition,.reading-step{padding:1.1rem 1.3rem;border-radius:.75rem;border:1px solid #bfd2df;border-left:4px solid #28668d}.reading-concept{background:#edf7f3;border-left-color:#086c68}.reading-example{background:#f1f6fc}.reading-question{background:#f5f1fb;border-left-color:#6541a5}.reading-note{background:#f1f6f8;border-left-color:#476176}.reading-caution{background:#fff5e6;border-left-color:#975014}.reading-step{background:white;border-left-color:#086c68}.reading-definition{margin:0;background:#f4f9fc;height:100%}.gallery.reading-cards{grid-template-columns:repeat(3,minmax(0,1fr));align-items:stretch}.reading-cards .reading-label{font-size:1rem}@media(max-width:800px){.gallery.reading-cards{grid-template-columns:1fr}.reading-block{font-size:1rem}}@media print{.reading-block{font-size:11pt;line-height:1.55}.reading-label{break-after:avoid}.reading-definition,.reading-step{break-inside:avoid}.reading-cards{grid-template-columns:1fr!important}}
'''
PDF_CSS='''.reading-block{font-size:10.5pt;line-height:1.5;margin:10pt 0}.reading-label{font-size:12pt;page-break-after:avoid;color:#173e54}.reading-example,.reading-concept,.reading-note,.reading-question,.reading-caution,.reading-definition,.reading-step{padding:9pt;background-color:#edf4f8}.reading-caution{background-color:#fff5e6}.reading-eyebrow{font-size:9pt;color:#476176;font-weight:bold}'''

CSS+=".reading-section-intro{max-width:72ch;padding:14px 18px;border-left:3px solid #829eae;background:#f4f7fa;color:#405a6b;margin:0 0 24px}.reading-context{font-size:.95em;padding:10px;border-left:2px solid #829eae;background:#fff}"

CSS+=".reading-checklist ul{list-style:disc;padding-left:1.6rem}.reading-checklist li{padding:.35rem 0}.reading-check{border-left:3px solid #086c68;padding-left:1rem}"
