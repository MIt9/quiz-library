#!/usr/bin/env python3
"""Validate every quiz file and (re)generate index.json.

Usage: build_index.py          write index.json
       build_index.py --check  fail if index.json is out of date
Mirrors the app's Question.parseList rules.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANG_TITLES = {"uk": "Українська", "en": "English"}


def validate(path: Path) -> int:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise ValueError("root must be a non-empty array")
    ids = set()
    for i, q in enumerate(data, 1):
        def fail(msg):
            raise ValueError(f"question #{i}: {msg}")

        if not isinstance(q, dict):
            fail("must be an object")
        qid = q.get("id")
        if isinstance(qid, bool) or not isinstance(qid, (str, int, float)) or str(qid) == "":
            fail('"id" required (string or number)')
        if str(qid) in ids:
            fail(f'duplicate id "{qid}"')
        ids.add(str(qid))
        if not isinstance(q.get("question"), str) or not q["question"].strip():
            fail('"question" must be a non-empty string')
        opts = q.get("options")
        if not isinstance(opts, list) or len(opts) != 4 or any(
            not isinstance(o, str) or not o.strip() for o in opts
        ):
            fail('"options" must be exactly 4 non-empty strings')
        ci = q.get("correct_index")
        if isinstance(ci, bool) or not isinstance(ci, int) or not 0 <= ci <= 3:
            fail('"correct_index" must be an integer 0-3')
    return len(data)


def build() -> dict:
    languages = {}
    for lang_dir in sorted(p for p in ROOT.iterdir() if p.is_dir() and p.name in LANG_TITLES):
        quizzes = []
        for f in sorted(lang_dir.glob("*.json")):
            rel = f.relative_to(ROOT).as_posix()
            try:
                count = validate(f)
            except (ValueError, json.JSONDecodeError) as e:
                sys.exit(f"{rel}: {e}")
            quizzes.append({
                "file": rel,
                "title": f.stem.replace("-", " ").replace("_", " ").title(),
                "questions": count,
            })
        if quizzes:
            languages[lang_dir.name] = {"title": LANG_TITLES[lang_dir.name], "quizzes": quizzes}
    return {"version": 1, "languages": languages}


def main():
    text = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    index = ROOT / "index.json"
    if "--check" in sys.argv:
        if not index.exists() or index.read_text(encoding="utf-8") != text:
            sys.exit("index.json is out of date: run scripts/build_index.py")
        print("ok")
    else:
        index.write_text(text, encoding="utf-8")
        print("index.json written")


if __name__ == "__main__":
    main()
