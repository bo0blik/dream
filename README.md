# Dream

A concise, approval-gated GitHub development orchestrator for ChatGPT.

**Workflow:** Repository → Issue approval → Ponytail plan approval → Branch / commits → GitHub Actions → Pull Request → explicit merge approval.

## Installation

[Open the private Dream plugin in ChatGPT](https://chatgpt.com/plugins/plugins_6ac86e8247e881919d149fd5492e77aa)

> Plugin source is maintained here. Pushing to this repository does **not** automatically update the installed ChatGPT plugin. Publish a new release through Plugin Creator after reviewing a PR.

## Structure

- `plugin.json` — ChatGPT plugin manifest
- `.codex-plugin/plugin.json` — compatibility manifest
- `skills/github-development/SKILL.md` — orchestration instructions
- `skills/github-development/references/` — approval gates and templates

## Principles

Ponytail full for tasks and implementations; Grill Me for ambiguous requirements; no unapproved writes, merges, or force pushes. Existing GitHub tools and Actions provide execution and verification. All plugin instructions are in English; responses match the user's language.

## Global workflow UI

Dream uses one mandatory, compact, evidence-based interface contract across the seven **conceptual** stages: **Idea / Brainstorming → Repository Overview → Issue / Gate A → Plan / Gate B → Development → PR / CI / Gate C → Release**. Only the relevant current stage is shown, with localized stage identity, verified context, useful primary content, truthful status, safety boundary and functional next-action buttons when a meaningful next step exists. Gate A, Gate B, Gate C / merge and publication remain **separate** user approvals. A simple factual answer or an interim progress update does not need a full workflow interface.

Within **Repository Overview**, the existing **Repository → Rules → Docs → Tasks** four-stage navigator remains nested: repository choice belongs to the user, and already verified instructions, docs, Issues and PRs are reused across tabs rather than needlessly refetched. Dream must not substitute a speculative recommendation for a user-selection control. Stage navigation does not grant permission for GitHub writes.

For unsupported native controls, Dream offers a compact text fallback with truthful status, not simulated buttons. Consequential PR HEAD, CI, merge and plugin release states are refreshed before writes; when context is missing, Dream requests only the missing information. The full policy and 13 static scenario contracts are maintained in `skills/github-development/SKILL.md` and `scripts/validate_plugin.py`. Static CI checks cannot guarantee identical client rendering.

## Interactive repository onboarding

After selecting a repository, Dream automatically reads root and applicable nested AGENTS.md / AGENT.md instructions, README, open Issues and open PRs without another request. The mandatory native Repository Overview displays **Repo → Rules → Docs → Tasks** as clickable stages with icons and honest completion/error states. Only the selected stage's details are visible; switching stages reuses fetched context. Rules lists sourced instructions, Docs summarizes project context and Tasks shows actual linked open work by default. Missing files, failed reads and unsupported native controls have explicit fallbacks. Onboarding is read-only and never bypasses Gate A/B.

## Context-aware Project Preview

Dream can offer optional Project Preview for websites, HTML games and UI changes. It prefers verified existing GitHub Pages or other deployments and genuine project screenshots. A compact preview card has truthful Available, Screenshot, Build required, Unavailable or Error states; Open Preview links to verified pages, while Split View availability depends on the ChatGPT host. Never assume a guessed URL is live, execute unfamiliar builds, change GitHub Pages settings or publish private code without authorization. Preview does not add a fifth mandatory Repository Overview stage. The policy, workflow and detailed decisions live in AGENTS.md, the github-development skill and its references/preview.md.

## Brainstorming and intent-aware routing

Dream bundles an MIT-licensed adaptation of [obra/superpowers Brainstorming](https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/brainstorming/SKILL.md), pinned to revision `8ca22dba9a94f28898bbce59f2537ff4d87c747d` (license and attribution under `skills/brainstorming/LICENSE`). It explores ideas through Spike, Bounded and Architectural discussions, while Grill Me clarifies consequential uncertainty and Ponytail guides GitHub development. Idea/design approval never authorizes repository writes: Gate A/B and merge/publication consent remain separate. Meaningful completed responses offer functional next-action buttons where supported, with text fallback. No changes to root AGENTS.md are needed.

## Development

Open an Issue with acceptance criteria, approve the plan, implement on a feature branch, validate, and submit a PR. The installed plugin must be updated separately after merge.

## Branding and included skills

Dream icon: [`assets/dream-icon.svg`](assets/dream-icon.svg). The original emblem is included as a portable vector asset; application icon rendering depends on the ChatGPT plugin host's supported manifest settings.

Bundled MIT-licensed skills:
- [Ponytail](skills/ponytail/SKILL.md), original: https://github.com/DietrichGebert/ponytail
- [Grill Me](skills/grill-me/SKILL.md), original: https://github.com/satya-janghu/agent-skills/tree/main/skills/grill-me

GitHub Actions periodically checks upstream and opens an update PR; it never automatically merges or publishes outside changes.

## Branch cleanup

After each merged PR, remove the feature branch if it is safely obsolete. Preserve the default/protected branch and unfinished work. If deletion is not supported by the connected agent, use the GitHub **Delete branch** control on the merged PR.

## Release automation

The `Build Dream package` GitHub Actions workflow runs validation and creates a `dream-plugin.zip` artifact associated with the exact commit SHA. Download the artifact from the workflow run after CI success, then publish it to the existing private plugin through Plugin Creator after explicit approval. The installed plugin does not update merely by merging a PR.

On merged PRs, `Clean merged feature branch` automatically deletes an obsolete unchanged branch if it is neither protected nor used by another open PR. No additional confirmation is required for safe cleanup.

Dream presents native, functional action buttons for review, revision, merge and release whenever supported, with a concise fallback otherwise.
