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

## Bundled skills and upstream updates
- The authoritative built-in skill files are `skills/ponytail/SKILL.md` and `skills/grill-me/SKILL.md`, imported from their MIT-licensed originals and accompanied by license notices.
- Use bundled Ponytail full for Issue drafting, plans, code and UI. Offer bundled Grill Me when questions materially affect scope. No separate plugin installation is required.
- Never execute or silently trust a mutable upstream skill at chat runtime. The scheduled GitHub workflow may propose upstream changes in a reviewable PR, with provenance in `skills/upstream-lock.json`.

## Mandatory post-merge cleanup
- After a confirmed merge, remove the source feature branch if it is no longer used, has no work needing preservation, and is not protected/default. Verify the live state before deletion.
- A squash merge does not make source commits ancestors of `main`; verify the PR is merged and its diff integrated rather than relying solely on commit ancestry.
- If safe deletion tooling is unavailable, report that cleanup is pending and provide the GitHub UI action. Never falsely mark cleanup complete.

## Native next-action UI (mandatory)
After each decision milestone, present supported, functional native ChatGPT action buttons, not a text-only suggestion. Offer context-appropriate choices such as **Review**, **Revise**, **Merge**, and **Publish**, localized to the user's language. Every button must trigger the exact advertised next step; merge and publication still require confirmed authorization and safety checks. If native controls are unavailable, use short explicit text choices. Never make decorative or inert buttons.

## Automatic branch cleanup and release packaging
- After an approved merge, cleanup is automatic via `.github/workflows/cleanup-merged-branch.yml`. Never request an extra cleanup confirmation when the branch is safely obsolete. The workflow must protect default/protected branches, modified heads and branches shared by open PRs; skipped cleanup is reported, not forced.
- `.github/workflows/package.yml` validates and packages committed plugin source into a downloadable SHA-labelled `dream-plugin.zip` artifact. Do not rebuild by hand if the verified artifact can be retrieved.
- A release in ChatGPT still requires explicit approval: verify the artifact belongs to the merged `main` commit, download it, update the same plugin using Plugin Creator's release guard, and read back the installed version. If direct artifact-to-Plugin-Creator transfer is unsupported, disclose that and use a verified package built from the same commit; never assume a download URL is accepted as a local archive path.
