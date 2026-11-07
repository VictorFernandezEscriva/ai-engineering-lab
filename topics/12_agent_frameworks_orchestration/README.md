# Agent Frameworks and Orchestration

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 12](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** B — Applied AI Automation & Agentic Systems

## Purpose

Learn LangChain, LangGraph, n8n AI workflows and Microsoft Agent Framework as implementations of concepts already built by hand, and compare workflows with agents.

## Why it matters

Frameworks save effort only when you know what they do for you. Rule: primitive first, minimal implementation second, framework third.

## Prerequisites

- Phase 10 — Agentic Systems Fundamentals
- Phase 07 — AI Automation Foundations (for n8n)
- Phase 09 — RAG (for agentic RAG)
- Phase 11 — MCP (recommended)

## Core concepts

- LangGraph: explicit state, nodes, edges, routing, durable execution, checkpoints, human-in-the-loop, retries, subgraphs, multi-agent orchestration
- Microsoft Agent Framework: agents, tools, sessions / state, memory, middleware, workflows, MCP, human-in-the-loop, telemetry, hosting concepts
- n8n AI workflows
- Routers, handoffs, subagents; agentic RAG; workflow-versus-agent comparison
- Agent skills and reusable capabilities
- Low-code agents: when to use Copilot Studio versus custom Python agents

## Framework lens

What abstraction does it provide? What does it manage for me? What control do I lose? How does it handle state? How does it execute tools? How does it recover? How does it support evaluation and observability?

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Same workflow: manual versus LangChain / LangGraph
- Small LangGraph workflow with a checkpoint and human approval
- n8n AI workflow
- Subagent experiment
- Agentic RAG comparison
- Framework comparison write-up using the seven questions below

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **LangChain, LangGraph, n8n AI workflows, Microsoft Agent Framework** — hands-on
- **PydanticAI, LlamaIndex agents / workflows, OpenAI Agents SDK architecture, CrewAI** — compare / awareness; do not master all
- **AutoGen, Semantic Kernel** — historical / ecosystem awareness: Microsoft Agent Framework is the modern successor to ideas from both
- **Microsoft Foundry, Copilot Studio** — enterprise mapping; no paid features

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

LangChain / LangGraph learning material, Hugging Face Agents Course and n8n Academy. If a tutorial assumes a paid provider, document a local adaptation instead. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
