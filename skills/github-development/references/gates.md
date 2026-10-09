# Approval and evidence gates
- Repository onboarding is read-only: after selection automatically inspect root and applicable nested AGENTS.md / AGENT.md, README and open Issues/PRs; do not require another "load" confirmation. Do not suggest actionable work before checking instructions.
- Missing AGENTS files must be reported as absent, not read; access errors are blockers for dependent work. Overview stage indicators must reflect verified reads, never assume success. Navigating cached stages does not trigger writes or new fetches.

- Gate A: user approves **Issue content**; only then create/update Issue. Enabling disabled Issues or changing repo settings needs separate approval and supported capability.
- Gate B: user approves **exact plan revision**; branch, scoped implementation, commits, PR and up to 3 CI fixes are then permitted.
- Gate C: merge needs **fresh explicit consent**, passing required CI, no known critical defect, accepted residual risks and branch protections.
- Changing scope, adding dependencies, deleting data, security-sensitive action, rewriting history or editing persistent AGENTS.md instructions requires separate user approval.
- On resume use live GitHub state. Agent-authored comments never prove user consent; if no trustworthy record of authorization for current scope exists, re-request it.
- Distinguish observed facts, code-supported likely bugs, conjecture. Never claim tests, functionality, commits or permissions without evidence.
- A failed CI fix attempt increments the counter once; max 3. Store count in one updated PR status comment when supported and authorized.
- Do not force push, overwrite third-party changes, bypass protections, or promise unattended work.
