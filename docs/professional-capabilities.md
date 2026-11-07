# Professional capabilities and technology tiers

Reference for the final curriculum enrichment of Phases 05–17. It does not add phases. Everything here is a **curriculum target**; nothing implies the learner already has the skill. ZERO EXTRA COST applies: enterprise and cloud services are studied from documentation and mapped to concepts, never activated.

Target roles: AI Engineer, LLM Engineer, RAG Engineer, AI Agent Engineer, AI Automation Engineer, AI Solutions Engineer, Cloud AI Engineer, AI Solutions Architect. Main direction: **AI Automation & Agentic Systems Engineer** with strong Core AI foundations.

## Technology tiers

| Tier | Meaning | Cockpit representation |
|---|---|---|
| `hands-on` | We will practice it | `technologies` entry; a node only when it teaches a distinct concept |
| `compare` | Study its abstraction against a baseline we built | `technologies` entry |
| `awareness` | Know what problem it solves and when it appears | `technologies` entry |
| `enterprise-mapping` | A managed / Microsoft service mapped onto a generic concept | `technologies` entry; no paid use |

The machine-readable registry is `technologies` in `tools/learning_cockpit/catalog/catalog.json`; it is validated against known nodes.

## Technologies by phase

| Phase | Hands-on | Compare / awareness | Enterprise mapping |
|---|---|---|---|
| 05 | Ollama, llama.cpp / GGUF | vLLM (serving), LiteLLM (gateway) | — |
| 06 | Pydantic, JSON Schema, OpenAI-compatible HTTP | DSPy (later) | Azure OpenAI, Microsoft Foundry endpoints |
| 07 | n8n, OpenAPI, Playwright (fallback only) | OAuth2 / OIDC | Copilot Studio |
| 08 | one or two of FAISS, PostgreSQL + pgvector, Qdrant | BM25 | Azure AI Search |
| 09 | from-scratch local RAG | LlamaIndex | Azure AI Search |
| 10 | agent loop from scratch | — | — |
| 11 | MCP | A2A (awareness-to-practice), AG-UI (awareness) | — |
| 12 | LangChain, LangGraph, n8n AI, Microsoft Agent Framework | PydanticAI, LlamaIndex workflows, OpenAI Agents SDK, CrewAI; AutoGen / Semantic Kernel (historical) | Microsoft Foundry, Copilot Studio |
| 15 | FastAPI, Pydantic, PostgreSQL | Redis, RabbitMQ, Kafka (concepts) | Service Bus, Event Grid |
| 16 | Docker, Docker Compose | Kubernetes fundamentals, Helm (awareness) | AKS, Container Apps |
| 17 | Git, GitHub Actions (concepts) | OpenTelemetry (concepts) | Azure Monitor, Application Insights, Entra ID, Key Vault |

## Microsoft / Azure mapping (not a separate universe)

| Microsoft technology | Generic concept it maps to | Phases |
|---|---|---|
| Azure OpenAI | inference APIs, streaming, structured outputs, tool calling, tokens / context, rate limits, retries, authentication, deployments / versions; compare with OpenAI-style APIs, Ollama, local servers | 06 |
| Azure AI Search | BM25, vector retrieval, HNSW, hybrid search, semantic ranking, metadata filters, enterprise RAG, access control | 08–09 |
| Microsoft Copilot Studio | low-code agents, knowledge, tools / actions / connectors, workflow integration, conversation state, authentication / governance; **use it vs build custom Python agents** | 07, 12 |
| Microsoft Agent Framework | agents, tools, sessions / state, memory, middleware, workflows, MCP, human-in-the-loop, telemetry, hosting; successor to ideas from AutoGen and Semantic Kernel | 12 |
| Microsoft Foundry | model catalog, endpoints / deployments, agents / tools, evaluation, tracing, monitoring, governance | 06, 12, 17 |
| Azure Functions, App Service, Container Apps, AKS | serverless, web hosting, containers, Kubernetes | 15–17 |
| Storage, PostgreSQL / Cosmos DB | object storage, relational / document databases | 15 |
| Service Bus, Event Grid | message broker, event routing | 15 |
| Entra ID, Key Vault | identity / OIDC, secrets | 07, 16–17 |
| Azure Monitor, Application Insights | metrics, logs, tracing | 17 |

## Decision aids

- **Architecture:** plain function → deterministic workflow → LLM call → RAG → agent → multi-agent. Move on only when the previous level fails.
- **Integration:** prefer supported APIs before browser automation.
- **Adaptation:** change the context (RAG) before the prompt / program (DSPy) before the weights (fine-tuning).
- **Framework lens:** what abstraction, what it manages for me, what control I lose, how it handles state, tool execution, recovery, evaluation and observability.

## Awareness-only items

AG-UI and similar agent-to-UI protocols, legacy AutoGen and Semantic Kernel, CrewAI and Helm are recorded for vocabulary. Promote one only when a project or repeated market evidence justifies it.
