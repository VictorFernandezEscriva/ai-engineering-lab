# Experiment 22 — Complete Transformer Block

## Objective

How do the individual Transformer mechanisms studied so far fit together into one reusable block?

Previous experiments implemented the components independently:

```text
token embeddings
positional embeddings
self-attention
causal masking
multi-head attention
attention output projection
residual connection
LayerNorm
feed-forward network
```

This experiment combines the attention and feed-forward sublayers into one `TransformerBlock`.

The resulting block contains:

```text
causal multi-head attention
↓
attention output projection
↓
residual connection
↓
LayerNorm
↓
feed-forward network
↓
residual connection
↓
LayerNorm
```

---

## Architecture

The educational Transformer block implemented in this experiment follows:

```text
INPUT X
[sequence, d_model]
        │
        │
        ├──────────────────────────┐
        ↓                          │
Q / K / V                          │
        ↓                          │
Multi-Head Causal Attention        │
        ↓                          │
Concatenate Heads                  │
        ↓                          │
Output Projection W_O              │
        │                          │
        └────────────→ + ←─────────┘
                        │
                        ↓
                    LayerNorm 1
                        │
                        │
                        ├───────────────┐
                        ↓               │
                 Feed-Forward           │
                 8 → 32 → 8             │
                        │               │
                        └──────→ + ←────┘
                                 │
                                 ↓
                             LayerNorm 2
                                 │
                                 ↓
                     TRANSFORMER BLOCK OUTPUT
                           [sequence, d_model]
```

---

## Model Dimensions

The experiment uses:

```text
text = "hel"

sequence_length = 3
d_model = 8
num_heads = 2
head_dimension = 4
ffn_hidden_dimension = 32
```

Therefore:

```text
input shape = [3, 8]
```

---

## TransformerBlock Class

The mechanisms are now packaged inside:

```python
class TransformerBlock(nn.Module):
```

This is an important software-engineering step.

Instead of manually reconstructing the Transformer operations every time, the entire transformation can now be used as:

```python
block = TransformerBlock(...)

output = block(x)
```

Conceptually:

```text
x
↓
TransformerBlock
↓
x'
```

This will make it possible to stack multiple Transformer blocks in later experiments.

---

## First Sublayer — Causal Multi-Head Attention

The first sublayer creates:

```text
Q
K
V
```

from the input representation.

The projected dimensions are divided into multiple attention heads:

```text
d_model = 8
num_heads = 2

8 / 2 = 4 dimensions per head
```

Each head performs causal self-attention independently.

The causal mask prevents every position from attending to future positions.

After attention:

```text
2 heads
×
3 tokens
×
4 dimensions
```

are concatenated back into:

```text
[3, 8]
```

The attention output projection `W_O` then mixes information from the concatenated heads.

---

## First Residual Connection

The projected attention result is added to the original block input:

```text
attention_residual
=
x
+
attention_output
```

The verified attention output was:

```text
tensor([
    [-0.3481, -0.6149,  0.4784, -0.2926,
      0.3698, -0.3263, -0.0446, -0.4765],

    [-0.2008, -0.6260,  0.6287, -0.3382,
      0.3994,  0.0943,  0.2847, -0.5112],

    [-0.3508, -0.7050,  0.3541, -0.0907,
     -0.1180, -0.1696,  0.0480, -0.4124]
])
```

The verified first residual was:

```text
tensor([
    [-1.8948,  0.0420, -1.7421, -1.4791,
     -0.3681,  2.3211, -0.1381, -0.9128],

    [-0.8415, -1.9788, -0.6441,  1.9831,
     -1.0040, -1.1580,  1.9251, -0.8022],

    [-4.2636, -0.1810,  1.0752,  0.6135,
      0.4249,  2.2582, -0.0696,  0.5210]
])
```

Its shape remained:

```text
[3, 8]
```

---

## First LayerNorm

The attention residual is normalized:

```text
attention residual
↓
LayerNorm 1
↓
normalized attention representation
```

The verified representation was:

```text
tensor([
    [-1.0767,  0.4418, -0.9570, -0.7508,
      0.1202,  2.2287,  0.3006, -0.3068],

    [-0.3861, -1.2201, -0.2413,  1.6853,
     -0.5052, -0.6181,  1.6428, -0.3573],

    [-2.4250, -0.1284,  0.5782,  0.3185,
      0.2124,  1.2437, -0.0658,  0.2664]
])
```

---

## Second Sublayer — Feed-Forward Network

Each token representation is then processed independently by the same feed-forward network:

```text
8
↓
Linear
↓
32
↓
GELU
↓
Linear
↓
8
```

The verified FFN output was:

```text
tensor([
    [-0.1454,  0.2242,  0.1646,  0.2101,
     -0.2161, -0.0708, -0.0017,  0.0327],

    [-0.0364, -0.0573,  0.2052, -0.0648,
      0.1669, -0.0386,  0.2517,  0.3623],

    [ 0.3371,  0.2754,  0.2053,  0.0024,
     -0.3922,  0.1128, -0.1175,  0.0453]
])
```

Its shape was:

```text
[3, 8]
```

---

## Second Residual Connection

The FFN output is not used as a replacement for its input.

Instead:

```text
ffn_residual
=
normalized_attention
+
ffn_output
```

For token `"e"`:

```text
normalized representation:

[-0.3861, -1.2201, -0.2413,  1.6853,
 -0.5052, -0.6181,  1.6428, -0.3573]
```

The FFN produced:

```text
[-0.0364, -0.0573,  0.2052, -0.0648,
  0.1669, -0.0386,  0.2517,  0.3623]
```

Adding them produced:

```text
[-0.4224, -1.2774, -0.0361,  1.6205,
 -0.3383, -0.6567,  1.8945,  0.0050]
```

For example:

```text
-0.3861 + (-0.0364)
≈
-0.4224
```

and:

```text
-0.2413 + 0.2052
≈
-0.0361
```

The experiment verified:

```text
SECOND RESIDUAL MANUAL MATCH:
True
```

---

## Second LayerNorm

The second residual representation is normalized again:

```text
FFN residual
↓
LayerNorm 2
↓
Transformer block output
```

The final block output was:

```text
tensor([
    [-1.2723,  0.6544, -0.8338, -0.5770,
     -0.1231,  2.1768,  0.2798, -0.3049],

    [-0.5057, -1.3353, -0.1308,  1.4769,
     -0.4240, -0.7330,  1.7428, -0.0908],

    [-2.2827,  0.0940,  0.7709,  0.2790,
     -0.2535,  1.3803, -0.2572,  0.2692]
])
```

The final shape remained:

```text
[3, 8]
```

---

## Final Token Statistics

For token `"e"` the final representation was:

```text
[-0.5057, -1.3353, -0.1308,  1.4769,
 -0.4240, -0.7330,  1.7428, -0.0908]
```

The measured statistics were:

```text
Mean:
-1.210719347000122e-08

Variance:
0.9999904632568359
```

Therefore:

```text
mean ≈ 0
variance ≈ 1
```

as expected from the final LayerNorm with its initial parameters.

---

## Verified Shape Progression

The entire block preserved the external representation shape:

```text
Input
[3, 8]

↓ attention

Attention Output
[3, 8]

↓ residual

First Residual
[3, 8]

↓ LayerNorm

Normalized Attention
[3, 8]

↓ FFN

FFN Output
[3, 8]

↓ residual

Second Residual
[3, 8]

↓ LayerNorm

Transformer Block Output
[3, 8]
```

This shape preservation is essential because Transformer blocks can be stacked.

---

## Two Residual Paths

The block contains two major transformations:

```text
1. Attention
2. Feed-Forward Network
```

Each receives its own residual path.

### Attention residual

```text
x
+
attention(x)
```

### FFN residual

```text
x1
+
FFN(x1)
```

A useful mental model is:

```text
current representation
+
learned update
=
new representation
```

The model repeatedly refines representations rather than completely replacing them at every sublayer.

---

## Attention and FFN Responsibilities

The block combines two different forms of computation.

### Attention

```text
communication between token positions
```

A token can incorporate information from other allowed tokens.

### Feed-Forward Network

```text
nonlinear transformation within each position
```

Each contextual token representation is processed independently using shared FFN parameters.

Together:

```text
context exchange
↓
attention

local nonlinear processing
↓
FFN
```

---

## Post-Norm Organization

The educational block currently follows:

```text
Attention
↓
Residual
↓
LayerNorm
↓
FFN
↓
Residual
↓
LayerNorm
```

This is a post-normalization organization.

Many modern decoder-only Transformer architectures use pre-normalization variants instead.

For example:

```text
LayerNorm
↓
Attention
↓
Residual
↓
LayerNorm
↓
FFN
↓
Residual
```

The current implementation intentionally uses the post-norm structure because it makes the role of every mechanism explicit while learning the architecture.

Pre-norm and modern variants will be studied separately.

---

## Hypothesis

A complete educational Transformer block should:

1. perform causal multi-head self-attention,
2. project and mix the attention heads,
3. preserve the original representation through a residual connection,
4. normalize the resulting representation,
5. apply a position-wise nonlinear FFN,
6. preserve the FFN input through a second residual connection,
7. normalize again,
8. preserve the external `[sequence_length, d_model]` shape.

---

## Implementation

The experiment:

1. creates token and positional embeddings,
2. packages Transformer operations inside `TransformerBlock`,
3. computes Q, K and V,
4. performs causal multi-head attention,
5. concatenates the attention heads,
6. applies `W_O`,
7. applies the first residual connection,
8. applies the first LayerNorm,
9. applies the FFN,
10. applies the second residual connection,
11. applies the second LayerNorm,
12. inspects token `"e"`,
13. verifies the second residual manually,
14. verifies the final normalization statistics.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/10_transformer_block/main.py
```

---

## Interpretation

The experiments have progressed from isolated operations to a reusable computational block.

Previously:

```text
attention
LayerNorm
FFN
residuals
```

were studied separately.

Now:

```text
TransformerBlock(x)
```

performs the complete transformation.

The block receives contextual representations and produces new contextual representations of exactly the same dimensionality.

Because the shape is preserved, another Transformer block can receive the result directly.

---

## Conclusion

A single Transformer block can now be represented as:

```text
X
↓
Causal Multi-Head Attention
↓
Output Projection
↓
Residual
↓
LayerNorm
↓
Feed-Forward Network
↓
Residual
↓
LayerNorm
↓
X'
```

The experiment verified both residual connections, both normalization stages, and the preservation of:

```text
[sequence_length, d_model]
```

through the complete block.

The next step is to stack multiple blocks so representations can be refined through several Transformer layers.

---

## Limitations

The current implementation still does not include:

- batching,
- dropout,
- pre-norm organization,
- multiple stacked Transformer blocks,
- a language-model head,
- vocabulary logits,
- next-token targets,
- cross-entropy loss,
- model training,
- text generation.

All parameters remain randomly initialized.

The block therefore demonstrates Transformer architecture rather than learned language behavior.

---

## Product Connection

Real language models consist of many Transformer blocks stacked on top of one another.

Each block repeatedly performs:

```text
contextual communication
+
nonlinear processing
```

while residual paths preserve information across depth.

The reusable `TransformerBlock` abstraction is therefore the fundamental building block that will later allow the educational model to grow from one layer into a complete decoder-only language model.

---

## Check Yourself

### What are the two main learned sublayers?

Causal multi-head attention and the feed-forward network.

### How many residual connections are used?

Two.

One around attention and one around the FFN.

### What is added in the first residual?

```text
original block input
+
projected attention output
```

### What is added in the second residual?

```text
normalized attention representation
+
FFN output
```

### Does the Transformer block change `d_model`?

No.

Its input and output both use:

```text
d_model = 8
```

### Why is preserving the shape useful?

Because Transformer blocks can be stacked directly.

### What does attention provide?

Communication and contextual information between allowed token positions.

### What does the FFN provide?

A nonlinear transformation applied independently to each token position.

### What organization does this educational block use?

Post-Norm.

### What comes next?

Stacking multiple Transformer blocks.