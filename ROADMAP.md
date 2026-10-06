# AI Engineering Roadmap

This roadmap defines the main learning progression of the repository.

It is not the repository directory hierarchy.

Topics are grouped by technical domain, while this document describes learning order.

Future work remains documented here until implementation begins.

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

```text
Machine Learning
↓
Deep Learning
↓
Computer Vision Foundations
↓
Transformer / LLM Internals
↓
Local Inference
↓
LLM APIs
↓
Hardware and Quantization
↓
Embeddings
↓
Semantic Search
↓
RAG
↓
Tool Calling
↓
Agents
↓
Multimodal AI
↓
Fine-Tuning
↓
AI Backend Engineering
↓
Application Integration
↓
Production AI Engineering
```

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

**Status:** IN PROGRESS

## Goal

Understand how an autoregressive language model works internally before focusing on higher-level LLM applications.

The objective is not merely to call an API.

The objective is to understand:

```text
text
↓
tokenizer
↓
token IDs
↓
embeddings
↓
Transformer
↓
logits
↓
next-token probabilities
↓
generated text
```

---

## Experiment 13 — Tokenization

**Status:** COMPLETE

Studied:

```text
text
↓
character tokens
↓
token IDs
```

Verified:

- vocabulary construction,
- token-to-ID mapping,
- ID-to-token mapping,
- encoding,
- decoding.

Key distinction:

```text
token
≠
token ID
```

---

## Experiment 14 — Token Embeddings

**Status:** COMPLETE

Studied:

```text
token ID
↓
embedding-table lookup
↓
trainable vector
```

Verified:

```text
vocabulary size = 10
embedding dimension = 4

embedding table:
[10, 4]
```

and:

```text
8 token IDs
↓
8 embeddings

[8]
→
[8, 4]
```

Key distinction:

```text
token ID
=
index

embedding
=
trainable representation
```

---

## Experiment 15 — Positional Embeddings

**Status:** COMPLETE

Studied:

```text
token embedding
+
position embedding
=
position-aware representation
```

Verified:

```text
same token
+
different position
=
different combined representation
```

Key mental model:

```text
token embedding
→ WHAT

position embedding
→ WHERE
```

---

## Experiment 16 — Self-Attention

**Status:** COMPLETE

Implemented one attention head manually.

Studied:

```text
X
↓
Q, K, V
```

then:

```text
Q @ Kᵀ
↓
attention scores
↓
softmax
↓
attention weights
```

and:

```text
attention weights
@
Values
↓
contextual representations
```

Key interpretation:

```text
Q + K
→ determine where information should come from

V
→ contains the information being mixed
```

---

## Experiment 17 — Causal Self-Attention

**Status:** COMPLETE

Introduced autoregressive masking.

Without causal masking:

```text
h → h,e,l
e → h,e,l
l → h,e,l
```

With causal masking:

```text
h → h
e → h,e
l → h,e,l
```

Verified:

```text
future score
↓
-inf
↓
softmax
↓
attention weight = 0
```

Important distinction:

```text
ATTENTION
→ determines what contextual information is used
```

while:

```text
LANGUAGE-MODEL HEAD
→ produces scores over the complete vocabulary
```

---

## Experiment 18 — Multi-Head Attention

**Status:** COMPLETE

Implemented two-head causal self-attention.

Verified configuration:

```text
d_model = 8
num_heads = 2
head_dimension = 4
```

The model dimension was divided across the attention heads:

```text
8 model dimensions
↓
2 heads
↓
4 dimensions per head
```

Verified tensor progression:

```text
input
[3, 8]

↓ Q / K / V

[3, 8]

↓ split heads

[2, 3, 4]

↓ causal attention

attention weights
[2, 3, 3]

↓ head outputs

[2, 3, 4]

↓ concatenate

[3, 8]
```

The two heads produced different causal attention distributions over the same sequence.

Key conclusion:

```text
one sequence
↓
multiple attention heads
↓
different contextual views
↓
concatenated representation
```

The current attention patterns are not linguistically meaningful because the model has not yet been trained.

---

## Experiment 19 — Attention Output Projection and Residual Connection

**Status:** COMPLETE

Extended causal multi-head attention with the final attention output projection:

```text
concatenated heads
[3, 8]

↓ W_O

projected attention
[3, 8]
```

The projection allows information from the different heads to be mixed while preserving `d_model`.

A residual connection was then introduced:

```text
original X
+
projected attention
=
residual output
```

Verified shape progression:

```text
original X
[3, 8]

↓ multi-head attention

head outputs
[2, 3, 4]

↓ concatenate

[3, 8]

↓ output projection

[3, 8]

↓ residual addition

[3, 8]
```

Manual inspection of token `"e"` verified that:

```text
original representation
+
attention update
=
residual representation
```

using element-wise addition.

Key conclusion:

```text
new representation
=
previous representation
+
learned transformation
```

Residual connections preserve a direct information path through deep Transformer architectures.

---

## Experiment 20 — Layer Normalization

**Status:** NEXT

Goal:

Understand why Transformer representations are normalized and how LayerNorm operates across the feature dimensions of each token.

Planned progression:

```text
residual representation
↓
LayerNorm
↓
normalized representation
```

The experiment will inspect one token manually and verify how its mean and variance change under normalization.

---

## Remaining LLM Fundamentals

After the attention residual connection:

```text
Layer Normalization
↓
Feed-Forward Network
↓
Transformer Block
↓
Stacked Transformer Blocks
↓
Language-Model Head
↓
Vocabulary Logits
↓
CrossEntropyLoss
↓
Next-Token Training
↓
Sampling
↓
Generated Text
```

Additional concepts:

- context window,
- temperature,
- top-k,
- top-p,
- greedy decoding,
- model parameters,
- training vs inference,
- KV cache,
- modern positional methods such as RoPE,
- grouped and multi-query attention conceptually.

---

## Phase 04 Final Project

Build a small educational GPT-like model from scratch using PyTorch.

The project should include:

```text
tokenization
↓
embeddings
↓
causal Transformer
↓
LM head
↓
next-token loss
↓
training
↓
generation
```

The final implementation should make the connection between all previous experiments explicit.

---

# Phase 05 — Local Models and Inference

**Status:** PLANNED

## Concepts

- pretrained models,
- model loading,
- inference,
- context,
- generation,
- CPU inference,
- GPU inference,
- RAM,
- VRAM.

## Practical Work

Run a small compatible language model locally.

Record:

- model,
- model size,
- hardware,
- memory usage,
- generation parameters,
- latency,
- tokens per second.

---

# Phase 06 — Ollama and Local APIs

**Status:** PLANNED

## Concepts

- inference runtime,
- model management,
- local model server,
- HTTP,
- JSON,
- API requests,
- streaming.

## Practical Work

Run a model through Ollama and inspect:

```text
Python client
↓
HTTP
↓
Ollama
↓
runtime
↓
model
↓
generated tokens
↓
response
```

---

# Phase 07 — Python LLM Integration

**Status:** PLANNED

## Concepts

- HTTP clients,
- JSON,
- streaming,
- exceptions,
- timeouts,
- retries,
- configuration.

## Practical Work

Build a Python CLI that communicates with a local language model.

---

# Phase 08 — llama.cpp and GGUF

**Status:** PLANNED

## Concepts

- native inference,
- GGUF,
- model formats,
- quantization,
- CPU execution,
- GPU offload.

## Practical Work

Run compatible models through `llama.cpp`.

Compare:

```text
Ollama
vs
llama.cpp
```

---

# Phase 09 — Hardware and Quantization

**Status:** PLANNED

## Concepts

- parameter count,
- FP32,
- FP16,
- BF16,
- INT8,
- INT4,
- quantization,
- RAM,
- VRAM,
- memory bandwidth,
- GPU offload.

## Practical Work

Compare model configurations while controlling:

- model,
- prompt,
- hardware,
- context.

Measure:

- memory,
- latency,
- generation speed,
- output differences.

---

# Phase 10 — Inference Benchmarking

**Status:** PLANNED

## Concepts

- latency,
- time to first token,
- tokens per second,
- throughput,
- warm-up,
- repeatability,
- quality evaluation.

## Practical Work

Build a reproducible local inference benchmark.

---

# Phase 11 — Embedding Models

**Status:** PLANNED

This phase concerns semantic embedding models used for retrieval rather than internal Transformer token embeddings.

## Concepts

- vector representations,
- embedding models,
- cosine similarity,
- normalization,
- semantic similarity.

## Practical Work

Encode a text collection and compare semantic similarity.

---

# Phase 12 — Semantic Search

**Status:** PLANNED

## Concepts

- query embedding,
- document embedding,
- similarity search,
- top-k,
- retrieval evaluation.

## Practical Work

Build semantic search over a small document collection.

---

# Phase 13 — RAG

**Status:** PLANNED

## Concepts

- ingestion,
- chunking,
- embeddings,
- indexing,
- retrieval,
- reranking,
- context construction,
- grounded generation,
- citations,
- RAG evaluation.

## Practical Work

Build:

```text
documents
↓
chunks
↓
embeddings
↓
retrieval
↓
context
↓
LLM
↓
answer
```

Evaluate retrieval and generation separately.

---

# Phase 14 — Tool Calling

**Status:** PLANNED

## Concepts

- tool schemas,
- structured arguments,
- validation,
- execution boundaries,
- permissions,
- authorization.

## Practical Work

Expose controlled application functions to a model.

Important principle:

```text
model requests action
≠
application automatically authorizes action
```

---

# Phase 15 — Agents

**Status:** PLANNED

## Concepts

- state,
- actions,
- observations,
- tool loops,
- planning,
- retries,
- budgets,
- termination,
- tracing.

## Practical Work

Implement a bounded agent loop.

---

# Phase 16 — Multimodal AI

**Status:** PLANNED

## Concepts

- image input,
- text input,
- multimodal context,
- vision-language models,
- multimodal embeddings.

## Practical Work

Evaluate a compatible multimodal model.

---

# Phase 17 — Fine-Tuning, LoRA and QLoRA

**Status:** PLANNED

## Concepts

- pretrained models,
- adaptation,
- supervised fine-tuning,
- LoRA,
- QLoRA,
- PEFT,
- datasets,
- evaluation.

## Practical Work

Run a small controlled adaptation and compare it against a baseline.

---

# Phase 18 — AI Backend Engineering

**Status:** PLANNED

## Concepts

- FastAPI,
- service APIs,
- streaming,
- concurrency,
- cancellation,
- queues,
- resource management,
- logging,
- metrics,
- observability,
- failure handling.

## Practical Work

Build an inference service with:

- streaming,
- cancellation,
- bounded concurrency,
- structured errors,
- logs,
- metrics.

---

# Phase 19 — Client Integration

**Status:** PLANNED

## Concepts

- HTTP clients,
- asynchronous requests,
- streaming UI,
- application state,
- network failures.

## Practical Work

Build a client for an evaluated AI backend.

---

# Phase 20 — Packaging and Offline Distribution

**Status:** PLANNED

## Concepts

- packaging,
- dependencies,
- model artifacts,
- compatibility,
- installation,
- updates,
- offline operation.

## Practical Work

Install and run a prototype on another machine without requiring network access.

---

# Phase 21 — Production AI Engineering

**Status:** PLANNED

## Concepts

- product requirements,
- acceptance criteria,
- reliability,
- privacy,
- security,
- observability,
- evaluation,
- monitoring,
- regression testing,
- maintenance,
- recovery.

## Practical Work

Turn one previous prototype into a production-oriented system.

Be able to justify:

```text
requirement
↓
data
↓
model
↓
runtime
↓
backend
↓
client
↓
evaluation
↓
deployment
↓
monitoring
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

Evaluation is not a final optional step.

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
- agent security.

---

## Automation

**Priority:** B

Learn:

- REST APIs,
- JSON,
- webhooks,
- authentication,
- OAuth,
- schedulers,
- queues,
- event-driven systems,
- human-in-the-loop workflows.

Automation frameworks can be learned after the underlying concepts.

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
6. Embeddings and semantic search
7. RAG
8. Tool calling
9. AI backend engineering
10. Evaluation
11. Deployment and observability
12. Agents
```

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