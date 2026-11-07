# LLM Engineering

This topic studies how modern language models work internally and how they later become part of complete AI systems.

The current focus is not on calling an LLM API.

The objective is to understand the internal pipeline of an autoregressive Transformer progressively and experimentally:

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
Transformer blocks
↓
language-model head
↓
vocabulary logits
↓
next-token prediction
↓
training
↓
generation
```

Each experiment isolates one mechanism before combining them into a small educational GPT-like model.

---


## Role of this README

Phase purpose, conceptual progression, experiment index and status. The theory, hypothesis, implementation, actual run, interpretation and limitations of each experiment live in that experiment's own README; they are not repeated here. The ordered route and milestones are in [ROADMAP](../../ROADMAP.md#phase-04--transformer-and-llm-fundamentals).

## Topic Map

```text
✅ Tokenization → token IDs → token embeddings + positional information
    → ✅ Attention: Q / K / V → causal masking → multiple heads
    → ✅ Projection / residuals / LayerNorm / FFN → Transformer stack
    → ✅ LM Head / logits → Softmax → next-token loss → training
    → ⬜ Autoregressive generation + sampling [Experiment 30: NEXT]
    → ⬜ Local inference → structured interfaces / tool calling → agents
```

**Phase 04 remains IN PROGRESS.** Experiments 13–29 are complete; Experiment 30 is next, not completed. The token embeddings studied here are internal model representations. Retrieval embedding models for semantic search are a separate planned branch.

PyTorch supports the current mechanism-level experiments. Local runtimes and later MCP / LangChain / LangGraph / n8n study are tools and interfaces, not substitutes for these fundamentals. See the [field map](../../docs/ai-engineering-map.md#nlp-and-llm-fundamentals) and [selected route](../../ROADMAP.md#route-after-phase-04).

## Experiment index

"Experiment NN" is the global number across the whole Lab; the folder name is the local sequence inside this topic (see [Experiment numbering](../../docs/learning-method.md#experiment-numbering)).

| Experiment | Title | Folder | Status | New idea |
|---|---|---|---|---|
| 13 | [Tokenization](01_tokenization/README.md) | `01_tokenization` | COMPLETE | token ≠ token ID |
| 14 | [Token Embeddings](02_embeddings/README.md) | `02_embeddings` | COMPLETE | embedding table lookup, `[8] → [8, 4]` |
| 15 | [Positional Embeddings](03_positional_embeddings/README.md) | `03_positional_embeddings` | COMPLETE | token = WHAT, position = WHERE |
| 16 | [Self-Attention](04_self_attention/README.md) | `04_self_attention` | COMPLETE | Q, K, V, attention weights |
| 17 | [Causal Self-Attention](05_causal_attention/README.md) | `05_causal_attention` | COMPLETE | causal mask |
| 18 | [Multi-Head Attention](06_multi_head_attention/README.md) | `06_multi_head_attention` | COMPLETE | parallel attention spaces |
| 19 | [Attention Output Projection and Residual](07_attention_output_residual/README.md) | `07_attention_output_residual` | COMPLETE | output projection, residual path |
| 20 | [Layer Normalization](08_layer_normalization/README.md) | `08_layer_normalization` | COMPLETE | per-token normalization |
| 21 | [Feed-Forward Network](09_feed_forward_network/README.md) | `09_feed_forward_network` | COMPLETE | position-wise expansion and projection |
| 22 | [FFN Residual and Complete Transformer Block](10_transformer_block/README.md) | `10_transformer_block` | COMPLETE | the full block |
| 23 | [Stacked Transformer Blocks](11_stacked_transformer_blocks/README.md) | `11_stacked_transformer_blocks` | COMPLETE | depth |
| 24 | [Language-Model Head and Vocabulary Logits](12_lm_head_logits/README.md) | `12_lm_head_logits` | COMPLETE | hidden states → vocabulary logits |
| 25 | [Softmax and Next-Token Probabilities](13_softmax_probabilities/README.md) | `13_softmax_probabilities` | COMPLETE | logits → probabilities |
| 26 | [Shifted Targets and CrossEntropyLoss](14_shifted_targets_cross_entropy/README.md) | `14_shifted_targets_cross_entropy` | COMPLETE | next-token loss |
| 27 | [Backpropagation and Gradients](15_backpropagation_gradients/README.md) | `15_backpropagation_gradients` | COMPLETE | gradients per parameter |
| 28 | [Optimizer Update](16_optimizer_update/README.md) | `16_optimizer_update` | COMPLETE | `optimizer.step()` changes parameters |
| 29 | [Language-Model Training Loop](17_training_loop/README.md) | `17_training_loop` | COMPLETE | repeated training; a tiny trained LM |
| 30 | Autoregressive Generation and Sampling | _(not created yet)_ | **NEXT** | training vs inference |

## Conceptual progression

```text
TEXT → TOKENS → TOKEN IDs
  → TOKEN EMBEDDINGS + POSITION INFORMATION
  → Q / K / V → CAUSAL SELF-ATTENTION → MULTIPLE HEADS
  → projection + residual → LayerNorm → FFN → TRANSFORMER BLOCK → STACK
  → LM HEAD → VOCABULARY LOGITS → SOFTMAX → NEXT-TOKEN PROBABILITIES
  → SHIFTED TARGETS + CrossEntropyLoss → BACKPROPAGATION → OPTIMIZER UPDATE
  → TRAINING LOOP → (next) AUTOREGRESSIVE GENERATION
```

## Key synthesis

Distinctions this phase has established:

```text
token ≠ token ID ≠ embedding
token embedding (WHAT) ≠ position embedding (WHERE)
attention ≠ next-token prediction
single-head attention ≠ multi-head attention
training (parameters change) ≠ inference / generation (parameters fixed)
```

## Important limitations

The implementation is educational. Experiments through 29 include complete Transformer blocks, a language-model head, next-token loss and a tiny training loop; their recorded results demonstrate mechanics and memorization, not general language understanding.

Remaining future work: linguistically meaningful attention patterns, dropout, autoregressive generation and sampling, KV caching, modern positional methods such as RoPE.

## Long-term goal

Understand and build `text → tokenizer → token IDs → embeddings → causal Transformer → LM head → logits → probabilities → sampling → generated text` without treating the Transformer as a black box. Full learning path: [ROADMAP](../../ROADMAP.md).
