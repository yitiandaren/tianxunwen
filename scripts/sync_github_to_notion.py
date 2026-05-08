import os
import json
import requests

# =========================================
# CONFIG
# =========================================

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")

DATABASE_ID = "e4719781349347cfa1262a3aff867558"

INPUT_FILE = "data/tx_index.json"

NOTION_VERSION = "2022-06-28"

# =========================================
# HEADERS
# =========================================

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

# =========================================
# LOAD INDEX
# =========================================

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("items", [])

# =========================================
# QUERY EXISTING PAGES
# =========================================

existing_pages = {}

query_url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

response = requests.post(
    query_url,
    headers=headers
)

result = response.json()

for row in result.get("results", []):

    props = row.get("properties", {})

    tx_id = ""

    if "TX-ID" in props:

        rich_text = props["TX-ID"].get(
            "rich_text",
            []
        )

        if rich_text:
            tx_id = rich_text[0].get(
                "plain_text",
                ""
            )

    if tx_id:
        existing_pages[tx_id] = row["id"]

# =========================================
# SYNC
# =========================================

created = 0
updated = 0

for item in items:

    if not isinstance(item, dict):
        continue

    tx_id = item.get("tx_id", "")

    if not tx_id:
        continue

    subject = item.get("subject", "")

    category = item.get("category", "")

    summary = item.get(
        "meta_description",
        ""
    )

    payload = {
        "properties": {

            "TX-ID": {
                "rich_text": [
                    {
                        "text": {
                            "content": tx_id
                        }
                    }
                ]
            },

            "主題": {
                "title": [
                    {
                        "text": {
                            "content": subject
                        }
                    }
                ]
            },

            "摘要": {
                "rich_text": [
                    {
                        "text": {
                            "content": summary[:1800]
                        }
                    }
                ]
            }
        }
    }

    # =====================================
    # CATEGORY
    # =====================================

    if category:

        payload["properties"]["分類"] = {
            "select": {
                "name": category
            }
        }

    # =====================================
    # UPDATE
    # =====================================

    if tx_id in existing_pages:

        page_id = existing_pages[tx_id]

        update_url = f"https://api.notion.com/v1/pages/{page_id}"

        response = requests.patch(
            update_url,
            headers=headers,
            json=payload
        )

        print(f"Updated: {tx_id}")

        updated += 1

    # =====================================
    # CREATE
    # =====================================

    else:

        create_payload = {
            "parent": {
                "database_id": DATABASE_ID
            },
            **payload
        }

        create_url = "https://api.notion.com/v1/pages"

        response = requests.post(
            create_url,
            headers=headers,
            json=create_payload
        )

        print(f"Created: {tx_id}")

        created += 1

print("=================================")
print(f"Created: {created}")
print(f"Updated: {updated}")
print("GitHub → Notion sync completed.")
