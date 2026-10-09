---
name: brainstorming
description: Explore ideas, compare approaches, and agree on designs before implementation; use for exploratory intent rather than every development task.
---

# Brainstorming Ideas Into Designs (Dream adaptation)

Upstream: https://github.com/obra/superpowers/blob/8ca22dba9a94f28898bbce59f2537ff4d87c747d/skills/brainstorming/SKILL.md
Pinned revision: `8ca22dba9a94f28898bbce59f2537ff4d87c747d` (obra/superpowers).
License: MIT, Copyright (c) 2025 Jesse Vincent; see adjacent `LICENSE`.
Adaptation: preserves shared-understanding, Spike/Bounded/Architectural paths and human design review, but replaces upstream tool-specific writing-plans, browser companion, task manager, scaffolding and design-file commits with Dream's existing approval-gated workflow. This adaptation is not a verbatim upstream copy.

## Scope and entry

Activate for exploratory user intent: ideation, comparison, creative alternatives, or open-ended design questions. Do not force brainstorming for straightforward factual answers, routine fixes, or explicit approved GitHub development work. When requirement ambiguity is the core problem, use bundled Grill Me; when implementing, use Ponytail full in Dream's GitHub workflow. An exploratory discussion remains **read-only**; never treat an agreed design as GitHub authorization.

## Shared understanding

1. Identify the user's desired outcome, intended audience, constraints, and success criteria using existing context. If a material detail is missing, ask **one focused question** rather than inventing requirements.
2. Briefly reflect the inferred goal and any assumptions, invite correction, and reuse confirmed context in follow-up turns instead of restarting the interview.
3. Match the depth of exploration to the scope, and recommend an approach with clearly stated trade-offs.

## Choose proportionate depth

- **Spike — feasibility question.** Frame the question and minimal safe *read-only* investigation in two or three sentences; obtain agreement before sensitive probing. Investigate via available read-only tools and report findings, limitations and recommendation. Never execute arbitrary project code or retain throwaway artifacts without separate authorization.
- **Bounded — small change to an existing flow.** Inspect relevant project context, ask only essential questions, present a short design **in chat** (approach, affected areas, checks), and request design feedback. If the user then requests implementation, hand off to Dream Gate A/B; design approval alone does not grant write access.
- **Architectural — new system, project or major design.** Understand goals, compare two or three viable options with costs, benefits and risks; recommend one; discuss the design in manageable sections and confirm shared understanding. Provide a written specification only when requested or authorized. Implementation requires Dream's separately approved Issue and plan, rather than assuming upstream `writing-plans` or direct commits.

If hidden complexity appears, increase the depth and explain why. Avoid mandatory lengthy process for simple ideation.

## Authorization boundary (mandatory)

Brainstorming is read-only by default. A user's agreement with an idea, feasibility probe or design **is not Gate A, Gate B, merge consent, or publication consent**. Never create/edit GitHub Issues, branches, commits, PRs, workflows or deployments, install dependencies, publish private assets or execute untrusted code solely because of brainstorming. When the user explicitly requests implementation, switch to Dream's `skills/github-development/SKILL.md` process; draft an English Issue for Gate A and separately obtain Gate B plan approval. Preserve merge and publication approvals. Never assume tool availability; if a visual companion, terminal or other upstream tool is unavailable, explain the limitation and use grounded chat-native alternatives.

## Required next actions

For every completed substantive brainstorming response with a meaningful next step, offer **functional native ChatGPT buttons** such as Continue brainstorming, Compare approaches, Clarify with Grill Me, or Draft Issue for Gate A. Each callback must perform only its stated step. Draft Issue prepares a draft in chat and **must not create** a GitHub Issue. Localize labels. If native controls are unavailable, use concise text options. Do not add inert buttons or controls to mere progress updates.

## Verification cases

Game idea without coding → Brainstorming; architecture comparison → Brainstorming; conflicting requirements → Grill Me; routine fix → Dream/Ponytail; accepted design without Issue approval → read-only; explicit implementation request after design → Gate A then Gate B; resumed discussion → reuse context; straightforward factual question → answer directly; unavailable upstream tool → acknowledge limitation; private repository → preserve confidentiality.
