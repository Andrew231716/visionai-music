#!/usr/bin/env python3
import csv
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

PLACEHOLDER = "https://replace-with-your-r2-public-base.invalid"
root = Path(__file__).resolve().parents[1]
catalog_path = root / "music_catalog.json"

if len(sys.argv) != 2:
    raise SystemExit("Uso: python3 tools/set_r2_base_url.py https://pub-xxxxxxxx.r2.dev")
base = sys.argv[1].rstrip("/")
parsed = urlparse(base)
if parsed.scheme != "https" or not parsed.netloc:
    raise SystemExit("L'URL base deve essere un URL HTTPS assoluto.")

data = json.loads(catalog_path.read_text(encoding="utf-8"))
for track in data["tracks"]:
    for field in ("audioUrl", "previewUrl"):
        value = track.get(field)
        if value:
            path = urlparse(value).path
            track[field] = base + path
catalog_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()

upload_path = root / "metadata" / "upload_manifest.csv"
with upload_path.open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
    fieldnames = list(rows[0].keys())
for row in rows:
    if row["key"] == "music_catalog.json":
        row["sha256"] = digest(catalog_path)
        row["sizeBytes"] = str(catalog_path.stat().st_size)
with upload_path.open("w", newline="", encoding="utf-8") as handle:
    writer = csv.DictWriter(handle, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)

checksum_path = root / "CHECKSUMS.sha256"
files = sorted(path for path in root.rglob("*") if path.is_file() and path != checksum_path)
checksum_path.write_text("".join("%s  %s\n" % (digest(path), path.relative_to(root).as_posix()) for path in files), encoding="utf-8")
print(f"Catalogo configurato per {base}")
