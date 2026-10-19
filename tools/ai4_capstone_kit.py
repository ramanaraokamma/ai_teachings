"""Author-side construction of the documented Level4 72-record synthetic kit."""
from pathlib import Path
import csv,io,json
ROOT=Path(__file__).resolve().parents[1]
FIELDS=['id','group_id','split','width_cm','height_cm','label']
def rows():
 result=[]
 for i in range(72):
  width,height=2+i%9,2+i//9;selector=5*i%18
  result.append({'id':f'P{i:02}','group_id':f'P{i:02}',
   'split':'training' if selector<10 else 'validation' if selector<15 else 'final',
   'width_cm':width,'height_cm':height,'label':'blocked' if width+height>=12 else 'clear'})
 return result

def csv_text(teacher=False):
 stream=io.StringIO(newline='');writer=csv.DictWriter(stream,fieldnames=FIELDS,lineterminator='\n');writer.writeheader()
 for original in rows():
  r=dict(original)
  if not teacher and r['split']=='final':r['label']=''
  writer.writerow(r)
 return stream.getvalue()

def baseline_program():
 return '''import csv
from io import StringIO
from collections import Counter

# Complete student kit; final reference cells are deliberately blank.
DATA = """'''+csv_text()+'''"""
records = list(csv.DictReader(StringIO(DATA)))
for row in records:
    row['width_cm'] = int(row['width_cm'])
    row['height_cm'] = int(row['height_cm'])
train = [r for r in records if r['split'] == 'training']
valid = [r for r in records if r['split'] == 'validation']
final_features = [r for r in records if r['split'] == 'final']
assert len({r['id'] for r in records}) == len(records) == 72
sets = [{r['group_id'] for r in part} for part in [train, valid, final_features]]
assert not (sets[0] & sets[1] or sets[0] & sets[2] or sets[1] & sets[2])
assert all(not r['label'] for r in final_features)
counts = Counter(r['label'] for r in train)
constant = 'blocked' if counts['blocked'] > counts['clear'] else 'clear'
predictions = [constant] * len(valid)
correct = sum(p == r['label'] for p, r in zip(predictions, valid))
positives = sum(r['label'] == 'blocked' for r in valid)
found = sum(p == r['label'] == 'blocked' for p, r in zip(predictions, valid))
print('roles', len(train), len(valid), len(final_features))
print('training clear/blocked', counts['clear'], counts['blocked'])
print('frozen baseline', constant)
print('validation correct/total', correct, len(valid))
print('validation blocked found/total', found, positives)
print('final references absent: not scored')
# IDs/groups are audit metadata, not model features. Tie rule chooses clear.
'''

def candidate_program(teacher_final=False):
 code=baseline_program()+r'''
from fractions import Fraction

# Declare the two candidates and selection rule before inspecting validation.
# V2 changes only the available feature set. k=1 and all tie rules stay fixed.
def fit_neighbour(training, features):
    if not training or not features:
        raise ValueError('Need training records and named features')
    if any(r['label'] not in ('clear', 'blocked') for r in training):
        raise ValueError('Training labels must be known')
    lows = tuple(min(r[f] for r in training) for f in features)
    spans = tuple(max(r[f] for r in training) - lo for f, lo in zip(features, lows))
    if any(span == 0 for span in spans):
        raise ValueError('This experiment requires nonconstant training features')
    def scale(row):
        return tuple(Fraction(row[f] - lo, span) for f, lo, span in zip(features, lows, spans))
    stored = [(r['id'], scale(r), r['label']) for r in training]
    return features, lows, spans, stored

def predict(row, model):
    features, lows, spans, stored = model
    point = tuple(Fraction(row[f] - lo, span) for f, lo, span in zip(features, lows, spans))
    # Manhattan distance; exact ties use the smallest training ID.
    nearest = min(stored, key=lambda item: (sum(abs(a-b) for a,b in zip(point,item[1])), item[0]))
    return nearest[2]

def matrix(part, preds):
    if len(part) != len(preds) or not part:
        raise ValueError('Need one prediction per labelled case')
    cells = [0, 0, 0, 0]  # TN, FP, FN, TP; blocked positive
    for r, p in zip(part, preds):
        if r['label'] not in ('clear', 'blocked') or p not in ('clear', 'blocked'):
            raise ValueError('Unknown reference or prediction; do not score blank final labels')
        cells[2 * (r['label'] == 'blocked') + (p == 'blocked')] += 1
    return cells

models = {'V1': fit_neighbour(train, ('width_cm',)),
          'V2': fit_neighbour(train, ('width_cm', 'height_cm'))}
validation_predictions = {v: [predict(r,m) for r in valid] for v,m in models.items()}
validation_matrices = {v: matrix(valid, ps) for v,ps in validation_predictions.items()}
# Predeclared: most validation correct; then fewer features; then version name.
chosen = min(models, key=lambda v: (-(validation_matrices[v][0]+validation_matrices[v][3]), len(models[v][0]), v))
print('validation baseline TN FP FN TP', matrix(valid, [constant]*len(valid)))
for v in models:
    train_preds = [predict(r,models[v]) for r in train]
    print(v, 'training correct/40', sum(p==r['label'] for p,r in zip(train_preds,train)))
    print(v, 'validation TN FP FN TP', validation_matrices[v])
    print(v, 'validation errors', [r['id'] for r,p in zip(valid,validation_predictions[v]) if r['label']!=p])
gains = [r['id'] for r,a,b in zip(valid,validation_predictions['V1'],validation_predictions['V2']) if a!=r['label'] and b==r['label']]
regressions = [r['id'] for r,a,b in zip(valid,validation_predictions['V1'],validation_predictions['V2']) if a==r['label'] and b!=r['label']]
print('V2 gains', gains, 'regressions', regressions)
print('frozen choice', chosen)
# Save this code/data/feature contract and these predictions before key release.
final_predictions = [predict(r,models[chosen]) for r in final_features]
print('frozen final prediction ledger', list(zip([r['id'] for r in final_features], final_predictions)))
print('Final score withheld: teacher reference release and freeze check required.')
'''
 if teacher_final:
  key={r['id']:r['label'] for r in rows() if r['split']=='final'}
  code+='\n# TEACHER ONLY: run after verifying the saved freeze record.\nFINAL_KEY = '+repr(key)+r'''
assert set(FINAL_KEY) == {r['id'] for r in final_features}
final_labelled = [dict(r, label=FINAL_KEY[r['id']]) for r in final_features]
print('TEACHER frozen final TN FP FN TP', matrix(final_labelled, final_predictions))
print('TEACHER same-case baseline TN FP FN TP', matrix(final_labelled, [constant]*len(final_labelled)))
# These results do not document an actual classroom sign-off or permit retuning.
'''
 return code

if __name__=='__main__':
 out=ROOT/'outputs/ai4-capstone-data-kit';out.mkdir(parents=True,exist_ok=True)
 (out/'STUDENT_DATA.csv').write_text(csv_text())
 (out/'TEACHER_DATA_AND_FINAL_KEY.csv').write_text(csv_text(True))
 (out/'student-baseline.py').write_text(baseline_program())
 (out/'student-candidate.py').write_text(candidate_program())
 (out/'teacher-final-evaluation.py').write_text(candidate_program(True))
 (out/'README.md').write_text('''# Level4 synthetic capstone kit

This instantiates the 72-record geometric classroom dataset already specified in the teacher guide. It is fictional, hand-constructed and not a random population sample.

- Student data: 40 labelled training rows,20 labelled validation rows,12 final feature rows with blank labels.
- Each record/group is one distinct fictional parcel. Width and height are available features in cm; IDs/groups are metadata.
- Baseline: fit training majority only,choose clear on a tie. Training clear22/blocked18; validation correct9/20 and blocked recall0/11.
- Teacher file contains the final key and construction label rule is in teacher lesson materials. Keep that file out of student copies until the frozen-version gate.
- The public student baseline performs no final scoring. Later teacher-only guides evaluate a frozen candidate; do not publish the key or select settings from final results.
- Classroom labels are synthetic operational categories,not real parcel safety or plant diagnosis. Numerical examples elsewhere in the lessons are explicitly separate fixtures.
''')
 print(out)
