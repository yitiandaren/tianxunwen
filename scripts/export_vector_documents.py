import json
import os

INPUT_FILE = "data/tx_index.json"
OUTPUT_FILE = "data/vector_documents.jsonl"

if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(f"{INPUT_FILE} not found")

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])

count = 0

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for item in items:
        embedding_text = item.get("embedding_text", "")
        embedding_id = item.get("embedding_id", "")

        if not embedding_text or not embedding_id:
            continue

        doc = {
            "id": embedding_id,
            "text": embedding_text,
            "metadata": {
                "tx_id": item.get("tx_id"),
                "subject": item.get("subject"),
                "show_time": item.get("show_time"),
                "content_status": item.get("content_status"),
                "visibility": item.get("visibility"),
                "category": item.get("category"),
                "topic_family": item.get("topic_family"),
                "semantic_cluster": item.get("semantic_cluster", []),
                "keywords": item.get("keywords", []),
                "related_ids": item.get("related_ids", [])
            }
        }

        f.write(json.dumps(doc, ensure_ascii=False) + "\n")
        count += 1

print(f"Vector documents exported: {count}")
print(f"Output: {OUTPUT_FILE}")
