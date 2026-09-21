# AI Engineering Roadmap

This is a learning path, not the directory hierarchy. Topics are grouped by technical domain. Future work stays here until it starts; no placeholder folders are required. Existing implementations are not proof of mastery.

## Phase 01 — Machine Learning foundations

**Status:** Existing experiments; reviewed, with verification limits.

- **Concepts:** features, targets, trees, generalization.
- **Expected practical work:** Review the two existing ML experiments; later compare depths and splits.
- **Before continuing:** Explain held-out evaluation and the limits of tiny samples.

## Phase 02 — Deep Learning foundations

**Status:** Existing experiments; reviewed, with verification limits.

- **Concepts:** tensors, logits, loss, gradients, thresholds.
- **Expected practical work:** Review the two existing neural classifiers and their recorded metrics.
- **Before continuing:** Trace forward/backward passes and explain normalization without leakage.

## Phase 03 — Computer Vision foundations

**Status:** Existing experiments; reviewed, with verification limits.

- **Concepts:** kernels, channels, pooling, image datasets.
- **Expected practical work:** Review fixed filters; complete shape CNN runs and MNIST loading.
- **Before continuing:** Trace tensor shapes and distinguish training fit from held-out accuracy.

## Phase 04 — LLM fundamentals

**Status:** IN PROGRESS: conceptual introduction.

- **Concepts:** architecture, weights, tokens, embeddings, sampling, context.
- **Expected practical work:** Continue the introductory lesson; later inspect tokenization.
- **Before continuing:** Distinguish model, runtime, application and hardware.

## Phase 05 — Local models and inference

**Status:** Planned.

- **Concepts:** artifacts, loading, inference, resource use.
- **Expected practical work:** Run a compatible small model locally and record configuration.
- **Before continuing:** Explain training versus inference and basic memory constraints.

## Phase 06 — Ollama and local APIs

**Status:** Planned.

- **Concepts:** runtime management, HTTP, request/response.
- **Expected practical work:** Call a local inference endpoint and inspect requests and errors.
- **Before continuing:** Identify the model artifact and the process serving it.

## Phase 07 — Python integration

**Status:** Planned.

- **Concepts:** JSON, streaming, timeouts, configuration.
- **Expected practical work:** Build a small Python CLI client with explicit error handling.
- **Before continuing:** Understand the local API contract and Python exceptions.

## Phase 08 — llama.cpp and GGUF

**Status:** Planned.

- **Concepts:** model format, native/server execution, offload.
- **Expected practical work:** Compare compatible execution paths with recorded settings.
- **Before continuing:** Understand runtime boundaries and distinguish format from architecture.

## Phase 09 — Hardware and quantization

**Status:** Planned.

- **Concepts:** RAM, VRAM, numerical precision, bandwidth.
- **Expected practical work:** Use the hardware tool and compare supported precisions on fixed inputs.
- **Before continuing:** Explain parameter memory and recognize quality/resource trade-offs.

## Phase 10 — Inference benchmarking and evaluation

**Status:** Planned.

- **Concepts:** latency, throughput, quality, repeatability.
- **Expected practical work:** Build a benchmark with warm-up, repeated runs and a fixed evaluation set.
- **Before continuing:** Control model, prompts, hardware and sampling settings.

## Phase 11 — Embeddings

**Status:** Planned.

- **Concepts:** vector representations, similarity, normalization.
- **Expected practical work:** Encode a small text collection and inspect pairwise similarities.
- **Before continuing:** Understand vectors and distinguish embedding output from generated text.

## Phase 12 — Semantic search

**Status:** Planned.

- **Concepts:** ranking, top-k retrieval, relevance.
- **Expected practical work:** Build and evaluate retrieval over a small document collection.
- **Before continuing:** Explain embeddings and similarity; define relevance judgments.

## Phase 13 — RAG

**Status:** Planned.

- **Concepts:** chunking, retrieval, grounded prompts, citations.
- **Expected practical work:** Build document question answering with retrieval and answer evaluation.
- **Before continuing:** Measure retrieval quality and identify unsupported generated claims.

## Phase 14 — Tool calling

**Status:** Planned.

- **Concepts:** schemas, argument validation, execution boundaries.
- **Expected practical work:** Execute a small allowlisted set of application functions.
- **Before continuing:** Separate model requests from authorized application execution.

## Phase 15 — Agents

**Status:** Planned.

- **Concepts:** state, action loops, retries, stopping conditions.
- **Expected practical work:** Implement a bounded loop and inspect its traces and failures.
- **Before continuing:** Understand tool execution, budgets and observable termination.

## Phase 16 — Multimodal models

**Status:** Planned.

- **Concepts:** image/text inputs, representations, resource costs.
- **Expected practical work:** Evaluate a compatible model on a small image-and-text task.
- **Before continuing:** Understand image tensors and text inference evaluation.

## Phase 17 — Fine-tuning / LoRA / QLoRA

**Status:** Planned.

- **Concepts:** adaptation, adapters, quantization, evaluation.
- **Expected practical work:** Run a small controlled adaptation with an independent test set.
- **Before continuing:** Understand training objectives, data quality and baseline comparisons.

## Phase 18 — AI backend engineering

**Status:** Planned.

- **Concepts:** service APIs, concurrency, lifecycle, observability.
- **Expected practical work:** Build a service with streaming, cancellation and bounded resource use.
- **Before continuing:** Understand inference costs, API contracts and failure handling.

## Phase 19 — Flutter integration

**Status:** Planned.

- **Concepts:** Dart clients, streaming UI, application state.
- **Expected practical work:** Build a client for an evaluated backend and handle connection failures.
- **Before continuing:** Understand the backend contract and asynchronous state changes.

## Phase 20 — Packaging and offline distribution

**Status:** Planned.

- **Concepts:** installation, artifacts, compatibility, updates.
- **Expected practical work:** Package a prototype and test it on another machine without network access.
- **Before continuing:** Account for model files, dependency availability and artifact licenses.

## Phase 21 — Production/product engineering

**Status:** Planned.

- **Concepts:** requirements, reliability, privacy, security, maintenance.
- **Expected practical work:** Define acceptance criteria, threat model, regression evaluation and recovery behavior.
- **Before continuing:** Justify the full stack and distinguish a demo from a supported product.
