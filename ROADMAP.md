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
Python ↔ Local LLM
↓
Structured Outputs
↓
Function / Tool Calling
↓
Agentic AI Fundamentals
↓
Embeddings and Semantic Retrieval
↓
RAG
↓
Advanced Agentic Systems / Agentic RAG
↓
Multimodal / Voice
↓
Fine-Tuning / LoRA / QLoRA
↓
AI Backend Engineering
↓
Application Integration
↓
Production AI Engineering
```

## Route After Phase 04

**Current:** Phase 04 is `IN PROGRESS`; Experiments 13–29 are recorded as complete. **Experiment 30 — Autoregressive Generation and Sampling remains `NEXT`.** Its practical generation workflow has not been completed.

Existing phase numbers and completed experiment history are retained. The numbers identify study blocks; the planned visiting order below brings tool and agent primitives forward. It does not require finishing every topic in one block before beginning another.

| Route block | Existing phases / sections | Focus and readiness to continue |
|---|---|---|
| 1. Finish the current LLM workflow | Phase 04, Experiment 30 | Connect final-position logits, token selection and repeated generation; distinguish training from inference |
| 2. Run and call a local model | Phases 05–07 | Loading, local APIs, Python integration, chat messages and structured outputs; handle malformed responses and failures |
| 3. Learn bounded action loops | Phase 14, then Phase 15 foundations | Function/tool calling, validated execution, state and termination; test denied actions and recovery |
| 4. Retrieve evidence | Phases 11–12, then Phase 13 | Retrieval embeddings, semantic search and RAG; evaluate retrieval and generation separately |
| 5. Extend agentic systems | Phase 15 advanced blocks, after retrieval/RAG | Context engineering, MCP, framework comparisons, subagents and agentic RAG; measure added complexity against a simpler baseline |
| 6. Add modalities | Phase 16 and the Speech / Voice track | Multimodal inputs, speech recognition, response generation and speech synthesis; evaluate latency and turn handling |
| 7. Adapt models when justified | Phase 17 | Fine-tuning / LoRA / QLoRA, data quality and independent evaluation; compare with the unchanged model |
| 8. Study system engineering | Phases 18–21 | Services, clients, offline packaging and production concerns through small controlled exercises |

**Parallel tracks:** Phases 08–10 deepen runtime, hardware, quantization and benchmarking after an initial local run. Revisit them when compatibility or memory limits require it. Evaluation, safety, data engineering, testing and software engineering accompany every block. Reinforcement learning and advanced GPU/distributed topics remain later specializations, not immediate prerequisites.

Use sensible learning blocks rather than creating one experiment per API call or line of code. Future names in this document do not create experiment folders or imply completed work.

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

**Status:** COMPLETE

Introduced `nn.LayerNorm(d_model)` after the attention residual representation.

LayerNorm was applied independently to the feature dimensions of each token:

```text
h → normalize 8 features
e → normalize 8 features
l → normalize 8 features
```

The tensor shape remained:

```text
[3, 8]
```

For token `"e"`, the verified statistics before normalization were:

```text
mean     = -0.315053
variance =  1.859519
```

After LayerNorm:

```text
mean     ≈ 0
variance ≈ 1
```

Verified initialization:

```text
gamma = ones
beta  = zeros
```

A manual implementation of:

```text
(x - mean)
-----------------------
sqrt(variance + epsilon)
```

matched PyTorch exactly within floating-point tolerance:

```text
MANUAL NORMALIZATION MATCH:
True
```

Key conclusion:

```text
LayerNorm
→ normalizes each token across its feature dimensions
→ preserves sequence length and d_model
```

---

## Experiment 21 — Feed-Forward Network

**Status:** COMPLETE

Implemented the position-wise feed-forward network used inside a Transformer.

Architecture:

```text
d_model = 8
↓
Linear(8, 32)
↓
GELU
↓
Linear(32, 8)
↓
d_model = 8
```

Verified shape progression:

```text
[3, 8]
↓
[3, 32]
↓
[3, 32]
↓
[3, 8]
```

The experiment verified that the same FFN parameters are reused for every token position.

Processing token `"e"` independently produced the same result as processing it as part of the complete sequence:

```text
PROCESSING TOKEN ALONE MATCHES BATCHED RESULT:
True
```

Changing only token `"h"` produced:

```text
h output unchanged: False
e output unchanged: True
l output unchanged: True
```

This demonstrates that the FFN transforms token positions independently during the forward pass.

However, the parameters are shared.

During training:

```text
loss from multiple positions
↓
gradients
↓
shared FFN parameters
↓
optimizer update
```

Therefore different token positions can indirectly influence future FFN outputs by contributing to updates of the shared parameters.

Key distinction:

```text
ATTENTION
→ communication between token positions
```

```text
FFN
→ nonlinear computation within each token position
```

---

## Experiment 22 — FFN Residual and Complete Transformer Block

**Status:** COMPLETE

Combined the Transformer mechanisms studied so far into one reusable `TransformerBlock`.

Implemented:

```text
X
↓
Causal Multi-Head Attention
↓
Output Projection
↓
First Residual Connection
↓
LayerNorm
↓
Feed-Forward Network
↓
Second Residual Connection
↓
LayerNorm
↓
Transformer Block Output
```

The complete block preserved:

```text
[sequence_length, d_model]
```

through every external stage.

Verified:

```text
Input                    [3, 8]
Attention Output         [3, 8]
First Residual           [3, 8]
FFN Output               [3, 8]
Second Residual          [3, 8]
Transformer Block Output [3, 8]
```

For token `"e"`:

```text
normalized attention
+
FFN update
=
second residual
```

was verified manually:

```text
SECOND RESIDUAL MANUAL MATCH:
True
```

The final representation had:

```text
mean ≈ 0
variance ≈ 1
```

after the second LayerNorm.

Key conclusion:

```text
attention
→ communication between positions

FFN
→ nonlinear computation within positions

residuals
→ preserve direct information paths

LayerNorm
→ normalizes intermediate representations
```

These mechanisms now form a reusable Transformer block.

---

## Experiment 23 — Stacked Transformer Blocks

**Status:** COMPLETE

Introduced model depth by stacking multiple independently parameterized Transformer blocks.

Architecture:

```text
token + position embeddings
↓
Transformer Block 1
↓
Transformer Block 2
↓
Transformer Block 3
↓
final contextual representations
```

Verified that different blocks own different parameters:

```text
Block 1 and Block 2 share Query parameter object:
False

Block 1 and Block 2 Query values identical:
False
```

Tracked token `"e"` through the stack and observed a different representation after every block.

Verified:

```text
Block 1 output != input
Block 2 output != Block 1 output
Block 3 output != Block 2 output
```

All checks returned:

```text
True
```

Every block preserved:

```text
[sequence_length, d_model]
```

The experiment verified:

```text
ALL LAYERS PRESERVE [sequence_length, d_model]:
True
```

Key conclusion:

```text
each block receives the previous block's output
```

and:

```text
each block normally owns independent trainable parameters
```

This introduces Transformer depth while preserving the model representation width.

---

## Experiment 24 — Language-Model Head and Vocabulary Logits

**Status:** COMPLETE

Connected final Transformer representations to the vocabulary using:

```text
Linear(d_model, vocabulary_size)
```

For:

```text
d_model = 8
vocabulary_size = 10
```

the LM Head performs:

```text
[8]
→
[10]
```

per token position.

For the complete sequence:

```text
[3, 8]
→
[3, 10]
```

Verified that every sequence position produces a complete set of vocabulary logits.

Because causal attention restricts available context:

```text
position 0 → prediction after "h"

position 1 → prediction after "he"

position 2 → prediction after "hel"
```

During generation, the final row is selected:

```python
next_token_logits = logits[-1]
```

resulting in:

```text
[10]
```

next-token scores for the complete prompt.

A vocabulary logit for token `"l"` was manually reproduced as a dot product between:

```text
contextual representation [8]
```

and:

```text
LM-head token weight [8]
```

The result matched PyTorch:

```text
MANUAL LOGIT MATCH:
True
```

Key conclusion:

```text
Transformer
→ contextual representation

LM Head
→ vocabulary logits
```

---

## Experiment 25 — Softmax and Next-Token Probabilities

**Status:** COMPLETE

Converted verified vocabulary logits into next-token probabilities using Softmax.

Starting logits:

```text
[10]
```

Softmax output:

```text
[10]
```

Verified:

```text
PROBABILITY SUM:
1.0
```

The token with the highest logit and highest probability was:

```text
'd'
```

and:

```text
ARGMAX LOGIT MATCHES ARGMAX PROBABILITY:
True
```

Implemented numerically stable Softmax manually:

```text
logits
↓
subtract max(logits)
↓
exponential
↓
divide by exponential sum
```

The manual calculation matched PyTorch:

```text
MANUAL SOFTMAX MATCH:
True
```

For vocabulary token `"l"`:

```text
logit       ≈ -0.3606
probability ≈ 0.0717
            ≈ 7.17 %
```

Key conclusion:

```text
Softmax
→ converts relative vocabulary scores
→ into a probability distribution
```

while preserving the ranking of the logits.

---

## Experiment 26 — Shifted Targets and CrossEntropyLoss

**Status:** COMPLETE

Goal:

Teach the model what the correct next token actually is and quantify prediction error.

For a sequence such as:

```text
hello
```

the training relationship is:

```text
input:
h e l l

target:
e l l o
```

Each input position predicts the token immediately to its right.

Planned flow:

```text
logits
[sequence_length, vocabulary_size]

+

target token IDs
[sequence_length]

↓

CrossEntropyLoss

↓

single scalar loss
```

The experiment will also verify manually why a low probability assigned to the correct token produces a larger loss.

## Experiment 27 — Backpropagation and Gradients

**Status:** COMPLETE

Goal:

Understand how the scalar language-model loss produces gradients for trainable parameters throughout the complete model.

Planned flow:

```text
forward pass
↓
logits
↓
CrossEntropyLoss
↓
loss.backward()
↓
gradients
```

The experiment will inspect gradients for:

```text
LM Head
Transformer parameters
token embeddings
```

and verify an essential distinction:

```text
backward()
→ calculates gradients

optimizer.step()
→ changes parameters
```

The optimizer update will remain a separate experiment.

## Experiment 28 — Optimizer Update

**Status:** COMPLETE

Goal:

Use the gradients calculated by backpropagation to modify trainable model parameters.

Planned flow:

```text
forward
↓
loss
↓
backward
↓
gradients
↓
optimizer.step()
↓
updated parameters
```

The experiment will compare exact parameter values before and after the optimizer step and verify that the next forward pass produces a different loss.

## Experiment 29 — Language-Model Training Loop

**Status:** COMPLETE

Goal:

Combine the complete learning process into a repeated training loop.

The experiment will integrate:

```text
forward pass
↓
CrossEntropyLoss
↓
zero_grad()
↓
backward()
↓
optimizer.step()
↓
repeat
```

It will track loss over multiple training steps and inspect how the model's next-token predictions change as its parameters learn from the training text.

This marks the transition from isolated training mechanics to an actually trained tiny language model.

## Experiment 30 — Autoregressive Generation and Sampling

**Status:** NEXT

Goal:

Use a trained causal language model to generate a sequence one token at a time.

The generation loop will follow:

```text
current context
↓
model
↓
final-position logits
↓
token selection
↓
append selected token
↓
new context
↓
repeat
```

The experiment will connect previously learned concepts:

```text
causal attention
final-position logits
Softmax probabilities
greedy selection
sampling
```

and demonstrate the distinction between:

```text
training
```

and:

```text
inference / generation
```

Rather than splitting greedy decoding and probabilistic sampling into separate microscopic experiments, they will be studied together in the autoregressive generation workflow.

---

## Remaining LLM Fundamentals

After Next-Token Probabilities:

```text
Autoregressive Generation
↓
Greedy Decoding
↓
Probabilistic Sampling
↓
Generated Text
```

Additional concepts:

- greedy decoding,
- temperature,
- top-k,
- top-p,
- context window,
- training vs inference,
- model parameter count,
- KV cache,
- RoPE,
- multi-query attention,
- grouped-query attention,
- pre-norm vs post-norm architectures.

---

## Phase 04 Synthesis Exercise

Connect the studied components in a small controlled GPT-like exercise using PyTorch, with a tiny dataset and an explicit question about training versus generation.

This synthesis is educational lab work, not a plan for an external repository. Keep its scope bounded and its limitations visible.

The exercise should connect:

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

Extend these interface primitives with:

- Python ↔ LLM request/response boundaries,
- chat messages and system / user / assistant roles,
- prompt construction,
- structured outputs and JSON Schema,
- output parsing and validation,
- function/tool-call requests before their execution in Phase 14.

Pydantic is a possible validation tool to learn after understanding the contract. A parseable response does not by itself prove a correct answer or authorize an action.

## Practical Work

Build a Python CLI that communicates with a local language model.

Keep the lab exercise small: one local request workflow with streaming or structured-response validation and bounded retries. Continue to [Phase 14 — Tool Calling](#phase-14--tool-calling), then the basic [Phase 15 agent loop](#phase-15--agents), before the retrieval branch if following the selected route.

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

In the lab, isolate a benchmark question with fixed prompts, controlled settings and repeated measurements.

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

Start with exact in-memory similarity so ranking is visible. FAISS, SQLite-based approaches and other local vector indexes are optional later comparisons, not required dependencies. Study chunking, metadata and retrieval evaluation through a small semantic-search experiment before extending scope.

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

Also study parsing, metadata, abstention and citation support. Hybrid retrieval, query rewriting and reranking can be compared after a baseline exposes a concrete retrieval failure. A small end-to-end RAG experiment belongs in the lab to understand ingestion, retrieval and grounding with controlled data and explicit evaluation.

---

# Phase 14 — Tool Calling

**Status:** PLANNED

**Selected route:** visit after Phase 07 structured interfaces and before the minimal agent loop. Phase identifiers are preserved; this block need not wait for every retrieval phase.

## Concepts

- tool schemas,
- structured arguments,
- validation,
- execution boundaries,
- permissions,
- authorization.

Distinguish generating a function/tool-call request from validating arguments, checking permission, executing a function and returning its result. Structured output is an interface contract, not automatic authority.

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

**Selected route:** basic blocks follow Phase 14; advanced blocks can follow semantic retrieval and RAG. Every block below remains future work. These are grouped learning questions, not ten pre-created experiment directories.

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

## Agentic AI Learning Blocks

| Block | Concepts and small lab work | Evidence before extending |
|---|---|---|
| Minimal loop and tool execution | Combine a local model, a controlled tool set, actions, observations, state, budgets and stopping conditions; build the loop from scratch | Trace a complete task, a tool failure and budget termination |
| State, memory and context | Distinguish current state, short-term context and persisted long-term memory; compare context construction and recovery strategies | Explain what survives between steps/runs and check that stale state does not silently become authority |
| Permissions and human approval | Validate tool arguments, enforce allowlists and sandbox boundaries, handle approvals and denied actions | Exercise permission denial, untrusted input and recovery; authorization stays in application code |
| Planning, retries and evaluation | Compare a fixed workflow with planning, reflection / retry loops and error recovery on a small task set | Measure success, errors, time and tool usage; retries/reflection must show benefit, not merely extra steps |
| Protocols and frameworks | After the primitive loop, inspect MCP tool/context interfaces, then compare a small LangChain / LangGraph workflow; study workflow triggers/retries before n8n | Explain protocol versus framework versus workflow platform, and what each adds over the minimal implementation |
| Advanced orchestration | Study subagents, multi-agent orchestration, persistent state and agentic RAG after a retrieval baseline exists | Compare against a single-agent or deterministic baseline and track state, permissions, termination and evaluation |

**Fundamentals first, framework second:** understand the primitive → build a minimal version → understand its limitations → then learn the framework. Agent loop from scratch → LangChain / LangGraph; workflow / automation fundamentals → n8n. MCP is a protocol to study, not a replacement for permissions or an agent implementation. Small controlled MCP, memory, LangGraph and n8n experiments can belong here. Choose free local execution options within the cost policy; no framework is mandatory.

### Minimal Coding-Agent Experiment

**Planned small educational experiment inside the lab.** A local model would receive a failing test in a tiny deliberately broken toy workspace and a controlled tool set: `read_file(path)`, `write_file(path, content)` and `run_tests()`.

The Python host would represent and validate each tool request, enforce permissions, execute the action and return its result to the model. The loop would maintain conversation/state, allow bounded retries and stop on verified completion, budget exhaustion or an unrecoverable error. The model would inspect files, propose a change and rerun the test through those tools rather than receiving unrestricted execution access.

The learning question is how tool calling becomes iterative tool use: request → host execution → result → next action. Record a successful toy task, a denied action and a failed/retried action, including termination behavior. Group these related mechanisms into one meaningful experiment. No source code, toy workspace or future directory is created by this documentation task.

Research agents, subagents and multi-agent orchestration remain learning concepts in the advanced blocks above; bounded experiments can study their mechanisms without planning external systems.

See the [Agentic AI field map](docs/ai-engineering-map.md#agentic-ai).

---

# Phase 16 — Multimodal AI

**Status:** PLANNED

## Concepts

- image input,
- text input,
- multimodal context,
- vision-language models,
- multimodal embeddings.

Extend later to image generation, audio, speech-to-text, text-to-speech, multimodal prompting and video concepts. Voice overlaps multimodal and agentic AI but does not inherently require an agent loop.

## Practical Work

Evaluate a compatible multimodal model.

Use a bounded task and evaluation set. A small voice exercise may connect recognition → LLM response generation → speech synthesis, measuring streaming latency and turn detection before tool actions. Small multimodal and voice experiments belong here when they explain a concept or a controlled workflow.

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

Include instruction tuning, training data quality and model merging concepts as later topics. Scope any local training to available memory; no paid compute is required by the route.

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

Use small controlled exercises to study production concerns such as evaluation, logging, caching, async execution, queues, packaging and regression tests. Each exercise should answer a clear engineering question and document its limits; this phase does not plan an external integrated system.

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
6. Structured outputs, tool calling and a bounded agent loop
7. Embeddings and semantic search
8. RAG, then advanced agents when justified
9. AI backend engineering
10. Evaluation
11. Deployment and observability
12. Further agentic / multimodal specialization as needed
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
