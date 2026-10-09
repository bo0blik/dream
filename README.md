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

## Development

Open an Issue with acceptance criteria, approve the plan, implement on a feature branch, validate, and submit a PR. The installed plugin must be updated separately after merge.
