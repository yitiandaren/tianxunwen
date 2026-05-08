import os
import re
import yaml

ARCHIVE_DIR = "archive"

frontmatter_pattern = re.compile(
    r"^---\n(.*?)\n---\n",
    re.DOTALL
)

def split_frontmatter(content):
    match = frontmatter_pattern.match(content)
    if not match:
        return None, content
    return match.group(1), content[match.end():]

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

        subject = metadata.get("subject", "")
        category = metadata.get("category", "")
        keywords = metadata.get("keywords", []) or []
        topic_family = metadata.get("topic_family", "")
        semantic_cluster = metadata.get("semantic_cluster", []) or []
        meta_description = metadata.get("meta_description", "")

        embedding_text = "；".join([
            f"主題：{subject}",
            f"分類：{category}",
            f"思想體系：{topic_family}",
            f"語意群：{'、'.join(semantic_cluster)}",
            f"關鍵字：{'、'.join(keywords)}",
            f"摘要：{meta_description}"
        ])

        if (
            metadata.get("embedding_text") != embedding_text
            or metadata.get("embedding_ready") is not True
        ):
            metadata["embedding_ready"] = True
            metadata["embedding_text"] = embedding_text

            new_frontmatter = yaml.safe_dump(
                metadata,
                allow_unicode=True,
                sort_keys=False
            ).strip()

            new_content = f"---\n{new_frontmatter}\n---\n{body}"

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)

            updated_count += 1
            print(f"Embedding text updated: {path}")

print(f"Embedding text build completed. Updated files: {updated_count}")
