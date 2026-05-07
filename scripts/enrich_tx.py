import os
import re
import random
import yaml

ARCHIVE_DIR = "archive"

DEFAULT_QUESTIONS = [
    "這段內容讓你想到什麼？",
    "如果是你，你會如何選擇？",
    "你是否也曾經歷過類似狀態？",
    "你認為真正的改變從哪裡開始？",
    "你是否曾思考過這個問題？"
]

KEYWORD_RULES = {
    "AI": "AI時代",
    "人工智慧": "AI時代",
    "文明": "文明轉折",
    "時代": "時代",
    "系統": "系統",
    "宗教": "去宗教化",
    "信仰": "信仰",
    "覺醒": "覺醒",
    "覺者": "覺者",
    "本元": "本元",
    "太素": "太素",
    "道": "道",
    "法": "法",
    "經": "經",
    "心": "心",
    "念": "念",
    "靜": "靜定",
    "定": "靜定",
    "觀": "觀心",
    "順": "順隨",
    "行": "行動",
    "結果": "結果",
    "選擇": "選擇",
    "改變": "改變",
    "承載": "承載",
    "能量": "生命能量",
    "財富": "財富平衡",
    "金錢": "財富平衡",
    "自由": "自由",
    "需求": "需求",
    "眾生": "眾生",
    "生命": "生命",
    "地球": "守地",
    "權力": "權力",
    "政治": "政治",
    "責任": "責任",
    "真話": "真實",
    "角度": "角度",
    "苦": "苦",
    "破": "破",
    "穩": "穩定"
}

CATEGORY_KEYWORDS = {
    "本元覺醒": ["本元", "覺醒", "道", "太素", "生命"],
    "財富平衡": ["財富平衡", "生命能量", "需求", "自由", "承載"],
    "破與強・新時代": ["AI時代", "文明轉折", "時代", "系統", "選擇"],
    "權力與真實": ["權力", "真實", "責任", "角度", "政治"],
    "行動系統": ["行動", "結果", "系統", "選擇", "改變"],
    "素行心法": ["素行", "靜定", "觀心", "順隨", "承載"],
    "眾生與守地": ["眾生", "生命", "守地", "地球", "責任"],
    "短偈金句": ["短偈金句", "心", "道", "選擇", "覺醒"],
    "素語三百": ["素語三百", "素行", "心法", "覺醒", "實踐"]
}

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def split_frontmatter(content):

    match = frontmatter_pattern.match(content)

    if not match:
        return None, content

    frontmatter_text = match.group(1)
    body = content[match.end():]

    return frontmatter_text, body

def is_empty(value):

    return (
        value is None
        or value == ""
        or value == []
    )

def generate_keywords(text, category="", subject=""):

    keywords = []

    combined_text = f"{subject}\n{text}"

    for key, tag in KEYWORD_RULES.items():

        if key in combined_text and tag not in keywords:
            keywords.append(tag)

    for tag in CATEGORY_KEYWORDS.get(category, []):

        if tag not in keywords:
            keywords.append(tag)

    return keywords[:5]

def generate_meta_description(text):

    text = re.sub(r"\s+", " ", text).strip()
    text = text.replace('"', "'")

    if len(text) <= 120:
        return text

    return text[:117] + "..."

updated_count = 0

for root, dirs, files in os.walk(ARCHIVE_DIR):

    for file in files:

        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter_text, body = split_frontmatter(content)

        if frontmatter_text is None:
            continue

        metadata = yaml.safe_load(frontmatter_text) or {}

        updated = False

        current_keywords = metadata.get("keywords")

        if (
            current_keywords is None
            or current_keywords == ""
            or current_keywords == []
            or not isinstance(current_keywords, list)
        ):

            keywords = generate_keywords(
                body,
                metadata.get("category", ""),
                metadata.get("subject", "")
            )

            if keywords:
                metadata["keywords"] = keywords
                updated = True

        if is_empty(metadata.get("meta_description")):

            desc = generate_meta_description(body)

            if desc:
                metadata["meta_description"] = desc
                updated = True

        if is_empty(metadata.get("open_question")):

            metadata["open_question"] = random.choice(
                DEFAULT_QUESTIONS
            )

            updated = True

        if updated:

            new_frontmatter = yaml.safe_dump(
                metadata,
                allow_unicode=True,
                sort_keys=False
            ).strip()

            new_content = f"---\n{new_frontmatter}\n---\n{body}"

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)

            updated_count += 1

            print(f"Updated: {path}")

print(
    f"TX enrichment completed. Updated files: {updated_count}"
)
