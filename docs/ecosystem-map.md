# AI Ecosystem Map

Artificial Intelligence is not one technology.

It is an ecosystem of mathematical foundations, models, software systems, infrastructure and applications.

This document provides the high-level map used throughout the repository.

It is not a strict learning order.

The learning sequence is defined in:

```text
ROADMAP.md
```

---

# High-Level Map

```text
                          ARTIFICIAL INTELLIGENCE
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        │                          │                          │
   FOUNDATIONS                AI MODELS                 AI SYSTEMS
        │                          │                          │
        │                          │                          │
 Math / Data / SWE          ML / DL / LLMs          Applications / Infra
```

A more detailed view:

```text
AI ENGINEERING
│
├── Foundations
│   ├── Python
│   ├── mathematics
│   ├── statistics
│   ├── linear algebra
│   ├── optimization
│   ├── data structures
│   ├── algorithms
│   ├── Git
│   ├── Linux
│   └── software engineering
│
├── Data
│   ├── SQL
│   ├── databases
│   ├── data cleaning
│   ├── data validation
│   ├── ETL / ELT
│   ├── pipelines
│   └── datasets
│
├── Machine Learning
│   ├── supervised learning
│   ├── regression
│   ├── classification
│   ├── unsupervised learning
│   ├── clustering
│   ├── anomaly detection
│   ├── feature engineering
│   ├── evaluation
│   └── generalization
│
├── Deep Learning
│   ├── neural networks
│   ├── backpropagation
│   ├── optimization
│   ├── CNNs
│   ├── sequence models
│   └── Transformers
│
├── AI Domains
│   ├── Computer Vision
│   ├── Natural Language Processing
│   ├── Time Series
│   ├── Speech
│   ├── Multimodal AI
│   └── Recommender Systems
│
├── LLM Engineering
│   ├── tokenization
│   ├── embeddings
│   ├── positional information
│   ├── attention
│   ├── Transformer blocks
│   ├── next-token prediction
│   ├── inference
│   ├── sampling
│   ├── context management
│   └── evaluation
│
├── Local AI
│   ├── Ollama
│   ├── llama.cpp
│   ├── GGUF
│   ├── quantization
│   ├── CPU inference
│   └── GPU inference
│
├── Retrieval Systems
│   ├── embeddings
│   ├── semantic search
│   ├── vector indexes
│   ├── vector databases
│   ├── reranking
│   └── RAG
│
├── AI Applications
│   ├── structured outputs
│   ├── tool calling
│   ├── agents
│   ├── automation
│   ├── multimodal applications
│   └── AI backends
│
├── AI Infrastructure
│   ├── GPUs
│   ├── CUDA
│   ├── model serving
│   ├── batching
│   ├── caching
│   ├── distributed inference
│   └── distributed training
│
├── Production AI
│   ├── evaluation
│   ├── observability
│   ├── deployment
│   ├── MLOps
│   ├── LLMOps
│   ├── security
│   ├── privacy
│   └── reliability
│
└── Specializations
    ├── Edge AI
    ├── Robotics
    ├── Reinforcement Learning
    ├── Graph AI
    ├── Digital Twins
    ├── Scientific ML
    └── Generative Media
```

---

# Foundations

Foundations support almost every other branch.

Important areas include:

```text
Python
NumPy
linear algebra
probability
statistics
calculus
optimization
Git
Linux
software engineering
algorithms
```

These are not separate from AI Engineering.

They are the tools used to build and understand AI systems.

---

# Data

Most AI systems depend on data before they depend on models.

Typical responsibilities include:

```text
collection
↓
validation
↓
cleaning
↓
transformation
↓
storage
↓
training / retrieval / inference
```

Relevant technologies may include:

```text
SQL
PostgreSQL
Redis
data pipelines
ETL / ELT
Spark
Kafka
```

The exact technology depends on scale and system requirements.

---

# Machine Learning

Machine Learning learns patterns from data.

Typical problems include:

```text
classification
regression
clustering
anomaly detection
recommendation
ranking
```

Classical ML remains useful when:

- datasets are structured,
- interpretability matters,
- computational resources are limited,
- deep learning is unnecessary.

Common tools include:

```text
scikit-learn
XGBoost
LightGBM
```

---

# Deep Learning

Deep Learning uses neural networks with learnable representations.

Core concepts include:

```text
tensors
layers
weights
activations
loss functions
gradients
backpropagation
optimizers
```

Major architectures include:

```text
MLPs
CNNs
sequence models
Transformers
```

PyTorch is the main framework used in this repository.

---

# Computer Vision

Computer Vision processes visual information.

Typical tasks include:

```text
classification
object detection
segmentation
tracking
pose estimation
image embeddings
vision-language understanding
```

Relevant architectures include:

```text
CNNs
Vision Transformers
multimodal models
```

---

# Natural Language Processing

NLP processes human language.

Important concepts include:

```text
tokenization
embeddings
semantic similarity
classification
information extraction
sequence modelling
attention
Transformers
```

Modern LLMs are one branch of NLP, not the entire field.

---

# Transformers

Transformers use attention-based architectures to process sequences.

Important components include:

```text
token embeddings
positional information
queries
keys
values
self-attention
multi-head attention
residual connections
normalization
feed-forward networks
Transformer blocks
```

Transformers are used beyond text, including:

```text
vision
audio
time series
multimodal models
```

---

# Large Language Models

Large Language Models are large neural networks trained primarily on token prediction objectives.

A simplified autoregressive pipeline is:

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
sampling
↓
generated token
```

The process repeats autoregressively.

LLMs are models.

They are not applications by themselves.

---

# Embeddings

Embeddings convert objects into numerical vectors.

Examples include:

```text
text → vector
image → vector
audio → vector
user → vector
product → vector
```

Embeddings can support:

```text
similarity
retrieval
clustering
recommendation
RAG
```

Generation models and embedding models solve different problems.

---

# Semantic Search

Semantic search retrieves information based on meaning rather than only exact text matching.

Typical pipeline:

```text
documents
↓
embeddings
↓
vector index

query
↓
query embedding
↓
similarity search
↓
top-k documents
```

---

# Vector Databases

Vector databases store and search vector representations.

Examples include:

```text
Qdrant
Milvus
Weaviate
pgvector
```

A vector database is not always required.

Small systems can use:

```text
in-memory search
NumPy
FAISS
database extensions
```

depending on scale and operational requirements.

---

# Retrieval-Augmented Generation

RAG combines retrieval with generation.

Typical pipeline:

```text
documents
↓
chunking
↓
embeddings
↓
index

user query
↓
retrieval
↓
relevant context
↓
LLM
↓
grounded answer
```

RAG has at least two separate failure modes:

```text
retrieval failure
```

and:

```text
generation failure
```

They should be evaluated independently.

---

# Fine-Tuning

Fine-tuning modifies model parameters using additional training data.

Common approaches include:

```text
supervised fine-tuning
LoRA
QLoRA
adapters
preference optimization
```

Fine-tuning and RAG solve different problems.

RAG primarily provides external information.

Fine-tuning primarily changes model behaviour or internal parameter adaptation.

---

# Tool Calling

Tool calling allows an AI model to request actions through structured interfaces.

Example:

```text
model
↓
tool request
↓
validated arguments
↓
application authorization
↓
tool execution
↓
result
↓
model
```

The model should not directly control unrestricted external systems.

The application remains responsible for validation and authorization.

---

# Agents

An agent adds a control loop around a model.

A simplified loop is:

```text
state
↓
model
↓
action
↓
tool execution
↓
observation
↓
updated state
↓
repeat
```

Additional concerns include:

```text
budgets
permissions
stopping conditions
retries
memory
traceability
evaluation
security
```

An agent is therefore more than a chatbot.

---

# Automation

AI can be inserted into deterministic workflows.

Example:

```text
trigger
↓
data
↓
AI / ML
↓
decision
↓
tool
↓
action
↓
notification
```

Not every automation requires an LLM.

Traditional software logic should be preferred when it solves the problem reliably.

---

# Local AI

Local AI runs models on local hardware instead of depending entirely on remote APIs.

Relevant concepts include:

```text
model artifacts
inference runtimes
GGUF
quantization
RAM
VRAM
CPU inference
GPU inference
latency
```

Example runtimes include:

```text
Ollama
llama.cpp
ONNX Runtime
```

---

# AI Infrastructure

Infrastructure supports training or inference.

Important concepts include:

```text
GPUs
VRAM
memory bandwidth
batching
caching
model serving
latency
throughput
distributed inference
distributed training
```

Understanding infrastructure becomes increasingly important as models and workloads grow.

---

# MLOps and LLMOps

Production systems require more than model code.

Relevant responsibilities include:

```text
versioning
deployment
evaluation
monitoring
observability
tracing
drift detection
regression testing
cost tracking
latency tracking
model routing
```

LLMOps extends these concerns to language-model systems.

---

# Edge AI

Edge AI executes inference close to the data source.

Examples include:

```text
embedded devices
mobile devices
industrial hardware
robots
sensors
```

Important topics include:

```text
quantization
model optimization
ONNX
TensorRT
NPUs
latency
power consumption
memory limits
```

---

# Specialized Branches

Some areas are valuable but are not currently part of the main learning path.

These include:

```text
Reinforcement Learning
Robotics
Graph Neural Networks
Knowledge Graphs
Digital Twins
Physics-Informed ML
Scientific ML
Generative Image / Audio / Video
```

They can be studied later when required by a project or specialization.

---

# Core AI Engineering Perspective

The goal is not to use every technology.

The goal is to understand enough of the ecosystem to make decisions such as:

```text
Do I need ML?

Do I need an LLM?

Do I need embeddings?

Do I need retrieval?

Do I need a vector database?

Do I need RAG?

Do I need an agent?

Should inference be local or remote?

What should remain deterministic software?
```

Good AI Engineering often means deciding what not to use.

---

# Related Documentation

Learning sequence:

```text
../ROADMAP.md
```

Model/runtime/application distinction:

```text
model-runtime-application.md
```

Learning methodology:

```text
learning-method.md
```

Terminology:

```text
glossary.md
```

Verification evidence:

```text
verification.md
```