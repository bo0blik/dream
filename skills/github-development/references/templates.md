# Minimal output patterns

## Repository picker
**Choose a repository** — prefer native radio/select/action with owner/name, short description and verified attributes. Text fallback only if native choices unavailable.

## Repository Overview (mandatory after selection)
Show compact Dream header and one native interactive stepper: **Repo → Rules → Docs → Tasks** (each stage has an icon, active/completed/error state and a clickable stage control). Keep the navigation visible and display only the selected stage content. Use shared selection state for stage buttons and Back/Next; these are real UI actions, not decorative labels. Read repo metadata, root/applicable nested AGENTS.md or AGENT.md, README, open Issues and open Pull Requests automatically before showing the ready Tasks tab. Cache fetched data in the rendered view; switching tabs does not call GitHub. Rules displays an expandable sourced list; missing/error instructions are explicit. Docs gives a concise README summary. Tasks displays real linked open Issues and PRs or an honest empty/error state. Default to Tasks when initialization succeeds. Show compact Ponytail / Grill Me / Writes locked indicators. If native stateful controls are unavailable, provide a small textual overview and functional follow-up choices; never counterfeit completion.

### Canonical native stateful pattern

Use this as the **interaction pattern**, adapting localized labels, loaded real data and verified statuses. The example uses DIL native controls; never output a literal code fence as the UI. Declare state once, outside the markup, and update it from real clicks. Do not use a network request in a tab callback.

```jsx
{@body const [stage, setStage] = DIL.useState(3)}
{@body const stages = [
  { label: "Repo", icon: "github" },
  { label: "Rules", icon: "shield-check" },
  { label: "Docs", icon: "book-open" },
  { label: "Tasks", icon: "list-todo" }
]}
<box gap={3}>
  <row align="center" justify="between">
    **Dream · owner/repo**
    <badge>Ready</badge>
  </row>
  <grid columns={4} gap={1}>
    {#each stages as item, index}
      <grid-item>
        <pressable key={item.label} onClick={()=>setStage(index)}
          background={stage===index?"surface-tertiary":"surface-secondary"}
          radius="lg" padding={2} align="center" gap={1}>
          <icon name={item.icon}/>
          <text size="xs" weight={stage===index?"semibold":"normal"}>{item.label}</text>
          <icon name={stage===index?"circle-dot":"check-circle-2"} size="xs"
            color={stage===index?"default":"success"}/>
        </pressable>
      </grid-item>
    {/each}
  </grid>
  {#if stage===0}
    <text>Verified repository and default branch</text>
  {:else if stage===1}
    <text>Verified AGENTS.md rules with source paths; expandable list</text>
  {:else if stage===2}
    <text>Verified README summary and document links</text>
  {:else}
    <text>Real open Issues and PRs, or explicit empty/error state</text>
  {/if}
  <row justify="between">
    <button disabled={stage===0} onClick={()=>setStage(Math.max(0,stage-1))}>Back</button>
    <button disabled={stage===3} onClick={()=>setStage(Math.min(3,stage+1))}>Next</button>
  </row>
  <text size="xs" color="secondary">Ponytail · Grill Me · Writes locked</text>
</box>
```

The example's "Ready" badge and check icons are **illustrative only**: in a real response derive them from successfully completed read operations; replace unfinished/failed stages with truthful pending/error indicators. Populate the stage bodies with fetched data before rendering. The exact code syntax may vary with the host's supported native UI; if unavailable, use a truthful compact text fallback with functional next actions. Never display invented files, issues, PRs, or success badges.

## Issue draft
**Type:** bug (confirmed / suspected), feature, or chore. **Outcome:** measurable. **Evidence:** verified code path/reproduction or explicit hypothesis. **Scope / exclusions:** concise. **Acceptance:** checkable. **Checks:** observable verification. **Method:** Ponytail full (only if actually applied). **Grill Me:** used/offered/not needed.

## Plan
`Discover → Issue [approved] → Plan [approval] → Code → CI → PR → Merge [approval]`
3–6 actions; affected paths, verification, main risk. `Approve / Revise / Clarify`.

## Execution
`Done 2/5 · Current: CI · Blocker: none` with only tool-confirmed steps. Prefer real host system task tracker if accessible.

## Final
`repo · Issue #N · PR #N · Status` / Result, verified checks, real risk, one next action.
