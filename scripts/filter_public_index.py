import json
import os

INPUT_FILE = "data/tx_index.json"
OUTPUT_FILE = "data/public_tx_index.json"

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"{INPUT_FILE} not found")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

public_items = []

for item in data:

    visibility = item.get("visibility", "")
    content_status = item.get("content_status", "")

    if visibility != "public":
        continue

    if content_status not in [
        "publish_ready",
        "published"
    ]:
        continue

    cleaned_item = {
        "tx_id": item.get("tx_id"),
        "subject": item.get("subject"),
        "show_time": item.get("show_time"),

        "category": item.get("category"),
        "keywords": item.get("keywords", []),

        "topic_family": item.get("topic_family", ""),
        "semantic_cluster": item.get("semantic_cluster", []),

        "meta_description": item.get(
            "meta_description",
            ""
        ),

        "related_ids": item.get(
            "related_ids",
            []
        ),

        "semantic_edges": item.get(
            "semantic_edges",
            []
        ),

        "embedding_ready": item.get(
            "embedding_ready",
            False
        ),

        "embedding_text": item.get(
            "embedding_text",
            ""
        )
    }

    public_items.append(cleaned_item)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        public_items,
        f,
        ensure_ascii=False,
        indent=2
    )

print(
    f"Public index generated. "
    f"Items: {len(public_items)}"
)
