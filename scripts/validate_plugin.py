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
# Exact approved Russian onboarding scenarios: ideas, repository, then development.
expected_starter_prompts = [
    "У меня есть идея для проекта. Помоги её развить, сравнить варианты и выбрать лучшее решение. Пока ничего не создавай в GitHub.",
    "Покажи мои GitHub-репозитории, помоги выбрать проект и найти подходящую задачу. Пока ничего не изменяй.",
    "Помоги выбрать задачу из GitHub Issues, изучить проект и подготовить план реализации. Соблюдай все этапы согласования Dream; не начинай изменения до соответствующего разрешения.",
]
if version != "1.1.2":
    fail("Dream starter prompts release must use version 1.1.2 in both manifests")
if ui.get("defaultPrompt") != expected_starter_prompts:
    fail("plugin.json: defaultPrompt must contain the exact three approved Russian scenarios, in order")
if cui.get("defaultPrompt") != expected_starter_prompts:
    fail(".codex-plugin/plugin.json: defaultPrompt must match the same three approved Russian scenarios")
if not isinstance(ui.get("defaultPrompt"), list) or len(ui["defaultPrompt"]) != 3:
    fail("starter prompt count must be exactly three")

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
# Root AGENTS.md contains only the agreed 12 project-specific rules.
agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
project_rules = [line for line in agents.splitlines() if line.startswith("- ")]
if agents.splitlines()[0] != "# Dream — Project Rules" or len(project_rules) != 13:
    fail("AGENTS.md must contain the agreed heading and 13 project rules, including Skill Check")
if not project_rules or project_rules[0] != "- Before starting each new task, consult `skills/github-development/SKILL.md` and follow its applicable workflow. Do not rely on remembered instructions from previous tasks.":
    fail("AGENTS.md: mandatory Skill Check must be first")
if any(line.startswith("## ") for line in agents.splitlines()):
    fail("AGENTS.md must be a simple list without workflow sections")
for token in ("plugin.json", ".codex-plugin/plugin.json", "Ponytail", "Grill Me",
              "scripts/validate_plugin.py", "GitHub Actions", "README.md", "secrets"):
    if token not in agents:
        fail(f"AGENTS.md: missing project rule {token!r}")
if any(token in agents for token in ("Gate A", "Gate B", "Gate C", "Split View", "Plugin Creator")):
    fail("AGENTS.md must not duplicate skill workflow instructions")
# Single-file Dream blueprint: structural contract and safeguards.
skill_text = (ROOT / "skills/github-development/SKILL.md").read_text(encoding="utf-8")
expected_headings = ("Core", "Workflow", "Shared UI & compact examples", "Safety & evidence",
                     "Optional Project Preview", "Finish")
for heading in expected_headings:
    if skill_text.count("## " + heading + "\n") != 1:
        fail(f"SKILL.md: expected one section {heading}")
stages = ("Idea / Brainstorming", "Repository Overview", "Issue / Gate A",
          "Plan / Gate B", "Development", "PR / CI / Gate C", "Release")
stage_sections = re.findall(r"(?ms)^### (\d+)\. ([^\n]+)\n(.*?)(?=^### |^## |\Z)", skill_text)
if len(stage_sections) != 7 or [title for _, title, _ in stage_sections] != list(stages):
    fail("SKILL.md: expected seven ordered workflow stages")
for index, title, section in stage_sections:
    fields = re.findall(r"(?m)^(When|Read|Do|Gate|UI|Next):", section)
    if fields != ["When", "Read", "Do", "Gate", "UI", "Next"]:
        fail(f"SKILL.md: invalid six-field stage {index} {title}")
required_contract = {
    "skill_check": ("Mandatory Skill Check", "Before each new development task", "AGENTS.md", "stop dependent work"),
    "routing": ("Brainstorming", "Grill Me", "Ponytail full", "Direct answer", "read-only"),
    "repo": ("Repo → Rules → Docs → Tasks", "default to Tasks", "directory-ancestry",
             "disabled Issues", "Pull Requests", "No GitHub writes during initialization"),
    "approvals": ("Gate A", "Gate B", "Gate C", "separate publication", "exact draft",
                  "specific plan revision", "real user authorization", "fail closed"),
    "safety": ("force push", "protection", "destructive", "security-sensitive", "AGENTS.md",
               "max 3", "secrets", "third-party", "no direct default-branch"),
    "ci_merge": ("required CI", "recheck HEAD", "residual risk", "Issue closure",
                 "obsolete", "unmerged work", "actual CI logs"),
    "release": ("merged main SHA", "current-release guard", "SAME existing private plugin",
                "read back installed", "USER/PRIVATE", "successful merged-main artifact"),
    "ui": ("functional native actions", "shared state", "text alternatives", "no imaginary host APIs"),
    "preview": ("Optional Project Preview", "HTTPS reachability", "matching project content",
                "Build required", "Unavailable", "Error", "Open Preview", "Split View",
                "separate informed authorization"),
}
for label, terms in required_contract.items():
    for term in terms:
        if term.casefold() not in skill_text.casefold():
            fail(f"SKILL.md: missing {label} invariant {term!r}")
# The unchanged bundled references retain their validated detailed safety fixtures.
preview = (ROOT / "skills/github-development/references/preview.md").read_text(encoding="utf-8")
gate_policy = (ROOT / "skills/github-development/references/gates.md").read_text(encoding="utf-8")
template = (ROOT / "skills/github-development/references/templates.md").read_text(encoding="utf-8")
for term in ("Gate A", "Gate B", "Gate C", "read-only", "AGENTS.md"):
    if term not in gate_policy:
        fail(f"gates.md: missing safeguard {term}")
for term in ("DIL.useState(3)", "onClick={()=>setStage(index)}", "Repo", "Rules", "Docs", "Tasks"):
    if term not in template:
        fail(f"templates.md: missing canonical native UI pattern {term}")
# Verify the canonical native UI and deterministic policy scenarios.
for token in (
    'GenUI.openUrl(verifiedUrl)',
    'previewStatus === "Available" && urlVerified === true && typeof verifiedUrl === "string" && verifiedUrl.startsWith("https://")',
    'previewStatus === "Build required"',
    'GenUI.issueNewTurn(',
    'Do not execute or deploy anything.',
    'Host layouts without native buttons',
):
    if token not in preview:
        fail(f"preview.md: missing functional or safety condition {token!r}")
# Fail closed: the canonical UI must not ship with a fabricated active deployment.
for token in ('{@body const verifiedUrl = null}',
              '{@body const urlVerified = false}',
              '{@body const previewStatus = "Unavailable"}'):
    if token not in preview:
        fail(f"preview.md: unsafe default in native preview template: {token}")
if re.search(r'(?m)^\\{@body const verifiedUrl\\s*=\\s*["\\\']https?://', preview):
    fail("preview.md: canonical preview must not hard-code a URL")
if '{@body const previewStatus = "Available"}' in preview:
    fail("preview.md: canonical preview must not start in Available state")
if "never infer verification from the URL prefix alone" not in preview:
    fail("preview.md: URL prefix must not be used as verification evidence")
blocks = re.findall(r"```json\n(.*?)\n```", preview, re.S)
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
# Bundled Brainstorming remains pinned, credited, read-only and approval-gated.
brainstorm = (ROOT / "skills/brainstorming/SKILL.md").read_text(encoding="utf-8")
brain_license = (ROOT / "skills/brainstorming/LICENSE").read_text(encoding="utf-8")
pin = "8ca22dba9a94f28898bbce59f2537ff4d87c747d"
for term in ("Spike", "Bounded", "Architectural", "read-only", "Gate A",
             "Gate B", "merge consent", "publication consent", "Draft Issue", "unavailable"):
    if term.lower() not in brainstorm.lower():
        fail(f"brainstorming: missing safeguard {term!r}")
if pin not in brainstorm or "obra/superpowers" not in brainstorm:
    fail("brainstorming: missing pinned upstream provenance")
if "MIT License" not in brain_license or "Copyright (c) 2025 Jesse Vincent" not in brain_license:
    fail("brainstorming: missing MIT license and attribution")
for required in ("AGENTS.md", "README.md"):
    if not (ROOT / required).is_file():
        fail(f"missing {required}")
if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    sys.exit(1)
print(f"OK: Dream v{version}; {len(skills)} skill(s); manifests aligned")
