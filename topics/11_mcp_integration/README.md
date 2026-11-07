# MCP and Agent Interoperability

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 11](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** B — Applied AI Automation & Agentic Systems

## Purpose

Learn how tools and context are exposed to agents (MCP), how independent agents talk to each other (A2A) and which standards make that interoperable.

## Why it matters

Integration is the bulk of real agent work. Protocols define the boundary; they do not provide permission policy.

## Prerequisites

- Phase 10 — Agentic Systems Fundamentals (tools, permissions)

## Core concepts

- MCP: client / server, tools, resources, prompts, discovery, stdio and Streamable HTTP, authorization, local versus remote servers, tool schemas
- Security boundaries, least privilege, approval for sensitive actions
- A2A (Agent2Agent): agent discovery, capabilities, tasks, cross-framework interoperability, security boundaries
- MCP ↔ A2A: agent ↔ tools / context versus agent ↔ agent
- OpenAPI, JSON Schema, OAuth / OIDC for interoperable tools and services

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Minimal local MCP server with one or two safe tools
- MCP client interaction
- Least-privilege and approval exercise
- A2A concept walkthrough (reading / diagramming, not a dependency)

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **MCP** — hands-on
- **A2A** — planned: awareness-to-practice, not an immediate dependency
- **AG-UI and other agent / UI protocols** — awareness only unless later market evidence justifies promotion

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

None specific yet. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
