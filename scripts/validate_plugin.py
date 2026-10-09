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
if not re.fullmatch(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)", version):
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
# Regression checks for the two independent, user-approved write gates.
for policy_file in (ROOT / "AGENTS.md", ROOT / "skills/github-development/SKILL.md"):
    policy = policy_file.read_text(encoding="utf-8")
    for rule in ("Gate A", "Gate B", "Approve Issue", "Approve Plan", "real user", "Merge"):
        if rule.lower() not in policy.lower():
            fail(f"{policy_file.relative_to(ROOT)}: missing authorization rule {rule!r}")
    if policy.index("Gate A") > policy.index("Gate B"):
        fail(f"{policy_file.relative_to(ROOT)}: Issue gate must precede plan gate")
# Regression coverage for mandatory read-only repository onboarding.
overview = (ROOT / "skills/github-development/SKILL.md").read_text(encoding="utf-8")
template = (ROOT / "skills/github-development/references/templates.md").read_text(encoding="utf-8")
gates = (ROOT / "skills/github-development/references/gates.md").read_text(encoding="utf-8")
for label, value in (("Skill", overview), ("Template", template)):
    for stage in ("Repo", "Rules", "Docs", "Tasks"):
        if stage not in value:
            fail(f"{label}: missing Overview stage {stage}")
    for requirement in ("AGENTS.md", "README", "Issues", "Pull Requests"):
        if requirement not in value:
            fail(f"{label}: missing auto-inspection requirement {requirement}")
for requirement in ("read-only", "AGENTS.md", "README", "Issues/PRs"):
    if requirement not in gates:
        fail(f"gates: missing initialization safeguard {requirement}")
# Validate the interaction example and ordering, not just the names of the stages.
required_ui = ("DIL.useState(3)", "onClick={()=>setStage(index)}",
               "onClick={()=>setStage(Math.max(0,stage-1))}",
               "onClick={()=>setStage(Math.min(3,stage+1))}",
               "{#if stage===0}", "{:else if stage===1}", "{:else if stage===2}",
               "<pressable", "<grid", "No GitHub")
for token in required_ui[:-1]:
    if token not in template:
        fail(f"Overview template missing functional control: {token}")
if not (overview.index("1. **Repo:**") < overview.index("2. **Rules:**") <
        overview.index("3. **Docs:**") < overview.index("4. **Tasks:**")):
    fail("Overview initialization order is incorrect")
for rule in ("future task scope is unknown", "directory ancestry", "before"):
    if rule not in overview:
        fail(f"Overview missing scoped nested AGENTS safeguard: {rule}")
if "read-only initialization" not in overview or "No GitHub writes during initialization" not in overview:
    fail("Overview does not enforce read-only initialization")
# Preview instructions remain three-layered, contextual and approval-gated.
preview = (ROOT / "skills/github-development/references/preview.md").read_text(encoding="utf-8")
agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
for label, data, required in (
    ("AGENTS.md", agents, ("Project Preview policy", "Gate A/B", "Split View", "private")),
    ("SKILL.md", overview, ("Context-aware Project Preview", "references/preview.md", "Build required", "Open Preview", "Gate A/B")),
    ("preview.md", preview, ("GitHub Pages", "Available", "Screenshot", "Build required", "Unavailable", "Error", "Split View", "read-only", "untrusted", "Markdown", "Vite", "React")),
):
    for token in required:
        if token not in data:
            fail(f"{label}: missing required preview rule {token!r}")
if "a fifth mandatory Repo → Rules → Docs → Tasks stage" not in agents:
    fail("Preview must remain contextual, not a fifth onboarding stage")
if "Do not execute untrusted code" not in agents:
    fail("Preview must prohibit unauthorized execution")
if "never" not in preview.lower() or "verify" not in preview.lower():
    fail("Preview must document verification and negative paths")
# Verify the canonical native UI and deterministic policy scenarios.
for token in (
    'GenUI.openUrl(verifiedUrl)',
    'previewStatus === "Available" && verifiedUrl.startsWith("https://")',
    'previewStatus === "Build required"',
    'GenUI.issueNewTurn(',
    'Do not execute or deploy anything.',
    'Host layouts without native buttons',
):
    if token not in preview:
        fail(f"preview.md: missing functional or safety condition {token!r}")
blocks = re.findall(r"```json\\n(.*?)\\n```", preview, re.S)
if len(blocks) != 1:
    fail("preview.md: expected exactly one JSON scenario contract")
else:
    try:
        scenarios = json.loads(blocks[0])["scenarios"]
        by_id = {item["id"]: item for item in scenarios}
        expected = {
            "pages_verified": ("verified_https_url", "Available", ["open"]),
            "pages_guessed": ("guessed_url", "Unavailable", []),
            "pages_access_denied": ("fetch_error", "Error", []),
            "screenshot_verified": ("verified_image", "Screenshot", []),
            "vite_no_deploy": ("buildable_source", "Build required", ["prepare"]),
            "markdown_only": ("verified_markdown_file", "File", []),
            "backend_only": ("backend_only", "Unavailable", []),
        }
        if len(scenarios) != len(by_id) or set(by_id) != set(expected):
            fail("preview.md: missing/duplicate/unexpected preview scenarios")
        for name, (evidence, status, actions) in expected.items():
            item = by_id.get(name, {})
            if (item.get("evidence"), item.get("status"), item.get("actions")) != (evidence, status, actions):
                fail(f"preview.md: incorrect scenario {name}")
            if item.get("writes") is not False:
                fail(f"preview.md: discovery scenario {name} must never write")
            if "open" in item.get("actions", []) and item.get("evidence") != "verified_https_url":
                fail(f"preview.md: unverified URL opens in {name}")
            if "prepare" in item.get("actions", []) and item.get("status") != "Build required":
                fail(f"preview.md: prepare should only request approval for buildable source in {name}")
    except (ValueError, KeyError, TypeError) as exc:
        fail(f"preview.md: invalid JSON scenario contract: {exc}")
for required in ("AGENTS.md", "README.md"):
    if not (ROOT / required).is_file():
        fail(f"missing {required}")
if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    sys.exit(1)
print(f"OK: Dream v{version}; {len(skills)} skill(s); manifests aligned")
