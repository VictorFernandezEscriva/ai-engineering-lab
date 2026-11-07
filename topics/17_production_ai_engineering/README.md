# Production AI Engineering

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 17](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** Bridge (Core and Applied)

## Purpose

Integrate software engineering, LLMOps / MLOps and enterprise AI: delivery, evaluation pipelines, observability, governance.

## Why it matters

Production is where Core AI and Applied automation converge. Reliability is a measured property.

## Prerequisites

- Phases 09, 10 and 15 (RAG, agents, backend) and cross-cutting evaluation and security

## Core concepts

- Git, branching, PR discipline, CI / CD, GitHub Actions concepts, automated testing
- Evaluation pipelines and regression suites
- Model, prompt and dataset versioning; configuration management
- Rollback, canary and feature-flag concepts
- Observability: logging, tracing of LLM / tool / agent steps, metrics, latency, token and cost tracking, drift and feedback loops, OpenTelemetry concepts
- Security, privacy, safety, governance, audit trails
- Technical communication: decision records, runbooks, README evidence

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Evaluation pipeline run in CI
- Trace an agent run end to end
- Prompt rollback exercise
- Cost and latency report

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **Git, GitHub Actions (concepts)** — hands-on at small scale
- **OpenTelemetry** — concepts
- **Azure Monitor, Application Insights, Entra ID, Key Vault, Microsoft Foundry (evaluation, tracing, governance)** — enterprise mapping, conceptual; no paid Azure resources

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

None selected yet. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
