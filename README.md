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

## Branding and included skills

Dream icon: [`assets/dream-icon.svg`](assets/dream-icon.svg). The original emblem is included as a portable vector asset; application icon rendering depends on the ChatGPT plugin host's supported manifest settings.

Bundled MIT-licensed skills:
- [Ponytail](skills/ponytail/SKILL.md), original: https://github.com/DietrichGebert/ponytail
- [Grill Me](skills/grill-me/SKILL.md), original: https://github.com/satya-janghu/agent-skills/tree/main/skills/grill-me

GitHub Actions periodically checks upstream and opens an update PR; it never automatically merges or publishes outside changes.

## Branch cleanup

After each merged PR, remove the feature branch if it is safely obsolete. Preserve the default/protected branch and unfinished work. If deletion is not supported by the connected agent, use the GitHub **Delete branch** control on the merged PR.
