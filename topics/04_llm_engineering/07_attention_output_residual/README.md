# Experiment 19 — Attention Output Projection and Residual Connection

## Objective

What happens to the original token representation after multi-head attention?

Previous experiments produced a contextual representation through causal multi-head attention:

```text
input
↓
Q / K / V
↓
multiple attention heads
↓
concatenated head outputs
```

This experiment introduces two additional Transformer mechanisms:

```text
attention output projection
```

and:

```text
residual connection
```

The output projection mixes information produced by the different attention heads.

The residual connection then combines that contextual update with the original token representation.

---

## Starting Point

The experiment uses the sequence:

```text
hel
```

with:

```text
d_model = 8
num_heads = 2
head_dimension = 4
```

The original input representation has shape:

```text
[3, 8]
```

which means:

```text
3 tokens
×
8 dimensions per token
```

Each input representation already contains:

```text
token embedding
+
position embedding
```

---

## Multi-Head Attention

As in the previous experiment, the input is projected into:

```text
Q
K
V
```

and divided into two attention heads.

The verified Query shape after splitting was:

```text
[2, 3, 4]
```

which means:

```text
2 heads
×
3 tokens
×
4 dimensions per head
```

After causal attention, the head outputs also had shape:

```text
[2, 3, 4]
```

---

## Concatenating the Heads

The two attention-head outputs are recombined.

Conceptually, for each token:

```text
head 1 → [4]
head 2 → [4]

↓ concatenate

[8]
```

The verified concatenated tensor shape was:

```text
[3, 8]
```

The verified output was:

```text
tensor([
    [-0.3139, -1.2152,  0.7477,  0.0956,
     -0.4502,  0.8714,  0.7095,  0.4604],

    [ 0.1239, -1.2965, -0.3575, -0.3174,
     -0.3469,  0.2765,  0.0768, -0.0344],

    [-0.1050, -1.1471,  0.5030, -0.0736,
     -0.3417,  0.3960, -0.0511, -0.7938]
])
```

Concatenation restores the model dimension, but the head outputs are still placed next to each other.

---

## Attention Output Projection

The experiment introduces another trainable linear transformation:

```text
W_O
```

implemented as:

```python
output_projection = nn.Linear(
    d_model,
    d_model,
    bias=False
)
```

Its transformation is:

```text
concatenated attention output
[3, 8]

↓ W_O

projected attention output
[3, 8]
```

The shape does not change.

The purpose of the output projection is not dimensionality reduction.

Its purpose is to allow information from the concatenated attention heads to be mixed into a new representation.

Conceptually:

```text
Head 1 ─┐
        ├→ concatenate → W_O → mixed attention representation
Head 2 ─┘
```

The verified projected attention output was:

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

with shape:

```text
[3, 8]
```

---

## Residual Connection

The original input representation is not discarded.

Instead, the Transformer adds the attention update to the original representation:

```text
residual_output
=
x
+
attention_output
```

Conceptually:

```text
                    ┌──────────────────────┐
                    │                      │
X ──────────────────┼──────────────────────┐
│                   │                      │
↓                   │                      │
Multi-Head Attention                       │
↓                                          │
Output Projection                          │
│                                          │
└──────────────────────→ + ←───────────────┘
                          │
                          ↓
                   residual output
```

The original input and attention output both have shape:

```text
[3, 8]
```

so element-wise addition is possible.

The residual output also has shape:

```text
[3, 8]
```

---

## Verified Residual Output

The experiment produced:

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

with:

```text
Residual output shape:
[3, 8]
```

---

## Inspecting Token `e`

The original representation of token `"e"` was:

```text
[-0.6407, -1.3528, -1.2728,  2.3213,
 -1.4034, -1.2523,  1.6404, -0.2911]
```

Its projected attention update was:

```text
[-0.2008, -0.6260,  0.6287, -0.3382,
  0.3994,  0.0943,  0.2847, -0.5112]
```

The residual representation became:

```text
[-0.8415, -1.9788, -0.6441,  1.9831,
 -1.0040, -1.1580,  1.9251, -0.8022]
```

For example:

```text
-0.6407 + (-0.2008)
≈
-0.8415
```

and:

```text
-1.2728 + 0.6287
≈
-0.6441
```

Therefore:

```text
original representation
+
attention update
=
residual representation
```

was verified explicitly.

The experiment produced:

```text
MANUAL RESIDUAL MATCH:
True
```

---

## Interpretation

Before attention, a token representation contains its current information.

At this stage of the experiments, that begins with:

```text
token information
+
position information
```

Multi-head causal attention then creates a contextual update using information available from the token and its permitted previous context.

The residual connection combines both:

```text
previous representation
+
new contextual transformation
=
updated representation
```

A useful mental model is:

```text
new state
=
previous state
+
learned update
```

This does not mean that the attention transformation is necessarily numerically small.

It means that the previous representation has a direct path into the output.

---

## Why Residual Connections Matter

Transformer models contain many successive blocks.

Without residual connections, each transformation would have to completely replace the previous representation.

Residual connections instead provide a direct path:

```text
X
│
├───────────────┐
│               │
↓               │
transformation  │
│               │
└──────→ + ←────┘
         │
         ↓
       output
```

This helps preserve information across deep networks.

Residual connections also provide important optimization benefits because they create direct computational paths through which gradients can propagate.

---

## Shape Requirement

Residual addition requires compatible shapes.

In this experiment:

```text
original X:
[3, 8]

projected attention:
[3, 8]
```

Therefore:

```text
X + projected_attention
```

produces:

```text
[3, 8]
```

This is one reason Transformer sublayers preserve the model dimension.

---

## Hypothesis

If multi-head attention is followed by an output projection and residual connection:

1. the concatenated attention result should remain compatible with `d_model`,
2. the output projection should preserve shape `[sequence_length, d_model]`,
3. the original input and projected attention result should be addable element by element,
4. the residual output should retain the same shape,
5. manual addition should match the computed residual output.

---

## Implementation

The experiment:

1. encodes the sequence `hel`,
2. creates token and positional embeddings,
3. computes Q, K and V,
4. splits them into two attention heads,
5. performs causal multi-head attention,
6. concatenates the head outputs,
7. applies a trainable output projection,
8. adds the original input through a residual connection,
9. inspects token `"e"` manually,
10. verifies the residual addition numerically.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/07_attention_output_residual/main.py
```

---

## Verified Shape Progression

```text
Original input:
[3, 8]

Q after splitting:
[2, 3, 4]

Head outputs:
[2, 3, 4]

Concatenated multi-head output:
[3, 8]

Projected attention output:
[3, 8]

Residual output:
[3, 8]
```

The model dimension remained eight throughout the external Transformer representation.

---

## Conclusion

The attention sublayer is now closer to the structure used inside a Transformer.

The progression is:

```text
X
↓
multi-head causal attention
↓
concatenate heads
↓
output projection W_O
↓
attention update
```

while a direct residual path preserves the original representation:

```text
X
│
├────────────────────┐
│                    │
↓                    │
attention + W_O      │
│                    │
└────────→ + ←───────┘
            │
            ↓
       updated X
```

This introduces an important Transformer principle:

```text
representation
+
learned transformation
=
updated representation
```

---

## Limitations

This experiment still does not include:

- layer normalization,
- feed-forward networks,
- dropout,
- a complete Transformer block,
- stacked Transformer blocks,
- model training,
- language-model head,
- vocabulary logits,
- next-token loss,
- text generation.

All trainable matrices are still randomly initialized.

The numerical values therefore should not be interpreted as learned linguistic knowledge.

---

## Product Connection

Residual connections are not specific to language models.

They are a general deep-learning technique that makes deep neural architectures easier to optimize and allows information to move through many transformations.

In Transformers they help representations survive and evolve through many stacked blocks.

A large language model can contain many Transformer layers, so preserving stable information paths is fundamental.

---

## Check Yourself

### What does `W_O` do?

It applies a trainable transformation to the concatenated attention-head outputs and allows information from the heads to be mixed.

### Does `W_O` change `d_model` in this experiment?

No.

It maps:

```text
8
→
8
```

for every token.

### What is a residual connection?

A direct connection that adds a sublayer input to its transformed output.

### What equation represents this experiment?

```text
residual_output
=
x
+
attention_output
```

where `attention_output` is the projected multi-head attention result.

### Why must both tensors have compatible shapes?

Residual addition is element-wise.

In this experiment both are:

```text
[3, 8]
```

### Does the residual connection mean attention information replaces the original representation?

No.

The original representation remains directly present through the addition.

### What does the residual representation of `e` contain conceptually?

Its previous representation plus the contextual transformation produced by the attention sublayer.

### Are the current values meaningful language representations?

Not yet.

The model has not been trained.

### What comes next?

Layer normalization.

The next experiment will study how a Transformer controls the scale and distribution of the evolving token representations.