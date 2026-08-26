#!/usr/bin/env python3
import hashlib
import json
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

root = Path(__file__).resolve().parents[1]
catalog = json.loads((root / "music_catalog.json").read_text(encoding="utf-8"))
license_manifest = json.loads((root / "metadata" / "license_manifest.json").read_text(encoding="utf-8"))
required = {"id", "title", "artist", "category", "moods", "durationMs", "bpm", "audioUrl", "previewUrl", "artworkUrl", "license", "licenseUrl", "sourceName", "sourceUrl", "downloadDate"}
expected = {"Cinematic": 20, "Chill": 16, "Travel": 12, "Action": 12, "Emotional": 10, "Electronic": 10, "Retro": 10, "Ambient": 10}
tracks = catalog.get("tracks", [])
assert catalog.get("version") == 1
assert len(tracks) == 100
assert len({t["id"] for t in tracks}) == 100
assert Counter(t["category"] for t in tracks) == Counter(expected)
audit = {item["id"]: item for item in license_manifest["tracks"]}
for track in tracks:
    assert set(track) == required, (track.get("id"), set(track) ^ required)
    assert track["license"] == "CC0-1.0"
    assert track["licenseUrl"] == "https://creativecommons.org/publicdomain/zero/1.0/"
    assert track["sourceUrl"].startswith("https://opengameart.org/")
    assert track["downloadDate"] == "2026-08-26"
    for field, checksum_field in (("audioUrl", "audioSha256"), ("previewUrl", "previewSha256")):
        path = root / urlparse(track[field]).path.lstrip("/")
        assert path.is_file(), path
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        assert actual == audit[track["id"]][checksum_field], path
print("OK: 100 tracce, schema v1, categorie, licenze, file e checksum validi.")
