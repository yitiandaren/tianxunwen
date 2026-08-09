import json
import os
import re
from datetime import datetime, timezone

import yaml

ARCHIVE_DIR = "archive"
OUTPUT_FILE = "data/tx_index.json"

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


tx_items = []

for root, dirs, filenames in os.walk(ARCHIVE_DIR):
    dirs.sort()
    for filename in sorted(filenames):
        if not filename.endswith(".md"):
            continue

        path = os.path.join(root, filename)
        metadata = load_metadata(path)

        tx_items.append({
            "yts_id": derive_yts_id(metadata),
            "tx_id": metadata.get("tx_id", ""),
            "legacy_id": metadata.get("legacy_id", ""),
            "old_id": metadata.get("old_id", ""),
            "subject": metadata.get("subject", ""),
            "show_time": str(metadata.get("show_time", "")),
            "category": metadata.get("category", ""),
            "tags": metadata.get("tags", []),
            "keywords": metadata.get("keywords", []),
            "publish_status": metadata.get("publish_status", ""),
            "related_ids": metadata.get("related_ids", []),
            "meta_description": metadata.get("meta_description", ""),
            "file_name": filename,
            "github_path": path,
            "content_status": metadata.get("content_status", ""),
            "visibility": metadata.get("visibility", ""),
            "topic_family": metadata.get("topic_family", ""),
            "semantic_cluster": metadata.get("semantic_cluster", []),
        })

output = {
    "schema_name": "suxing_tx_index",
    "version": "2.1",
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "source": "archive/**/*.md",
    "id_policy": {
        "canonical_master_id": "yts_id",
        "archive_id": "tx_id",
        "legacy_id": "legacy_id"
    },
    "total_count": len(tx_items),
    "items": sorted(tx_items, key=lambda item: item["tx_id"])
}

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print("===================================")
print("天訊文索引建立完成")
print(f"輸出檔案：{OUTPUT_FILE}")
print(f"總篇數：{len(tx_items)}")
print("===================================")
