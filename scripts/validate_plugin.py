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
if version != "1.1.1":
    fail("Dream starter prompts release must use version 1.1.1 in both manifests")
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
# Skill Check applies before each task while reusing verified same-task context.
required_skill_check = ("## Mandatory Skill Check", "Before starting each new GitHub development task",
                        "re-check when the repository or skill changes",
                        "Do not rely solely on remembered instructions from previous tasks",
                        "This check never replaces Gate A, Gate B, merge approval or publication approval")
skill_text = (ROOT / "skills/github-development/SKILL.md").read_text(encoding="utf-8")
for rule in required_skill_check:
    if rule not in skill_text:
        fail(f"SKILL.md: missing required Skill Check safeguard {rule!r}")
# Authorization rules belong to the development skill and existing gates reference.
skill_policy = (ROOT / "skills/github-development/SKILL.md").read_text(encoding="utf-8")
gate_policy = (ROOT / "skills/github-development/references/gates.md").read_text(encoding="utf-8")
for rule in ("Gate A", "Gate B", "Approve Issue", "Approve Plan", "real user", "Merge"):
    if rule.lower() not in skill_policy.lower():
        fail(f"SKILL.md: missing authorization rule {rule!r}")
if skill_policy.index("Gate A") > skill_policy.index("Gate B"):
    fail("SKILL.md: Issue gate must precede plan gate")
for rule in ("Gate A", "Gate B", "Gate C", "read-only", "AGENTS.md"):
    if rule not in gate_policy:
        fail(f"gates.md: missing safeguard {rule!r}")
for rule in ("publication approval", "merge approval", "No GitHub writes during initialization"):
    if rule.lower() not in skill_policy.lower():
        fail(f"SKILL.md: missing separation or read-only rule {rule!r}")
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
    ("SKILL.md", overview, ("Context-aware Project Preview", "references/preview.md", "Build required", "Open Preview", "Gate A/B")),
    ("preview.md", preview, ("GitHub Pages", "Available", "Screenshot", "Build required", "Unavailable", "Error", "Split View", "read-only", "untrusted", "Markdown", "Vite", "React")),
):
    for token in required:
        if token not in data:
            fail(f"{label}: missing required preview rule {token!r}")
if "must not" not in overview or "mandatory Repo → Rules → Docs → Tasks" not in overview:
    fail("Preview must not extend mandatory onboarding")
if "Execution of repository code" not in preview or "explicit user authorization" not in preview:
    fail("Preview must prohibit unapproved execution or publication")
if "never" not in preview.lower() or "verify" not in preview.lower():
    fail("Preview must document verification and negative paths")
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
# Brainstorming discovery, pinned attribution, read-only routing and next actions.
brainstorm = (ROOT / "skills/brainstorming/SKILL.md").read_text(encoding="utf-8")
brain_license = (ROOT / "skills/brainstorming/LICENSE").read_text(encoding="utf-8")
pin = "8ca22dba9a94f28898bbce59f2537ff4d87c747d"
for term in (f"Pinned revision: \`{pin}\`", "Spike", "Bounded", "Architectural",
             "read-only", "Gate A", "Gate B", "merge consent", "publication consent",
             "Draft Issue", "unavailable"):
    # Pin formatting is checked separately to avoid interpretation of Markdown markup.
    if term.startswith("Pinned revision:"):
        continue
    if term.lower() not in brainstorm.lower():
        fail(f"brainstorming: missing required method/safety instruction {term!r}")
if pin not in brainstorm or "obra/superpowers" not in brainstorm:
    fail("brainstorming: missing pinned upstream provenance")
if "MIT License" not in brain_license or "Copyright (c) 2025 Jesse Vincent" not in brain_license:
    fail("brainstorming: missing upstream MIT license and attribution")
for term in ("## Intent-aware skill routing", "skills/brainstorming/SKILL.md",
             "Brainstorming", "Grill Me", "Ponytail full",
             "Direct answer", "Gate A", "Gate B", "never authorize any GitHub write"):
    if term not in overview:
        fail(f"SKILL.md: missing intent routing {term!r}")
for term in ("completed substantive Dream response", "functional native ChatGPT buttons",
             "exactly the advertised action", "Draft Issue (chat-only)",
             "text alternatives", "Gate A, Gate B, merge and publication"):
    if term not in overview:
        fail(f"SKILL.md: missing next-action requirement {term!r}")
# Static policy scenario matrix; these assert routing intent and authorization boundaries.
scenarios = {
    "game_idea": ("Brainstorming", False),
    "architecture_comparison": ("Brainstorming", False),
    "conflicting_requirements": ("Grill Me", False),
    "routine_fix": ("Dream + Ponytail full", False),
    "design_approved": ("Brainstorming", False),
    "implementation_requested": ("Dream + Ponytail full", False),
    "resumed_idea": ("Brainstorming", False),
    "simple_fact": ("Direct answer", False),
    "unsupported_upstream_tool": ("Brainstorming", False),
    "private_repository": ("Brainstorming", False),
}
if len(scenarios) != 10 or any(mode not in overview or writes for mode, writes in scenarios.values()):
    fail("brainstorming: invalid routing scenario matrix")
if "Design approval" not in brainstorm and "design approval" not in brainstorm:
    fail("brainstorming: design approval cannot grant write access")
for required in ("AGENTS.md", "README.md"):
    if not (ROOT / required).is_file():
        fail(f"missing {required}")
if errors:
    for error in errors:
        print("FAIL:", error, file=sys.stderr)
    sys.exit(1)
print(f"OK: Dream v{version}; {len(skills)} skill(s); manifests aligned")
