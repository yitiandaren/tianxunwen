import os
import re
import shutil

ARCHIVE_DIR = "archive"
RAW_DIR = "raw"

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

os.makedirs(RAW_DIR, exist_ok=True)

moved_count = 0

for root, dirs, files in os.walk(ARCHIVE_DIR):
    for file in files:
        if not file.endswith(".md"):
            continue

        source_path = os.path.join(root, file)

        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()

        if frontmatter_pattern.match(content):
            continue

        target_path = os.path.join(RAW_DIR, file)

        if os.path.exists(target_path):
            base, ext = os.path.splitext(file)
            target_path = os.path.join(RAW_DIR, f"{base}_raw{ext}")

        shutil.move(source_path, target_path)

        moved_count += 1
        print(f"Moved: {source_path} -> {target_path}")

print(f"Move completed. Moved files: {moved_count}")
