import os
import re
import yaml

ARCHIVE_DIR = "archive"

STATUS_MAP = {
    "已發布": "published",
    "待發布": "draft",
    "隱藏": "restricted",
    "全平台完成": "published"
}

VISIBILITY_MAP = {
    "公開": "public",
    "內部": "internal",
    "限制": "restricted",
    "隱藏": "hidden"
}

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

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
        updated = False

        old_status = metadata.get("publish_status")
        if old_status in STATUS_MAP:
            metadata["publish_status"] = STATUS_MAP[old_status]
            updated = True

        old_visibility = metadata.get("visibility")
        if old_visibility in VISIBILITY_MAP:
            metadata["visibility"] = VISIBILITY_MAP[old_visibility]
            updated = True

        if "visibility" not in metadata or metadata["visibility"] in [None, "", []]:
            metadata["visibility"] = "public"
            updated = True

        if "license" not in metadata or metadata["license"] in [None, "", []]:
            metadata["license"] = "CC BY-ND 4.0"
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
            print(f"Normalized: {path}")

print(f"Metadata normalization completed. Updated files: {updated_count}")
