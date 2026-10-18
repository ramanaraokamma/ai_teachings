"""Draw the authored binary-grid comparison as a scalable teaching diagram."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
parts=['''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="880" viewBox="0 0 1400 880" role="img" aria-labelledby="title desc"><title id="title">Two pixel badges: equal counts, different arrangements</title><desc id="desc">Using 1 for black and 0 for white, Badge A has top row 1 0 1 and bottom row 0 1 0. Badge B has top row 1 1 1 and bottom row 0 0 0. Each has three black pixels. The top-middle and bottom-middle pixels differ.</desc><rect width="1400" height="880" rx="32" fill="#f3f8fb"/><g font-family="Arial, sans-serif" fill="#17384e"><text x="60" y="65" font-size="19" font-weight="700" fill="#286d77">AI ACADEMY / LEVEL 1 · WEEK 5</text><text x="60" y="121" font-size="38" font-weight="700">Same black-pixel count. Different positions.</text><text x="60" y="166" font-size="23">Two rows × three columns · top row first · left to right · 1 = black, 0 = white</text>''']
for label,x,grid in [('Badge A',65,[[1,0,1],[0,1,0]]),('Badge B',725,[[1,1,1],[0,0,0]])]:
 parts.append(f'<rect x="{x}" y="205" width="610" height="475" rx="24" fill="white" stroke="#b9d2df" stroke-width="2"/><text x="{x+30}" y="256" font-size="30" font-weight="700">{label}</text>')
 for c,name in enumerate(('Left','Middle','Right')):parts.append(f'<text x="{x+200+c*123}" y="308" text-anchor="middle" font-size="20" fill="#405b6a">{name}</text>')
 for r,row in enumerate(grid):
  parts.append(f'<text x="{x+26}" y="{394+r*123}" font-size="21" font-weight="700">{"Top" if r==0 else "Bottom"}</text>')
  for c,v in enumerate(row):
   xx=x+143+c*123;yy=329+r*123;fill='#17384e' if v else '#fff';ink='#fff' if v else '#17384e'
   parts.append(f'<rect x="{xx}" y="{yy}" width="112" height="112" rx="8" fill="{fill}" stroke="#17384e" stroke-width="3"/><text x="{xx+56}" y="{yy+71}" text-anchor="middle" font-size="40" font-weight="700" fill="{ink}">{v}</text>')
 parts.append(f'<text x="{x+30}" y="637" font-size="26" font-weight="700" fill="#167069">Black pixels = 3 out of 6</text>')
parts.append('''<rect x="65" y="718" width="1270" height="112" rx="18" fill="#e5f2ef"/><text x="95" y="762" font-size="26" font-weight="700">Compare the middle column.</text><text x="95" y="802" font-size="24">A is white above black. B is black above white. Counting alone loses those positions.</text></g></svg>''')
p=R/'assets/academy-pixels-ai-1-5-badges.svg';p.write_text(''.join(parts));print(p)
