import os
import json
import requests

NOTION_API_KEY = os.environ.get("NOTION_API_KEY")
DATABASE_ID = "e4719781349347cfa1262a3aff867558"
OUTPUT_FILE = "data/notion_schema_inventory.json"
NOTION_VERSION = "2022-06-28"

if not NOTION_API_KEY:
    raise RuntimeError("NOTION_API_KEY is not set")

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION
}

url = f"https://api.notion.com/v1/databases/{DATABASE_ID}"

response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(response.text)
    raise RuntimeError(f"Failed to fetch Notion database schema: {response.status_code}")

database = response.json()
properties = database.get("properties", {})

inventory = {
    "database_id": DATABASE_ID,
    "database_title": "",
    "property_count": len(properties),
    "properties": []
}

title_items = database.get("title", [])
if title_items:
    inventory["database_title"] = title_items[0].get("plain_text", "")

for name, prop in properties.items():
    prop_type = prop.get("type", "")

    item = {
        "name": name,
        "id": prop.get("id", ""),
        "type": prop_type
    }

    if prop_type in ["select", "multi_select", "status"]:
        options = prop.get(prop_type, {}).get("options", [])
        item["options"] = [
            {
                "name": opt.get("name", ""),
                "color": opt.get("color", "")
            }
            for opt in options
        ]

    if prop_type == "relation":
        relation = prop.get("relation", {})
        item["relation"] = {
            "database_id": relation.get("database_id", ""),
            "type": relation.get("type", "")
        }

    if prop_type == "formula":
        item["formula_type"] = prop.get("formula", {}).get("type", "")

    if prop_type == "rollup":
        rollup = prop.get("rollup", {})
        item["rollup"] = {
            "relation_property_name": rollup.get("relation_property_name", ""),
            "rollup_property_name": rollup.get("rollup_property_name", ""),
            "function": rollup.get("function", "")
        }

    inventory["properties"].append(item)

inventory["properties"].sort(key=lambda x: x["name"])

os.makedirs("data", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(inventory, f, ensure_ascii=False, indent=2)

print(f"Notion schema exported: {OUTPUT_FILE}")
print(f"Database title: {inventory['database_title']}")
print(f"Property count: {inventory['property_count']}")
