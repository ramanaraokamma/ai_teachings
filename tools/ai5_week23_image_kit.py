"""Author-side complete public model and separate teacher final reference evaluator."""
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def student_program():
 return Path(__file__).with_name('ai5_week23_image_model.py').read_text()
def teacher_program():
 return student_program()+'''
# TEACHER ONLY: inspect the actual saved freeze record before releasing these cases.
assert best_index == 2 and abs(selected-.45) < 1e-12
final = [([[1,1],[1,0]],1), ([[1,1],[0,1]],-1), ([[1,0],[0,1]],-1)]
final_ledger = audit(selected,final,['G','H','I'],baseline_class)
for row in final_ledger:
    print('TEACHER frozen final',{**row,'score':round(row['score'],6)})
print('TEACHER candidate / baseline correct / total',
      sum(r['prediction']==r['class'] for r in final_ledger),
      sum(r['baseline']==r['class'] for r in final_ledger),len(final_ledger))
print('TEACHER candidate signed-target MSE',round(mse(selected,final),6))
# This reference run does not assert a real classroom approval or support retuning on final errors.
'''
if __name__=='__main__':
 out=R/'outputs/ai5-week23-image-kit';out.mkdir(parents=True,exist_ok=True)
 (out/'student-model.py').write_text(student_program());(out/'teacher-final.py').write_text(teacher_program())
 (out/'README.md').write_text('Complete fictional binary-image experiment. Student program supplies all six training/validation cases, fits only the output scalar, selects by validation MSE and records the class-0 baseline. Teacher program additionally contains the three final cases: keep private until the actual freeze record has been checked. Neither program claims a real image-recognition deployment or classroom approval.\n')
 print(out)
