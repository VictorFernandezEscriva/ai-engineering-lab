# AI ecosystem map

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

This is a conceptual dependency map, not a literal call stack: the runtime executes model operations through compute libraries on hardware, and returns outputs to the application.

| Layer | Responsibility | Examples |
|---|---|---|
| Application | User interaction and product logic | Programs written in Python or C++, Flutter clients, backend services |
| API / interface | Boundary through which callers request work | HTTP/JSON, a Python function or native interface |
| Runtime / inference engine | Load compatible artifacts and execute inference | Ollama, llama.cpp, ONNX Runtime; Transformers provides model implementations and inference workflows with a tensor backend |
| Model | Architecture and learned parameter values | Qwen, Llama, Mistral and gpt-oss model families |
| Compute | Numerical operations implementing the model | Matrix multiplication, convolution and execution kernels |
| Hardware | Physical processing and memory resources | CPU, GPU, NPU, system RAM and GPU VRAM |

**A model and a runtime are different things.** Weights do not execute themselves; compatible software must interpret them and schedule computation. An application defines what users can do with the resulting outputs. Python and C++ are languages; Flutter is an application framework, not a model.

The examples identify roles only, not tested compatibility combinations. Current executable work uses scikit-learn and PyTorch. Runtime-specific practical study is planned in the [roadmap](../ROADMAP.md).

For the introductory vocabulary, see [LLM fundamentals](../topics/04_llm_engineering/01_llm_fundamentals/README.md). Inspect local hardware with `python tools/hardware_report.py` from the repository root; this tool is not an inference benchmark.
