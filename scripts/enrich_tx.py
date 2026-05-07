import os
import re
from pathlib import Path

ARCHIVE_DIR = "archive"

frontmatter_pattern = re.compile(r"---(.*?)---", re.DOTALL)

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

def parse_frontmatter(content):
    match = frontmatter_pattern.search(content)

    if not match:
        return None, None

    frontmatter = match.group(1)
    body = content[match.end():]

    return frontmatter, body

def extract_metadata(frontmatter):
    metadata = {}

    for line in frontmatter.splitlines():
        if ":" not in line:
            continue

        key, value = line.split(":", 1)

        metadata[key.strip()] = value.strip()

    return metadata

def generate_keywords(text):
    keywords = set()

    for key, tag in KEYWORD_RULES.items():
        if key in text:
            keywords.add(tag)

    return list(keywords)[:5]

def generate_meta_description(text):
    text = re.sub(r"\s+", " ", text).strip()

    if len(text) <= 120:
        return text

    return text[:117] + "..."

def generate_open_question():
    import random
    return random.choice(DEFAULT_QUESTIONS)

for root, dirs, files in os.walk(ARCHIVE_DIR):

    for file in files:

        if not file.endswith(".md"):
            continue

        path = os.path.join(root, file)

        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        frontmatter, body = parse_frontmatter(content)

        if not frontmatter:
            continue

        metadata = extract_metadata(frontmatter)

        updated = False

        # keywords
        if "keywords" not in metadata or metadata["keywords"] in ["", "[]"]:
            keywords = generate_keywords(body)

            keyword_block = "\n".join([f'  - "{k}"' for k in keywords])

            frontmatter += f'\nkeywords:\n{keyword_block}\n'

            updated = True

        # meta_description
        if (
            "meta_description" not in metadata
            or metadata["meta_description"] == ""
        ):
            desc = generate_meta_description(body)

            frontmatter += f'\nmeta_description: "{desc}"\n'

            updated = True

        # open_question
        if (
            "open_question" not in metadata
            or metadata["open_question"] == ""
        ):
            q = generate_open_question()

            frontmatter += f'\nopen_question: "{q}"\n'

            updated = True

        if updated:

            new_content = f"---{frontmatter}---{body}"

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"Updated: {path}")

print("TX enrichment completed")
