# AI Automation Foundations

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 07](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** B — Applied AI Automation

## Purpose

Begin the applied track: learn to analyse a business process, separate deterministic steps from semantic ones, and build reliable workflows around APIs and data before adding AI.

## Why it matters

Most business value comes from choosing the simplest sound architecture. Rules, APIs and validation solve many problems without a model; knowing the boundary is the core professional skill.

## Prerequisites

- Phase 06 — LLM Application Interfaces (for the AI steps); the process, HTTP and workflow fundamentals can start independently

## Core concepts

- Business-process decomposition
- Deterministic workflows and rules vs AI
- HTTP, REST APIs, JSON, webhooks
- API authentication concepts
- Data transformation and validation
- Retries, timeouts, idempotency and error handling
- Human approval and auditability
- Workflow evaluation: baseline, failure modes, generalization
- n8n fundamentals (local / self-hosted)

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet.

- Deterministic incident triage (an existing external exercise may eventually become the first experiment here; it is not moved by this documentation)
- Webhook → validation → routing
- API → transform → output
- Retry / error-handling exercise
- Human-approval workflow
- Simple local n8n workflow

Every applied experiment should state its baseline, what success means, the failure modes, how generalization is tested, whether AI beats deterministic logic, what happens when the model fails, and when a human intervenes.

## Relevant technologies

- Python
- n8n (self-hosted / local only; no paid Cloud tier)
- Free public APIs only where explicitly permitted
- SQLite

ZERO EXTRA COST: local models, open-source tools and free official resources only.

## Selected learning resources

n8n Academy. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
