# Model Adaptation: Fine-Tuning, LoRA and QLoRA

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 14](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** A — Core AI Engineering

## Purpose

Adapt a pretrained model to a task and compare it against the unchanged baseline.

## Why it matters

Adaptation is costly and often unnecessary; knowing when it beats prompting or retrieval is a core judgement.

## Prerequisites

- Phase 04 — LLM Engineering (training loop)
- Phase 05 — Local Models & Inference
- Phase 09 — RAG (to contrast context with parameter changes)

## Core concepts

- Supervised fine-tuning and instruction tuning
- LoRA, QLoRA, PEFT
- Training-data quality and datasets
- Evaluation against a baseline
- Model merging concepts

## Potential small Lab experiments

Ideas only; no experiment directory or code exists yet.

- Small controlled LoRA adaptation compared with the base model
- Dataset-quality experiment

## Relevant technologies and resources

- PyTorch, PEFT (open source, sized to local memory)
- Resources: Hugging Face LLM Course (adaptation chapters)

ZERO EXTRA COST: local models, open-source tools and free official resources only. Resource links are canonical in the Learning Cockpit catalog.
