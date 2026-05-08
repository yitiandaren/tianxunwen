import os
import re
import sys
import yaml

ARCHIVE_DIR = "archive"
SCHEMA_FILE = "schema/tx_metadata_schema.yaml"

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
tx_id_pattern = re.compile(r"^TX-\d{8}-\d{3}$")

with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
    schema = yaml.safe_load(f) or {}

required_fields = schema.get("required_fields", [])
allowed_content_status = schema.get("allowed_content_status", [])
allowed_visibility = schema.get("allowed_visibility", [])
required_array_fields = schema.get("required_array_fields", [])

errors = []
seen_tx_ids = set()

def parse_frontmatter(content):
    match = frontmatter_pattern.match(content)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}

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
            if not tx_id_pattern.match(tx_id):
                errors.append(f"{path}: tx_id 格式錯誤：{tx_id}")

            if tx_id in seen_tx_ids:
                errors.append(f"{path}: tx_id 重複：{tx_id}")

            seen_tx_ids.add(tx_id)

            expected_filename = f"{tx_id}.md"
            if file != expected_filename:
                errors.append(f"{path}: 檔名與 tx_id 不一致，應為 {expected_filename}")

        content_status = metadata.get("content_status")

        if content_status and content_status not in allowed_content_status:
            errors.append(f"{path}: content_status 不合法：{content_status}")

        visibility = metadata.get("visibility")

        if visibility and visibility not in allowed_visibility:
            errors.append(f"{path}: visibility 不合法：{visibility}")

        for field in required_array_fields:
            value = metadata.get(field)
            if not isinstance(value, list):
                errors.append(f"{path}: {field} 必須是 list")

if errors:
    print("驗證失敗：")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("===================================")
print("TX Governance v2 Validation Passed")
print(f"Checked files: {len(seen_tx_ids)}")
print("===================================")
