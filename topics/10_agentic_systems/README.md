# Agentic Systems Fundamentals

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 10](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** B — Applied AI Automation & Agentic Systems

## Purpose

Build the agent loop from scratch and learn what makes it safe and evaluable: tools, state, termination, permissions and human approval.

## Why it matters

Agents are one option, not the default. Understanding the bare loop is what lets you judge frameworks, set permissions and decide when a deterministic workflow is better.

## Prerequisites

- Phase 06 — LLM Application Interfaces (structured outputs, tool-call requests)
- Phase 07 — AI Automation Foundations (workflows, approval, reliability)

## Core concepts

- Validated tool execution
- Agent loop from scratch: state, actions, observations, termination
- Short-term memory and long-term memory concepts
- Planning, retry / reflection loops and error recovery
- Human approval, permissions and sandboxing
- Context engineering
- Agent evaluation

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet.

- Agent loop from scratch
- Agent with 2–3 controlled tools
- Memory / state experiment
- Minimal Coding-Agent Experiment: a tiny controlled repository with `read_file(path)`, `write_file(path, content)` and `run_tests()`
- Agent evaluation

Every applied experiment should state its baseline, what success means, the failure modes, how generalization is tested, whether AI beats deterministic logic, what happens when the model fails, and when a human intervenes.

## Relevant technologies

- Python
- Local models
- pytest for the toy workspace

ZERO EXTRA COST: local models, open-source tools and free official resources only.

## Selected learning resources

Hugging Face Agents Course, consumed after structured outputs, tool calling and the minimal loop. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
