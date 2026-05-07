import os
import re
import sys
import yaml

ARCHIVE_DIR = "archive"
SCHEMA_FILE = "schema/tx_metadata_schema.yaml"

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
    schema = yaml.safe_load(f)

required_fields = schema.get("required_fields", [])

field_definitions = schema.get("field_definitions", {})

errors = []
seen_tx_ids = set()

def parse_frontmatter(content):

    match = frontmatter_pattern.match(content)

    if not match:
        return {}

    frontmatter_text = match.group(1)

    metadata = yaml.safe_load(frontmatter_text)

    return metadata or {}

for root, dirs, files in os.walk(ARCHIVE_DIR):

    for file in files:

        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        metadata = parse_frontmatter(content)

        if not metadata:
            errors.append(f"{path}: 缺少 YAML frontmatter")
            continue

        for field in required_fields:

            value = metadata.get(field)

            if value in [None, "", []]:
                errors.append(f"{path}: 缺少必要欄位 {field}")

        tx_id = metadata.get("tx_id", "")

        if tx_id:

            pattern = field_definitions.get(
                "tx_id",
                {}
            ).get("pattern")

            if pattern:

                if not re.match(pattern, tx_id):
                    errors.append(
                        f"{path}: tx_id 格式錯誤：{tx_id}"
                    )

            if tx_id in seen_tx_ids:
                errors.append(
                    f"{path}: tx_id 重複：{tx_id}"
                )

            seen_tx_ids.add(tx_id)

        for field_name, rules in field_definitions.items():

            allowed_values = rules.get("allowed_values")

            if not allowed_values:
                continue

            value = metadata.get(field_name)

            if value is None:
                continue

            if value not in allowed_values:

                errors.append(
                    f"{path}: {field_name} 不合法：{value}"
                )

if errors:

    print("驗證失敗：")

    for error in errors:
        print(f"- {error}")

    sys.exit(1)

print("===================================")
print("TX Schema Validation Passed")
print(f"Checked files: {len(seen_tx_ids)}")
print("===================================")
