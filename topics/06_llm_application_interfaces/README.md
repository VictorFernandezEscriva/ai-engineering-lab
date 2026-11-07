# LLM Application Interfaces

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 06](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** Bridge (Core and Applied)

## Purpose

Connect Python to a model server and treat prompts as engineering artifacts: contracts, structured outputs, tool calls, evaluation and versioning.

## Why it matters

Everything applied (automation, RAG, agents) sits on this boundary. A parseable answer is not a correct one, and a requested action is not an authorized one.

## Prerequisites

- Phase 04 — LLM Engineering (generation, Experiment 30)
- Phase 05 — Local Models & Inference (a model running locally)

## Core concepts

- Python ↔ model server, HTTP inference, REST, OpenAI-compatible APIs
- Chat / message models; system, developer, user roles
- Streaming, SSE concepts, async requests, concurrency concepts
- Structured outputs: JSON Schema and Pydantic
- Function calling and tool calling
- Timeouts, retry / backoff, rate limits
- Context management and token budgeting
- **Prompt engineering as engineering:** prompt contracts, instruction hierarchy, structured prompts, templates, few-shot examples, typed inputs / outputs, prompt versioning, failure-mode analysis, golden evaluation datasets, regression testing, A/B comparisons, model-specific behavior and migration, prompt-injection resistance, context-budget awareness

## Prompt workflow

```text
define expected behavior → write prompt / instructions → build evaluation cases → observe failures → classify failure modes → modify prompt / context / tools → rerun evaluations → version the improvement
```

Prompting is not ad-hoc wording experimentation.

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Local chat client
- Structured-output extractor with a golden evaluation set
- Streaming client
- First controlled tool call
- Prompt-version regression run: define behavior → prompt → eval cases → observe → classify failures → change → rerun → version

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **Pydantic, JSON Schema, OpenAI-compatible HTTP** — hands-on
- **DSPy** — later: declarative LM programs and metric-driven optimization, after manual prompt fundamentals and an eval set exist
- **Azure OpenAI, Microsoft Foundry endpoints** — enterprise mapping: compare auth, deployments, streaming, structured outputs, tool calling and rate limits conceptually; no paid inference unless explicitly authorized

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

None specific yet; the Hugging Face LLM Course is a general complement. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
