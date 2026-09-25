# AI Engineering Roadmap

This roadmap describes the learning path of the repository.

It is not the directory hierarchy.

Topics are grouped by technical domain, and future work remains documented here until implementation begins. Existing code is not considered proof of understanding by itself: experiments should be executed, inspected and explained before a phase is considered complete.

The general learning pattern is:

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

---

# Phase 01 — Machine Learning Foundations

**Status:** COMPLETE

## Concepts

* features and targets,
* supervised learning,
* decision trees,
* training and inference,
* model capacity,
* overfitting,
* train/test splits,
* generalization,
* evaluation limitations.

## Verified practical work

Implemented and reviewed experiments covering:

```text
Decision Tree
↓
explicit learned decision boundaries
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

## Completion checkpoint

The following concepts can now be explained:

* difference between features and targets,
* difference between `fit()` and `predict()`,
* why training performance is not enough,
* what held-out evaluation means,
* why model capacity can produce overfitting,
* why a single small test split provides limited evidence.

---

# Phase 02 — Deep Learning Foundations

**Status:** COMPLETE

## Concepts

* tensors,
* matrix operations,
* neural-network layers,
* weights and biases,
* activations,
* logits,
* sigmoid,
* binary classification,
* loss functions,
* gradient descent,
* backpropagation,
* optimizers,
* thresholds,
* normalization,
* evaluation metrics.

## Verified practical work

Implemented neural classifiers using PyTorch.

The experiments covered:

```text
input features
↓
Linear layer
↓
ReLU
↓
Linear layer
↓
logit
↓
prediction
```

Training was implemented using:

```text
forward pass
↓
loss
↓
backpropagation
↓
gradients
↓
optimizer
↓
updated weights
```

Additional experiments studied:

* train/test separation,
* normalization using training statistics,
* classification thresholds,
* accuracy,
* precision,
* recall,
* F1,
* confusion matrices,
* individual forward-pass inspection.

## Completion checkpoint

The following concepts can now be explained:

* what a tensor represents,
* what weights and biases are,
* why a neural network produces logits,
* difference between logits and probabilities,
* purpose of an activation function,
* purpose of a loss function,
* how backpropagation calculates gradients,
* how an optimizer changes model parameters,
* why thresholds affect precision and recall,
* why preprocessing must avoid test-data leakage.

---

# Phase 03 — Computer Vision Foundations

**Status:** IN PROGRESS — near completion

## Concepts

* images as tensors,
* channels,
* convolution kernels,
* feature maps,
* learned convolution filters,
* ReLU,
* pooling,
* spatial dimensions,
* CNN architectures,
* image datasets,
* DataLoaders,
* mini-batches,
* multiclass classification,
* image-model evaluation.

## Verified practical work

### Manual convolution

Implemented convolution using manually selected kernels.

Learned the relationship:

```text
image
+
kernel
↓
convolution
↓
feature map
```

### Multiple filters

Applied several filters to the same image and verified:

```text
1 input channel
↓
multiple filters
↓
multiple output feature maps
```

### Learned convolution filters

Built a CNN where convolution kernels were no longer manually defined.

Instead:

```text
initialized convolution weights
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

### Synthetic shape classification

Built a CNN that classified:

```text
circle
vs
square
```

and inspected:

* convolution weight shapes,
* feature-map shapes,
* learned filters,
* training accuracy.

### Held-out evaluation

Introduced an independent train/test split and inspected internal feature maps.

Verified:

```text
Training accuracy: 100%
Test accuracy:     100%
```

on the restricted synthetic dataset.

The limitations of this result were documented.

### MNIST dataset

Moved from manually generated images to a standard labelled dataset.

Verified:

```text
60,000 training images
10,000 test images
```

with individual image shape:

```text
[1, 28, 28]
```

### DataLoader and mini-batches

Introduced PyTorch `DataLoader`.

Verified:

```text
batch size = 64

training batches = 938
test batches     = 157
```

and learned that:

```text
1 epoch
=
one complete traversal of all training batches
```

### MNIST multiclass CNN

Built the first multiclass CNN in the repository.

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

Training used:

```text
Dataset
↓
DataLoader
↓
mini-batch
↓
CNN
↓
CrossEntropyLoss
↓
backpropagation
↓
Adam
```

Verified after three epochs:

```text
Test accuracy: 98.08%
```

## Remaining practical work

Before closing this phase:

1. perform MNIST error analysis,
2. build a confusion matrix,
3. inspect misclassified digits,
4. inspect per-class performance,
5. understand why aggregate accuracy can hide specific failure modes,
6. update the Computer Vision topic overview.

## Completion checkpoint

Before continuing, be able to explain:

* `[batch, channels, height, width]`,
* difference between a filter and a feature map,
* why convolution preserves local structure,
* why pooling reduces spatial resolution,
* why `out_channels` creates multiple feature maps,
* how convolution filters are learned,
* why `Flatten()` reorganizes rather than deletes values,
* how a DataLoader produces batches,
* what an epoch means,
* why one optimizer update normally occurs per training batch,
* difference between binary and multiclass classification,
* why MNIST produces ten logits,
* how `argmax` selects a class,
* why `CrossEntropyLoss` consumes raw logits,
* difference between training performance and held-out test performance.

---

# Phase 04 — LLM Fundamentals

**Status:** NEXT

## Goal

Understand how a language model works internally before focusing on LLM applications and infrastructure.

The objective is not only to call an LLM API.

The objective is to understand the pipeline:

```text
text
↓
tokenizer
↓
tokens
↓
embeddings
↓
transformer
↓
logits
↓
next-token probabilities
↓
generated text
```

## Concepts

* language modelling,
* tokens,
* token IDs,
* vocabulary,
* tokenization,
* embeddings,
* positional information,
* attention,
* queries,
* keys,
* values,
* self-attention,
* transformer blocks,
* feed-forward networks,
* residual connections,
* normalization,
* logits,
* softmax,
* next-token prediction,
* context windows,
* sampling,
* temperature,
* model weights.

## Expected practical work

Build small experiments progressing toward a minimal GPT-like model.

Suggested progression:

```text
text
↓
tokenization
↓
token IDs
↓
embedding vectors
↓
attention
↓
transformer block
↓
next-token logits
↓
sampling
```

Later combine the pieces into a small educational language model.

## Completion checkpoint

Before continuing, be able to explain:

* why LLMs operate on tokens instead of raw text,
* difference between a token and a token ID,
* what an embedding represents,
* why embedding vectors are learned,
* what attention is trying to accomplish,
* what queries, keys and values represent,
* why transformer blocks are stacked,
* what the final logits represent,
* how next-token prediction produces text,
* difference between model architecture, weights, runtime and application.

---

# Phase 05 — Local Models and Inference

**Status:** PLANNED

## Concepts

* pretrained model artifacts,
* model loading,
* inference,
* context,
* generation,
* CPU inference,
* GPU inference,
* RAM,
* VRAM,
* runtime configuration.

## Expected practical work

Run a compatible small language model locally and record:

* model,
* model size,
* hardware,
* context configuration,
* generation settings,
* latency,
* memory usage.

## Completion checkpoint

Explain:

* training vs inference,
* model architecture vs model weights,
* why models require memory,
* basic CPU/GPU inference differences.

---

# Phase 06 — Ollama and Local APIs

**Status:** PLANNED

## Concepts

* inference runtime,
* model management,
* local model server,
* HTTP,
* API requests,
* responses,
* generation parameters.

## Expected practical work

Run a local model through Ollama and call it through its HTTP API.

Inspect:

```text
Python / client
↓
HTTP request
↓
Ollama
↓
model runtime
↓
generated tokens
↓
HTTP response
```

## Completion checkpoint

Identify:

* which model is loaded,
* which process serves it,
* which process calls it,
* where inference occurs,
* what the HTTP API is responsible for.

---

# Phase 07 — Python Integration

**Status:** PLANNED

## Concepts

* HTTP clients,
* JSON,
* streaming,
* exceptions,
* timeouts,
* configuration,
* application boundaries.

## Expected practical work

Build a Python CLI that communicates with a local language model.

Include:

* structured requests,
* error handling,
* streaming,
* timeouts,
* configuration.

## Completion checkpoint

Understand the complete contract between:

```text
Python application
↔
LLM runtime
```

---

# Phase 08 — llama.cpp and GGUF

**Status:** PLANNED

## Concepts

* native inference runtimes,
* GGUF,
* model formats,
* quantized model artifacts,
* CPU execution,
* GPU offload,
* local servers.

## Expected practical work

Run compatible models through `llama.cpp`.

Compare:

```text
Ollama
vs
llama.cpp
```

while keeping model and test prompts controlled where possible.

## Completion checkpoint

Distinguish clearly between:

* model architecture,
* model weights,
* model file format,
* inference runtime.

---

# Phase 09 — Hardware and Quantization

**Status:** PLANNED

## Concepts

* parameter count,
* numerical precision,
* FP32,
* FP16,
* BF16,
* INT8,
* lower-bit quantization,
* RAM,
* VRAM,
* memory bandwidth,
* GPU offloading.

## Expected practical work

Compare compatible model configurations using fixed prompts and hardware.

Record:

* memory consumption,
* loading behavior,
* latency,
* generation speed,
* qualitative output changes.

## Completion checkpoint

Explain approximately why model memory requirements change with numerical precision and quantization.

---

# Phase 10 — Inference Benchmarking and Evaluation

**Status:** PLANNED

## Concepts

* latency,
* time to first token,
* tokens per second,
* throughput,
* warm-up,
* repeatability,
* evaluation datasets,
* output quality.

## Expected practical work

Build a reproducible inference benchmark.

Control:

* model,
* hardware,
* prompts,
* context,
* sampling settings,
* number of runs.

## Completion checkpoint

Distinguish performance benchmarking from model-quality evaluation.

---

# Phase 11 — Embeddings

**Status:** PLANNED

## Concepts

* vector representations,
* embedding models,
* vector dimensions,
* cosine similarity,
* normalization,
* semantic similarity.

## Expected practical work

Encode a small text collection and compare vector similarities.

## Completion checkpoint

Understand the difference between:

```text
text generation
```

and:

```text
text → vector representation
```

---

# Phase 12 — Semantic Search

**Status:** PLANNED

## Concepts

* retrieval,
* similarity ranking,
* top-k,
* document representations,
* relevance,
* retrieval evaluation.

## Expected practical work

Build semantic search over a small document collection.

Measure whether relevant documents appear in the top results.

## Completion checkpoint

Explain:

* query embedding,
* document embedding,
* similarity search,
* top-k retrieval,
* relevance evaluation.

---

# Phase 13 — RAG

**Status:** PLANNED

## Concepts

* document ingestion,
* chunking,
* embeddings,
* indexing,
* retrieval,
* context construction,
* grounded generation,
* citations,
* hallucination analysis.

## Expected practical work

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

Evaluate both retrieval and generated answers.

## Completion checkpoint

Distinguish:

```text
retrieval failure
```

from:

```text
generation failure
```

and detect unsupported generated claims.

---

# Phase 14 — Tool Calling

**Status:** PLANNED

## Concepts

* tool schemas,
* structured arguments,
* validation,
* execution boundaries,
* allowlists,
* application authorization.

## Expected practical work

Expose a small set of application functions to a model.

Validate arguments before execution.

## Completion checkpoint

Understand that:

```text
model requests action
```

is different from:

```text
application authorizes and executes action
```

---

# Phase 15 — Agents

**Status:** PLANNED

## Concepts

* state,
* planning,
* actions,
* observations,
* tool loops,
* retries,
* budgets,
* stopping conditions,
* traces.

## Expected practical work

Implement a bounded agent loop with observable execution.

## Completion checkpoint

Explain:

* agent state,
* action selection,
* execution,
* observation,
* termination,
* failure handling.

---

# Phase 16 — Multimodal Models

**Status:** PLANNED

## Concepts

* image inputs,
* text inputs,
* image representations,
* multimodal context,
* vision-language models,
* resource requirements.

## Expected practical work

Evaluate a compatible multimodal model using a small image-and-text task.

## Completion checkpoint

Connect previous computer-vision concepts with language-model inference.

---

# Phase 17 — Fine-Tuning / LoRA / QLoRA

**Status:** PLANNED

## Concepts

* pretrained models,
* adaptation,
* supervised fine-tuning,
* adapters,
* LoRA,
* QLoRA,
* datasets,
* training objectives,
* evaluation.

## Expected practical work

Run a small controlled adaptation and compare it against an unchanged baseline.

## Completion checkpoint

Understand:

* why fine-tuning is used,
* what parameters are updated,
* role of training-data quality,
* why independent evaluation is required.

---

# Phase 18 — AI Backend Engineering

**Status:** PLANNED

## Concepts

* service APIs,
* model lifecycle,
* concurrency,
* streaming,
* cancellation,
* queues,
* resource management,
* observability,
* failure handling.

## Expected practical work

Build an inference service with:

* streaming,
* request cancellation,
* bounded concurrency,
* structured errors,
* logging,
* metrics.

## Completion checkpoint

Understand how inference behavior affects backend architecture.

---

# Phase 19 — Flutter Integration

**Status:** PLANNED

## Concepts

* Dart HTTP clients,
* asynchronous requests,
* streaming UI,
* application state,
* connection failures.

## Expected practical work

Build a client for an evaluated AI backend.

## Completion checkpoint

Understand:

```text
Flutter application
↔
AI backend
↔
model runtime
```

and the asynchronous state transitions between them.

---

# Phase 20 — Packaging and Offline Distribution

**Status:** PLANNED

## Concepts

* application packaging,
* dependencies,
* model artifacts,
* compatibility,
* installation,
* updates,
* offline operation.

## Expected practical work

Package a prototype and install it on another machine without relying on network access.

## Completion checkpoint

Account for:

* model files,
* runtime dependencies,
* hardware requirements,
* licenses,
* updates,
* storage requirements.

---

# Phase 21 — Production and Product Engineering

**Status:** PLANNED

## Concepts

* product requirements,
* acceptance criteria,
* reliability,
* privacy,
* security,
* observability,
* evaluation,
* maintenance,
* recovery.

## Expected practical work

Turn one previous prototype into a production-oriented system.

Define:

* functional requirements,
* quality requirements,
* evaluation criteria,
* threat model,
* failure behavior,
* monitoring,
* regression tests,
* recovery behavior.

## Completion checkpoint

Be able to justify the complete system:

```text
product requirement
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

and clearly distinguish an experimental demo from a supported product.