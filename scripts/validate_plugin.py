#!/usr/bin/env python3
"""Validate Dream's portable plugin package without third-party dependencies."""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
errors = []

def fail(message):
    errors.append(message)

def load(path):
    try:
        return json.loads((ROOT / path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        fail(f"{path}: {exc}")
        return {}

main = load("plugin.json")
compat = load(".codex-plugin/plugin.json")
if main.get("name") != "github-dev-orchestrator":
    fail("plugin.json: immutable plugin package name changed")
if compat.get("name") != main.get("name"):
    fail("compatibility name differs")
version = main.get("version", "")
if not re.fullmatch(r"(0|[1-9]\\d*)\\.(0|[1-9]\\d*)\\.(0|[1-9]\\d*)", version):
    fail("version must be semantic x.y.z")
if compat.get("version") != version:
    fail("compatibility version differs")
if compat.get("description") != main.get("description"):
    fail("compatibility description differs")
ui = main.get("extensions", {}).get("com.openai", {}).get("interface", {})
cui = compat.get("interface", {})
for key in ("displayName", "shortDescription", "longDescription", "developerName", "category", "capabilities", "defaultPrompt"):
    if ui.get(key) != cui.get(key):
        fail(f"interface.{key} differs")
if ui.get("displayName") != "Dream":
    fail("displayName must be Dream")

skill_root = ROOT / "skills"
skills = sorted(skill_root.glob("*/SKILL.md"))
if not skills:
    fail("no discoverable skills found")
for file in skills:
    data = file.read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", data, re.S)
    if not match:
        fail(f"{file}: missing skill frontmatter")
        continue
    front = match.group(1)
    for key in ("name", "description"):
        if not re.search(rf"(?m)^{key}:\s*\S+", front):
            fail(f"{file}: missing {key}")
    name = re.search(r"(?m)^name:\s*(\S+)", front)
    if name and name.group(1) != file.parent.name:
        fail(f"{file}: skill directory/name mismatch")
    for ref in re.findall(r"`(references/[^\`]+\.md)`", data):
        if not (file.parent / ref).is_file():
            fail(f"{file}: missing {ref}")
for required in ("AGENTS.md", "README.md"):
    if not (ROOT / required).is_file():
        fail(f"missing {required}")
if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    sys.exit(1)
print(f"OK: Dream v{version}; {len(skills)} skill(s); manifests aligned")
