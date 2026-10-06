# Model, Runtime and Application

AI systems contain several layers that are often confused with each other.

A model is not a runtime.

A runtime is not an application.

Hardware is not a model.

This document explains those boundaries.

For the broader AI technology landscape, see:

```text
ecosystem-map.md
```

---

# Simplified Stack

```text
APPLICATION
↓
API / INTERFACE
↓
RUNTIME / INFERENCE ENGINE
↓
MODEL
↓
COMPUTE
↓
HARDWARE
```

This is a conceptual dependency model rather than a strict literal call stack.

---

# Application

The application defines what the user can actually do.

Examples include:

```text
CLI
web application
mobile application
backend service
desktop application
automation workflow
```

Responsibilities can include:

- user interaction,
- business logic,
- validation,
- error handling,
- persistence,
- authentication,
- authorization,
- orchestration.

An application may use AI, but AI is only one component of the complete system.

---

# API / Interface

The interface defines how one software component communicates with another.

Examples include:

```text
Python function call
HTTP API
REST endpoint
WebSocket
native library interface
command-line interface
```

For example:

```text
Python application
↓
HTTP request
↓
local model server
```

The interface is not the model itself.

---

# Runtime / Inference Engine

A runtime loads compatible model artifacts and executes model operations.

Examples include:

```text
Ollama
llama.cpp
ONNX Runtime
TensorRT
vLLM
```

A runtime may handle:

- model loading,
- memory allocation,
- inference execution,
- hardware acceleration,
- batching,
- caching,
- token generation,
- model serving.

The runtime executes the model.

The runtime is not the learned model itself.

---

# Model

A model consists conceptually of:

```text
architecture
+
learned parameters
```

Examples of architecture families include:

```text
CNN
Transformer
GPT-style decoder
Vision Transformer
```

Examples of model families include:

```text
Llama
Qwen
Mistral
```

Model weights contain learned numerical parameters.

Weights do not execute themselves.

They require compatible software.

---

# Model Artifact

A model may be stored in different file formats.

Examples include:

```text
PyTorch checkpoint
safetensors
GGUF
ONNX
```

The file format is not the model architecture.

It is a representation used to store or distribute model information.

A useful distinction is:

```text
architecture
≠
weights
≠
file format
≠
runtime
```

---

# Compute

The model ultimately consists of numerical operations.

Examples include:

```text
matrix multiplication
convolution
normalization
activation functions
attention
```

Compute libraries and kernels perform these operations efficiently.

Examples can include:

```text
PyTorch tensor operations
CUDA kernels
cuDNN
BLAS implementations
TensorRT kernels
```

---

# Hardware

Hardware performs the physical computation and provides memory.

Examples include:

```text
CPU
GPU
NPU
TPU
system RAM
GPU VRAM
```

Hardware constraints affect:

- model size,
- numerical precision,
- context size,
- batch size,
- latency,
- throughput.

---

# Example: Local LLM Application

Consider a Python application using a locally running model.

```text
Python application
↓
HTTP request
↓
Ollama server
↓
model runtime
↓
model weights
↓
GPU / CPU computation
↓
generated tokens
↓
HTTP response
↓
Python application
```

Each layer has a different responsibility.

---

# Example: Direct Native Inference

A different architecture may be:

```text
C++ application
↓
llama.cpp library
↓
GGUF model
↓
CPU / GPU
```

There may be no HTTP server at all.

The conceptual layers still exist even though their implementation boundaries are different.

---

# Example: PyTorch Experiment

The experiments in this repository often use:

```text
Python script
↓
PyTorch
↓
PyTorch model
↓
tensor operations
↓
CPU / GPU
```

In this case PyTorch provides both:

- model implementation tools,
- tensor execution infrastructure.

---

# Architecture vs Weights

An architecture describes the structure of the model.

For example:

```text
token embeddings
↓
Transformer blocks
↓
language-model head
```

Weights are the learned numerical values inside that structure.

Two models can share similar architecture while having different weights.

---

# Training vs Inference

Training changes model parameters.

```text
input
↓
model
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

Inference does not normally update model parameters.

```text
input
↓
model
↓
output
```

The same architecture may participate in both processes, but the execution behaviour is different.

---

# Model vs Application

A language model may produce:

```text
next-token probabilities
```

but an application decides:

- what prompt is created,
- which model is used,
- what tools are available,
- how results are displayed,
- what errors are allowed,
- what actions are authorized.

Therefore:

```text
model capability
≠
complete product capability
```

---

# Runtime vs Model

A runtime can often support multiple models.

For example:

```text
runtime
├── model A
├── model B
└── model C
```

Likewise, some model families may be supported by multiple runtimes.

Compatibility depends on:

- architecture support,
- file format,
- numerical precision,
- hardware,
- implementation details.

---

# Hardware vs Runtime

A GPU does not automatically execute an AI model.

Software must:

```text
load model
↓
allocate memory
↓
prepare tensors
↓
schedule operations
↓
execute kernels
```

The runtime and compute libraries provide this bridge.

---

# Key Distinctions

Always distinguish:

```text
MODEL
What mathematical transformation has been learned?
```

```text
MODEL ARTIFACT
How are architecture information and/or parameters stored?
```

```text
RUNTIME
What software executes the model?
```

```text
INTERFACE
How do other components communicate with the runtime?
```

```text
APPLICATION
What useful system is built around the model?
```

```text
HARDWARE
Where does computation physically occur?
```

---

# Connection to Current Learning

Current LLM experiments are studying the model itself:

```text
tokenization
↓
embeddings
↓
attention
↓
Transformer components
↓
next-token prediction
```

Later roadmap phases will move outward:

```text
model internals
↓
local runtime
↓
API
↓
Python application
↓
backend
↓
client
↓
production system
```

The LLM Engineering topic overview is located at:

```text
../topics/04_llm_engineering/README.md
```

The complete learning path is documented in:

```text
../ROADMAP.md
```

Local hardware can be inspected with:

```bash
python tools/hardware_report.py
```

The hardware report is a diagnostic tool.

It is not an inference benchmark.