"""Verify packaged teaching files, hashes, ZIP integrity and learner role boundaries."""
from pathlib import Path
import hashlib,json,re,zipfile
R=Path(__file__).resolve().parents[1];O=R/'outputs/ai-academy-complete-programme'
manifest=json.loads((O/'reports/file-manifest.json').read_text());checked=0
for row in manifest:
 file=O/row['file'];assert file.is_file(),row['file']
 assert file.stat().st_size==row['bytes'],row['file']
 assert hashlib.sha256(file.read_bytes()).hexdigest()==row['sha256'],row['file'];checked+=1
for role in ['student','teacher','workbook']:
 for ext in ['docx','pdf']:
  root_files=sorted((R/'downloads'/role).glob('*.'+ext));assert len(root_files)==264,(role,ext)
  for file in root_files:assert file.read_bytes()==(O/'downloads'/role/file.name).read_bytes(),str(file)
 for file in (R/role).glob('*.html'):assert file.read_bytes()==(O/role/file.name).read_bytes(),str(file)
assert (R/'content/programme.json').read_bytes()==(O/'content/programme.json').read_bytes()
assert (R/'content/learning-tools.json').read_bytes()==(O/'content/learning-tools.json').read_bytes()
student=O.parent/'ai-academy-student-bundle.zip';teacher=O.parent/'ai-academy-teacher-bundle.zip'
for file in [student,teacher]:
 with zipfile.ZipFile(file) as z:assert z.testzip() is None,file.name
with zipfile.ZipFile(student) as z:
 assert not any('/teacher/' in name or '/content/' in name or '/tools/' in name or '/reports/' in name for name in z.namelist())
 for role in ['student','workbook']:
  for ext in ['docx','pdf']:assert len([n for n in z.namelist() if n.startswith(f'ai-academy-student/downloads/{role}/') and n.endswith('.'+ext)])==264
with zipfile.ZipFile(teacher) as z:assert z.read('ai-academy-complete-programme/content/programme.json')==(R/'content/programme.json').read_bytes()
print('Verified',checked,'mirrored file hashes; all 1584 teaching downloads match; both ZIPs pass integrity; learner bundle excludes teacher/source material.')
