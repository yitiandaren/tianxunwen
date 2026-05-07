import os
import re
import json
from datetime import datetime

ARCHIVE_DIR = "archive"
OUTPUT_FILE = "data/metadata_audit.json"

fields_to_check = [
    "editor_intro",
    "open_question",
    "related_ids",
    "keywords",
    "meta_description",
    "og_image",
    "published_platforms"
]

frontmatter_pattern = re.compile(r"---(.*?)---", re.DOTALL)

def parse_frontmatter(content):
    match = frontmatter_pattern.search(content)
    if not match:
        return {}

    block = match.group(1)
    data = {}
    current_key = None

    for line in block.splitlines():
        if not line.strip():
            continue

        if line.strip().startswith("- ") and current_key:
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(line.strip()[2:].strip().strip('"'))
            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().split("#")[0].strip().strip('"')

        current_key = key

        if value in ["", "[]"]:
            data[key] = [] if value == "[]" else ""
        else:
            data[key] = value

    return data

items = []
missing_field_counts = {field: 0 for field in fields_to_check}

for root, dirs, files in os.walk(ARCHIVE_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = parse_frontmatter(content)

        missing = []

        for field in fields_to_check:
            value = metadata.get(field)

            if value is None or value == "" or value == []:
                missing.append(field)
                missing_field_counts[field] += 1

        if missing:
            items.append({
                "tx_id": metadata.get("tx_id", ""),
                "subject": metadata.get("subject", ""),
                "category": metadata.get("category", ""),
                "show_time": metadata.get("show_time", ""),
                "file": path,
                "missing_fields": missing
            })

output = {
    "schema_name": "suxing_metadata_audit",
    "version": "1.1",
    "generated_at": datetime.utcnow().isoformat(),
    "total_missing_items": len(items),
    "missing_field_counts": missing_field_counts,
    "checked_fields": fields_to_check,
    "items": items
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("Metadata audit completed")
print(f"Output: {OUTPUT_FILE}")
print(f"Items with missing metadata: {len(items)}")
print("Missing field counts:")
for field, count in missing_field_counts.items():
    print(f"- {field}: {count}")
