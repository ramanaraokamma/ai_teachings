# Repository and website

This root contains the complete offline AI Academy programme and its protected Cloudflare website. Website setup and publishing instructions are in [CLOUDFLARE_DEPLOYMENT.md](CLOUDFLARE_DEPLOYMENT.md). Run `npm test` to build the website and verify its unified curriculum and role access. For local offline reading, open `START_HERE.html`.

# AI Academy — Complete Learning Programme

Open **START_HERE.html** for the complete programme. Read **TEACHING_METHOD.html** for the teaching cycle and **student/LEARNING_GUIDE.html** for learner instructions. Read **PROGRAMME_GUIDE.html** for placement, pacing, projects, assessment and distribution.

The goal is a complete AI education programme for children, with everything their teachers need to teach it: clear explanations, worked examples, visual traces, investigations, independent assessment and cumulative projects. Learners progress from understanding simple decisions to designing, building, testing and explaining AI systems responsibly.

## Contents

- Seven levels, 36 weeks each: 252 main weeks.
- Twelve additional Python preparation lessons, required before the Machine Learning coding pathway unless equivalent readiness is demonstrated.
- 792 weekly HTML resources: 264 student lessons, 264 teacher guides and 264 workbooks.
- Matching Word and PDF editions under downloads/student, downloads/teacher and downloads/workbook.
- 1,874 active original instructional images, plus corrected native diagrams and an interactive sensor example.
- Every original Curriculum 2.0 week retains its full teaching content. Every later source lesson is integrated into a required week or the Python bridge.

| Level | Typical grade | Focus | Cumulative project |
|---|---|---|---|
| 1 | 6 | Foundations | Helpful Classroom Sorter |
| 2 | 7 | Algorithms and Data | Transparent Book Recommender |
| 3 | 8 | Generative AI Systems | Verified Study Buddy |
| Bridge | Readiness | Python preparation after Level 3 | Python readiness portfolio |
| 4 | 9 | Machine Learning | Responsible Plant Classifier |
| 5 | 10 | Neural Networks | Image-pattern Network Investigation |
| 6 | 11 | AI Engineering | Grounded Learning Service |
| 7 | 12 | Research and Advanced Projects | Reproducible AI Research Study |

Grade labels are placement guidance; prerequisites and demonstrated independence determine readiness. Begin with three 45-minute sessions for the core week and reserve more sessions for connected topics, investigations and project construction. The expanded content is not claimed to fit one fixed 90-minute lesson.

## Organisation

- student/: full original weekly teaching model plus lesson routes, goals and finish-and-return checks; two original coding weeks retain a fifteenth laboratory.
- teacher/: preparation, explanation, guided teaching, misconceptions, assessment answers and progression; original laboratory guidance is retained.
- workbook/: original activities, integrated examples, independent cases and project evidence.
- content/programme.json: canonical content, including teacher answers.
- tools/: preserved source inputs, rebuild scripts and validation scripts.
- reports/: content, browser and download checks, source coverage and week-by-week review.
- assets/: offline images, shared styles and response/sensor behaviour.

The first four levels preserve the original sequence. The later topics supplement that sequence rather than replacing it with five short sections. Twenty-six otherwise unrepresented later lessons are integrated into appropriate weeks. This includes attention, retrieval, file operations, experiment versioning and distribution shift.

## Privacy and distribution

The complete folder contains teacher solutions and is intended for the teacher. Give learners the separate **ai-academy-student-bundle.zip** in the parent outputs folder; it includes student lessons and workbooks without teacher documents or canonical answer data. Teacher pages are separate files, not protected by authentication in this offline package.

Student typed responses are retained only while the HTML page remains open. Print or save a PDF to keep them. All supplied content uses fictional or teacher-approved data. The supplied lesson examples do not require a paid account or live API.

## Sources and reproducibility

Original source: commit 16554c5564e721ecde6dbbad5cf4caf330a74076. Later source: recovery/before-16554c55-restoration at cbcdd6675ae628a5c96e64bb7b4e0488f0e36543. The preserved source JSON is bundled under tools/source-inputs.json. Seven inconsistent worked-image cards are replaced by corrected native diagrams; original cards are retained only in private source provenance. The dedicated programme contains local corrections and does not alter the restored root project.

Rebuild canonical content with Python 3 tools/build_programme.py, then tools/render_programme.py and tools/build_guide.py. Generate Word files with tools/export_word.py (python-docx and Pillow). Generate PDFs and browser checks with Node tools/export_pdf.mjs (playwright-core and Chrome; PLAYWRIGHT_MODULE and CHROME_PATH can override local paths). Validate content with tools/validate_content.py and exported editions with tools/validate_downloads.py.

Technical review references for the corrected concepts: [probability calibration](https://scikit-learn.org/stable/modules/calibration.html), [data leakage](https://scikit-learn.org/stable/common_pitfalls.html), [diffusion pipelines](https://huggingface.co/docs/diffusers/using-diffusers/write_own_pipeline), [paired comparisons and uncertainty](https://arxiv.org/abs/1606.05328), and [copyright fair use](https://www.copyright.gov/fair-use/).

This is a reviewed teaching package, not a classroom trial. Teacher observation must establish suitable pacing, support and readiness for actual learners. Nothing has been deployed.

## Teaching-method revision

All 264 lessons now include retrieval, modelling, fading help, individual reasoning checks, independent transfer, feedback and delayed return. All 264 selected assessment prompts are distinct; 33 repeated source lessons have new parallel cases and the 12 Python readiness lessons have new executable cases. These checks establish curriculum structure and answer alignment, not effectiveness with real learners. Use reports/classroom-pilot.csv to record actual evidence.

Current PDFs use tools/export_pdf_local.py (PyMuPDF Story), with long comparison tables printed as labelled rows to preserve pagination for readable pagination. Current desktop and phone browser navigation and interactive checks pass; see reports/classroom-browser-validation.json. Word pagination has not been rendered.

After rebuilding content, run tools/build_method_guides.py, tools/validate_teaching_method.py and tools/validate_links.py in addition to the existing checks.

## Weekly examples and pictorial teaching

Three lesson agents each owned 88 weekly reviews, covering all 252 main weeks and 12 readiness lessons. Every week now has an explicit end goal, a topic-specific worked case, a labelled pictorial trace, a changed-condition comparison, an explanation question, a reasoned teacher key and project evidence. There are 264 new trace diagrams and 110 additional numerical plots/grids/weighted models, distributed as editable SVG and high-resolution PNG.

Open PICTORIAL_LESSONS.html to find a worked picture and its complete lesson. The original sections remain intact. Supported picture practice is distinct from the separately selected independent assessment. Python readiness checks follow the actual twelve topic titles; base and changed/error programs are executed.

Editorial review covers every case:176 received author-to-author review and 88 root peer review. Reports record limitations and resolved findings. Current Word/PDF checks verify the new pictures as well as text. Classroom impact and browser layout remain unverified under the current restrictions.

Rebuild after authoring with tools/draw_lesson_visuals.py and tools/draw_topic_visuals.py (PyMuPDF), tools/build_programme.py, tools/render_programme.py, tools/build_pictorial_hub.py, tools/build_method_guides.py and tools/build_guide.py. The READY.json manifest gates the full 264-case integration; validate with tools/validate_lesson_upgrades.py and tools/validate_bridge_alignment.py as well as the existing checks.

The completed classroom improvements and validation evidence are in [reports/CLASSROOM_IMPROVEMENTS.md](reports/CLASSROOM_IMPROVEMENTS.md). Hosted drafts and practice progress stay in the current browser; keep printed or downloaded evidence for the portfolio.
