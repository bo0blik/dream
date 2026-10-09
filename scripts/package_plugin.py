#!/usr/bin/env python3
"""Build a deterministic standalone Dream plugin archive from tracked sources."""
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "dream-plugin.zip"
tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
paths = [p for p in tracked if p in ("plugin.json", ".codex-plugin/plugin.json")
         or p.startswith("skills/") or p.startswith("assets/")]
required = {"plugin.json", ".codex-plugin/plugin.json", "assets/dream-icon.svg",
            "skills/github-development/SKILL.md", "skills/ponytail/SKILL.md",
            "skills/grill-me/SKILL.md", "skills/ponytail/LICENSE", "skills/grill-me/LICENSE"}
missing = required - set(paths)
if missing:
    raise SystemExit(f"Missing package files: {sorted(missing)}")
with ZipFile(OUTPUT, "w", ZIP_DEFLATED, compresslevel=9) as zip_file:
    for path in sorted(paths):
        info = ZipInfo(f"github-dev-orchestrator/{path}", date_time=(2020, 1, 1, 0, 0, 0))
        info.compress_type = ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        zip_file.writestr(info, (ROOT / path).read_bytes())
print(f"Built {OUTPUT.name}: {len(paths)} files")
