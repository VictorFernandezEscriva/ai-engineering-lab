# AI Automation Foundations

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 07](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** B — Applied AI Automation

## Purpose

Analyze real business processes and automate them with deterministic workflows, reliable API integration and human approval, adding AI only where it helps.

## Why it matters

Most real automation value is plumbing done reliably. The decision hierarchy keeps agents from being the default answer.

## Prerequisites

- Phase 06 — LLM Application Interfaces (for the AI steps); the process, HTTP and workflow fundamentals can start independently

## Core concepts

- Business-process discovery and workflow mapping
- Deterministic versus probabilistic steps
- HTTP, REST, JSON, OpenAPI, webhooks
- API keys, OAuth2 / OIDC concepts
- Pagination, rate limiting, timeouts, retries, exponential backoff, idempotency
- Input validation, data transformation, error handling
- Human approval and auditability
- n8n (local, self-hosted)
- Decision hierarchy: plain function → deterministic workflow → LLM call → RAG → agent → multi-agent
- API-first versus browser automation: prefer supported APIs before browser automation

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Deterministic incident triage
- Webhook → validation → routing
- API → transform → output with pagination and retry
- Human-approval workflow
- A simple local n8n workflow
- Small API versus Playwright comparison

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **n8n (self-hosted), OpenAPI** — hands-on
- **Playwright** — hands-on as an open-source fallback when no supported API exists
- **OAuth2 / OIDC** — awareness of concepts
- **Microsoft Copilot Studio** — enterprise mapping: low-code agents; compared in Phase 12; no paid features

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

n8n Academy (self-hosted / local; no paid tier required). Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
