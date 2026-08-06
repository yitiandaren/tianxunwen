import os
import re
import sys
from datetime import datetime

import yaml

ARCHIVE_DIR = "archive"
SCHEMA_FILE = "schema/tx_metadata_schema.yaml"

FRONTMATTER_PATTERN = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
TX_ID_PATTERN = re.compile(r"^TX-(\d{14})$")
YTS_ID_PATTERN = re.compile(r"^YTS-TX-(\d{14})-(\d{3})$")
LEGACY_ID_PATTERN = re.compile(r"^TX-\d{8}-\d{3}$")


def parse_frontmatter(content: str) -> dict:
    match = FRONTMATTER_PATTERN.match(content)
    if not match:
        return {}
    return yaml.safe_load(match.group(1)) or {}


def timestamp_from_show_time(value: object) -> str:
    if isinstance(value, datetime):
        return value.strftime("%Y%m%d%H%M%S")
    digits = re.sub(r"\D", "", str(value or ""))
    return digits[:14]


with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
    schema = yaml.safe_load(f) or {}

required_fields = schema.get("required_fields", [])
allowed_content_status = set(schema.get("allowed_content_status", []))
allowed_visibility = set(schema.get("allowed_visibility", []))
required_array_fields = schema.get("required_array_fields", [])

errors = []
seen_tx_ids = set()
seen_yts_ids = set()
checked_files = 0

for root, dirs, filenames in os.walk(ARCHIVE_DIR):
    dirs.sort()
    for filename in sorted(filenames):
        if not filename.endswith(".md"):
            continue

        checked_files += 1
        path = os.path.join(root, filename)

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

        tx_id = str(metadata.get("tx_id", ""))
        tx_match = TX_ID_PATTERN.fullmatch(tx_id)
        if not tx_match:
            errors.append(f"{path}: tx_id 格式錯誤：{tx_id}；應為 TX-YYYYMMDDHHMMSS")
            tx_timestamp = ""
        else:
            tx_timestamp = tx_match.group(1)
            if tx_id in seen_tx_ids:
                errors.append(f"{path}: tx_id 重複：{tx_id}")
            seen_tx_ids.add(tx_id)

            expected_filename = f"{tx_id}.md"
            if filename != expected_filename:
                errors.append(f"{path}: 檔名與 tx_id 不一致，應為 {expected_filename}")

        yts_id = str(metadata.get("yts_id", "") or "")
        if yts_id:
            yts_match = YTS_ID_PATTERN.fullmatch(yts_id)
            if not yts_match:
                errors.append(
                    f"{path}: yts_id 格式錯誤：{yts_id}；"
                    "應為 YTS-TX-YYYYMMDDHHMMSS-SEQ"
                )
            else:
                yts_timestamp, sequence = yts_match.groups()
                if tx_timestamp and yts_timestamp != tx_timestamp:
                    errors.append(f"{path}: yts_id 與 tx_id 的時間戳不一致")
                if sequence != "001":
                    errors.append(f"{path}: 單一 TX 原典的 yts_id SEQ 目前應為 001")
                if yts_id in seen_yts_ids:
                    errors.append(f"{path}: yts_id 重複：{yts_id}")
                seen_yts_ids.add(yts_id)

        legacy_id = str(metadata.get("legacy_id", "") or "")
        if legacy_id and not LEGACY_ID_PATTERN.fullmatch(legacy_id):
            errors.append(
                f"{path}: legacy_id 格式錯誤：{legacy_id}；"
                "應為 TX-YYYYMMDD-NNN"
            )

        publish_code = str(metadata.get("publish_code", "") or "")
        if tx_timestamp and publish_code and publish_code != tx_timestamp:
            errors.append(
                f"{path}: publish_code 與 tx_id 不一致："
                f"{publish_code} != {tx_timestamp}"
            )

        show_timestamp = timestamp_from_show_time(metadata.get("show_time"))
        if tx_timestamp and show_timestamp != tx_timestamp:
            errors.append(
                f"{path}: show_time 與 tx_id 不一致："
                f"{show_timestamp or '(空值)'} != {tx_timestamp}"
            )

        content_status = metadata.get("content_status")
        if content_status and content_status not in allowed_content_status:
            errors.append(f"{path}: content_status 不合法：{content_status}")

        visibility = metadata.get("visibility")
        if visibility and visibility not in allowed_visibility:
            errors.append(f"{path}: visibility 不合法：{visibility}")

        for field in required_array_fields:
            if not isinstance(metadata.get(field), list):
                errors.append(f"{path}: {field} 必須是 list")

if errors:
    print("驗證失敗：")
    for error in errors:
        print(f"- {error}")
    sys.exit(1)

print("===================================")
print("TX Governance v2.1 Validation Passed")
print(f"Checked files: {checked_files}")
print(f"Unique tx_id: {len(seen_tx_ids)}")
print(f"Records with yts_id: {len(seen_yts_ids)}")
print("===================================")
