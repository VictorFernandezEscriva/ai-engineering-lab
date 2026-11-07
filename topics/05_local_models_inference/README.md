# Local Models and Inference

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 05](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** A — Core AI Engineering (bridge to the applied track)

## Purpose

Run pretrained language models locally and understand what limits them: memory, context, speed and quantization.

## Why it matters

Every later phase calls a model. Knowing what a local runtime does, and what it costs in RAM / VRAM and latency, lets you choose models and set expectations on real hardware (the learner's RTX 2060 Max-Q).

## Prerequisites

- Phase 04 — LLM Engineering (generation, Experiment 30 comes first)

## Core concepts

- Pretrained models, model loading, model selection
- Inference, generation parameters, context windows
- KV-cache concepts
- CPU versus GPU inference; RAM versus VRAM
- Quantization and GGUF
- Tokens per second, time to first token, latency, throughput, batching concepts
- OpenAI-compatible local endpoints

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Run a small model with Ollama and record model, size, hardware, memory, parameters, latency, tokens per second
- Ollama versus llama.cpp on the same prompt
- Quantization comparison with fixed prompts and repeated measurements
- Context length versus memory

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **Ollama, llama.cpp / GGUF** — hands-on: the first practical path
- **vLLM** — awareness: production-oriented serving with an OpenAI-compatible server; not required on this hardware
- **LiteLLM** — awareness: model gateway for routing, retries and provider abstraction

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

Hugging Face LLM Course (pretrained models, model usage). Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
