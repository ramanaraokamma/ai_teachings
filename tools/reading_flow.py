"""Shared connected-week ordering and semantic chunks for offline/Word editions."""
from copy import deepcopy
from html import escape

def ordered_sections(sections):
 overview=sections[0].get('reading_flow',{}).get('overview')
 numbers=overview['order'] if overview else range(1,len(sections)+1)
 return [(n,sections[n-1]) for n in numbers]

def plain_block(source):
 b=deepcopy(source);f=b.get('presentation')
 if f and f['kind'] not in ['checklist','definition']:
  f['kind']='body';f.pop('label',None);f.pop('context',None)
 return b

def overview_html(overview):
 return '<section class="flow-overview"><p class="flow-kicker">THE CONNECTED WEEK</p><h2>'+escape(overview['title'])+'</h2><p>'+escape(overview['lead'])+'</p><nav class="flow-route" aria-label="Six steps through the week">'+''.join('<a href="#section-'+str(step['section'])+'"><span>'+str(i+1)+'</span>'+escape(step['label'])+'</a>' for i,step in enumerate(overview['route']))+'</nav><p class="flow-outcome"><strong>Keep one habit:</strong> '+escape(overview['outcome'])+'</p></section>'

def flow_html(section,render_block,slots=None):
 def show(i,card=False):
  source=section['blocks'][i];b=plain_block(source);body=render_block(b)
  if slots and i in slots:body=body.replace('<textarea ',f'<textarea data-response-slot="{slots[i]}" ',1)
  label=source.get('presentation',{}).get('label')
  context=source.get('presentation',{}).get('context')
  return '<div class="flow-item">'+('<h4 class="flow-card-title">'+escape(label)+'</h4>' if card and label else '')+('<p class="flow-note">'+escape(context)+'</p>' if context else '')+body+'</div>'
 out=[]
 for g in section['reading_flow']['groups']:
  kind=g.get('kind','text');indices=g['indices'];note='<p class="flow-note">'+escape(g['note'])+'</p>' if g.get('note') else ''
  if kind in ['steps','prompts']:
   prose=[i for i in indices if section['blocks'][i]['type'] in ['paragraph','step','list']];rest=[i for i in indices if i not in prose];tag='ol' if kind=='steps' else 'ul'
   body='<'+tag+' class="flow-list'+(' flow-steps' if tag=='ol' else '')+'">'+''.join('<li>'+show(i)+'</li>' for i in prose)+'</'+tag+'>'+''.join(show(i) for i in rest)
  else:body='<div class="'+('flow-card-grid' if kind=='cards' else 'flow-prose')+'">'+''.join(show(i,kind=='cards') for i in indices)+'</div>'
  if g.get('collapsed'):out.append('<details class="flow-reference"><summary>'+escape(g['title'])+'</summary><div class="flow-reference-body">'+note+body+'</div></details>')
  else:out.append('<section class="flow-chunk flow-'+kind+'"><h3 class="flow-chunk-title">'+escape(g['title'])+'</h3>'+note+body+'</section>')
 return ''.join(out)
