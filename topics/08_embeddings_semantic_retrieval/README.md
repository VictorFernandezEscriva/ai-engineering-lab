# Embeddings and Semantic Retrieval

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 08](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** A — Core AI Engineering

## Purpose

Learn how text becomes vectors for retrieval and how similarity search ranks documents.

## Why it matters

Retrieval quality limits every RAG system. This phase separates the *internal* token embeddings of a Transformer (studied in Experiment 14) from *external* embedding models used for semantic search.

## Prerequisites

- Phase 06 — LLM Application Interfaces
- Phase 04, Experiment 14 (internal token embeddings) for the contrast

## Core concepts

- Embedding models, sentence and document embeddings
- Vector similarity and cosine similarity
- Nearest-neighbor and semantic search
- Chunking and metadata
- Local indexes (FAISS concepts)
- Retrieval evaluation and reranking

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet.

- Sentence similarity
- Semantic search over a small collection
- Local vector index
- Retrieval evaluation

Every applied experiment should state its baseline, what success means, the failure modes, how generalization is tested, whether AI beats deterministic logic, what happens when the model fails, and when a human intervenes.

## Relevant technologies

- NumPy (exact in-memory similarity first)
- FAISS or SQLite-based approaches as optional later comparisons
- Local open embedding models

ZERO EXTRA COST: local models, open-source tools and free official resources only.

## Selected learning resources

None specific yet. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
