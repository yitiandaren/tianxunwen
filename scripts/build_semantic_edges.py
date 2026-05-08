import os
import re
import yaml

ARCHIVE_DIR = "archive"

frontmatter_pattern = re.compile(
    r"^---\n(.*?)\n---\n",
    re.DOTALL
)

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
            "metadata": metadata,
            "tx_id": metadata.get("tx_id", ""),
            "topic_family": metadata.get("topic_family", ""),
            "semantic_cluster": metadata.get("semantic_cluster", []) or [],
            "related_ids": metadata.get("related_ids", []) or []
        })

def detect_relation(a, b):

    if a["topic_family"] != b["topic_family"]:
        return "related"

    overlap = len(
        set(a["semantic_cluster"])
        &
        set(b["semantic_cluster"])
    )

    if overlap >= 5:
        return "foundation_of"

    if overlap >= 3:
        return "expands"

    if overlap >= 1:
        return "continues"

    return "related"

updated_count = 0

tx_lookup = {
    item["tx_id"]: item
    for item in items
}

for item in items:

    metadata = item["metadata"]

    related_ids = item["related_ids"]

    semantic_edges = []

    for related_id in related_ids:

        target = tx_lookup.get(related_id)

        if not target:
            continue

        relation = detect_relation(item, target)

        edge = {
            "target": related_id,
            "relation": relation,
            "topic_family": target["topic_family"]
        }

        semantic_edges.append(edge)

    if semantic_edges:

        metadata["semantic_edges"] = semantic_edges

        with open(item["path"], "r", encoding="utf-8") as f:
            content = f.read()

        _, body = split_frontmatter(content)

        new_frontmatter = yaml.safe_dump(
            metadata,
            allow_unicode=True,
            sort_keys=False
        ).strip()

        new_content = (
            f"---\n"
            f"{new_frontmatter}\n"
            f"---\n"
            f"{body}"
        )

        with open(item["path"], "w", encoding="utf-8") as f:
            f.write(new_content)

        updated_count += 1

        print(
            f"Semantic edges updated: "
            f"{item['tx_id']}"
        )

print(
    f"Semantic edge build completed. "
    f"Updated files: {updated_count}"
)
