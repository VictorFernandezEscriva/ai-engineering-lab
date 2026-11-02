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

**Track:** A — Core AI Engineering (bridge to the applied track). Topic directory: `topics/05_local_models_inference/`. Absorbs the former Phases 06 (Ollama), 08 (llama.cpp / GGUF), 09 (hardware / quantization) and 10 (benchmarking), grouped as the blocks below.

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

## Block 5B — Ollama and local APIs

- inference runtime, model management, local model server,
- HTTP, JSON, API requests, streaming.

```text
Python client → HTTP → Ollama → runtime → model → generated tokens → response
```

## Block 5C — llama.cpp and GGUF

- native inference, GGUF, model formats, quantization, CPU execution, GPU offload.

Run compatible models through `llama.cpp` and compare Ollama versus llama.cpp.

## Block 5D — Hardware, quantization and benchmarking

- parameter count, FP32, FP16, BF16, INT8, INT4, RAM, VRAM, memory bandwidth, GPU offload,
- latency, time to first token, tokens per second, throughput, warm-up, repeatability, quality evaluation.

Compare configurations while controlling model, prompt, hardware and context; measure memory, latency, generation speed and output differences. Isolate a benchmark question with fixed prompts, controlled settings and repeated measurements.

**Resources:** Hugging Face LLM Course (pretrained models, model usage).

---

# Phase 06 — LLM Application Interfaces

**Status:** PLANNED

**Track:** bridge. Topic directory: `topics/06_llm_application_interfaces/`. Replaces the former Phase 07 (Python LLM Integration) and the request half of the former Phase 14 (Tool Calling).

Purpose: bridge model fundamentals to usable applications.

## Concepts

- Python ↔ local LLM boundaries,
- chat / message interfaces, system / user / assistant roles,
- prompt construction,
- streaming,
- structured outputs, JSON Schema, validation (Pydantic is a possible tool after the contract is understood),
- function calling and tool-calling foundations,
- error handling, timeouts, bounded retries, configuration.

Distinguish generating a tool-call request from validating arguments, checking permission, executing a function and returning its result. A parseable response does not prove a correct answer or authorize an action.

## Practical Work

Small educational experiments (none created yet): local chat client, structured-output extractor, streaming client, first controlled tool call.

```text
model requests action
≠
application automatically authorizes action
```

---

# Phase 07 — AI Automation Foundations

**Status:** PLANNED

**Track:** B — Applied AI Automation. Topic directory: `topics/07_ai_automation_foundations/`. New phase; it begins the explicit applied track. Supersedes the former "Automation" parallel track as a sequential block.

## Concepts

- business-process decomposition,
- deterministic workflows,
- rules versus AI (and when AI is not appropriate),
- HTTP fundamentals, REST APIs, JSON, webhooks,
- API authentication concepts,
- data transformation and validation,
- retries, timeouts, idempotency, error handling,
- human approval and auditability,
- workflow evaluation,
- n8n fundamentals (local / self-hosted).

n8n progression: fundamentals → API / workflow integrations → testing and error handling → (Phase 12) AI workflows → tools / agents. n8n is a workflow platform; learning it does not replace the fundamentals above.

## Practical Work

Small future experiments (none created yet): deterministic incident triage, webhook → validation → routing, API → transform → output, retry / error-handling exercise, human-approval workflow, a simple local n8n workflow.

The existing deterministic-triage exercise is kept outside this repository for now and may eventually become the first experiment here. Its `10/10` original cases and `4/4` tests are a baseline only, not proof of generalization.

**Resources:** n8n Academy (self-hosted / local; no paid tier required).

---

# Phase 08 — Embeddings and Semantic Retrieval

**Status:** PLANNED

**Track:** A — Core AI Engineering. Topic directory: `topics/08_embeddings_semantic_retrieval/`. Replaces the former Phases 11 (Embedding Models) and 12 (Semantic Search).

This phase concerns **external embedding models used for retrieval**, not the internal Transformer token embeddings already studied in Experiment 14.

## Concepts

- embedding models, sentence / document embeddings,
- vector similarity, cosine similarity, normalization,
- nearest-neighbor search, semantic search,
- chunking and metadata,
- local indexes (FAISS concepts),
- retrieval evaluation, reranking.

## Practical Work

Small future experiments: sentence similarity, semantic search, local vector index, retrieval evaluation. Start with exact in-memory similarity so ranking is visible. FAISS, SQLite-based approaches and other local vector indexes are optional later comparisons, not required dependencies. No paid vector service.

---

# Phase 09 — RAG and Knowledge Systems

**Status:** PLANNED

**Track:** bridge (Core and Applied). Topic directory: `topics/09_rag_knowledge_systems/`. Replaces the former Phase 13 (RAG).

## Concepts

- ingestion, parsing, chunking,
- embeddings, indexing, retrieval, reranking,
- context construction, grounded generation,
- citations, abstention,
- hybrid retrieval, query rewriting,
- RAG evaluation and failure modes (missing evidence, poor chunks, irrelevant retrieval, stale documents, unsupported claims, misleading citations).

## Practical Work

```text
documents → chunks → embeddings → retrieval → context → LLM → answer
```

Evaluate retrieval and generation separately. Small future experiments: minimal local RAG with citations, retrieval failure analysis. Hybrid retrieval, query rewriting and reranking are compared after a baseline exposes a concrete failure. A small end-to-end RAG experiment belongs in the lab to understand ingestion, retrieval and grounding with controlled data.

**Resources:** LangChain / LangGraph learn (RAG), after the from-scratch version.

---

# Phase 10 — Agentic Systems Fundamentals

**Status:** PLANNED

**Track:** B — Applied AI Automation & Agentic Systems. Topic directory: `topics/10_agentic_systems/`. Replaces the former Phase 14 (execution half) and Phase 15 (Agents).

## Concepts

- validated tool execution and execution boundaries,
- agent loop from scratch: state, actions, observations, termination,
- short-term memory, long-term memory concepts, context engineering,
- planning, retry / reflection loops, error recovery,
- permissions, sandboxing, human approval,
- budgets and tracing,
- agent evaluation.

## Practical Work

Small future experiments: agent loop from scratch, agent with two or three controlled tools, memory / state experiment, Minimal Coding-Agent Experiment, agent evaluation. These are grouped learning questions, not pre-created directories.

| Block | Concepts and small lab work | Evidence before extending |
|---|---|---|
| Minimal loop and tool execution | Local model, controlled tool set, actions, observations, state, budgets, stopping conditions | Trace a complete task, a tool failure and budget termination |
| State, memory and context | Current state, short-term context, persisted memory; context construction and recovery | Explain what survives between steps / runs; stale state must not become authority |
| Permissions and human approval | Argument validation, allowlists, sandbox boundaries, approvals, denied actions | Exercise permission denial, untrusted input and recovery; authorization stays in application code |
| Planning, retries and evaluation | Compare a fixed workflow with planning, reflection and retries on a small task set | Success, errors, time and tool usage; retries must show benefit, not merely extra steps |

### Minimal Coding-Agent Experiment

**Planned small educational experiment inside the lab.** A local model receives a failing test in a tiny deliberately broken toy workspace and a controlled tool set: `read_file(path)`, `write_file(path, content)` and `run_tests()`.

The Python host represents and validates each tool request, enforces permissions (including path restrictions), executes the action and returns its result to the model. The loop maintains state, allows bounded retries and stops on verified completion, budget exhaustion or an unrecoverable error.

The learning question is how tool calling becomes iterative tool use: request → host execution → result → next action. Record a successful toy task, a denied action and a failed / retried action, including termination behavior. A larger coding-agent product is not a lab experiment. No source code, toy workspace or directory is created by this documentation.

**Resources:** Hugging Face Agents Course — consume after structured outputs, tool calling and the minimal agent loop. See the [Agentic AI field map](docs/ai-engineering-map.md#agentic-ai).

---

# Phase 11 — MCP and AI Integration Protocols

**Status:** PLANNED

**Track:** B. Topic directory: `topics/11_mcp_integration/`. Split out of the former Phase 15 "Protocols and frameworks" block.

## Concepts

MCP architecture, client / server model, tools, resources, prompts, transports, permissions, local MCP servers, tool discovery, security boundaries. MCP is a protocol for connecting tools and context; it is not an agent loop or a permission policy.

## Practical Work

Small future experiments: minimal local MCP server exposing one or two safe tools, MCP client interaction, safe local tool exposure.

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

## Concepts

LangChain, LangGraph, state graphs, durable workflows, n8n AI workflows, subagents, handoffs, routers, multi-agent concepts, orchestration, agentic RAG, workflow-versus-agent comparison.

## Practical Work

Small future experiments: the same workflow implemented manually versus with LangChain / LangGraph, a small LangGraph workflow, an n8n AI workflow, a subagent experiment, an agentic-RAG comparison. Each is compared against a single-agent or deterministic baseline, tracking state, permissions, termination and evaluation. Choose free local execution options; if a tutorial assumes a paid provider, document a local adaptation instead.

**Resources:** LangChain / LangGraph learn, Hugging Face Agents Course, n8n Academy.

---

# Phase 13 — Multimodal AI and Voice

**Status:** PLANNED

**Track:** A — Core AI Engineering. Former Phase 16; no topic directory yet.

## Concepts

- image input, text input, multimodal context,
- vision-language models, multimodal embeddings,
- later: image generation, audio, speech-to-text, text-to-speech, multimodal prompting, video concepts.

Voice overlaps multimodal and agentic AI but does not inherently require an agent loop.

## Practical Work

Evaluate a compatible multimodal model on a bounded task and evaluation set. A small voice exercise may connect recognition → LLM response generation → speech synthesis, measuring streaming latency and turn detection before tool actions. Voice agents come only after the agent fundamentals (Phase 10).

---

# Phase 14 — Fine-Tuning, LoRA and QLoRA

**Status:** PLANNED

**Track:** A — Core AI Engineering. Former Phase 17; no topic directory yet.

## Concepts

- pretrained models, adaptation, supervised fine-tuning,
- LoRA, QLoRA, PEFT,
- datasets and training-data quality, evaluation.

## Practical Work

Run a small controlled adaptation and compare it against a baseline. Include instruction tuning and model-merging concepts as later topics. Distinguish changing parameters from providing retrieved context. Scope any local training to available memory; no paid compute is required.

**Resources:** Hugging Face LLM Course (fine-tuning chapters).

---

# Phase 15 — AI Backend Engineering and Client Integration

**Status:** PLANNED

**Track:** bridge. Former Phases 18 and 19; no topic directory yet.

## Concepts

- FastAPI, service APIs, streaming, concurrency, cancellation, queues, resource management,
- logging, metrics, observability, failure handling,
- HTTP clients, asynchronous requests, streaming UI, application state, network failures.

## Practical Work

Build a small inference service with streaming, cancellation, bounded concurrency, structured errors, logs and metrics, and a client for it.

---

# Phase 16 — Packaging and Offline Distribution

**Status:** PLANNED

**Track:** A / bridge. Former Phase 20; no topic directory yet.

## Concepts

packaging, dependencies, model artifacts, compatibility, installation, updates, offline operation.

## Practical Work

Install and run a prototype on another machine without requiring network access.

---

# Phase 17 — Production AI Engineering

**Status:** PLANNED

**Track:** bridge. Former Phase 21; no topic directory yet. Where Core and Applied converge.

## Concepts

- product requirements, acceptance criteria,
- reliability, privacy, security, AI safety,
- observability, monitoring, regression testing, maintenance, recovery,
- MLOps / LLMOps, local / offline deployment, performance, cost awareness.

## Practical Work

Use small controlled exercises to study production concerns such as evaluation, logging, caching, async execution, queues, packaging and regression tests. Each exercise answers a clear engineering question and documents its limits; this phase does not plan an external integrated system.

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
