import os
import re
import sys
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

if len(sys.argv) < 2:
    print("Usage: python restrict_tx.py TX-YYYYMMDD-XXX")
    sys.exit(1)

target_tx_id = sys.argv[1]

updated = False

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

        if tx_id != target_tx_id:
            continue

        metadata["visibility"] = "restricted"
        metadata["content_status"] = "archived"

        metadata["published_platforms"] = []

        metadata["ai_policy"] = {
            "allow_embedding": False,
            "allow_public_gpt": False,
            "allow_external_ai": False
        }

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

        updated = True

        print(
            f"Restricted TX: {tx_id}"
        )

if not updated:
    print(f"TX not found: {target_tx_id}")
    sys.exit(1)

print("Restriction completed.")
