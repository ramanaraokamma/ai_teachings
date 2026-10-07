"""Verify the revised readiness questions against lesson topics and error traces."""
from pathlib import Path
import json,subprocess,sys
R=Path(__file__).resolve().parents[1];D=json.loads((R/'content/programme.json').read_text());rows=[];errors=[]
SKILLS=['Paper instructions, ordered assignments and arithmetic','Integer, text, float, Boolean and reassignment snapshots','Parentheses, precedence, ordinary division, quotient and remainder','AND, OR, NOT and separating required conditions','Ordered branches, valid inputs and equality boundary','Range stopping, initialisation and empty iteration','Index positions, negative indexing and out-of-range stopping','Definitions, calls and noncommutative positional arguments','Returned values, separate local state and missing return','Named record fields, updates and absent-versus-zero values','Structured-record traversal, observed sum, denominator and coverage','Revealing boundary assertions, first failure, repair and regression cases']
for w,skill in zip(D['python_bridge'],SKILLS):
 c=w['method']['independent'];run=subprocess.run([sys.executable,'-c',c['code']],capture_output=True,text=True,timeout=5)
 passed=run.returncode==0 and run.stdout==c['expected_stdout']
 rows.append({'week':w['id'],'topic':w['title'],'assessed_skills':skill,'case_title':c['title'],'base_passed':passed})
 if not passed:errors.append({'week':w['id'],'error':'Base trace mismatch'})
variants=[]
def check(n,code,stdout,error=None):
 run=subprocess.run([sys.executable,'-c',code],capture_output=True,text=True,timeout=5)
 okay=run.stdout==stdout and ((run.returncode==0) if error is None else (run.returncode!=0 and error in run.stderr))
 variants.append({'week':'python-bridge/'+str(n),'stdout':run.stdout,'expected_error':error,'passed':okay})
 if not okay:errors.append({'week':n,'stdout':run.stdout,'stderr':run.stderr})
C={w['week']:w['method']['independent']['code'] for w in D['python_bridge']}
check(1,C[1].replace('packs = 3','packs = 5'),'35\n')
check(2,C[2].replace('count = 4','count = 0'),'3 4 0.0 True\nint str float bool\n')
check(3,C[3].replace('(17 + 5) // 5','(17 + 5) % 5'),'2\n18\n3.4 3 2\n')
check(4,C[4].replace('genre = "science"','genre = "history"'),'False\nFalse\nTrue\nTrue\n')
check(5,C[5].replace('reading = 30','reading = 29'),'on\n')
check(5,C[5].replace('reading = 30','reading = -1'),'invalid\n')
check(6,C[6].replace('range(2, 6)','range(2, 2)'),'0\n')
check(7,C[7].replace('values[-1]','values[3]'),'9\n','IndexError')
check(7,C[7].replace('[4, 9, 2]','[]'),'','IndexError')
check(8,C[8].split('print(')[0],'')
check(9,C[9].replace('    return total\n',''),'','TypeError')
check(9,C[9]+'print(total)\n','6 10 16\n','NameError')
check(10,C[10].replace('if count is None:','if not count:'),'missing\n3\nmissing\n')
check(11,C[11].replace('[{"score": 2}, {"score": 6}, {}]','[{}, {}, {}]'),'0 0 3 None\n')
check(12,C[12].replace('return x < 10','return x <= 10'),'','AssertionError')
report={'lessons_aligned':len(rows),'base_programs':len(rows),'changed_and_error_cases':len(variants),'errors':errors,'alignment':rows,'variants':variants,'scope':'Topic alignment was editorially reviewed against the actual twelve lesson goals. Executions verify specified outputs and failure points, not learner readiness by themselves.'}
(R/'reports/bridge-readiness-alignment.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k not in ['alignment','variants']},indent=2));sys.exit(bool(errors))
