import csv
import json

with open("data/id_mapping.json", "r", encoding="utf-8") as source_file:
    source = json.load(source_file)

with open("id_mapping.csv", "w", encoding="utf-8", newline="") as output_file:
    fieldnames = ["yts_id", "legacy_id", "tx_id", "legacy_filename", "new_filename", "show_time", "timestamp"]
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    for item in source.get("mappings", []):
        tx_id = item.get("new_id", "")
        writer.writerow({
            "yts_id": f"YTS-{tx_id}-001" if tx_id else "",
            "legacy_id": item.get("legacy_id", ""),
            "tx_id": tx_id,
            "legacy_filename": item.get("legacy_filename", ""),
            "new_filename": item.get("new_filename", ""),
            "show_time": item.get("show_time", ""),
            "timestamp": item.get("timestamp", "")
        })

print("ID mapping CSV rebuilt")
