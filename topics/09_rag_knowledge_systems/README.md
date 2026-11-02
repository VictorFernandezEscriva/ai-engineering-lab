# RAG and Knowledge Systems

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 09](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** Bridge (Core and Applied)

## Purpose

Ground generation in external documents: ingest, retrieve, build context, cite and abstain, and evaluate each stage separately.

## Why it matters

Companies mostly need models that answer from their own documents. RAG also fails in specific ways (missing evidence, poor chunks, unsupported claims) that must be measured.

## Prerequisites

- Phase 06 — LLM Application Interfaces
- Phase 08 — Embeddings & Semantic Retrieval

## Core concepts

- Ingestion, parsing and chunking
- Embeddings, indexing, retrieval and reranking
- Context construction and grounded generation
- Citations and abstention
- Hybrid retrieval and query rewriting
- RAG evaluation and failure modes

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet.

- Minimal local RAG with citations
- Retrieval failure analysis

Every applied experiment should state its baseline, what success means, the failure modes, how generalization is tested, whether AI beats deterministic logic, what happens when the model fails, and when a human intervenes.

## Relevant technologies

- Local models via Ollama / llama.cpp
- Local indexes (NumPy, FAISS, SQLite)
- LangChain only after the from-scratch version

ZERO EXTRA COST: local models, open-source tools and free official resources only.

## Selected learning resources

LangChain / LangGraph learning material (RAG), after the from-scratch version. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
