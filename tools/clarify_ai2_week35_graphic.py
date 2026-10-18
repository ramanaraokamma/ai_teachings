"""Clarify the native SVG's alternative comparison before raster export."""
from pathlib import Path
p=Path('assets/academy-story-ai-2-35-04.svg');s=p.read_text()
s=s.replace('An alternative patch simply increases the limit to 101.','An alternative patch uses pages &lt;= 101 instead of the required pages &lt;= 100.')
s=s.replace('An alternative patch simply increases the</tspan><tspan x="652" dy="32.66">limit to 101.','Alternative patch: pages &lt;= 101.</tspan><tspan x="652" dy="32.66">The contract requires pages &lt;= 100.')
p.write_text(s)
