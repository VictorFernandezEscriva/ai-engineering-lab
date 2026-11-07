# RAG and Knowledge Systems

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 09](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** Bridge (Core and Applied)

## Purpose

Build grounded question answering over documents and evaluate retrieval and generation separately, including security of the knowledge base.

## Why it matters

RAG is the most common enterprise pattern. Failures are usually retrieval, permission or provenance failures, not model failures.

## Prerequisites

- Phase 08 — Embeddings & Semantic Retrieval
- Phase 06 — LLM Application Interfaces

## Core concepts

- Ingestion, parsing, OCR concepts, chunking, metadata
- Embedding, indexing, retrieval, reranking
- Context construction, citations, grounding, abstention
- Query rewriting, multi-query retrieval, hybrid RAG
- RAG evaluation and failure modes
- Document-level security and permission-aware retrieval
- RAG poisoning and data provenance

## Enterprise scenarios

Internal knowledge base · technical documentation · policy assistant · support knowledge assistant · document intelligence.

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Minimal local RAG with citations (from scratch first)
- Retrieval failure analysis
- Permission-aware retrieval toy
- Hybrid retrieval or query rewriting once a baseline exposes a failure

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **From-scratch local RAG** — hands-on
- **LlamaIndex** — compare: retrieval / RAG / workflows framework, only after the from-scratch experiment
- **Azure AI Search** — enterprise mapping for enterprise RAG and access control

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

LangChain / LangGraph learn (RAG), after the from-scratch version. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
