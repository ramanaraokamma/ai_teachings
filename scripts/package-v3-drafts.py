"""Bundle the 112 continuation packages separately by audience.

The hash manifest documents artifact integrity; it is not a release receipt.
"""
import hashlib
import json
from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs/curriculum-continuation'
OUT.mkdir(parents=True, exist_ok=True)
chapters = []
for path in sorted((ROOT / 'curriculum-v3').glob('ai-*-week-*.json')):
    w = json.loads(path.read_text())
    if w['level'] in ('ai-5','ai-6','ai-7') or (w['level']=='ai-4' and w['week']>=33):
        chapters.append((path, w))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


manifest = {'status': 'Local continuation artifacts; see releases.json for registration status',
            'chapters': {}}
for source, w in chapters:
    stem = source.stem
    docs = {f'{role}.{ext}': ROOT / f'work/{"v3-docs" if ext=="docx" else "v3-pdf"}/{stem}-{role}.{ext}'
            for role in ('lesson', 'workbook', 'guide') for ext in ('docx','pdf')}
    assert all(path.is_file() for path in docs.values()), stem
    diagram = ROOT / f'work/v3-diagrams/{stem}-diagram-1.png'
    assert diagram.is_file(), stem
    manifest['chapters'][f'{w["level"]}/{w["week"]}'] = {
        'sourceHash': digest(source),
        'documents': {role: digest(path) for role, path in docs.items()},
        'diagramHash': digest(diagram),
    }

notice = ('CURRICULUM 3 CONTINUATION\n'
          'Grade 9 Weeks 33–36; Grades 10–12 Weeks 1–36.\n'
          'Canonical content and local mechanism checks passed.\n'
          'DOCX and PDF files are separated by audience.\n'
          'No live deployment has been performed.\n')
for audience, roles in [('student', ('lesson', 'workbook')), ('teacher', ('guide',))]:
    target = OUT / f'{audience}-continuation.zip'
    with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
        archive.writestr('READ_ME.txt', notice +
                         ('Keep teacher solutions in teacher access only.\n' if audience == 'teacher' else
                          'Teacher answer guides are in a separate archive.\n'))
        for source, w in chapters:
            for role in roles:
                for ext,folder in [('docx','v3-docs'),('pdf','v3-pdf')]:
                    path = ROOT / f'work/{folder}/{source.stem}-{role}.{ext}'
                    archive.write(path, f'{w["level"]}/{path.name}')
        for path in sorted((ROOT/'examples/curriculum-v3').glob('*')):
            if path.is_file():archive.write(path,f'local-labs/{path.name}')
    print(f'{audience}: {len(chapters) * len(roles)} Word files and matching PDFs -> {target}')

target = OUT / 'private-canonical-continuation.zip'
with ZipFile(target, 'w', ZIP_DEFLATED) as archive:
    archive.writestr('READ_ME.txt', notice + 'PRIVATE: canonical JSON includes teacher answers.\n')
    archive.writestr('artifact-manifest.json', json.dumps(manifest, indent=2) + '\n')
    for source, _ in chapters:
        archive.write(source, f'curriculum-v3/{source.name}')
    archive.write(ROOT / 'curriculum-v3/progression.json', 'curriculum-v3/progression.json')

(OUT / 'artifact-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(f'Private canonical source: {len(chapters)} chapters -> {target}')
