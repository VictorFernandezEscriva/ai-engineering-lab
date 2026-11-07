# Agentic Systems Fundamentals

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 10](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** B — Applied AI Automation & Agentic Systems

## Purpose

Build a bounded agent from scratch: tools, state, memory, planning, permissions, checkpoints and evaluation.

## Why it matters

Frameworks are only understandable once the loop, its state and its failure modes are. Agents are never the default answer.

## Prerequisites

- Phase 06 — LLM Application Interfaces (structured outputs, tool-call requests)
- Phase 07 — AI Automation Foundations (workflows, approval, reliability)

## Core concepts

- Tool schemas, tool execution, observation / result loop
- Agent loop from scratch; state; termination
- Short-term and long-term memory concepts
- Planning, task decomposition, ReAct, plan-and-execute, routing, reflection / retry
- Context engineering and compaction
- Human-in-the-loop, approvals, permissions, sandboxing
- Background / long-running agents, checkpoints, resume and recovery
- Agent evaluation
- Patterns: single agent + tools, router, supervisor, handoff, planner / executor, parallel fan-out / fan-in, subagents, specialized agents
- Integrations: files, REST APIs, SQL / database, search / retrieval, business systems
- Agent skills: reusable instructions, tool bundles, progressive context loading (later concept)

Early experiments never get unrestricted shell or system access.

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Agent loop from scratch
- Agent with two or three controlled tools
- Memory / state experiment
- Checkpoint and resume
- Pattern comparison against a single-agent baseline
- Minimal Coding-Agent Experiment
- Agent evaluation

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **Plain Python + local model** — hands-on: no framework in this phase

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

Hugging Face Agents Course, consumed after structured outputs, tool calling and the minimal loop. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
