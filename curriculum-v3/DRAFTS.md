# Curriculum 3 continuation — completed locally

All **252 weekly packages** are authored, reviewed and registered in protected storage. The final 112 packages cover:

| Level | Weeks | Topics |
| --- | --- | --- |
| AI 4, Grade 9 | 33–36 | Capstone hypothesis, controlled experiments, limitations and experiment defense |
| AI 5, Grade 10 | 1–36 | Generation, attention, retrieval, grounding, permissions, evaluation and capstone |
| AI 6, Grade 11 | 1–36 | Contracts, access, tests, bounded agents, recovery, operations and service capstone |
| AI 7, Grade 12 | 1–36 | Research design, sampling, uncertainty, controlled studies, reporting and defense |

Each continuation package includes three outcomes, prerequisites, vocabulary, five lesson sections, a teaching diagram, guided and exit responses, five workbook tasks with teacher explanations, two 45-minute teaching sequences, misconceptions, an independent assessment and a fresh retry. The constructed examples require no external AI account.

The continuation adds **336 DOCX files and 336 PDFs**, with 112 teaching figures. All 1,234 downloadable PDF pages were inspected on contact sheets; long-code page breaks in AI 6 Week 15 and AI 7 Week 14 were corrected and changed pages inspected at full size. Canonical source, renderer, artifact and page-image hashes are recorded in `print-review.json`. The release manifest and server imports cover all 252 weeks.

Documents are under `work/v3-docs` and `work/v3-pdf`, and figures under `work/v3-diagrams`. Audience-separated bundles are under `outputs/curriculum-continuation`: `student-continuation.zip`, `teacher-continuation.zip` and `private-canonical-continuation.zip`. Work/output directories are ignored by Git; canonical JSON, generator/checking scripts, protected blobs and release receipts are durable repository artifacts. The teacher and private archives include solutions and must remain separate from student/public assets. Older archives in `outputs/curriculum-drafts` describe an earlier draft stage.

Complete seven-level bundles are also available under `outputs/curriculum-complete`: `student-complete.zip` contains 1,008 lesson/workbook Word/PDF files and 252 diagrams; `teacher-complete.zip` contains 504 teacher-guide Word/PDF files. Both include the chapter index, lab instructions, companion Python fixtures and an artifact hash manifest. `node scripts/package-v3-complete.mjs` rebuilds these archives from protected release artifacts, checks roles and source hashes, and verifies every ZIP entry against its artifact hash. The complete teacher archive contains solutions and is for teacher access only.

Thirteen chapters include standalone local Python examples. Companion fixture programs and lab instructions are in `examples/curriculum-v3` and included in the audience bundles. Engineering examples perform no real side effects and simulate trusted session roles. Research calculations state their statistical assumptions.

## Validation

```sh
python3 scripts/verify-v3-neural-capstone.py
python3 scripts/verify-v3-generative-opening.py
python3 scripts/verify-v3-continuation.py
work/curriculum-python/bin/python scripts/check-v3-draft-documents.py
work/curriculum-python/bin/python scripts/check-v3-draft-pdfs.py --render
node scripts/verify-v3.mjs
python3 scripts/package-v3-drafts.py
npm run build
npx tsc --noEmit
node --loader ./tests/cloudflare-loader.mjs tests/academy-access.mjs
```

All listed checks passed. The continuation suite validates all 252 source structures, executes all 13 new inline examples, and checks selected retrieval, permissions, state, cache, idempotency, sampling and statistical calculations. The 336 DOCX/PDF audits found no missing canonical text, student/teacher answer leakage or text outside page bounds. These checks do not automatically assess every open-ended explanation or establish classroom effectiveness.

The production build and TypeScript check passed with all 252 registered packages. All 33 access-test groups passed, including canonical content across 756 web resources, role enforcement and reviewed bytes for 1,512 downloads, and absence of teacher solutions from public JavaScript. The resource audit verified all 3,937 protected resources. Headless Chrome passed 672 desktop/mobile chapter checks (336 new web resources at each width), four complete-map checks and no page JavaScript errors. Twelve browser-print PDFs retained canonical content; all 45 sample print pages and representative screen layouts were visually inspected. The current task is content preparation only; no website deployment is requested.

## Technical source check

The attention calculation, distinction between value width and key width, and references to the original Transformer's positional information and residual sublayers were checked against sections 3.1–3.5 of Vaswani et al., [Attention Is All You Need](https://arxiv.org/html/1706.03762v7). Numerical vectors, exercises, simplified blocks and application contracts are independently constructed teaching examples. The simplified block intentionally omits operations and is not presented as a complete Transformer.

Research interval interpretation and multiple-comparison logic were checked against the NIST handbook's [confidence interval discussion](https://www.itl.nist.gov/div898/handbook/eda/section3/eda352.htm) and [Bonferroni inequality](https://www.itl.nist.gov/div898/handbook/prc/section4/prc473.htm). The known-sigma and exact sign-flip activities use independently constructed numbers with assumptions stated in each chapter. Python testing terminology follows the [standard library documentation](https://docs.python.org/3/library/unittest.html). Copyright and retention lessons use explicitly fictional supplied policies and do not state universal legal rules.

## Enriched study editions

The latest student and teacher offline HTML collections are in `outputs/curriculum-reviewed`. See [CONTENT_REVIEW.md](CONTENT_REVIEW.md) for the 252-week screening record, targeted editorial improvements and final presentation checks. These editions supplement the original reviewed Word/PDF downloads; their additions are also included in the local portal.
