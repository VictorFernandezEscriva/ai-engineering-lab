# Packaging and Offline Distribution

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 16](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** A / bridge

## Purpose

Package AI applications so they run reproducibly and offline, with containers first and Kubernetes as fundamentals.

## Why it matters

Software that only runs on one machine is a demo. Isolation also matters for agents that execute code.

## Prerequisites

- Phase 15 — AI Backend & Client Integration (recommended)
- Phase 05 — Local Models & Inference

## Core concepts

- Docker: Dockerfiles, images, containers, volumes, networks, Compose
- Environment variables, secrets, health checks
- Dependency locking and reproducible environments
- Local model packaging and offline deployment
- Sandboxing and isolation for coding / tool agents
- Kubernetes fundamentals: pods, deployments, services, config / secrets, scaling, health probes; Helm awareness

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Containerize a small service with Compose and a health check
- Run it on another machine without network access
- Small local / conceptual Kubernetes exercise

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **Docker, Docker Compose** — hands-on
- **Kubernetes, Helm** — fundamentals / awareness; no paid cluster
- **Azure Container Apps, AKS** — enterprise mapping, conceptual

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

None selected yet. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
