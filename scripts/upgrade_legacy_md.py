import os
import re
import yaml

ARCHIVE_DIR = "archive"

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
tx_id_pattern = re.compile(r"(TX-\d{8}-\d{3})")
h1_pattern = re.compile(r"^#\s+天訊文\s+(TX-\d{8}-\d{3})[｜　|\s]*(.*?)[｜　|\s]*一天大人", re.MULTILINE)

def extract_table_value(content, field_name):
    pattern = re.compile(rf"\|\s*{re.escape(field_name)}\s*\|\s*(.*?)\s*\|")
    match = pattern.search(content)
    if not match:
        return ""
    return match.group(1).strip()

def normalize_show_time(value):
    if not value:
        return ""

    value = value.strip()

    # 2026/01/11 11:19:21 → 2026-01-11T11:19:21
    match = re.match(r"(\d{4})/(\d{2})/(\d{2})\s+(\d{2}):(\d{2}):(\d{2})", value)
    if match:
        y, m, d, hh, mm, ss = match.groups()
        return f"{y}-{m}-{d}T{hh}:{mm}:{ss}"

    # 2026年01月11日 11:19:21 → 2026-01-11T11:19:21
    match = re.match(r"(\d{4})年(\d{2})月(\d{2})日\s+(\d{2}):(\d{2}):(\d{2})", value)
    if match:
        y, m, d, hh, mm, ss = match.groups()
        return f"{y}-{m}-{d}T{hh}:{mm}:{ss}"

    return value

def publish_code_from_show_time(show_time):
    if not show_time:
        return ""

    digits = re.sub(r"\D", "", show_time)
    return digits[:14]

def split_keywords(value):
    if not value:
        return []

    parts = re.split(r"[、,，\s]+", value)
    return [p.strip() for p in parts if p.strip()]

def infer_category(content, keywords):
    text = content + " " + " ".join(keywords)

    if "財富" in text or "金錢" in text:
        return "財富平衡"
    if "AI" in text or "文明" in text or "時代" in text:
        return "破與強・新時代"
    if "權力" in text or "政治" in text or "真話" in text:
        return "權力與真實"
    if "眾生" in text or "地球" in text or "生命" in text:
        return "眾生與守地"
    if "行動" in text or "結果" in text:
        return "行動系統"
    if "本元" in text or "太素" in text or "覺醒" in text:
        return "本元覺醒"

    return "短偈金句"

updated_count = 0

for root, dirs, files in os.walk(ARCHIVE_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        # 已經有 frontmatter 的略過
        if frontmatter_pattern.match(content):
            continue

        tx_id_match = tx_id_pattern.search(file)
        tx_id = tx_id_match.group(1) if tx_id_match else ""

        h1_match = h1_pattern.search(content)
        subject_from_h1 = ""

        if h1_match:
            tx_id = h1_match.group(1)
            subject_from_h1 = h1_match.group(2).strip()

        subject = (
            extract_table_value(content, "主題")
            or subject_from_h1
            or file.replace(".md", "")
        )

        show_time_raw = extract_table_value(content, "現示時間")
        show_time = normalize_show_time(show_time_raw)

        keywords_raw = extract_table_value(content, "關鍵字")
        keywords = split_keywords(keywords_raw)

        category = extract_table_value(content, "分類")
        if not category:
            category = infer_category(content, keywords)

        metadata = {
            "tx_id": tx_id,
            "old_id": "",
            "subject": subject,
            "source_author": "一天大人 太素天尊",
            "source_type": "天訊文",
            "show_time": show_time,
            "publish_code": publish_code_from_show_time(show_time),
            "category": category,
            "tags": keywords,
            "keywords": keywords[:5],
            "editor_intro": "",
            "open_question": "",
            "related_ids": [],
            "meta_description": "",
            "og_image": "",
            "url_slug": f"tianxunwen-{tx_id}",
            "publish_status": "draft",
            "published_platforms": [],
            "visibility": "public",
            "license": "CC BY-ND 4.0"
        }

        new_frontmatter = yaml.safe_dump(
            metadata,
            allow_unicode=True,
            sort_keys=False
        ).strip()

        new_content = f"---\n{new_frontmatter}\n---\n{content}"

        with open(path, "w", encoding="utf-8") as f:
            f.write(new_content)

        updated_count += 1
        print(f"Upgraded legacy MD: {path}")

print(f"Legacy MD upgrade completed. Updated files: {updated_count}")
