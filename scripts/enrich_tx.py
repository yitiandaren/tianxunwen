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
    "財富": "財富平衡",
    "自由": "財富平衡",
    "本元": "本元",
    "覺醒": "覺醒",
    "能量": "生命能量",
    "眾生": "眾生",
    "地球": "守地",
    "文明": "文明轉折"
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
    return value is None or value == "" or value == []

def generate_keywords(text):
    keywords = []
    for key, tag in KEYWORD_RULES.items():
        if key in text and tag not in keywords:
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

        if is_empty(metadata.get("keywords")):
            keywords = generate_keywords(body)
            if keywords:
                metadata["keywords"] = keywords
                updated = True

        if is_empty(metadata.get("meta_description")):
            desc = generate_meta_description(body)
            if desc:
                metadata["meta_description"] = desc
                updated = True

        if is_empty(metadata.get("open_question")):
            metadata["open_question"] = random.choice(DEFAULT_QUESTIONS)
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

print(f"TX enrichment completed. Updated files: {updated_count}")
