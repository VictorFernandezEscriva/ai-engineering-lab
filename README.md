# AI Engineering Lab

A hands-on AI Engineering laboratory focused on understanding modern AI systems through implementation, experiments, evaluation and engineering analysis.

This repository is both:

- a structured technical learning notebook,
- and an engineering portfolio showing what has actually been implemented, executed and understood.

The objective is not to collect disconnected tutorials or simply call existing AI APIs.

The objective is to understand how AI systems work internally and how their components connect:

```text
data
↓
machine learning
↓
deep learning
↓
transformers
↓
language models
↓
inference
↓
embeddings
↓
retrieval
↓
tools
↓
agents
↓
applications
↓
production systems
```

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

Experiments are deliberately small so that individual mechanisms remain visible.

The existence of an experiment does not imply mastery of an entire field or production readiness.

---

## Repository Structure

```text
AiEngineeringLab/
│
├── docs/
│   ├── ecosystem-map.md
│   ├── glossary.md
│   ├── learning-method.md
│   ├── model-runtime-application.md
│   └── verification.md
│
├── projects/
│   └── README.md
│
├── tools/
│   └── hardware_report.py
│
├── topics/
│   ├── 01_machine_learning/
│   ├── 02_deep_learning/
│   ├── 03_computer_vision/
│   └── 04_llm_engineering/
│
├── .gitignore
├── README.md
├── requirements.txt
└── ROADMAP.md
```

### `topics/`

Small experiments used to understand individual concepts and mechanisms.

Examples:

```text
decision trees
overfitting
neural networks
CNNs
tokenization
embeddings
self-attention
causal attention
```

### `projects/`

Index of larger standalone AI Engineering projects.

Project source code lives in independent repositories rather than inside this laboratory.

### `docs/`

Cross-topic documentation explaining concepts that span multiple experiments.

### `tools/`

Reusable engineering utilities supporting the laboratory.

### `ROADMAP.md`

The main learning path, current progress and planned future work.

The roadmap describes progression.

It is not the repository directory structure.

---

# Current Progress

| Domain | Status |
|---|---|
| Machine Learning Foundations | Complete |
| Deep Learning Foundations | Complete |
| Computer Vision Foundations | Complete |
| LLM Fundamentals | In progress |
| Local Model Inference | Planned |
| LLM APIs and Integration | Planned |
| Hardware and Quantization | Planned |
| Embeddings and Semantic Search | Planned |
| RAG | Planned |
| Tool Calling | Planned |
| Agents | Planned |
| Multimodal AI | Planned |
| Fine-Tuning | Planned |
| AI Backend Engineering | Planned |
| Production AI Engineering | Planned |

---

# Current Learning Position

The current main path is:

```text
AI Engineering
│
├── Machine Learning ✅
├── Deep Learning ✅
├── Computer Vision Foundations ✅
│
└── LLM Engineering ← CURRENT
    │
    ├── Tokenization ✅
    ├── Token IDs ✅
    ├── Token Embeddings ✅
    ├── Positional Embeddings ✅
    ├── Self-Attention ✅
    ├── Causal Self-Attention ✅
    ├── Multi-Head Attention ✅
    ├── Attention Output Projection ✅
    ├── Residual Connection ✅
    ├── Layer Normalization ✅
    └── Feed-Forward Network ← NEXT
```

The current objective is to understand the internal mechanics of a GPT-like language model before moving into higher-level LLM applications.

The progression is:

```text
text
↓
tokenization
↓
token IDs
↓
embeddings
↓
positional information
↓
causal self-attention
↓
multi-head attention
↓
Transformer block
↓
Transformer stack
↓
language-model head
↓
vocabulary logits
↓
next-token prediction
↓
training
↓
sampling
↓
generation
```

The eventual result of this phase will be a small educational GPT-like model implemented from first principles using PyTorch.

---

# Completed Foundations

## Machine Learning

Implemented experiments covering:

- supervised learning,
- decision trees,
- train/test separation,
- model capacity,
- overfitting,
- generalization,
- evaluation limitations.

The experiments demonstrated that stronger training performance does not necessarily imply better generalization.

---

## Deep Learning

Implemented PyTorch experiments covering:

- tensors,
- linear layers,
- activations,
- logits,
- binary classification,
- loss functions,
- backpropagation,
- optimizers,
- normalization,
- classification thresholds,
- precision,
- recall,
- F1,
- confusion matrices.

The training loop was studied explicitly:

```text
forward pass
↓
prediction
↓
loss
↓
backpropagation
↓
gradients
↓
optimizer
↓
updated parameters
```

---

## Computer Vision

Implemented experiments covering:

- convolution,
- manually defined filters,
- multiple feature maps,
- learned convolution filters,
- pooling,
- CNN architectures,
- synthetic image classification,
- PyTorch DataLoaders,
- mini-batches,
- MNIST,
- multiclass classification,
- error analysis,
- confusion matrices,
- per-class evaluation.

A multiclass CNN achieved approximately:

```text
98%+ held-out MNIST test accuracy
```

The focus was not the score itself, but understanding the complete training and evaluation pipeline.

---

# LLM Engineering Experiments

Current experiments live under:

```text
topics/04_llm_engineering/
```

Implemented so far:

```text
01_tokenization
02_embeddings
03_positional_embeddings
04_self_attention
05_causal_attention
06_multi_head_attention
07_attention_output_residual
```

These experiments progressively build the internal representation pipeline of an autoregressive Transformer.

The next experiment introduces:

```text
multi-head attention
```

---

# Standalone Engineering Projects

Larger projects are developed in independent repositories.

This repository keeps only an index under:

```text
projects/README.md
```

Examples of future standalone projects include:

- MiniGPT from scratch,
- local LLM CLI,
- inference benchmark,
- semantic search engine,
- RAG system,
- tool-using assistant,
- local/offline AI application.

This separation keeps the laboratory focused on learning mechanisms while standalone repositories demonstrate larger engineering systems.

---

# AI Ecosystem Map

The high-level map of AI technologies and systems is maintained in:

```text
docs/ecosystem-map.md
```

It distinguishes between:

- foundations,
- machine learning,
- deep learning,
- AI domains,
- LLM engineering,
- AI applications,
- infrastructure,
- production engineering,
- specialized branches.

---

# Model, Runtime and Application

A model is not an application and model weights do not execute themselves.

The relationship between:

```text
application
runtime
model
compute
hardware
```

is documented separately in:

```text
docs/model-runtime-application.md
```

---

# Learning Principles

The repository follows several rules.

## Understand before abstracting

Start with visible mechanisms before relying on frameworks that hide them.

For example:

```text
manual convolution
↓
PyTorch Conv2d
```

and:

```text
manual self-attention
↓
Transformer abstractions
```

## Change one variable at a time

Experiments should isolate a specific question whenever possible.

## Separate evidence from assumptions

A result is only evidence for the conditions actually tested.

## Understand tensor shapes

Tensor shapes should always have a physical or conceptual interpretation.

## Evaluate, do not only train

Training metrics alone do not demonstrate useful generalization.

## Prefer transferable concepts

Frameworks change.

Core ideas such as:

```text
embeddings
attention
retrieval
evaluation
inference
latency
memory
tool boundaries
```

are more durable.

---

# Setup

Create a virtual environment:

```bash
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Activate on Linux or macOS:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Experiments should normally be executed from the repository root.

Example:

```bash
python topics/04_llm_engineering/05_causal_attention/main.py
```

Reusable hardware inspection:

```bash
python tools/hardware_report.py
```

Downloaded datasets are stored under ignored local directories such as:

```text
data/
```

Large model artifacts and generated caches should not be committed to Git.

---

# Verification

Execution evidence and verification notes are documented in:

```text
docs/verification.md
```

Fixed random seeds improve reproducibility but do not guarantee identical results across:

- operating systems,
- hardware,
- library versions,
- numerical backends.

---

# Roadmap

The complete progression is documented in:

```text
ROADMAP.md
```

The roadmap intentionally separates:

```text
core learning path
```

from:

```text
parallel skills and future specializations
```

Not every AI technology requires the same depth of study.

---

# License

No open-source license is provided for this repository.

The source code and documentation are published as part of a personal technical learning and engineering portfolio.