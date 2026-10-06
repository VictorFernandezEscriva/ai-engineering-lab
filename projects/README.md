# Standalone AI Engineering Projects

This directory is an index of larger engineering projects built while progressing through the AI Engineering roadmap.

The actual project source code lives in independent repositories.

This repository therefore keeps:

```text
topics/
→ small experiments used to understand individual mechanisms
```

while:

```text
projects/
→ references to larger standalone systems
```

No large project implementation should be placed directly inside this directory.

---

# Why Projects Are Separate

Experiments and engineering projects have different goals.

An experiment asks:

```text
How does this mechanism work?
```

A project asks:

```text
Can these mechanisms be combined into a useful and maintainable system?
```

For example:

```text
topics/04_llm_engineering/04_self_attention/
```

studies the internal mechanism of attention.

A standalone MiniGPT repository would instead combine:

```text
tokenization
+
embeddings
+
attention
+
Transformer blocks
+
training
+
generation
+
evaluation
```

into one complete system.

Separating them keeps this repository readable while allowing larger projects to have their own:

- architecture,
- source tree,
- tests,
- documentation,
- issues,
- releases,
- benchmarks,
- CI/CD.

---

# Project Index

| Project | Main Areas | Status | Repository |
|---|---|---|---|
| MiniGPT from Scratch | PyTorch, Transformers, LLM internals | Planned | — |
| Local LLM CLI | Local inference, APIs, Python | Planned | — |
| Inference Benchmark | Performance, hardware, quantization | Planned | — |
| Semantic Search Engine | Embeddings, similarity search | Planned | — |
| RAG Engine | Retrieval, embeddings, generation | Planned | — |
| Tool-Using Assistant | Tool calling, structured outputs | Planned | — |
| AI Agent | Agent loops, tools, state | Planned | — |
| Local Offline AI Application | Local inference, backend, client | Planned | — |

Projects should only be added to this table when their scope becomes concrete.

---

# Project Lifecycle

A project can move through:

```text
PLANNED
↓
BUILDING
↓
FUNCTIONAL
↓
EVALUATED
↓
COMPLETE
```

A project should not be considered complete only because it runs.

Evaluation and documented limitations are required.

---

# Recommended Project Repository Structure

Standalone projects may use a structure similar to:

```text
project-name/
│
├── src/
├── tests/
├── docs/
├── examples/
├── scripts/
│
├── README.md
├── requirements.txt
└── .gitignore
```

The exact structure should depend on the project.

---

# Project README Expectations

Each standalone project should explain:

## Problem

What problem is being solved?

## Architecture

What are the major components?

## AI Concepts

Which concepts from the AI Engineering roadmap are used?

## Implementation

How is the system implemented?

## Setup

How can another person run it?

## Evaluation

How is correctness or usefulness measured?

## Limitations

What has not been demonstrated?

## Engineering Decisions

Why were particular architectures, tools or models selected?

## Future Work

What would be required to improve the system?

---

# Relationship With This Repository

Standalone projects should reference the concepts studied here when useful.

For example:

```text
MiniGPT
↓
tokenization experiment
↓
embedding experiment
↓
attention experiment
↓
causal attention experiment
↓
Transformer block
```

The laboratory explains individual mechanisms.

Standalone projects demonstrate integration.