import os
import re
import sys

ARCHIVE_DIR = "archive"

required_fields = [
    "tx_id",
    "subject",
    "show_time",
    "category",
    "publish_status",
    "license"
]

tx_id_pattern = re.compile(r"^TX-\d{8}-\d{3}$")
frontmatter_pattern = re.compile(r"---(.*?)---", re.DOTALL)

errors = []
seen_tx_ids = set()

def parse_frontmatter(content):
    match = frontmatter_pattern.search(content)
    if not match:
        return {}

    block = match.group(1)
    data = {}

    for line in block.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')

    return data

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
            if field not in metadata or metadata[field] == "":
                errors.append(f"{path}: 缺少必要欄位 {field}")

        tx_id = metadata.get("tx_id", "")

        if tx_id:
            if not tx_id_pattern.match(tx_id):
                errors.append(f"{path}: tx_id 格式錯誤：{tx_id}")

            if tx_id in seen_tx_ids:
                errors.append(f"{path}: tx_id 重複：{tx_id}")

            seen_tx_ids.add(tx_id)

        expected_filename = f"{tx_id}.md" if tx_id else ""
        if expected_filename and file != expected_filename:
            errors.append(f"{path}: 檔名與 tx_id 不一致，應為 {expected_filename}")

if errors:
    print("驗證失敗：")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("驗證通過：所有天訊文格式符合 v1.0 基本規則")
print(f"檢查篇數：{len(seen_tx_ids)}")
