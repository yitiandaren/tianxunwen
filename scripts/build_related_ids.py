import os
import re
import yaml
from collections import defaultdict

ARCHIVE_DIR = "archive"

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def split_frontmatter(content):
    match = frontmatter_pattern.match(content)
    if not match:
        return None, content
    return match.group(1), content[match.end():]

items = []

for root, dirs, files in os.walk(ARCHIVE_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter_text, body = split_frontmatter(content)

        if frontmatter_text is None:
            continue

        metadata = yaml.safe_load(frontmatter_text) or {}

        items.append({
            "path": path,
            "body": body,
            "metadata": metadata,
            "tx_id": metadata.get("tx_id", ""),
            "category": metadata.get("category", ""),
            "tags": metadata.get("tags", []) or [],
            "keywords": metadata.get("keywords", []) or []
        })

def score_related(a, b):
    if a["tx_id"] == b["tx_id"]:
        return 0

    score = 0

    if a["category"] and a["category"] == b["category"]:
        score += 3

    score += len(set(a["tags"]) & set(b["tags"])) * 2
    score += len(set(a["keywords"]) & set(b["keywords"])) * 2

    return score

updated_count = 0

for item in items:
    metadata = item["metadata"]

existing_related = metadata.get("related_ids")

if isinstance(existing_related, list) and len(existing_related) > 0:
    continue

    scored = []

    for other in items:
        score = score_related(item, other)
        if score > 0:
            scored.append((score, other["tx_id"]))

    scored.sort(reverse=True)

    related_ids = [tx_id for score, tx_id in scored[:3]]

    if related_ids:
        metadata["related_ids"] = related_ids

        new_frontmatter = yaml.safe_dump(
            metadata,
            allow_unicode=True,
            sort_keys=False
        ).strip()

        with open(item["path"], "r", encoding="utf-8") as f:
            content = f.read()

        _, body = split_frontmatter(content)

        new_content = f"---\n{new_frontmatter}\n---\n{body}"

        with open(item["path"], "w", encoding="utf-8") as f:
            f.write(new_content)

        updated_count += 1
        print(f"Related IDs updated: {item['path']} → {related_ids}")

print(f"Related ID build completed. Updated files: {updated_count}")
