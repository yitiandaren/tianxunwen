import json
import os
import sys

NOTION_SCHEMA_FILE = "data/notion_schema_inventory.json"
GOVERNANCE_SCHEMA_FILE = "data/governance_schema_dictionary.json"
OUTPUT_FILE = "data/schema_validation_report.json"

for path in [NOTION_SCHEMA_FILE, GOVERNANCE_SCHEMA_FILE]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"{path} not found")

with open(NOTION_SCHEMA_FILE, "r", encoding="utf-8") as f:
    notion_schema = json.load(f)

with open(GOVERNANCE_SCHEMA_FILE, "r", encoding="utf-8") as f:
    governance_schema = json.load(f)

notion_properties = {
    prop["name"]: prop
    for prop in notion_schema.get("properties", [])
}

errors = []
warnings = []
checked_fields = []

for field in governance_schema.get("fields", []):
    notion_name = field.get("notion_name")
    expected_type = field.get("type")
    expected_options = field.get("options", {})

    checked_fields.append(notion_name)

    if notion_name not in notion_properties:
        errors.append({
            "field": notion_name,
            "issue": "missing_notion_field",
            "message": f"Notion 缺少欄位：{notion_name}"
        })
        continue

    notion_prop = notion_properties[notion_name]
    actual_type = notion_prop.get("type")

    if actual_type != expected_type:
        errors.append({
            "field": notion_name,
            "issue": "type_mismatch",
            "expected": expected_type,
            "actual": actual_type
        })

    if expected_type in ["select", "multi_select"]:
        notion_options = [
            opt.get("name", "")
            for opt in notion_prop.get("options", [])
        ]

        for option_name in expected_options.keys():
            if option_name not in notion_options:
                errors.append({
                    "field": notion_name,
                    "issue": "missing_option",
                    "option": option_name,
                    "message": f"{notion_name} 缺少選項：{option_name}"
                })

        extra_options = [
            opt for opt in notion_options
            if opt not in expected_options.keys()
        ]

        if extra_options:
            warnings.append({
                "field": notion_name,
                "issue": "extra_options",
                "options": extra_options,
                "message": f"{notion_name} 有未登記選項"
            })

report = {
    "schema_name": "suxing_schema_validation_report",
    "version": "1.0",
    "checked_fields": checked_fields,
    "error_count": len(errors),
    "warning_count": len(warnings),
    "errors": errors,
    "warnings": warnings
}

os.makedirs("data", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("Schema validation completed.")
print(f"Errors: {len(errors)}")
print(f"Warnings: {len(warnings)}")
print(f"Output: {OUTPUT_FILE}")

if errors:
    sys.exit(1)
