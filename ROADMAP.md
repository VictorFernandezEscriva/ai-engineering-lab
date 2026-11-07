# AI Engineering Roadmap

This roadmap defines the main learning progression of the repository.

It is not the repository directory hierarchy.

Topics are grouped by technical domain, while this document describes learning order.

Future work remains documented here until implementation begins.

The [AI Engineering Map](docs/ai-engineering-map.md) describes the territory: what exists and how the branches relate. This roadmap describes the selected route through it. Neither requires mastering every branch before building useful systems.

**Lab scope:** theory, concept explanations, small focused exercises and small controlled experiments that explain concepts from first principles. Learn the underlying concepts here before combining them into larger systems in independent repositories. This lab does not plan or catalog those repositories. Complex areas such as RAG, coding agents, MCP, workflow frameworks, voice and multimodal AI can have small educational experiments here.

**ZERO EXTRA COST:** prefer open-source software, local models, local execution and free official datasets/resources. No paid API, credits, hosted inference or paid infrastructure is required. Adapt experiment scale to available hardware.

The learning process follows:

```text
CONCEPT
↓
QUESTION
↓
HYPOTHESIS
↓
IMPLEMENTATION
↓
EXPERIMENT
↓
EVIDENCE
↓
INTERPRETATION
↓
LIMITATIONS
↓
PRODUCT CONNECTION
```

The objective is not to study every AI technology with equal depth.

The main path prioritizes:

1. transferable fundamentals,
2. practical AI Engineering,
3. employability,
4. ability to build real systems,
5. architectural judgement,
6. local and production AI.

---

# Main Learning Path

The professional direction is **AI Automation & Agentic Systems Engineering**. The lab teaches it through two complementary tracks that never replace each other:

| Track | Question it answers | Examples |
|---|---|---|
| **A — Core AI Engineering** | How do AI systems work, well enough not to treat models, frameworks and agents as black boxes? | ML, DL, CV, Transformer internals, LLM generation, local models, embeddings, RAG, evaluation, model adaptation, production AI |
| **B — Applied AI Automation & Agentic Systems** | How do I identify, design, build and evaluate useful AI-powered automations and agents for real processes? | process analysis, APIs, webhooks, n8n, structured outputs, tool calling, agent loops, MCP, LangChain / LangGraph, orchestration, human approval |
| **Bridge** | Topics that belong to both | local models, structured outputs, tool calling, RAG, evaluation, security, production engineering |

Track B builds on Track A. It does not shortcut it: a framework or an agent is learned after the primitive it implements.

```text
PHASES 01–05 (Core AI, current)
ML → DL → CV → Transformer / LLM internals → Local models & inference
                                                   │
                                                   ▼
                              06 LLM Application Interfaces      (bridge)
                                                   │
                       ┌───────────────────────────┴───────────────────────────┐
                       │                                                       │
        CORE AI                                                  APPLIED AUTOMATION
   08 Embeddings & Semantic Retrieval                       07 AI Automation Foundations
                       │                                    (process analysis, APIs, webhooks, n8n)
                       ▼                                                       │
   09 RAG & Knowledge Systems  ◄── bridge ──┐                                  │
                       │                     └──► 10 Agentic Systems Fundamentals
                       │                                    (tool use, agent loop, state, approval)
                       │                                                       │
                       │                                            11 MCP & Integration
                       │                                                       │
                       └───────────────► 12 Agent Frameworks & Orchestration ◄─┘
                                                   │
        Later Core AI: 13 Multimodal / Voice · 14 Model adaptation
                                                   │
                       15 AI Backend · 16 Offline packaging · 17 Production AI
```

Phase numbers stay sequential and identify study blocks; the two tracks run in parallel conceptually. Phase 07 depends on Phase 06 for the AI steps but its process, API and workflow fundamentals do not need retrieval; Phase 10 depends on Phase 06 and Phase 07, not on RAG.

## Professional problem-solving is part of the curriculum

Track B is not "learn n8n buttons, the LangChain API and LangGraph syntax". It teaches reasoning about a business problem:

```text
Problem / process discovery
↓
Map the current workflow
↓
Identify deterministic steps
↓
Identify uncertain / semantic steps
↓
Decide whether AI is actually appropriate
↓
Select model / tool / workflow architecture
↓
Define structured inputs and outputs
↓
Integrate APIs and data
↓
Handle failures, retries and timeouts
↓
Add human approval where necessary
↓
Evaluate against a baseline
↓
Observe and monitor
```

Choose the simplest architecture that solves the problem. An agent is never the default answer.

| Architecture | Use it when | Main cost |
|---|---|---|
| Normal deterministic code | Rules are known, inputs are structured | Rigid on unforeseen inputs |
| Workflow automation | Steps are known, systems must be connected | Maintenance of integrations |
| Single LLM call | One semantic step (classify, extract, summarize) | Output must be validated; can be wrong |
| RAG | The answer depends on external documents | Retrieval quality limits the answer |
| Agent | The sequence of steps cannot be fixed in advance | Unpredictable path, cost and failure modes; needs permissions and evaluation |
| Multi-agent system | Separable roles that a single agent cannot hold | Coordination overhead; needs a single-agent baseline |

## Evaluation, security and reliability apply to every phase

Every applied automation or agent experiment should eventually answer:

```text
What is the baseline?
What does success mean?
What failure modes exist?
How do we test generalization?
How do we know AI is better than deterministic logic?
What happens when the model fails?
When should a human intervene?
```

Security and reliability topics appear from the first interface onward: input validation, prompt injection, untrusted data, tool permissions, path restrictions, secret handling, privacy, timeouts, retries, idempotency, human approval, sandboxing, structured-output validation, logging and observability. The goal is systems a company could realistically trust, not demos.

Cross-cutting skills: requirements and problem framing, process mapping, API integration, data schemas, validation, reliability, error handling, human-in-the-loop, evaluation, observability, privacy, security, cost awareness, build-vs-buy reasoning and local-vs-hosted architecture.

## Professional competency layer (curriculum targets, not claimed skills)

Real AI-agent job descriptions repeat the same capabilities. They are **targets** of this curriculum; the lab does not claim the learner has them. Each is taught inside existing phases, not in a new one.

| Competency | Where it is taught |
|---|---|
| Complex tool integration | 06 tool calling · 10 validated tool execution · 11 MCP |
| Multiple data sources | 08–09 retrieval · 10 files / REST / SQL / search integrations |
| Agent orchestration | 10 patterns · 12 LangGraph, Microsoft Agent Framework, n8n |
| Third-party API integration | 07 REST / OpenAPI / OAuth, pagination, rate limits, idempotency |
| Prompt engineering as product work | 06 prompt contracts, evaluation sets, versioning · 17 regression |
| Incremental delivery | Lab-wide rule (see below) · 17 Git / PR discipline |
| Testing and evaluation | 06 golden sets · 08–09 retrieval / RAG evaluation · 10 agent evaluation · 17 pipelines |
| Backend engineering | 15 FastAPI, Pydantic, async, PostgreSQL, queues |
| State management | 10 state / memory / checkpoints · 12 explicit graph state |
| Event-driven architectures | 15 pub/sub, brokers, background jobs, sagas (concepts) |
| Deterministic + generative hybrid systems | 07 decision hierarchy · 12 workflow versus agent |
| CI/CD | 17 GitHub Actions concepts, automated tests, rollback, canary |
| Containerization | 16 Docker, Compose, Kubernetes fundamentals |
| Cloud architecture | 15–17 Azure mapping (conceptual, no paid resources) |
| Observability | 17 tracing, metrics, cost · cross-cutting from Phase 06 |
| MCP | 11 |
| Technical communication | every experiment README · 17 decision records and runbooks |

The full map, including the Microsoft / Azure concept mapping, is in [Professional capabilities and technology tiers](docs/professional-capabilities.md).

## Technology tiers (avoid curriculum explosion)

```text
CONCEPT / CAPABILITY
→ curriculum node (Cockpit)

IMPORTANT TECHNOLOGY WE WILL PRACTICE
→ technology metadata, and a node only when pedagogically justified

ALTERNATIVE / ECOSYSTEM TOOL
→ technology reference: comparison or awareness
```

"Agent state management" is a concept (node); **LangGraph** is a hands-on technology that implements it; **CrewAI** is comparison / awareness unless later evidence justifies deeper study. The Cockpit keeps a `technologies` registry with one of these tiers per technology (`hands-on`, `compare`, `awareness`, `enterprise-mapping`) instead of one node per product.

## Incremental delivery (Lab-wide engineering rule)

Larger future experiments are decomposed so every meaningful commit / PR-sized increment either delivers user value or creates a deliberate, verified technical milestone.

```text
problem
↓
small milestone
↓
acceptance criterion
↓
implementation
↓
tests / evaluation
↓
evidence
↓
next milestone
```

For non-trivial experiments: clear scope, acceptance criteria, small commits, tests, README / result evidence, known limitations and a next step. Tiny exercises do not need manufactured commits.

## Outcome-oriented engineering

Every relevant automation or AI experiment answers:

```text
What problem are we solving?
What is the baseline?
What metric defines success?
What changed?
What evidence shows improvement?
What failure modes remain?
What is the simplest architecture that works?
```

This builds a track record of engineering outcomes rather than demos.

---

## Route After Phase 04

**Current:** Phase 04 is `IN PROGRESS`; Experiments 13–29 are recorded as complete. **Experiment 29 — Language-Model Training Loop is `COMPLETE`. Experiment 30 — Autoregressive Generation and Sampling remains `NEXT`.** Its practical generation workflow has not been completed.

**Then:** Phase 05 — Local Models and Inference, followed by the combined route below.

Existing phase numbers 01–05 and completed experiment history are retained. Phases 06 onward were reorganized (before any of them started) to separate the two tracks; former phase numbers are mapped in each phase below. The numbers identify study blocks; they do not require finishing every topic in one block before beginning another.

| Route block | Phases | Track | Focus and readiness to continue |
|---|---|---|---|
| 1. Finish the current LLM workflow | Phase 04, Experiment 30 | A | Connect final-position logits, token selection and repeated generation; distinguish training from inference |
| 2. Run a local model | Phase 05 | A / bridge | Loading, runtimes, hardware, quantization, benchmarking |
| 3. Call it from code | Phase 06 | bridge | Chat messages, streaming, structured outputs, validation, first controlled tool call; handle malformed responses and failures |
| 4. Automation fundamentals | Phase 07 | B | Process decomposition, deterministic workflows, HTTP / REST / webhooks, reliability, human approval, n8n basics; rules versus AI |
| 5. Retrieve evidence | Phases 08–09 | A / bridge | Retrieval embeddings, semantic search, RAG; evaluate retrieval and generation separately |
| 6. Bounded action loops | Phase 10 | B | Validated tool execution, agent loop from scratch, state, permissions, agent evaluation |
| 7. Protocols and frameworks | Phases 11–12 | B | MCP, then LangChain / LangGraph / n8n AI workflows as implementations of concepts already understood |
| 8. Add modalities and adapt models | Phases 13–14 | A | Multimodal / voice; fine-tuning / LoRA / QLoRA against an unchanged baseline |
| 9. Study system engineering | Phases 15–17 | A / bridge | Services, offline packaging, production AI, MLOps / LLMOps through small controlled exercises |

Blocks 4 and 5 can be visited in either order after Phase 06. **Parallel tracks:** evaluation, safety, data engineering, testing and software engineering accompany every block. Reinforcement learning and advanced GPU / distributed topics remain later specializations, not immediate prerequisites.

**Rule for frameworks:** primitive first, minimal implementation second, framework third. Agent loop from scratch → LangChain / LangGraph; workflow fundamentals → n8n.

Use sensible learning blocks rather than creating one experiment per API call or line of code. Future names in this document do not create experiment folders or imply completed work.

### External learning resources

Selected free resources complement the experiments; they do not replace them. They are registered once, with their links, in the Learning Cockpit catalog (`resources`), which maps each to the concepts where it is relevant. No course content is copied into the lab, and any assumed paid provider must be replaced by a local or free equivalent.

| Resource | Maps to | When |
|---|---|---|
| Hugging Face LLM Course | LLM fundamentals, tokenizers, pretrained models, datasets, later adaptation (Phases 04, 05, 14) | As industry-tooling reference; do not redo Transformer theory already built here |
| Hugging Face Agents Course | Agent fundamentals, frameworks, agentic RAG, evaluation (Phases 10, 12) | After structured outputs, tool calling and a minimal agent loop |
| LangChain / LangGraph learn | RAG, agents, LangGraph, memory, context engineering, multi-agent patterns (Phases 09, 10, 12) | After the corresponding from-scratch experiment |
| n8n Academy | n8n fundamentals, API / workflow integration, AI workflows (Phases 07, 12) | N8N101 → N8N102 → N8N103; self-hosted / local only, n8n Cloud is not required |

---

# Phase 01 — Machine Learning Foundations

**Status:** COMPLETE

## Concepts

- features and targets,
- supervised learning,
- decision trees,
- training and inference,
- model capacity,
- overfitting,
- train/test splits,
- generalization,
- evaluation limitations.

## Verified Practical Work

Implemented and reviewed experiments covering:

```text
Decision Tree
↓
learned decision boundaries
↓
predictions
```

and:

```text
model capacity
↓
training performance
↓
test performance
↓
overfitting
```

Experiments demonstrated that a more expressive model can achieve better training performance while generalizing worse.

## Completion Checkpoint

Can explain:

- features vs targets,
- `fit()` vs `predict()`,
- training vs held-out performance,
- model capacity,
- overfitting,
- generalization,
- limitations of small test sets.

---

# Phase 02 — Deep Learning Foundations

**Status:** COMPLETE

## Concepts

- tensors,
- matrix operations,
- neural-network layers,
- weights and biases,
- activations,
- logits,
- sigmoid,
- loss functions,
- gradient descent,
- backpropagation,
- optimizers,
- normalization,
- thresholds,
- evaluation metrics.

## Verified Practical Work

Implemented PyTorch classifiers.

Training pipeline:

```text
input
↓
Linear
↓
ReLU
↓
Linear
↓
logit
↓
loss
↓
backpropagation
↓
optimizer
```

Evaluation included:

- accuracy,
- precision,
- recall,
- F1,
- confusion matrices,
- threshold analysis.

## Completion Checkpoint

Can explain:

- tensors,
- weights and biases,
- logits,
- probabilities,
- activations,
- loss,
- gradients,
- backpropagation,
- optimizer updates,
- threshold trade-offs,
- preprocessing leakage.

---

# Phase 03 — Computer Vision Foundations

**Status:** COMPLETE

## Concepts

- images as tensors,
- channels,
- convolution,
- kernels,
- filters,
- feature maps,
- learned filters,
- ReLU,
- pooling,
- CNNs,
- datasets,
- DataLoaders,
- mini-batches,
- multiclass classification,
- evaluation.

## Verified Practical Work

### Manual Convolution

```text
image
+
kernel
↓
convolution
↓
feature map
```

### Multiple Filters

```text
1 input channel
↓
multiple filters
↓
multiple feature maps
```

### Learned Filters

```text
random convolution weights
↓
forward pass
↓
loss
↓
backpropagation
↓
optimizer
↓
learned filters
```

### Synthetic Shape CNN

Built a CNN classifying:

```text
circle
vs
square
```

### Held-Out Evaluation

Evaluated generalization using separate training and test data.

The limitations of the synthetic generator were documented.

### MNIST Dataset

Verified:

```text
60,000 training images
10,000 test images
```

with image shape:

```text
[1, 28, 28]
```

### DataLoader

Verified:

```text
batch size = 64

training batches = 938
test batches = 157
```

### Multiclass CNN

Architecture:

```text
MNIST image
↓
Conv2d
↓
ReLU
↓
MaxPool
↓
Conv2d
↓
ReLU
↓
MaxPool
↓
Flatten
↓
Linear
↓
10 logits
```

Held-out test performance exceeded:

```text
98%
```

### Error Analysis

Performed:

- confusion matrix analysis,
- per-class accuracy,
- frequent confusion analysis,
- misclassified-image inspection.

Verified test accuracy in the error-analysis run:

```text
98.55%
```

## Completion Checkpoint

Can explain:

- `[batch, channels, height, width]`,
- filter vs feature map,
- convolution,
- pooling,
- `out_channels`,
- learned filters,
- Flatten,
- DataLoader,
- batches,
- epochs,
- multiclass logits,
- `argmax`,
- `CrossEntropyLoss`,
- held-out evaluation.

---

# Phase 04 — Transformer and LLM Fundamentals

**Status:** IN PROGRESS (Experiments 13–29 COMPLETE; Experiment 30 is the current target)

## Goal

Understand how an autoregressive language model works internally before focusing on higher-level LLM applications.

```text
text → tokenizer → token IDs → embeddings → Transformer
     → logits → next-token probabilities → generated text
```

The roadmap holds the ordered route only. Each experiment's theory, hypothesis, implementation, actual run and limitations live in its own README under [topics/04_llm_engineering/](topics/04_llm_engineering/README.md); do not duplicate them here.

## Experiment sequence

"Experiment NN" is the global number across the whole Lab (see [Experiment numbering](docs/learning-method.md#experiment-numbering)). The folder column is the local sequence inside `topics/04_llm_engineering/`.

| Experiment | Title | Folder | Status | New idea |
|---|---|---|---|---|
| 13 | Tokenization | `01_tokenization` | COMPLETE | token ≠ token ID |
| 14 | Token Embeddings | `02_embeddings` | COMPLETE | embedding table lookup, `[8] → [8, 4]` |
| 15 | Positional Embeddings | `03_positional_embeddings` | COMPLETE | token = WHAT, position = WHERE |
| 16 | Self-Attention | `04_self_attention` | COMPLETE | Q, K, V and attention weights |
| 17 | Causal Self-Attention | `05_causal_attention` | COMPLETE | causal mask |
| 18 | Multi-Head Attention | `06_multi_head_attention` | COMPLETE | heads and concatenation |
| 19 | Attention Output Projection and Residual | `07_attention_output_residual` | COMPLETE | output projection, residual path |
| 20 | Layer Normalization | `08_layer_normalization` | COMPLETE | per-token normalization |
| 21 | Feed-Forward Network | `09_feed_forward_network` | COMPLETE | position-wise expansion and projection |
| 22 | FFN Residual and Complete Transformer Block | `10_transformer_block` | COMPLETE | the full block |
| 23 | Stacked Transformer Blocks | `11_stacked_transformer_blocks` | COMPLETE | depth |
| 24 | Language-Model Head and Vocabulary Logits | `12_lm_head_logits` | COMPLETE | hidden states → vocabulary logits |
| 25 | Softmax and Next-Token Probabilities | `13_softmax_probabilities` | COMPLETE | logits → probabilities |
| 26 | Shifted Targets and CrossEntropyLoss | `14_shifted_targets_cross_entropy` | COMPLETE | next-token loss |
| 27 | Backpropagation and Gradients | `15_backpropagation_gradients` | COMPLETE | gradients per parameter |
| 28 | Optimizer Update | `16_optimizer_update` | COMPLETE | `optimizer.step()` changes parameters |
| 29 | Language-Model Training Loop | `17_training_loop` | COMPLETE | repeated training; a tiny trained LM |
| 30 | Autoregressive Generation and Sampling | _(not created yet)_ | **NEXT — current target** | training vs inference |

### Experiment 30 — Autoregressive Generation and Sampling (current target)

Use the trained causal language model to generate one token at a time:

```text
current context → model → final-position logits → token selection
→ append selected token → new context → repeat
```

Greedy decoding and probabilistic sampling are studied together in this one workflow rather than as separate microscopic experiments. It connects causal attention, final-position logits and Softmax probabilities, and makes the difference between training and inference/generation explicit.

## Remaining LLM fundamentals

After Experiment 30, short concept studies (no separate experiments planned unless needed): temperature, top-k, top-p, context window, training vs inference, model parameter count, KV cache, RoPE, multi-query and grouped-query attention, pre-norm vs post-norm.

## Phase 04 synthesis exercise

Connect the studied components in a small controlled GPT-like exercise in PyTorch with a tiny dataset and an explicit question about training versus generation. It is educational lab work, not a plan for an external repository; keep its scope bounded and its limitations visible.

---

# Phase 05 — Local Models and Inference

**Status:** PLANNED

**Track:** A — Core AI Engineering (bridge to the applied track). Topic directory: `topics/05_local_models_inference/`. Absorbs the former Phases 06 (Ollama), 08 (llama.cpp / GGUF), 09 (hardware / quantization) and 10 (benchmarking), grouped as the blocks below.

## Concepts

- pretrained models, model loading, model selection,
- inference, context windows, KV-cache concepts, generation,
- CPU inference, GPU inference, RAM versus VRAM,
- tokens per second, time to first token, latency, throughput, batching concepts,
- OpenAI-compatible local endpoints (the same request shape later reused in Phase 06).

## Practical Work

Run a small compatible language model locally.

Record:

- model, model size, quantization,
- hardware,
- memory usage,
- generation parameters, context length,
- latency, tokens per second.

## Block 5B — Ollama and local APIs

- inference runtime, model management, local model server,
- HTTP, JSON, API requests, streaming, OpenAI-compatible endpoint.

```text
Python client → HTTP → Ollama → runtime → model → generated tokens → response
```

## Block 5C — llama.cpp and GGUF

- native inference, GGUF, model formats, quantization, CPU execution, GPU offload.

Run compatible models through `llama.cpp` and compare Ollama versus llama.cpp.

## Block 5D — Hardware, quantization and benchmarking

- parameter count, FP32, FP16, BF16, INT8, INT4, RAM, VRAM, memory bandwidth, GPU offload,
- context length versus KV-cache memory, batching concepts,
- latency, time to first token, tokens per second, throughput, warm-up, repeatability, quality evaluation.

Compare configurations while controlling model, prompt, hardware and context; measure memory, latency, generation speed and output differences. Isolate a benchmark question with fixed prompts, controlled settings and repeated measurements.

## Block 5E — Serving and gateways (awareness, later)

| Technology | Architectural purpose | Status |
|---|---|---|
| Ollama, llama.cpp | first practical path on the learner's RTX 2060 Max-Q | hands-on |
| **vLLM** | production-oriented model serving with an OpenAI-compatible server | awareness; not required on this hardware |
| **LiteLLM** | model gateway: routing, retries, fallbacks, provider abstraction | awareness; understand the pattern before any use |

Learn why serving and gateways exist (concurrency, batching, provider independence). Neither is a prerequisite for Phase 06.

**Resources:** Hugging Face LLM Course (pretrained models, model usage).

---

# Phase 06 — LLM Application Interfaces

**Status:** PLANNED

**Track:** bridge. Topic directory: `topics/06_llm_application_interfaces/`. Replaces the former Phase 07 (Python LLM Integration) and the request half of the former Phase 14 (Tool Calling).

Purpose: bridge model fundamentals to usable applications, and treat prompts as engineering artifacts.

## Concepts

- Python ↔ model server boundary, HTTP inference, REST concepts,
- OpenAI-compatible APIs, chat / message models (system / developer / user / assistant roles),
- streaming, SSE concepts, async requests, concurrency concepts,
- structured outputs, JSON Schema, Pydantic validation (after the contract is understood),
- function calling and tool calling,
- timeouts, retry / backoff, rate limits,
- context management, token budgeting.

Distinguish generating a tool-call request from validating arguments, checking permission, executing a function and returning its result. A parseable response does not prove a correct answer or authorize an action.

## Prompt engineering is engineering

Prompting is product and software work, not ad-hoc wording experiments.

- prompt contracts: purpose, inputs, outputs, constraints, refusal / abstention behavior,
- system / developer / user instruction hierarchy,
- structured prompts, prompt templates, few-shot examples,
- typed inputs and outputs (JSON Schema, Pydantic),
- model-specific prompt behavior and prompt migration between models,
- prompt injection resistance and context-budget awareness,
- prompt versioning, golden evaluation datasets, regression testing, A/B comparisons, failure-mode analysis.

```text
define expected behavior
↓
write prompt / instructions
↓
build evaluation cases
↓
observe failures
↓
classify failure modes
↓
modify prompt / context / tools
↓
rerun evaluations
↓
version the improvement
```

**DSPy** (declarative LM programs; metric-driven prompt / program optimization) is a *later* technology, studied after manual prompt-engineering fundamentals and an evaluation set exist (see Phase 14 for how it differs from fine-tuning). It is not required before the manual workflow above.

## Enterprise comparison (conceptual)

Compare one request shape across: a local Ollama endpoint, an OpenAI-style API, **Azure OpenAI** and **Microsoft Foundry** model endpoints — authentication, deployments / versions, streaming, structured outputs, tool calling, tokens / context, rate limits and retries. ZERO EXTRA COST: hosted endpoints are studied architecturally from documentation unless the learner explicitly authorizes paid use.

## Practical Work

Small educational experiments (none created yet): local chat client, structured-output extractor with a golden evaluation set, streaming client, first controlled tool call, prompt-version regression run.

```text
model requests action
≠
application automatically authorizes action
```

---

# Phase 07 — AI Automation Foundations

**Status:** PLANNED

**Track:** B — Applied AI Automation. Topic directory: `topics/07_ai_automation_foundations/`. New phase; it begins the explicit applied track. Supersedes the former "Automation" parallel track as a sequential block.

This phase should support real business automation work.

## Concepts

- business-process discovery, workflow mapping,
- deterministic versus probabilistic steps; rules versus AI (and when AI is not appropriate),
- HTTP, REST, JSON, OpenAPI, webhooks,
- authentication: API keys, OAuth2 / OIDC concepts,
- pagination, rate limiting, timeouts, retries, exponential backoff, idempotency,
- input validation, data transformation, error handling,
- human approval and auditability,
- workflow evaluation,
- n8n fundamentals (local / self-hosted).

## Decision hierarchy

```text
plain function
↓
deterministic workflow
↓
LLM call
↓
RAG
↓
agent
↓
multi-agent
```

Move down the list only when the previous level demonstrably cannot solve the problem. Choose the simplest architecture that works.

## API-first versus browser automation

```text
prefer supported APIs
before browser automation
```

Browser automation (**Playwright**, open source) is a useful fallback when no supported API exists. It is brittle (UI changes), harder to secure and harder to audit; reason about that trade-off before using it. Respect terms of service and authorization.

n8n progression: fundamentals → API / workflow integrations → testing and error handling → (Phase 12) AI workflows → tools / agents. n8n is a workflow platform; learning it does not replace the fundamentals above.

## Practical Work

Small future experiments (none created yet): deterministic incident triage, webhook → validation → routing, API → transform → output (with pagination and retry), retry / error-handling exercise, human-approval workflow, a simple local n8n workflow, a small browser-automation versus API comparison.

The existing deterministic-triage exercise is kept outside this repository for now and may eventually become the first experiment here. Its `10/10` original cases and `4/4` tests are a baseline only, not proof of generalization.

**Enterprise mapping:** Microsoft Copilot Studio (low-code agents) is introduced here conceptually and compared in Phase 12. No paid features are activated.

**Resources:** n8n Academy (self-hosted / local; no paid tier required).

---

# Phase 08 — Embeddings and Semantic Retrieval

**Status:** PLANNED

**Track:** A — Core AI Engineering. Topic directory: `topics/08_embeddings_semantic_retrieval/`. Replaces the former Phases 11 (Embedding Models) and 12 (Semantic Search).

This phase concerns **external embedding models used for retrieval**, not the internal Transformer token embeddings already studied in Experiment 14.

## Concepts

- embedding models, dense vectors, sentence / document embeddings,
- cosine similarity, normalization,
- BM25 and sparse (lexical) retrieval concepts,
- nearest-neighbor search, approximate nearest neighbors (ANN), HNSW,
- metadata filtering, chunking and metadata,
- hybrid retrieval (lexical + vector), reranking,
- retrieval evaluation: recall, precision, ranking quality.

## Practical Work

Small future experiments: sentence similarity, semantic search, BM25 versus dense comparison, local vector index, retrieval evaluation. Start with exact in-memory similarity so ranking is visible.

Local technologies to compare (use one or two; mastering all three is not required): **FAISS**, **PostgreSQL + pgvector**, **Qdrant**. No paid vector service.

## Enterprise mapping — Azure AI Search

Understand how a managed enterprise service maps onto the same concepts: lexical search, vector search, hybrid search, semantic ranking, metadata filtering and enterprise access patterns. Studied from documentation; no Azure deployment is required.

---

# Phase 09 — RAG and Knowledge Systems

**Status:** PLANNED

**Track:** bridge (Core and Applied). Topic directory: `topics/09_rag_knowledge_systems/`. Replaces the former Phase 13 (RAG).

## Concepts

- document ingestion, parsing, OCR concepts, chunking, metadata,
- embedding, indexing, retrieval, reranking,
- context construction, grounded generation, citations, abstention,
- query rewriting, multi-query retrieval, hybrid RAG,
- RAG evaluation and failure modes (missing evidence, poor chunks, irrelevant retrieval, stale documents, unsupported claims, misleading citations),
- document-level security and permission-aware retrieval,
- RAG poisoning and data provenance.

## Practical Work

```text
documents → chunks → embeddings → retrieval → context → LLM → answer
```

Evaluate retrieval and generation separately. Small future experiments: minimal local RAG with citations, retrieval failure analysis, a permission-aware retrieval toy. Hybrid retrieval, query rewriting and reranking are compared after a baseline exposes a concrete failure. A small end-to-end RAG experiment belongs in the lab to understand ingestion, retrieval and grounding with controlled data.

Enterprise scenarios used as problem framings: internal knowledge base, technical documentation, policy assistant, support knowledge assistant, document intelligence.

**LlamaIndex** is a useful framework to *compare* for retrieval, RAG and workflows — after the from-scratch / local RAG experiment, never before it.

**Resources:** LangChain / LangGraph learn (RAG), after the from-scratch version.

---

# Phase 10 — Agentic Systems Fundamentals

**Status:** PLANNED

**Track:** B — Applied AI Automation & Agentic Systems. Topic directory: `topics/10_agentic_systems/`. Replaces the former Phase 14 (execution half) and Phase 15 (Agents).

## Concepts

- validated tool schemas and execution boundaries; the observation / result loop,
- agent loop from scratch: state, actions, observations, termination,
- short-term memory, long-term memory concepts,
- planning, task decomposition, ReAct, plan-and-execute, routing, reflection / retry, error recovery,
- context engineering and context compaction,
- permissions, sandboxing, human-in-the-loop approvals,
- background / long-running agents, checkpoints, resume / recovery,
- budgets and tracing,
- agent evaluation.

## Patterns

single agent + tools · router · supervisor · handoff · planner / executor · parallel fan-out / fan-in · subagents · specialized agents. Each pattern is compared with a single-agent baseline; multi-agent is justified only by separable roles.

## Tool and data integrations

files · REST APIs · SQL / database · search / retrieval · business systems. Early experiments never receive unrestricted shell or system access; tools are small, typed, allowlisted and sandboxed.

## Agent skills and reusable capabilities (later concept)

Reusable instructions, tool bundles, domain capabilities and progressive context loading (load detail only when needed). A concept inside this phase and Phase 12, not a separate phase.

## Practical Work

Small future experiments: agent loop from scratch, agent with two or three controlled tools, memory / state experiment, checkpoint / resume experiment, Minimal Coding-Agent Experiment, agent evaluation. These are grouped learning questions, not pre-created directories.

| Block | Concepts and small lab work | Evidence before extending |
|---|---|---|
| Minimal loop and tool execution | Local model, controlled tool set, actions, observations, state, budgets, stopping conditions | Trace a complete task, a tool failure and budget termination |
| State, memory and context | Current state, short-term context, persisted memory; context construction, compaction and recovery | Explain what survives between steps / runs; stale state must not become authority |
| Permissions and human approval | Argument validation, allowlists, sandbox boundaries, approvals, denied actions | Exercise permission denial, untrusted input and recovery; authorization stays in application code |
| Planning, retries and evaluation | Compare a fixed workflow with planning, reflection and retries on a small task set | Success, errors, time and tool usage; retries must show benefit, not merely extra steps |
| Patterns and long-running work | Router / supervisor / handoff versus a single agent; checkpoints and resume | Single-agent baseline first; resume must not repeat side effects |

### Minimal Coding-Agent Experiment

**Planned small educational experiment inside the lab.** A local model receives a failing test in a tiny deliberately broken toy workspace and a controlled tool set: `read_file(path)`, `write_file(path, content)` and `run_tests()`.

The Python host represents and validates each tool request, enforces permissions (including path restrictions), executes the action and returns its result to the model. The loop maintains state, allows bounded retries and stops on verified completion, budget exhaustion or an unrecoverable error.

The learning question is how tool calling becomes iterative tool use: request → host execution → result → next action. Record a successful toy task, a denied action and a failed / retried action, including termination behavior. A larger coding-agent product is not a lab experiment. No source code, toy workspace or directory is created by this documentation.

**Resources:** Hugging Face Agents Course — consume after structured outputs, tool calling and the minimal agent loop. See the [Agentic AI field map](docs/ai-engineering-map.md#agentic-ai).

---

# Phase 11 — MCP and Agent Interoperability

**Status:** PLANNED

**Track:** B. Topic directory: `topics/11_mcp_integration/`. Split out of the former Phase 15 "Protocols and frameworks" block. The directory name is unchanged; the scope now covers agent interoperability beyond MCP alone.

## MCP

Client / server architecture, tools, resources, prompts, discovery, transports (stdio, Streamable HTTP), authorization, permissions, local versus remote servers, tool schemas, security boundaries, least privilege and approval for sensitive actions. MCP is a protocol for connecting tools and context; it is not an agent loop or a permission policy.

## A2A — Agent2Agent

A distinct concept from MCP:

```text
MCP → agent / application ↔ tools, context, resources
A2A → independent agent   ↔ independent agent
```

Conceptually: agent discovery, capabilities, tasks, interoperability across frameworks, security boundaries. A2A is **PLANNED as awareness-to-practice**, not an immediate hands-on dependency.

## Standards that make tools interoperable

OpenAPI (describing HTTP services), JSON Schema (typed tool inputs / outputs), OAuth / OIDC (delegated authorization and identity). Emerging agent-to-UI protocols (for example AG-UI) are recorded as **awareness only** and promoted only if later market evidence justifies it.

## Practical Work

Small future experiments: minimal local MCP server exposing one or two safe tools, MCP client interaction, a least-privilege / approval exercise, an A2A concept walkthrough (reading and diagramming, not a dependency).

---

# Phase 12 — Agent Frameworks and Orchestration

**Status:** PLANNED

**Track:** B. Topic directory: `topics/12_agent_frameworks_orchestration/`. Split out of the former Phase 15 "Protocols and frameworks" and "Advanced orchestration" blocks.

Fundamentals come first; frameworks are implementations of concepts already understood.

```text
primitive first → minimal implementation second → framework third
agent loop from scratch → LangChain / LangGraph
workflow fundamentals   → n8n
```

## Hands-on priority

| Technology | What to learn |
|---|---|
| **LangChain** | model / tool / retriever abstractions, structured output |
| **LangGraph** | explicit state, nodes, edges, routing, durable execution, checkpoints, human-in-the-loop, retries, subgraphs, multi-agent orchestration |
| **n8n AI workflows** | AI nodes inside deterministic workflows |
| **Microsoft Agent Framework** | agents, tools, sessions / state, memory, middleware, workflows, MCP, human-in-the-loop, telemetry, hosting concepts |

Microsoft Agent Framework is included because of the learner's Enterprise / Azure direction. It is the modern Microsoft successor to ideas from **AutoGen** and **Semantic Kernel**; those legacy frameworks are *historical / ecosystem awareness* only unless a job or project needs them.

## Comparison and awareness

PydanticAI · LlamaIndex agents / workflows · OpenAI Agents SDK architecture · CrewAI. Do not try to master every framework. For each, answer:

```text
What abstraction does this framework provide?
What does it manage for me?
What control do I lose?
How does it handle state?
How does it execute tools?
How does it recover?
How does it support evaluation / observability?
```

## Enterprise mapping

- **Microsoft Foundry:** model catalog, endpoints / deployments, agents / tools, evaluation, tracing, monitoring, governance.
- **Microsoft Copilot Studio** (also Phase 07): low-code agents, knowledge, tools / actions / connectors, workflow integration, state / conversations, authentication / governance. Learn *when to use Copilot Studio versus when to build custom Python agents*. No paid features are activated.

## Practical Work

Small future experiments: the same workflow implemented manually versus with LangChain / LangGraph, a small LangGraph workflow with checkpoints and a human approval, an n8n AI workflow, a subagent experiment, an agentic-RAG comparison, a framework-comparison write-up using the questions above. Each is compared against a single-agent or deterministic baseline, tracking state, permissions, termination and evaluation. Choose free local execution options; if a tutorial assumes a paid provider, document a local adaptation instead.

**Resources:** LangChain / LangGraph learn, Hugging Face Agents Course, n8n Academy.

---

# Phase 13 — Multimodal AI and Voice

**Status:** PLANNED

**Track:** A — Core AI Engineering. Former Phase 16; no topic directory yet.

## Concepts

- image input, text input, multimodal context, vision-language models, image understanding, multimodal embeddings,
- document AI and OCR,
- speech-to-text, text-to-speech, audio pipelines, streaming voice, turn detection, latency,
- voice agents, multimodal tools,
- later: image generation, video concepts.

Voice overlaps multimodal and agentic AI but does not inherently require an agent loop.

## Practical Work

Evaluate a compatible multimodal model on a bounded task and evaluation set. A small voice exercise may connect recognition → LLM response generation → speech synthesis, measuring streaming latency and turn detection before tool actions. Voice agents come only after the agent fundamentals (Phase 10).

Microsoft speech / vision / document services may be compared conceptually. ZERO EXTRA COST: exercises use local or free open-source models.

---

# Phase 14 — Model Adaptation: Fine-Tuning, LoRA and QLoRA

**Status:** PLANNED

**Track:** A — Core AI Engineering. Former Phase 17; no topic directory yet.

## Concepts

- pretrained models, adaptation, supervised fine-tuning, instruction tuning,
- LoRA, QLoRA, PEFT,
- dataset quality, train / eval splits, synthetic-data concepts,
- model distillation,
- **when NOT to fine-tune:** RAG versus fine-tuning, prompt optimization versus fine-tuning.

Keep three levers distinguishable:

```text
change the context   → RAG
change the prompt / program (DSPy-style optimization) → no model weights change
change the weights   → fine-tuning / LoRA / QLoRA
```

## Practical Work

Run a small controlled adaptation and compare it against a baseline, including a prompt-only and a retrieval baseline. Include model-merging concepts as a later topic. Scope any local training to available memory; no paid compute is required.

**Resources:** Hugging Face LLM Course (fine-tuning chapters).

---

# Phase 15 — AI Backend Engineering and Client Integration

**Status:** PLANNED

**Track:** bridge. Former Phases 18 and 19; no topic directory yet.

Strong enough for real AI-engineering jobs: agent systems combine API requests, background work, events, tools, human approvals and long-running tasks.

## Concepts

- **FastAPI, Pydantic, async Python, REST APIs, OpenAPI,**
- streaming: SSE, WebSockets concepts; cancellation, concurrency, resource management,
- background jobs, queues, workers,
- **PostgreSQL:** transactions, connection pooling; **Redis** concepts and caching,
- architecture: microservices versus modular monolith, event-driven architecture, pub/sub, message brokers,
- reliability patterns: idempotency, circuit breakers, sagas / compensation concepts,
- logging, metrics, structured errors, failure handling,
- client side: HTTP clients, asynchronous requests, streaming UI, application state, network failures.

Understand or compare **Redis**, **RabbitMQ** and **Kafka** (concepts); mastering every broker is not required.

## Practical Work

Build a small inference service with streaming, cancellation, bounded concurrency, a background-job queue, structured errors, logs and metrics, and a client for it. Add one event-driven interaction (for example a long-running task with a human approval).

---

# Phase 16 — Packaging and Offline Distribution

**Status:** PLANNED

**Track:** A / bridge. Former Phase 20; no topic directory yet.

## Concepts

- Docker: Dockerfiles, images, containers, volumes, networks, Docker Compose,
- environment variables, secrets, health checks,
- dependency locking, reproducible environments,
- local model packaging, compatibility, installation, updates, offline deployment,
- sandboxing and isolation for coding / tool agents.

Then Kubernetes fundamentals: pods, deployments, services, config / secrets, scaling, health probes; Helm as awareness.

## Practical Work

Install and run a prototype on another machine without requiring network access. Kubernetes is local / conceptual with small exercises only; no paid cluster is required.

---

# Phase 17 — Production AI Engineering

**Status:** PLANNED

**Track:** bridge. Former Phase 21; no topic directory yet. Where Core, Applied, Software Engineering, LLMOps / MLOps and Enterprise AI converge.

## Concepts

- **Software delivery:** Git, branching, pull-request discipline, CI / CD, GitHub Actions concepts, automated testing,
- **Versioning and release:** model, prompt and dataset versioning; configuration management; rollback; canary and feature-flag concepts,
- **Evaluation pipelines:** golden datasets, regression suites, LLM-as-judge limits, human review, agent evaluation,
- **Observability:** logging, tracing of LLM / tool / agent steps, metrics, latency, token and cost tracking, error budgets, drift and feedback loops, OpenTelemetry concepts,
- **Safety and governance:** security, privacy, prompt-injection defense, permissions, audit trails, compliance awareness,
- product requirements, acceptance criteria, reliability, maintenance, recovery, local / offline deployment, performance, cost awareness,
- technical communication: decision records, runbooks, README evidence, explaining trade-offs to non-engineers.

## Azure / Microsoft architecture mapping (conceptual)

Azure Functions · App Service · Container Apps · AKS / Kubernetes concepts · Storage · PostgreSQL / Cosmos DB concepts · Service Bus · Event Grid · Entra ID · Key Vault · Azure Monitor · Application Insights · private networking concepts. Map each to the generic concept already learned (queues, containers, secrets, identity, telemetry). **Microsoft Foundry** maps to model catalog, deployments, agents, evaluation, tracing, monitoring and governance. No paid Azure resources are required.

## Practical Work

Use small controlled exercises to study production concerns such as evaluation pipelines, logging and tracing, caching, async execution, queues, packaging, CI and regression tests. Each exercise answers a clear engineering question and documents its limits; this phase does not plan an external integrated system.

Be able to justify:

```text
requirement → data → model → runtime → backend → client → evaluation → deployment → monitoring
```

---

# Parallel Professional Tracks

Not every important skill should become a sequential roadmap phase.

Some areas should develop alongside the main path.

---

## Data Engineering

**Priority:** A / B

Learn progressively:

- SQL,
- PostgreSQL,
- data modelling,
- ETL / ELT,
- data validation,
- pipelines,
- Redis,
- queues.

Later if required:

- Kafka,
- Spark,
- data lakes,
- warehouses,
- lakehouses.

---

## Software Engineering for AI

**Priority:** A

Continuously practice:

- clean architecture,
- typing,
- testing,
- packaging,
- configuration,
- logging,
- error handling,
- profiling,
- async programming,
- concurrency,
- caching,
- CI/CD,
- documentation.

AI systems are software systems.

---

## AI Evaluation

**Priority:** A

Learn throughout the roadmap:

```text
classification metrics
↓
model evaluation
↓
retrieval evaluation
↓
RAG evaluation
↓
LLM evaluation
↓
agent evaluation
```

Evaluation is not a final optional step. Every applied automation or agent experiment states its baseline, success criteria, failure modes, generalization test, comparison with deterministic logic, model-failure behavior and the point where a human intervenes. A passing score on the original cases is a baseline, not proof of generalization.

---

## AI Security

**Priority:** B

Learn progressively:

- prompt injection,
- tool permissions,
- data leakage,
- secrets,
- sandboxing,
- model supply-chain risk,
- adversarial inputs,
- input validation and untrusted data,
- path restrictions,
- privacy,
- agent security.

---

## Automation

**Priority:** B

Now a sequential block: [Phase 07 — AI Automation Foundations](#phase-07--ai-automation-foundations). Deeper topics continue in parallel:

- OAuth,
- schedulers,
- queues,
- event-driven systems.

Automation frameworks (n8n) are learned after the underlying concepts.

---

## MLOps / LLMOps

**Priority:** B

Learn when systems become large enough to justify it:

- experiment tracking,
- model versioning,
- prompt versioning,
- evaluation pipelines,
- tracing,
- observability,
- deployment,
- monitoring,
- drift,
- model routing.

---

# Specialization Tracks

These are valuable but are not currently part of the core sequential path.

They should be studied when required by a project or professional direction.

---

## Time Series

**Priority:** B

Relevant areas:

- forecasting,
- anomaly detection,
- telemetry,
- sensor data,
- predictive maintenance,
- signal processing.

---

## Edge AI

**Priority:** B

Relevant areas:

- embedded inference,
- ONNX,
- TensorRT,
- TensorFlow Lite,
- NPUs,
- quantization,
- latency,
- memory constraints.

---

## Speech AI

**Priority:** C / B when required

- speech-to-text,
- text-to-speech,
- audio embeddings,
- voice models,
- audio classification.

---

## Reinforcement Learning

**Priority:** C

Understand conceptually:

- environment,
- state,
- action,
- reward,
- policy,
- Q-learning,
- policy gradients,
- PPO.

Deep specialization can come later.

---

## Robotics

**Priority:** C

Potential areas:

- perception,
- localization,
- SLAM,
- planning,
- control,
- robot learning.

---

## Graph AI

**Priority:** C

Potential areas:

- graphs,
- graph databases,
- knowledge graphs,
- graph embeddings,
- GNNs.

---

## Digital Twins and Scientific ML

**Priority:** C

Potential areas:

- simulation,
- surrogate models,
- physics-informed ML,
- neural operators,
- engineering AI.

---

## Generative Media

**Priority:** C

Potential areas:

- image generation,
- diffusion,
- audio generation,
- video generation,
- multimodal generation.

---

# 80/20 Professional Path

If only a subset of this roadmap could be learned, prioritize:

```text
1. Python + software engineering
2. Machine Learning fundamentals
3. PyTorch + Deep Learning
4. Transformers and LLM internals
5. Local and API-based LLM inference
6. Structured outputs, tool calling and a bounded agent loop
7. Automation fundamentals: process analysis, APIs, webhooks, workflows, human approval
8. Embeddings and semantic search
9. RAG, then advanced agents, MCP and frameworks when justified
10. AI backend engineering
11. Evaluation
12. Deployment and observability
13. Further agentic / multimodal specialization as needed
```

This is a prioritization guide, not permission to defer evaluation or safety until the end. Apply both throughout, and use the [selected route](#route-after-phase-04) to distinguish basic agent primitives from later orchestration.

This path provides the strongest combination of:

- fundamentals,
- employability,
- engineering capability,
- AI product development,
- transferable knowledge.

---

# Final Goal

The target capability is not:

```text
"I know many AI libraries."
```

The target capability is:

```text
"I can understand a problem,
identify which AI components are useful,
reject unnecessary complexity,
build the system,
evaluate it,
deploy it,
and explain the engineering trade-offs."
```

The final mental model should allow reasoning across:

```text
DATA
↓
ML / DL
↓
LLM
↓
EMBEDDINGS
↓
RETRIEVAL
↓
RAG
↓
TOOLS
↓
AGENTS
↓
BACKEND
↓
APPLICATION
↓
DEPLOYMENT
↓
EVALUATION
↓
PRODUCTION
```
