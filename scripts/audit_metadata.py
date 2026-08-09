import json
import os
import re
from datetime import datetime, timezone

import yaml

ARCHIVE_DIR = "archive"
OUTPUT_FILE = "data/metadata_audit.json"

FIELDS_TO_CHECK = [
    "editor_intro",
    "open_question",
    "related_ids",
    "keywords",
    "meta_description",
    "og_image",
    "published_platforms",
]

FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def load_metadata(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def derive_yts_id(metadata: dict) -> str:
    yts_id = str(metadata.get("yts_id", "") or "")
    if yts_id:
        return yts_id
    tx_id = str(metadata.get("tx_id", "") or "")
    if tx_id.startswith("TX-") and len(tx_id) == 17:
        return f"YTS-{tx_id}-001"
    return ""


items = []
missing_field_counts = {field: 0 for field in FIELDS_TO_CHECK}

for root, dirs, filenames in os.walk(ARCHIVE_DIR):
    dirs.sort()
    for filename in sorted(filenames):
        if not filename.endswith(".md"):
            continue

        path = os.path.join(root, filename)
        metadata = load_metadata(path)
        missing = []

        for field in FIELDS_TO_CHECK:
            value = metadata.get(field)
            if value is None or value == "" or value == []:
                missing.append(field)
                missing_field_counts[field] += 1

        if missing:
            items.append({
                "yts_id": derive_yts_id(metadata),
                "tx_id": metadata.get("tx_id", ""),
                "legacy_id": metadata.get("legacy_id", ""),
                "subject": metadata.get("subject", ""),
                "category": metadata.get("category", ""),
                "show_time": str(metadata.get("show_time", "")),
                "file": path,
                "missing_fields": missing,
            })

output = {
    "schema_name": "suxing_metadata_audit",
    "version": "2.1",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "total_missing_items": len(items),
    "missing_field_counts": missing_field_counts,
    "checked_fields": FIELDS_TO_CHECK,
    "items": items,
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Metadata audit completed")
print(f"Output: {OUTPUT_FILE}")
print(f"Items with missing metadata: {len(items)}")
