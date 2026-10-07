"""Check every local file and anchor referenced by the generated HTML."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1];errors=[];count=0
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=set()
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  self.links += [a[key] for key in ['href','src'] if key in a]
parsed={}
for p in ROOT.rglob('*.html'):
 parser=Links();parser.feed(p.read_text());parsed[p]=parser
for p,parser in parsed.items():
 for raw in parser.links:
  u=urlsplit(raw)
  if u.scheme or u.netloc:continue
  dest=(p.parent/unquote(u.path)).resolve() if u.path else p;count+=1
  if not dest.is_file():errors.append({'page':str(p.relative_to(ROOT)),'missing':raw})
  elif u.fragment and dest in parsed and unquote(u.fragment) not in parsed[dest].ids:errors.append({'page':str(p.relative_to(ROOT)),'missing_anchor':raw})
report={'html_pages':len(parsed),'local_targets_checked':count,'errors':errors}
(ROOT/'reports/link-validation.json').write_text(json.dumps(report,indent=2));print(report)
if errors:raise SystemExit(1)
