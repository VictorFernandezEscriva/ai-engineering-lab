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

## Learning Progression

### Experiment 13 — Character Tokenization and Token IDs

Folder:

```text
01_tokenization/
```

Status:

```text
COMPLETE
```

Studied:

```text
raw text
↓
character tokens
↓
vocabulary
↓
token IDs
```

Verified:

- vocabulary construction,
- token-to-ID mapping,
- ID-to-token mapping,
- encoding,
- decoding,
- PyTorch integer token tensors.

Key distinction:

```text
token
≠
token ID
```

A token ID is an identifier, not a numerical representation of meaning.

---

### Experiment 14 — Token Embeddings

Folder:

```text
02_embeddings/
```

Status:

```text
COMPLETE
```

Studied:

```text
token ID
↓
embedding-table lookup
↓
trainable vector
```

Verified configuration:

```text
vocabulary size = 10
embedding dimension = 4
```

Embedding table shape:

```text
[10, 4]
```

For the sequence:

```text
hello ai
```

eight token IDs became eight embedding vectors:

```text
[8]
↓
[8, 4]
```

Key distinction:

```text
token ID
=
lookup index

embedding
=
trainable vector representation
```

---

### Experiment 15 — Positional Embeddings

Folder:

```text
03_positional_embeddings/
```

Status:

```text
COMPLETE
```

Studied:

```text
token embedding
+
position embedding
=
position-aware representation
```

Verified that repeated tokens initially receive identical token embeddings.

For repeated `"l"` tokens, the token embeddings match because both use the same token ID.

After adding different positional embeddings:

```text
same token
+
different position
=
different combined representation
```

Key mental model:

```text
token embedding
→ WHAT token is this?

position embedding
→ WHERE is this token?
```

---

### Experiment 16 — Self-Attention

Folder:

```text
04_self_attention/
```

Status:

```text
COMPLETE
```

Implemented a single self-attention head manually.

Studied:

```text
input representation
↓
Q
K
V
```

Queries and Keys determine attention scores:

```text
Q @ Kᵀ
↓
scale
↓
softmax
↓
attention weights
```

Attention weights are then used to combine Value vectors:

```text
attention weights
@
V
↓
contextual representations
```

Key mental model:

```text
Q + K
→ determine where information should come from

V
→ contains the information being transferred
```

Self-attention allows each token representation to incorporate information from other tokens in the sequence.

---

### Experiment 17 — Causal Self-Attention

Folder:

```text
05_causal_attention/
```

Status:

```text
COMPLETE
```

Introduced causal masking for autoregressive language modelling.

Normal self-attention allows:

```text
h → h, e, l
e → h, e, l
l → h, e, l
```

Causal self-attention restricts this to:

```text
h → h
e → h, e
l → h, e, l
```

Future attention scores are replaced with:

```text
-inf
```

before softmax.

Therefore:

```text
future position
↓
-inf
↓
softmax
↓
attention weight = 0
```

Important distinction:

```text
ATTENTION
→ determines what information from the available context is used
```

while:

```text
LANGUAGE-MODEL HEAD
→ later produces scores for every token in the vocabulary
```

Attention itself does not choose the next token.

---

### Experiment 18 — Multi-Head Causal Self-Attention

Folder:

```text
06_multi_head_attention/
```

Status:

```text
COMPLETE
```

Extended causal self-attention to multiple attention heads.

Verified configuration:

```text
d_model = 8
num_heads = 2
head_dimension = 4
```

The eight model dimensions were divided between two heads:

```text
8 dimensions
↓
2 heads
↓
4 dimensions per head
```

Verified tensor progression:

```text
input
[3, 8]

↓ Q / K / V

[3, 8]

↓ reshape

[3, 2, 4]

↓ transpose

[2, 3, 4]

↓ causal attention

attention weights
[2, 3, 3]

↓ weighted Values

head outputs
[2, 3, 4]

↓ concatenate heads

[3, 8]
```

The two heads produced different attention distributions over the same sequence.

For token `"l"`:

```text
Head 1:

80.50% → h
10.11% → e
 9.39% → l
```

while:

```text
Head 2:

12.46% → h
38.16% → e
49.37% → l
```

The current patterns are not linguistically meaningful because the model has not been trained.

The experiment demonstrates that multiple heads provide multiple attention spaces in parallel.

---

## Current Position

We are currently here:

```text
LLM Engineering
│
├── Tokenization ✅
├── Token IDs ✅
├── Token Embeddings ✅
├── Positional Embeddings ✅
├── Self-Attention ✅
├── Causal Self-Attention ✅
├── Multi-Head Attention ✅
├── Attention Output Projection ✅
├── Residual Connection ✅
├── Layer Normalization ✅
│
└── Feed-Forward Network ← NEXT
```

---

## Experiment 19 — Attention Output Projection and Residual Connection

Folder:

```text
07_attention_output_residual/
```

Status:

```text
COMPLETE
```

Extended the multi-head attention mechanism with:

```text
concatenated heads
↓
output projection W_O
↓
attention update
```

followed by:

```text
original representation
+
attention update
=
residual representation
```

The residual path preserves direct access to the previous representation.

---

## Experiment 20 — Layer Normalization

Folder:

```text
08_layer_normalization/
```

Status:

```text
COMPLETE
```

Introduced LayerNorm over the feature dimension of each token.

Verified for token `"e"`:

```text
before:

mean     = -0.315053
variance =  1.859519
```

after normalization:

```text
mean     ≈ 0
variance ≈ 1
```

The tensor shape remained:

```text
[3, 8]
```

LayerNorm was also reproduced manually and matched PyTorch:

```text
MANUAL NORMALIZATION MATCH:
True
```

Verified initial learnable parameters:

```text
gamma = ones
beta  = zeros
```

Key mental model:

```text
each token
↓
normalize its own feature dimensions
↓
preserve the same tensor shape
```

---

## Next Steps

The next progression is:

```text
feed-forward network
↓
second residual connection
↓
Transformer block
↓
stacked Transformer blocks
↓
language-model head
↓
vocabulary logits
↓
CrossEntropyLoss
↓
next-token training
↓
sampling
↓
generated text
```

After these mechanisms are understood individually, they will be combined into a small educational GPT-like language model.

---

## Key Concepts Learned So Far

The current experiments establish the following pipeline:

```text
TEXT
↓
TOKENS
↓
TOKEN IDs
↓
TOKEN EMBEDDINGS
+
POSITION INFORMATION
↓
CONTEXT-AWARE INPUT REPRESENTATIONS
↓
Q / K / V
↓
CAUSAL SELF-ATTENTION
↓
MULTIPLE ATTENTION HEADS
↓
CONTEXTUAL TOKEN REPRESENTATIONS
```

Important distinctions include:

```text
token
≠
token ID
≠
embedding
```

```text
token embedding
≠
position embedding
```

```text
attention
≠
next-token prediction
```

```text
single-head attention
≠
multi-head attention
```

---

## Important Limitations

The current implementation is educational.

It does not yet include a complete Transformer block or language model.

The experiments currently do not include:

- trained attention patterns,
- attention output projection,
- residual connections,
- layer normalization,
- feed-forward networks,
- dropout,
- complete Transformer blocks,
- vocabulary logits,
- next-token loss,
- autoregressive training,
- text generation,
- KV caching,
- modern positional methods such as RoPE.

These mechanisms will be introduced progressively.

---

## Long-Term Goal

The goal of this topic is to understand and build:

```text
text
↓
tokenizer
↓
token IDs
↓
embeddings
↓
causal Transformer
↓
language-model head
↓
vocabulary logits
↓
next-token probability distribution
↓
sampling
↓
generated text
```

without treating the Transformer as a black box.

See the complete learning path in:

```text
../../ROADMAP.md
```