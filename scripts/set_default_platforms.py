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

        current = metadata.get("published_platforms")

        if (
            current is None
            or current == ""
            or current == []
        ):

            metadata["published_platforms"] = [
                "GitHub"
            ]

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

            print(f"Updated: {path}")

print(
    f"Default platforms set. Updated files: {updated_count}"
)
