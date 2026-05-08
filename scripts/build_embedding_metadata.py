import os
import re
import yaml
import hashlib
from datetime import datetime

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

        tx_id = metadata.get("tx_id", "")

        embedding_text = metadata.get(
            "embedding_text",
            ""
        )

        if not embedding_text:
            continue

        embedding_hash = hashlib.sha256(
            embedding_text.encode("utf-8")
        ).hexdigest()

        embedding_id = f"emb_{tx_id}"

        updated = False

        if metadata.get("embedding_id") != embedding_id:
            metadata["embedding_id"] = embedding_id
            updated = True

        if metadata.get("embedding_hash") != embedding_hash:
            metadata["embedding_hash"] = embedding_hash
            updated = True

        current_time = datetime.utcnow().isoformat()

        if updated:
            metadata["embedding_updated_at"] = current_time

            new_frontmatter = yaml.safe_dump(
                metadata,
                allow_unicode=True,
                sort_keys=False
            ).strip()

            new_content = (
                f"---\n"
                f"{new_frontmatter}\n"
                f"---\n"
                f"{body}"
            )

            with open(path, "w", encoding="utf-8") as f:
                f.write(new_content)

            updated_count += 1

            print(
                f"Embedding metadata updated: "
                f"{tx_id}"
            )

print(
    f"Embedding metadata build completed. "
    f"Updated files: {updated_count}"
)
