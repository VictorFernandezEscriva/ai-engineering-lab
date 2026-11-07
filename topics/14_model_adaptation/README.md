# Model Adaptation

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 14](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** A — Core AI Engineering

## Purpose

Adapt a pretrained model with fine-tuning, LoRA and QLoRA, and know when not to.

## Why it matters

Most problems are solved with better context or prompts. Adaptation needs a baseline, quality data and an evaluation set.

## Prerequisites

- Phase 05 — Local Models & Inference
- Phase 06 — prompt evaluation (baseline)

## Core concepts

- Fine-tuning and instruction tuning
- LoRA, QLoRA, PEFT
- Dataset quality, train / eval splits, synthetic-data concepts
- Model distillation
- When NOT to fine-tune; RAG versus fine-tuning; prompt optimization versus fine-tuning

```text
change the context → RAG
change the prompt / program → DSPy-style optimization
change the weights → fine-tuning / LoRA / QLoRA
```

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Small controlled adaptation compared with prompt-only and retrieval baselines

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **Hugging Face PEFT tooling** — hands-on, scoped to available memory
- **DSPy** — later: prompt / program optimization, kept conceptually distinct from changing weights

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

Hugging Face LLM Course (fine-tuning chapters). Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
