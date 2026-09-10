#!/usr/bin/env python3
"""Convert the approved AI Academy Word curriculum into server-side web data."""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


LEVELS = {
    "AI-1_Explorer": {
        "slug": "ai-1",
        "code": "AI-1",
        "name": "Explorer",
        "ages": "Ages 7–9",
        "accent": "sky",
        "summary": "See how AI systems sense, decide, learn from examples, and stay under human direction.",
        "capstone": "Helpful Classroom Sorter",
        "focus": ["AI foundations", "Patterns & data", "Responsible design"],
        "phaseNames": ["Discover AI", "Sense & represent", "Learn from examples", "Predict & recommend", "Design responsibly", "Build & defend"],
    },
    "AI-2_Thinker": {
        "slug": "ai-2",
        "code": "AI-2",
        "name": "Thinker",
        "ages": "Ages 8–10",
        "accent": "violet",
        "summary": "Reason with algorithms, structured data, evaluation evidence, and transparent recommendations.",
        "capstone": "Transparent Book Recommender",
        "focus": ["Algorithms", "Evaluation", "Recommendations"],
        "phaseNames": ["Algorithms", "Structured data", "Test & evaluate", "Recommend transparently", "Agents & trust", "Build & defend"],
    },
    "AI-3_Creator": {
        "slug": "ai-3",
        "code": "AI-3",
        "name": "Creator",
        "ages": "Ages 9–11",
        "accent": "amber",
        "summary": "Build reliable generative-AI workflows with prompts, retrieval, tools, verification, and safety.",
        "capstone": "Verified Study Buddy",
        "focus": ["Generative AI", "RAG & tools", "Verification"],
        "phaseNames": ["Generate", "Prompt precisely", "Work across media", "Verify", "Retrieve & use tools", "Build & defend"],
    },
    "AI-4_ML_Builder": {
        "slug": "ai-4",
        "code": "AI-4",
        "name": "ML Builder",
        "ages": "Ages 10–12",
        "accent": "emerald",
        "summary": "Train, evaluate, improve, document, and defend a responsible machine-learning model.",
        "capstone": "Responsible Plant Classifier",
        "focus": ["Python & data", "ML metrics", "Generalization"],
        "phaseNames": ["ML lifecycle", "Prepare data", "Classify & measure", "Predict numbers", "Generalize responsibly", "Build & defend"],
    },
}

PHASE_NAMES = [
    "Discover",
    "Represent",
    "Learn",
    "Evaluate",
    "Build responsibly",
    "Create & defend",
]


def clean_text(value: str) -> str:
    value = value.replace("\u00a0", " ").replace("\u200b", "")
    value = re.sub(r"[ \t]+", " ", value)
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value.strip()


def iter_blocks(document: Document):
    for child in document.element.body.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, document)
        elif isinstance(child, CT_Tbl):
            yield Table(child, document)


def paragraph_block(paragraph: Paragraph):
    text = clean_text(paragraph.text)
    if not text:
        return None
    if re.fullmatch(r"[_\-–—. ]{10,}", text):
        return {"type": "response", "text": "Response space"}

    style = (paragraph.style.name or "Normal").strip()
    lower_style = style.lower()
    if lower_style == "title":
        kind = "title"
    elif lower_style.startswith("heading 1"):
        kind = "heading"
    elif lower_style.startswith("heading 2") or lower_style.startswith("heading 3"):
        kind = "subheading"
    elif "code" in lower_style:
        kind = "code"
    elif lower_style.startswith("list bullet"):
        return {"type": "list", "marker": "bullet", "text": text}
    elif lower_style.startswith("list number"):
        return {"type": "list", "marker": "number", "text": text}
    elif style in {"Key Idea", "Think Box", "Caution Box", "Teacher Note", "Answer Box"}:
        tones = {
            "Key Idea": "idea",
            "Think Box": "think",
            "Caution Box": "caution",
            "Teacher Note": "teacher",
            "Answer Box": "answer",
        }
        return {"type": "callout", "tone": tones[style], "text": text}
    elif text.startswith(("STEP ", "Step ")):
        kind = "step"
    else:
        kind = "paragraph"
    return {"type": kind, "text": text}


def table_block(table: Table):
    rows = []
    for row in table.rows:
        cells = [clean_text(cell.text) for cell in row.cells]
        if any(cells):
            rows.append(cells)
    if not rows:
        return None
    width = max(len(row) for row in rows)
    rows = [row + [""] * (width - len(row)) for row in rows]
    return {"type": "table", "rows": rows}


def page_label(blocks):
    for block in blocks:
        if block["type"] == "paragraph" and len(block["text"]) <= 42:
            text = block["text"]
            letters = [c for c in text if c.isalpha()]
            if letters and sum(c.isupper() for c in letters) / len(letters) > 0.75:
                return text
        if block["type"] == "table":
            for row in block["rows"][:2]:
                for cell in row:
                    first = clean_text(cell.split("\n", 1)[0])
                    letters = [c for c in first if c.isalpha()]
                    if first and len(first) <= 42 and letters and sum(c.isupper() for c in letters) / len(letters) > 0.75:
                        return first
    return "LESSON SECTION"


def derive_title(path: Path, week: int, pages, kind: str):
    for page in pages[:2]:
        for block in page["blocks"]:
            if block["type"] in {"title", "heading", "subheading", "paragraph"}:
                match = re.match(rf"Week\s+0?{week}\s*[:—–-]\s*(.+)", block["text"], re.I)
                if match:
                    return f"Week {week}: {match.group(1).strip()}"
            if kind == "teacher" and block["type"] == "table":
                for row in block["rows"][:2]:
                    for cell in row:
                        lines = [clean_text(line) for line in cell.split("\n") if clean_text(line)]
                        for index, line in enumerate(lines):
                            if re.match(rf"WEEK\s+0?{week}\b", line, re.I) and index + 1 < len(lines):
                                return f"Week {week}: {lines[index + 1]}"
    stem = path.stem
    stem = re.sub(r"^AI_Academy_AI\d_(?:Curriculum_2_0_)?", "", stem, flags=re.I)
    stem = re.sub(r"_Illustrated_Student$|_Teacher_Guide$", "", stem, flags=re.I)
    stem = re.sub(rf"^Week_0?{week}_", "", stem, flags=re.I)
    return f"Week {week}: {stem.replace('_', ' ')}" + (" — Teacher Guide" if kind == "teacher" else "")


def parse_module(path: Path, week: int, kind: str):
    document = Document(path)
    pages = []
    current = []
    title = None

    for item in iter_blocks(document):
        if isinstance(item, Paragraph):
            text = clean_text(item.text)
            if text.startswith("AI ACADEMY") and "WEEK" in text:
                if current:
                    pages.append(current)
                    current = []
                continue
            if text in {"MASTER CURRICULUM 2.0"} or "EDITION" in text and len(text) < 90:
                continue
            block = paragraph_block(item)
            if block:
                if block["type"] == "title" and title is None:
                    title = block["text"]
                current.append(block)
            has_page_break = bool(item._p.xpath('.//w:br[@w:type="page"]'))
            if has_page_break and current:
                pages.append(current)
                current = []
        else:
            block = table_block(item)
            if block:
                current.append(block)
    if current:
        pages.append(current)

    normalized_pages = []
    for index, blocks in enumerate(pages, start=1):
        label = page_label(blocks)
        removed_label = False
        cleaned = []
        for block in blocks:
            if not removed_label and block["type"] == "paragraph" and block["text"] == label:
                removed_label = True
                continue
            cleaned.append(block)
        normalized_pages.append({"number": index, "label": label, "blocks": cleaned})

    if title is None:
        title = derive_title(path, week, normalized_pages, kind)
    return {"title": title, "pages": normalized_pages}


def parse_workbook(path: Path):
    document = Document(path)
    weeks = {}
    current_week = None
    current_blocks = []

    def finish():
        nonlocal current_blocks
        if current_week is not None:
            weeks[str(current_week)] = current_blocks
        current_blocks = []

    for item in iter_blocks(document):
        if isinstance(item, Paragraph):
            text = clean_text(item.text)
            match = re.match(r"Week\s+(\d+)\s*[:—–-]\s*(.+)", text, re.I)
            if match and (item.style.name or "") in {"Title", "Heading 1"}:
                finish()
                current_week = int(match.group(1))
                current_blocks = [{"type": "title", "text": f"Week {current_week}: {match.group(2)}"}]
                continue
            if current_week is None:
                continue
            block = paragraph_block(item)
            if block:
                current_blocks.append(block)
        elif current_week is not None:
            block = table_block(item)
            if block:
                current_blocks.append(block)
    finish()
    return weeks


def extract_hero(docx_path: Path, output_dir: Path):
    try:
        with zipfile.ZipFile(docx_path) as archive:
            media = [
                name
                for name in archive.namelist()
                if name.startswith("word/media/") and name.lower().endswith((".png", ".jpg", ".jpeg", ".webp"))
            ]
            if not media:
                return None
            candidates = sorted(media, key=lambda name: archive.getinfo(name).file_size, reverse=True)
            name = candidates[0]
            data = archive.read(name)
            digest = hashlib.sha256(data).hexdigest()[:18]
            suffix = Path(name).suffix.lower().replace(".jpeg", ".jpg")
            output_name = f"{digest}{suffix}"
            target = output_dir / output_name
            if not target.exists():
                target.write_bytes(data)
            return f"/academy-art/{output_name}"
    except (zipfile.BadZipFile, KeyError):
        return None


def find_week_file(folder: Path, week: int):
    pattern = re.compile(rf"Week_0?{week}(?:_|\b)", re.I)
    matches = sorted(path for path in folder.glob("*.docx") if pattern.search(path.name) and not path.name.endswith('.tmp.docx'))
    if len(matches) != 1:
        raise RuntimeError(f"Expected one Week {week} file in {folder}, found {len(matches)}")
    return matches[0]


def build(source_root: Path, output_json: Path, hero_dir: Path):
    hero_dir.mkdir(parents=True, exist_ok=True)
    for old in hero_dir.iterdir():
        if old.is_file():
            old.unlink()

    levels = []
    for directory_name, metadata in LEVELS.items():
        level_dir = source_root / directory_name
        student_dir = level_dir / "Student_Modules"
        teacher_dir = level_dir / "Teacher_Guides"
        if not teacher_dir.is_dir():
            teacher_dir = level_dir / "Teacher_Modules"
        workbook_files = sorted((level_dir / "Workbooks").glob("*.docx"))
        if len(workbook_files) != 1:
            raise RuntimeError(f"Expected one workbook in {level_dir}, found {len(workbook_files)}")
        workbook = parse_workbook(workbook_files[0])

        weeks = []
        for week in range(1, 37):
            student_path = find_week_file(student_dir, week)
            teacher_path = find_week_file(teacher_dir, week)
            student = parse_module(student_path, week, "student")
            teacher = parse_module(teacher_path, week, "teacher")
            hero = extract_hero(student_path, hero_dir)
            weeks.append(
                {
                    "number": week,
                    "phase": (week - 1) // 6 + 1,
                    "student": student,
                    "teacher": teacher,
                    "workbook": {
                        "title": next(
                            (
                                block["text"]
                                for block in workbook.get(str(week), [])
                                if block["type"] == "title"
                            ),
                            f"Week {week} practice",
                        ),
                        "blocks": workbook.get(str(week), []),
                    },
                    "hero": hero,
                }
            )

        level = dict(metadata)
        names = level.pop("phaseNames")
        level["phases"] = [
            {"number": i + 1, "name": name, "weeks": f"{i * 6 + 1}–{i * 6 + 6}"}
            for i, name in enumerate(names)
        ]
        level["weeks"] = weeks
        levels.append(level)

    payload = {"version": "Curriculum 2.0 — Refined Edition", "levels": levels}
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(
        json.dumps(
            {
                "levels": len(levels),
                "weeks": sum(len(level["weeks"]) for level in levels),
                "heroes": len(list(hero_dir.iterdir())),
                "bytes": output_json.stat().st_size,
            }
        )
    )


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("usage: extract_curriculum.py SOURCE_ROOT OUTPUT_JSON HERO_DIR")
    build(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
