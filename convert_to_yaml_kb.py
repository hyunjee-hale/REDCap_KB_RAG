"""
convert_to_yaml_kb.py

Converts REDCap KB articles from the kb/ folder (which use a markdown
metadata table at the top) into YAML front matter format, writing results
to kb (YAML)/.

Usage:
    python convert_to_yaml_kb.py

Output:
    - One converted .md file per source article in kb (YAML)/
    - A summary printed to stdout listing successes and any parse failures
"""

import os
import re
import yaml

KB_DIR = os.path.join(os.path.dirname(__file__), "kb")
OUT_DIR = os.path.join(os.path.dirname(__file__), "kb (YAML)")

# Files to skip (not articles)
SKIP_FILES = {"KB-REFERENCE-MAP.md"}

# Regex to pull a value from a markdown table row
# Matches:  | **Field Name** | value |
ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.*?)\s*\|?\s*$")


def parse_related_topics(raw: str) -> list[dict]:
    """
    Parse 'RC-FD-02 — Online Designer; RC-FD-03 — Data Dictionary' into:
    [{"id": "RC-FD-02", "title": "Online Designer"}, ...]

    Handles em dash (—) and regular dash with spaces ( - ).
    Falls back to plain string entry if a segment can't be split.
    """
    results = []
    segments = [s.strip() for s in raw.split(";") if s.strip()]
    for seg in segments:
        # Try splitting on em dash or ' - '
        match = re.match(r"^(RC-[\w-]+)\s+[—\-]\s+(.+)$", seg)
        if match:
            results.append({"id": match.group(1).strip(), "title": match.group(2).strip()})
        else:
            # Can't parse as ID — Title; store as plain note
            results.append({"note": seg})
    return results


def parse_prerequisites(raw: str) -> list[str]:
    """
    Store prerequisites as a list of plain strings.
    Split on ';' if multiple are present.
    """
    return [s.strip() for s in raw.split(";") if s.strip()]


def domain_to_tags(domain: str) -> list[str]:
    """Generate a basic tag list from the domain string."""
    tags = [domain.lower()]
    # Add a few common secondary tags based on domain keyword
    domain_lower = domain.lower()
    if "api" in domain_lower:
        tags.append("api")
    if "survey" in domain_lower:
        tags.append("surveys")
    if "form" in domain_lower or "field" in domain_lower:
        tags.append("instruments")
    if "user" in domain_lower or "rights" in domain_lower:
        tags.append("user management")
    if "export" in domain_lower or "import" in domain_lower:
        tags.append("data")
    if "branching" in domain_lower or "logic" in domain_lower:
        tags.append("branching logic")
    if "action tag" in domain_lower:
        tags.append("action tags")
    if "longitudinal" in domain_lower:
        tags.append("longitudinal")
    if "randomiz" in domain_lower:
        tags.append("randomization")
    # Deduplicate while preserving order
    seen = set()
    result = []
    for t in tags:
        if t not in seen:
            seen.add(t)
            result.append(t)
    return result


def extract_header_block(lines: list[str]) -> tuple[dict, int]:
    """
    Find and parse the metadata table from the top of the file.
    Returns (metadata_dict, index_of_first_line_after_header).

    Expected structure:
        Line 0: article ID (e.g. "RC-FD-01")
        Line 1: blank
        Line 2: **Title**
        Line 3: blank
        Lines 4+: | **Field** | Value | rows until "---"
    """
    meta = {}
    i = 0

    # Article ID — first non-blank line
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines):
        meta["id"] = lines[i].strip()
        i += 1

    # Skip blank lines
    while i < len(lines) and not lines[i].strip():
        i += 1

    # Bold title line: **Title**
    if i < len(lines):
        title_match = re.match(r"^\*\*(.+?)\*\*\s*$", lines[i].strip())
        if title_match:
            meta["title"] = title_match.group(1).strip()
            i += 1

    # Now scan for table rows until we hit the --- separator
    table_fields = {}
    while i < len(lines):
        line = lines[i].strip()
        if line == "---":
            i += 1  # move past the ---
            break
        row_match = ROW_RE.match(line)
        if row_match:
            field = row_match.group(1).strip()
            value = row_match.group(2).strip()
            table_fields[field] = value
        i += 1

    # Map table fields to our schema
    field_map = {
        "Article ID": "id_confirm",  # confirms the ID we already got
        "Domain": "domain",
        "Applies To": "applies_to",
        "Prerequisite": "prerequisites",
        "Prerequisites": "prerequisites",
        "Version": "version",
        "Last Updated": "last_updated",
        "Author": "author",
        "Source": "source",
        "Related Topics": "related_topics_raw",
    }
    for raw_field, key in field_map.items():
        if raw_field in table_fields:
            meta[key] = table_fields[raw_field]

    # If we didn't get an ID from line 0, try the table
    if "id_confirm" in meta and "id" not in meta:
        meta["id"] = meta["id_confirm"]
    meta.pop("id_confirm", None)

    return meta, i


def build_front_matter(meta: dict) -> dict:
    """Build the structured YAML front matter dict from parsed metadata."""
    fm = {}

    fm["id"] = meta.get("id", "")
    fm["title"] = meta.get("title", "")
    fm["domain"] = meta.get("domain", "")

    applies_raw = meta.get("applies_to", "")
    if applies_raw:
        # Split on ';' if multiple values, otherwise wrap in list
        parts = [p.strip() for p in applies_raw.split(";") if p.strip()]
        fm["applies_to"] = parts if len(parts) > 1 else [applies_raw.strip()]

    prereq_raw = meta.get("prerequisites", "")
    if prereq_raw:
        fm["prerequisites"] = parse_prerequisites(prereq_raw)

    if meta.get("version"):
        fm["version"] = str(meta["version"])

    if meta.get("last_updated"):
        fm["last_updated"] = str(meta["last_updated"])

    if meta.get("source"):
        fm["source"] = meta["source"]

    related_raw = meta.get("related_topics_raw", "")
    if related_raw:
        fm["related"] = parse_related_topics(related_raw)

    if meta.get("domain"):
        fm["tags"] = domain_to_tags(meta["domain"])

    return fm


def convert_file(src_path: str, dst_path: str) -> bool:
    """Convert a single article. Returns True on success."""
    with open(src_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Strip trailing newlines from each line for processing
    stripped = [l.rstrip("\n") for l in lines]

    try:
        meta, body_start = extract_header_block(stripped)
    except Exception as e:
        print(f"  PARSE ERROR in {os.path.basename(src_path)}: {e}")
        return False

    if not meta.get("id"):
        print(f"  SKIPPED (no ID found): {os.path.basename(src_path)}")
        return False

    fm = build_front_matter(meta)

    # Body is everything after the header block
    body_lines = stripped[body_start:]

    # Strip leading blank lines from body
    while body_lines and not body_lines[0].strip():
        body_lines.pop(0)

    body = "\n".join(body_lines)

    # Render YAML (default_flow_style=False = block style; allow_unicode for em dashes etc.)
    yaml_str = yaml.dump(
        fm,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )

    output = f"---\n{yaml_str}---\n\n{body}\n"

    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w", encoding="utf-8") as f:
        f.write(output)

    return True


def main():
    files = sorted(
        f for f in os.listdir(KB_DIR)
        if f.endswith(".md") and f not in SKIP_FILES
    )

    success = 0
    failures = []

    print(f"Converting {len(files)} articles from kb/ → kb (YAML)/\n")

    for filename in files:
        src = os.path.join(KB_DIR, filename)
        dst = os.path.join(OUT_DIR, filename)

        # Always read from kb/ and write to kb (YAML)/ — overwrite any existing file
        ok = convert_file(src, dst)
        if ok:
            print(f"  OK: {filename}")
            success += 1
        else:
            failures.append(filename)

    print(f"\nDone. {success} succeeded, {len(failures)} failed.")
    if failures:
        print("Failures:")
        for f in failures:
            print(f"  - {f}")


if __name__ == "__main__":
    main()
