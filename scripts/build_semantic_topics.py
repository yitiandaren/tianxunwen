import os
import re
import yaml

ARCHIVE_DIR = "archive"
TOPIC_FILE = "core/topic_families_v1.yaml"

frontmatter_pattern = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def split_frontmatter(content):
    match = frontmatter_pattern.match(content)
    if not match:
        return None, content
    return match.group(1), content[match.end():]

def load_topic_families():
    with open(TOPIC_FILE, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data.get("topic_families", {})

def score_topic(text, keywords):
    score = 0
    for keyword in keywords:
        if keyword in text:
            score += 1
    return score

topic_families = load_topic_families()

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
        keywords = metadata.get("keywords", []) or []
        tags = metadata.get("tags", []) or []
        category = metadata.get("category", "")

        combined_text = "\n".join([
            subject,
            category,
            " ".join(keywords),
            " ".join(tags),
            body
        ])

        scores = []

        for topic_name, topic_data in topic_families.items():
            topic_keywords = topic_data.get("keywords", [])
            score = score_topic(combined_text, topic_keywords)
            scores.append((score, topic_name))

        scores.sort(reverse=True)

        best_score, best_topic = scores[0] if scores else (0, "")

        updated = False

        if best_score > 0:
            if metadata.get("topic_family") != best_topic:
                metadata["topic_family"] = best_topic
                updated = True

            # semantic_cluster 初版：取命中的 topic keywords
            cluster = []
            topic_keywords = topic_families.get(best_topic, {}).get("keywords", [])

            for keyword in topic_keywords:
                if keyword in combined_text and keyword not in cluster:
                    cluster.append(keyword)

            if not cluster:
                cluster = [best_topic]

            if metadata.get("semantic_cluster") != cluster:
                metadata["semantic_cluster"] = cluster
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
            print(f"Semantic topics updated: {path} → {metadata.get('topic_family')}")

print(f"Semantic topic build completed. Updated files: {updated_count}")
