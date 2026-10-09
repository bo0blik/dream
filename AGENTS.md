# Dream Agent Guidelines

- Apply installed **Ponytail full** before drafting issues, planning, coding or UI changes. Use Grill Me for material ambiguity.
- Write prompts in English; respond in the user's language. Prefer native ChatGPT controls, concise progress and diagrams.
- Read current code, manifests, CI and relevant instructions. Minimize scope, dependencies, tokens and risk.
- Issue approval → plan approval → branch/commits/CI/PR → explicit merge approval. Never force-push, bypass checks or overwrite unrelated work.
- Keep `plugin.json` and `.codex-plugin/plugin.json` consistent. Run `python3 scripts/validate_plugin.py` and inspect Actions results before proposing merge.

## Dream self-update (in ChatGPT)

The authoritative source is the **merged `main`** branch of `bo0blik/dream`; pushing GitHub changes alone does not update the ChatGPT plugin.

1. Before any release, verify the relevant PR was merged, required checks passed, current `main` HEAD and source files are read from GitHub, and the user explicitly authorized **publishing this release**. Merge approval alone is **not** release approval.
2. Read installed plugin metadata and current release ID using Plugin Creator for the existing private plugin `plugins_6ac86e8247e881919d149fd5492e77aa`. Never create a replacement plugin or rename its immutable identity. Keep current privacy, owner, display name Dream and interface prompts.
3. Compare GitHub `main` manifest/skills with installed plugin source. Reject missing paths, malformed manifests, wrong plugin identity, missing skill references or a version not greater than the installed version. Build one self-contained release archive from the **verified merged commit**, without secrets, local files or unnecessary assets; preserve compatibility metadata and unrelated files.
4. If Plugin Creator update tools are available, update the **existing** plugin using the exact plugin ID, archive and `expected_release_id` observed just before publishing. Do not retry a result with uncertain status; re-check the release first. If tooling is unavailable, stop and provide the precise manual release steps; never claim publishing succeeded.
5. After a confirmed update, read back plugin version, release ID, manifest, skills and file inventory. Check they match the merged source. Only then report deployment complete, with commit, PR, version and plugin link; otherwise report the exact discrepancy.
6. Repository and installed plugin are separate states. Never edit the plugin directly as a substitute for an approved GitHub change. If release fails, preserve the merged source and report the plugin still at its previously verified version.

## Safety

Keep changes in PRs until explicit merge approval. Changes to project policy, dependencies, secrets, destructive operations and releases need their own scope-specific consent. Do not expose credentials or personal information.

## Mandatory language policy

- Write code, comments, tests, configuration, documentation, GitHub Issues, PRs, reviews, branches, commit messages and release notes in **English**.
- Translate user requirements into English before writing GitHub artifacts; preserve external API contracts and existing identifiers.
- Respond in the user's language when clear, otherwise English. Localize ChatGPT UI labels, not code identifiers.
- Apply this rule to new or edited content; do not rewrite unrelated legacy code solely for translation.
