# LLM Application Interfaces

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 06](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** Bridge (Core and Applied)

## Purpose

Bridge model fundamentals to usable applications: call a local model from Python, shape its input, and turn its output into data a program can trust.

## Why it matters

Every automation, RAG system and agent starts with a reliable boundary between application code and a model. Errors here (malformed output, timeouts, unvalidated arguments) propagate to everything built on top.

## Prerequisites

- Phase 04 — LLM Engineering (generation, Experiment 30)
- Phase 05 — Local Models & Inference (a model running locally)

## Core concepts

- Python ↔ local LLM request/response boundary
- Chat/message interfaces and system/user/assistant roles
- Prompt construction
- Streaming
- Structured outputs, JSON Schema and validation
- Function calling and tool-calling foundations (a request is not an authorization)
- Error handling, timeouts and bounded retries

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet.

- Local chat client
- Structured-output extractor
- Streaming client
- First controlled tool call

Every applied experiment should state its baseline, what success means, the failure modes, how generalization is tested, whether AI beats deterministic logic, what happens when the model fails, and when a human intervenes.

## Relevant technologies

- Python standard library HTTP client
- Ollama / llama.cpp local servers (from Phase 05)
- JSON Schema; Pydantic as an optional validation tool

ZERO EXTRA COST: local models, open-source tools and free official resources only.

## Selected learning resources

None specific yet; the Hugging Face LLM Course is a general complement. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
