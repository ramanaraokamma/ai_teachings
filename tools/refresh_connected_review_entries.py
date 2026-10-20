"""Refresh review navigation after the sequential full-programme review completes."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import json,subprocess,sys
R=Path(__file__).resolve().parents[1]
p=json.loads((R/'reports/CONNECTED_READING_PROGRESS.json').read_text())
assert p['completed_lessons']==264 and p['remaining_lessons']==0 and p['next']=='complete'
def refresh(row):
 result=subprocess.run([sys.executable,str(R/'tools/build_connected_review.py'),row['week']],cwd=R,capture_output=True,text=True)
 if result.returncode:raise RuntimeError(row['week']+': '+result.stderr)
 return row['week']
with ThreadPoolExecutor(max_workers=4) as pool:done=list(pool.map(refresh,p['completed']))
subprocess.run([sys.executable,str(R/'tools/build_connected_review_index.py')],cwd=R,check=True)
print('Refreshed',len(done),'complete review entries and the programme index.')
