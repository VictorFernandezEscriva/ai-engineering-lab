# AI Backend and Client Integration

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 15](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** Bridge (Core and Applied)

## Purpose

Serve AI capabilities through robust backend services and clients: APIs, streaming, background jobs, queues and events.

## Why it matters

Agent systems combine API requests, background work, events, tools, human approvals and long-running tasks. This is core to real AI-engineering jobs.

## Prerequisites

- Phase 06 — LLM Application Interfaces
- Phase 05 — Local Models & Inference
- Phase 07 — reliability and idempotency

## Core concepts

- FastAPI, Pydantic, async Python, REST, OpenAPI
- SSE and WebSockets concepts; cancellation; bounded concurrency
- Background jobs, queues, workers
- PostgreSQL, transactions, connection pooling; Redis concepts and caching
- Microservices versus modular monolith
- Event-driven architecture, pub/sub, message brokers
- Idempotency, circuit breakers, sagas / compensation concepts
- Logging, metrics, structured errors; HTTP clients and streaming UI

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Small inference service with streaming, cancellation, bounded concurrency, structured errors, logs and metrics
- Background-job queue for a long-running task
- Event-driven approval flow

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **FastAPI, Pydantic, PostgreSQL** — hands-on
- **Redis, RabbitMQ, Kafka** — compare / concepts; mastery of all brokers is not required
- **Azure Service Bus, Event Grid** — enterprise mapping, conceptual

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

None selected yet. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
