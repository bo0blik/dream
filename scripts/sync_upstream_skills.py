#!/usr/bin/env python3
"""Propose reviewed updates for MIT-licensed upstream skill sources."""
import json
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SOURCES = {
    "ponytail": ("DietrichGebert", "ponytail", "skills/ponytail/SKILL.md"),
    "grill-me": ("satya-janghu", "agent-skills", "skills/grill-me/SKILL.md"),
}

def download(url):
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "Dream-skill-sync"})
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8")

versions = {}
for name, (owner, repo, path) in SOURCES.items():
    metadata = json.loads(download(f"https://api.github.com/repos/{owner}/{repo}"))
    head = metadata["default_branch"]
    commit = json.loads(download(f"https://api.github.com/repos/{owner}/{repo}/commits/{head}"))["sha"]
    base = f"https://raw.githubusercontent.com/{owner}/{repo}/{commit}"
    skill = download(f"{base}/{path}")
    license_text = download(f"{base}/LICENSE")
    if not skill.startswith("---\n") or f"name: {name}" not in skill.split("---", 2)[1]:
        raise ValueError(f"invalid upstream skill: {name}")
    if not license_text.startswith("MIT License"):
        raise ValueError(f"license changed: {name}; manual inspection required")
    folder = ROOT / "skills" / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(skill, encoding="utf-8")
    (folder / "LICENSE").write_text(license_text, encoding="utf-8")
    versions[name] = {"source": f"https://github.com/{owner}/{repo}", "commit": commit, "path": path, "license": "MIT"}
lock = ROOT / "skills" / "upstream-lock.json"
lock.write_text(json.dumps(versions, indent=2) + "\n", encoding="utf-8")
print("Upstream skills checked. Any changed files require PR review.")
