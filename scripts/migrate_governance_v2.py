import os
import re
import yaml

ARCHIVE_DIR = "archive"

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

STATUS_MAP = {
    "published": "published",
    "draft": "structured",
    "internal": "archived_internal",
    "restricted": "restricted",
    "已發布": "published",
    "待發布": "structured",
    "隱藏": "archived_internal",
    "全平台完成": "published"
}

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

        if "content_status" not in metadata or metadata["content_status"] in [None, "", []]:
            old_status = metadata.get("publish_status", "draft")
            metadata["content_status"] = STATUS_MAP.get(old_status, "structured")
            updated = True

        if "visibility" not in metadata or metadata["visibility"] in [None, "", []]:
            if metadata.get("content_status") in ["published", "publish_ready"]:
                metadata["visibility"] = "public"
            elif metadata.get("content_status") in ["archived_internal"]:
                metadata["visibility"] = "internal"
            elif metadata.get("content_status") in ["restricted"]:
                metadata["visibility"] = "restricted"
            else:
                metadata["visibility"] = "internal"
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
            print(f"Migrated governance v2: {path}")

print(f"Governance v2 migration completed. Updated files: {updated_count}")
