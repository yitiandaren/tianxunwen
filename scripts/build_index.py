import os
import re
import json
from datetime import datetime

ARCHIVE_DIR = "archive"
OUTPUT_FILE = "data/tx_index.json"

tx_items = []

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

        # array item
        if line.strip().startswith("- ") and current_key:
            if not isinstance(data[current_key], list):
                data[current_key] = [data[current_key]]

            data[current_key].append(
                line.strip()[2:].strip().strip('"')
            )

            continue

        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        key = key.strip()
        value = value.strip().strip('"')

        current_key = key

        # empty list support
        if value == "":
            data[key] = []
        else:
            data[key] = value

    return data

for root, dirs, files in os.walk(ARCHIVE_DIR):

    for file in files:

        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = parse_frontmatter(content)

        tx_item = {
            "tx_id": metadata.get("tx_id", ""),
            "subject": metadata.get("subject", ""),
            "show_time": metadata.get("show_time", ""),
            "category": metadata.get("category", ""),
            "tags": metadata.get("tags", []),
            "keywords": metadata.get("keywords", []),
            "publish_status": metadata.get("publish_status", ""),
            "related_ids": metadata.get("related_ids", []),
            "meta_description": metadata.get("meta_description", ""),
            "file_name": file,
            "github_path": path
        }

        tx_items.append(tx_item)

output = {
    "schema_name": "suxing_tx_index",
    "version": "1.0",
    "generated_at": datetime.utcnow().isoformat(),
    "source": "archive/*.md",
    "total_count": len(tx_items),
    "items": sorted(
        tx_items,
        key=lambda x: x["tx_id"]
    )
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("===================================")
print("天訊文索引建立完成")
print(f"輸出檔案：{OUTPUT_FILE}")
print(f"總篇數：{len(tx_items)}")
print("===================================")
