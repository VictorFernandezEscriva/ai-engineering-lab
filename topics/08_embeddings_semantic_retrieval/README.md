# Embeddings and Semantic Retrieval

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 08](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** A — Core AI Engineering

## Purpose

Learn how text becomes vectors and how lexical, vector and hybrid retrieval rank documents, and how to evaluate that ranking.

## Why it matters

RAG quality is bounded by retrieval quality. This phase is about external embedding models used for retrieval, not the internal Transformer token embeddings of Experiment 14.

## Prerequisites

- Phase 06 — LLM Application Interfaces (calling an embedding model)
- Phase 04 — LLM Engineering (embeddings concept)

## Core concepts

- Embedding models, dense vectors, cosine similarity
- BM25 and sparse retrieval concepts
- Nearest neighbors, approximate nearest neighbors (ANN), HNSW
- Chunking, metadata, metadata filtering
- Hybrid retrieval and reranking
- Retrieval evaluation: recall and precision

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet. Larger experiments follow the Lab-wide incremental-delivery rule (milestone → acceptance criterion → implementation → tests → evidence).

- Sentence similarity
- Semantic search over a small corpus (exact in-memory first)
- BM25 versus dense retrieval
- One local vector index
- Retrieval evaluation with labeled queries

Every applied experiment states its problem, baseline, success metric, what changed, evidence of improvement, remaining failure modes and the simplest architecture that works.

## Relevant technologies

- **FAISS, PostgreSQL + pgvector, Qdrant** — hands-on: use one or two for a practical comparison; mastering all three is not required
- **Azure AI Search** — enterprise mapping: lexical, vector, hybrid, semantic ranking, metadata filtering, access patterns; no Azure deployment required

See [Professional capabilities and technology tiers](../../docs/professional-capabilities.md) for tiers. ZERO EXTRA COST: local models, open-source tools and free official resources only; enterprise and paid services are studied conceptually unless explicitly authorized.

## Selected learning resources

None selected yet. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
