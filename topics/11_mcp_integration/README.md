# MCP and AI Integration Protocols

**Status: PLANNED (future work).** Corresponds to [ROADMAP Phase 11](../../ROADMAP.md). It has not started and this directory contains no experiments. Nothing here implies mastery.

**Track:** B — Applied AI Automation & Agentic Systems

## Purpose

Understand the Model Context Protocol as a way to expose tools and context to AI clients, and its security boundaries.

## Why it matters

MCP standardizes tool exposure but does not provide an agent loop or a permission policy. Seeing it after the primitives makes those limits clear.

## Prerequisites

- Phase 10 — Agentic Systems Fundamentals (tools, permissions)

## Core concepts

- MCP architecture and the client/server model
- Tools, resources and prompts
- Transports
- Tool discovery
- Permissions and security boundaries
- Local MCP servers

## Small future Lab experiments

Ideas only; no experiment directory or code exists yet.

- Minimal local MCP server exposing 1–2 safe tools
- MCP client interaction
- Safe local tool exposure

Every applied experiment should state its baseline, what success means, the failure modes, how generalization is tested, whether AI beats deterministic logic, what happens when the model fails, and when a human intervenes.

## Relevant technologies

- Official open-source MCP SDKs (local use)
- Python

ZERO EXTRA COST: local models, open-source tools and free official resources only.

## Selected learning resources

None specific yet. Resources are registered once, with their links, in the Learning Cockpit catalog (`tools/learning_cockpit/catalog/catalog.json`) and summarized in the roadmap.

## Boundary

Small experiments belong here; large multi-technology systems belong in independent repositories.
