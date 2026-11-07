# AI Ecosystem Map — technologies and frameworks

This document answers one question: **which tools, frameworks, platforms and protocols exist, and where does each fit?**

It is a landscape for orientation, not a curriculum.

| Question | Document |
|---|---|
| What is there to know, and how do concepts relate? | [AI Engineering Map](ai-engineering-map.md) |
| In what order do I learn it? | [ROADMAP](../ROADMAP.md) |
| Which technologies are hands-on, compared, awareness-only or enterprise-mapping? | [Professional capabilities and technology tiers](professional-capabilities.md) |
| How do model, runtime and application differ? | [Model, runtime and application](model-runtime-application.md) |

Technologies are tools that serve concepts. Nothing below is a prerequisite until its phase begins, and the lab never requires a paid service (ZERO EXTRA COST). The tier of each technology is stored once, in the Learning Cockpit catalog, and summarized in the professional-capabilities document; it is deliberately not repeated here.

## Landscape by role

| Role | Technologies | Lab phase |
|---|---|---|
| **Numerical and ML libraries** | NumPy, scikit-learn, PyTorch | 01–04 |
| **Model runtimes (local inference)** | Ollama, llama.cpp / GGUF | 05 |
| **Serving and gateways** | vLLM, LiteLLM | 05 (awareness) |
| **Model APIs and cloud platforms** | Azure OpenAI, Microsoft Foundry, other hosted model APIs | 06 (enterprise mapping) |
| **Structured interfaces** | Pydantic, JSON Schema, DSPy | 06 |
| **Automation and integration** | n8n, OpenAPI, OAuth2 / OIDC, Playwright, Copilot Studio | 07, 12 |
| **Retrieval and vector search** | BM25, FAISS, PostgreSQL + pgvector, Qdrant, Azure AI Search | 08 |
| **RAG toolkits** | LlamaIndex | 09 |
| **Protocols** | MCP (agent ↔ tools and data), A2A (agent ↔ agent), AG-UI (agent ↔ UI) | 11 |
| **Agent frameworks** | LangChain, LangGraph, Microsoft Agent Framework, AutoGen / Semantic Kernel, PydanticAI, OpenAI Agents SDK, CrewAI | 12 |
| **Backend and data** | FastAPI, PostgreSQL, Redis / RabbitMQ / Kafka | 15 |
| **Packaging and delivery** | Docker and Compose, Kubernetes (awareness), GitHub Actions, infrastructure as code | 16–17 |
| **Evaluation** | Promptfoo, DeepEval / Ragas | 06, 09, 17 |
| **Observability** | OpenTelemetry, Arize Phoenix | 17 |
| **Azure / Microsoft mapping** | Azure Functions, Container Apps, Service Bus, Entra ID, Key Vault, Monitor | 17 (conceptual) |

## How the layers stack

```text
APPLICATION      chat UI · automation · agent · RAG service
     │            built with: n8n · LangGraph · MCP clients · FastAPI
RUNTIME          loads weights and executes the model
     │            Ollama · llama.cpp · vLLM · hosted APIs
MODEL            weights + architecture (Transformer)
                  PyTorch · GGUF / safetensors files
```

Frameworks sit in the application layer: they orchestrate calls to a model, tools and data. They do not replace understanding the model, the runtime or the loop underneath, which is why the roadmap builds each primitive from scratch before comparing a framework.

## Where protocols fit

```text
user ↔ UI ──(AG-UI)── agent ──(MCP)── tools and data sources
                        │
                        └──(A2A)── other agents
```

## Reading the landscape critically

- A technology is a means. Choose it when a measured problem justifies it.
- Tools change quickly; the concepts they implement (retrieval, state, tool calling, evaluation) change slowly.
- Vendor names appear where an enterprise mapping is useful. Mapping a concept to a vendor product is not the same as having used it.
