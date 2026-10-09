# Minimal output patterns

## Repository picker
**Choose a repository** — prefer native radio/select/action with owner/name, short description and verified attributes. Text fallback only if native choices unavailable.

## Repository Overview (mandatory after selection)
Show compact Dream header and one native interactive stepper: **Repo → Rules → Docs → Tasks** (each stage has an icon, active/completed/error state and a clickable stage control). Keep the navigation visible and display only the selected stage content. Use shared selection state for stage buttons and Back/Next; these are real UI actions, not decorative labels. Read repo metadata, root/applicable nested AGENTS.md or AGENT.md, README, open Issues and open PRs automatically before showing the ready Tasks tab. Cache fetched data in the rendered view; switching tabs does not call GitHub. Rules displays an expandable sourced list; missing/error instructions are explicit. Docs gives a concise README summary. Tasks displays real linked open Issues and PRs or an honest empty/error state. Default to Tasks when initialization succeeds. Show compact Ponytail / Grill Me / Writes locked indicators. If native stateful controls are unavailable, provide a small textual overview and functional follow-up choices; never counterfeit completion.

## Issue draft
**Type:** bug (confirmed / suspected), feature, or chore. **Outcome:** measurable. **Evidence:** verified code path/reproduction or explicit hypothesis. **Scope / exclusions:** concise. **Acceptance:** checkable. **Checks:** observable verification. **Method:** Ponytail full (only if actually applied). **Grill Me:** used/offered/not needed.

## Plan
`Discover → Issue [approved] → Plan [approval] → Code → CI → PR → Merge [approval]`
3–6 actions; affected paths, verification, main risk. `Approve / Revise / Clarify`.

## Execution
`Done 2/5 · Current: CI · Blocker: none` with only tool-confirmed steps. Prefer real host system task tracker if accessible.

## Final
`repo · Issue #N · PR #N · Status` / Result, verified checks, real risk, one next action.
