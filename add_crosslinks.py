#!/usr/bin/env python3
"""
add_crosslinks.py — Convert bare RC-XX-XX article ID references in kb/ articles
into working markdown hyperlinks.

Usage:
    python add_crosslinks.py           # dry run: prints what would change
    python add_crosslinks.py --apply   # writes changes to files

What it does:
  - Reads meta/KB-INDEX.md to build an ID → (title, filename) map
  - For each article, matches occurrences like:
      RC-AI-02 — AI Writing Tools      →  [RC-AI-02 — AI Writing Tools](RC-AI-02_AI-Writing-Tools.md)
      RC-AI-02                         →  [RC-AI-02 — AI Writing Tools](RC-AI-02_AI-Writing-Tools.md)
  - Skips patterns already inside a markdown link [...](...)
  - Skips code blocks, the KB-REFERENCE-MAP.md stub, and index.md

Strategy: uses the canonical title from KB-INDEX.md rather than trying to parse the
inline title text. This prevents the regex from "eating" words that follow the title.
For each ID, we first try to match "ID — Canonical Title", then fall back to bare "ID".

Safe to re-run: already-linked IDs are not double-linked.
"""

import os
import re
import sys

KB_DIR = "kb"
INDEX_FILE = "meta/KB-INDEX.md"
APPLY = "--apply" in sys.argv

# ── 1. Build ID → (title, filename) map from KB-INDEX.md ──────────────────────

id_map = {}  # e.g. "RC-AI-02" → ("AI Writing Tools", "RC-AI-02_AI-Writing-Tools.md")

with open(INDEX_FILE, encoding="utf-8") as fh:
    for line in fh:
        m = re.match(r'\|\s*(RC-[A-Z0-9-]+)\s*\|\s*(.+?)\s*\|\s*(RC-\S+\.md)\s*\|', line)
        if m:
            id_map[m.group(1).strip()] = (m.group(2).strip(), m.group(3).strip())

print(f"Loaded {len(id_map)} article IDs from {INDEX_FILE}")

# ── 2. Build per-ID patterns (longest IDs first to avoid partial matches) ─────

# Sort IDs longest-first so RC-NAV-UI-01 is matched before RC-NAV
sorted_ids = sorted(id_map.keys(), key=len, reverse=True)

def make_per_id_pattern(article_id, title):
    """
    Returns a regex that matches:
      - "RC-XX-XX — Canonical Title"  (with em dash or double hyphen)
      - "RC-XX-XX"                    (bare ID)
    Not preceded by [ (already inside a link label).
    """
    eid = re.escape(article_id)
    etitle = re.escape(title)
    # Try "ID — Title" first (with optional em dash variations), then bare ID
    return re.compile(
        rf'(?<!\[)(?<!\]\()({eid}(?:\s*[—\-]{{1,2}}\s*{etitle})?)(?!\])',
    )

# Pre-compile all patterns
patterns = [
    (article_id, id_map[article_id][0], id_map[article_id][1],
     make_per_id_pattern(article_id, id_map[article_id][0]))
    for article_id in sorted_ids
]

def linkify_line(line):
    """Apply all ID→link substitutions to a single line."""
    for article_id, title, filename, pattern in patterns:
        link_text = f"[{article_id} — {title}]({filename})"

        def replacer(m, aid=article_id, t=title, fn=filename):
            matched = m.group(1)
            # Don't re-link if already inside [...](...)
            # Check what follows the match
            return f"[{aid} — {t}]({fn})"

        line = pattern.sub(replacer, line)
    return line

# ── 3. Process each file ───────────────────────────────────────────────────────

skip_files = {"KB-REFERENCE-MAP.md", "index.md"}
changed_files = []

for fname in sorted(os.listdir(KB_DIR)):
    if not fname.endswith(".md"):
        continue
    if fname in skip_files:
        continue

    fpath = os.path.join(KB_DIR, fname)
    with open(fpath, encoding="utf-8") as fh:
        original = fh.read()

    lines = original.split("\n")
    new_lines = []
    in_code_block = False

    for line in lines:
        # Track fenced code blocks
        if re.match(r'^\s*(`{3,}|~{3,})', line):
            in_code_block = not in_code_block

        if in_code_block:
            new_lines.append(line)
            continue

        new_lines.append(linkify_line(line))

    updated = "\n".join(new_lines)

    if updated != original:
        changed_files.append(fname)
        if APPLY:
            with open(fpath, "w", encoding="utf-8") as fh:
                fh.write(updated)

# ── 4. Report ──────────────────────────────────────────────────────────────────

mode = "APPLIED" if APPLY else "DRY RUN"
print(f"\n[{mode}] {len(changed_files)} files would be/were updated:\n")
for f in changed_files:
    print(f"  {f}")

if not APPLY:
    print("\nRun with --apply to write changes.")
