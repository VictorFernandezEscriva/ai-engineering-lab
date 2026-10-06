# Experiment 21 — Feed-Forward Network

## Objective

What does the feed-forward network do inside a Transformer, and how is it different from attention?

Attention allows tokens to exchange information.

The feed-forward network performs a nonlinear transformation independently on each token representation.

This experiment implements a Transformer-style feed-forward network and verifies that the same network is applied separately to every token position.

---

## Starting Point

The experiment uses:

```text
hel
```

with:

```text
d_model = 8
num_heads = 2
head_dimension = 4
ffn_hidden_dimension = 32
```

The feed-forward hidden dimension is:

```text
4 × d_model

4 × 8 = 32
```

This is an educational Transformer-style configuration.

---

## Feed-Forward Architecture

The network is:

```text
8
↓
Linear
↓
32
↓
GELU
↓
32
↓
Linear
↓
8
```

For each token:

```text
token representation
[8]

↓ Linear(8, 32)

expanded representation
[32]

↓ GELU

nonlinear representation
[32]

↓ Linear(32, 8)

FFN output
[8]
```

---

## Why Expand the Representation?

The first linear layer maps:

```text
d_model
↓
ffn_hidden_dimension
```

In this experiment:

```text
8
↓
32
```

The larger intermediate representation gives the network additional capacity to transform the token representation.

The second linear layer returns to:

```text
d_model = 8
```

so the output remains compatible with the rest of the Transformer block.

---

## Why Use GELU?

Without a nonlinear activation:

```text
Linear
↓
Linear
```

would still represent a linear transformation.

Adding GELU gives the network nonlinear transformation capacity:

```text
Linear
↓
GELU
↓
Linear
```

This allows the FFN to represent more complex functions.

---

## Shared Parameters

The Transformer does not create a different FFN for every token.

There is one shared network:

```text
W1
b1
GELU
W2
b2
```

and the same parameters are applied to every token position:

```text
h → FFN → h'

e → FFN → e'

l → FFN → l'
```

The function is shared.

The inputs are different.

Therefore the outputs can also be different.

---

## Shared Parameters Do Not Mean Token Interaction

For each token:

```text
output_h = FFN(input_h)

output_e = FFN(input_e)

output_l = FFN(input_l)
```

The FFN does not calculate:

```text
FFN(h, e, l)
```

Changing the input representation of one token therefore does not directly change the FFN output of another token during the same forward pass.

Token interaction happened earlier through attention.

---

## Attention vs Feed-Forward Network

A useful distinction is:

```text
ATTENTION
→ communication between token positions
```

while:

```text
FEED-FORWARD NETWORK
→ computation within each token position
```

Attention can construct a contextual representation:

```text
h ─┐
   ├→ contextual e
e ─┘
```

The FFN then processes that contextual representation:

```text
contextual e
↓
FFN
↓
transformed e
```

Therefore the FFN processes one token at a time, but its input may already contain information collected from other tokens through attention.

---

## Training and Shared Weights

Although token positions are processed independently during the FFN forward pass, they train the same parameters.

Conceptually:

```text
loss from h ─┐
             │
loss from e ─┼→ gradients for shared FFN parameters
             │
loss from l ─┘
```

Backpropagation accumulates contributions from the token positions that use the shared parameters.

After an optimizer update, the same updated FFN is used again for every token.

Therefore:

```text
shared training
≠
direct token interaction
```

---

## Verified Tensor Shapes

The input to the FFN had shape:

```text
[3, 8]
```

After the first linear layer:

```text
[3, 32]
```

After GELU:

```text
[3, 32]
```

After the second linear layer:

```text
[3, 8]
```

Therefore:

```text
[3, 8]
↓
[3, 32]
↓
[3, 32]
↓
[3, 8]
```

The sequence length remained unchanged.

---

## Inspecting Token `e`

The input representation was:

```text
[-0.3861, -1.2201, -0.2413,  1.6853,
 -0.5052, -0.6181,  1.6428, -0.3573]
```

The first linear layer expanded it to:

```text
32 features
```

The expanded representation was:

```text
[-6.7833e-01, -3.2342e-01,  6.6249e-01,  1.7566e-01,
 -1.8935e-01,  7.9309e-01, -2.5992e-01, -1.7963e-01,
 -1.3833e+00,  4.5063e-01, -4.8613e-01, -2.7718e-01,
 -8.6998e-02, -2.3044e-01, -7.0804e-01,  2.4254e-01,
  8.3669e-02, -4.7272e-01,  1.3054e+00, -1.9412e-01,
 -4.9298e-04, -3.2683e-01, -3.1025e-01, -5.9474e-01,
  4.0252e-01, -2.2563e-02,  4.9333e-01,  6.8501e-01,
  5.8700e-01, -1.6072e-01,  9.1560e-01,  3.1289e-02]
```

After GELU:

```text
[-1.6876e-01, -1.2070e-01,  4.9433e-01,  1.0008e-01,
 -8.0456e-02,  6.2348e-01, -1.0331e-01, -7.7011e-02,
 -1.1521e-01,  3.0366e-01, -1.5237e-01, -1.0833e-01,
 -4.0483e-02, -9.4222e-02, -1.6955e-01,  1.4451e-01,
  4.4624e-02, -1.5042e-01,  1.1802e+00, -8.2119e-02,
 -2.4639e-04, -1.2155e-01, -1.1733e-01, -1.6415e-01,
  2.6419e-01, -1.1078e-02,  3.3996e-01,  5.1604e-01,
  4.2346e-01, -7.0098e-02,  7.5085e-01,  1.6035e-02]
```

The final FFN representation returned to eight dimensions:

```text
[-0.0364, -0.0573, 0.2052, -0.0648,
  0.1669, -0.0386, 0.2517, 0.3623]
```

---

## Processing One Token Independently

The experiment processed token `"e"` in two ways.

First as part of:

```text
[h, e, l]
```

and then separately:

```text
[e]
```

The result was:

```text
PROCESSING TOKEN ALONE MATCHES BATCHED RESULT:
True
```

This verifies that the FFN applies the same transformation independently to each token position.

---

## Modifying One Token

The experiment then changed only the representation of token `"h"`.

The result was:

```text
h output unchanged: False
e output unchanged: True
l output unchanged: True
```

Changing `"h"` changed the FFN output for `"h"`.

It did not change the FFN outputs for `"e"` or `"l"`.

This provides direct evidence that the FFN does not mix information between token positions.

---

## Hypothesis

A Transformer feed-forward network should:

1. use the same parameters for every token position,
2. process each token independently,
3. expand the feature dimension,
4. apply a nonlinear activation,
5. return to `d_model`,
6. preserve sequence length.

---

## Implementation

The experiment:

1. creates contextual normalized token representations,
2. defines `Linear(8, 32)`,
3. applies GELU,
4. defines `Linear(32, 8)`,
5. inspects token `"e"`,
6. processes `"e"` separately,
7. compares it with batched processing,
8. changes only `"h"`,
9. verifies that `"e"` and `"l"` remain unchanged.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/09_feed_forward_network/main.py
```

---

## Interpretation

The Transformer now contains two fundamentally different operations:

```text
ATTENTION
↓
exchange information between tokens
```

and:

```text
FFN
↓
transform each token independently
```

A useful conceptual model is:

```text
communication
↓
attention

computation
↓
feed-forward network
```

This is only an intuition, but it clearly separates the responsibilities of the two mechanisms.

---

## Conclusion

The feed-forward network transforms each contextual token representation independently.

Its shape progression is:

```text
[8]
↓
[32]
↓
GELU
↓
[32]
↓
[8]
```

The same parameters are reused for every token position.

During training, gradients from multiple positions contribute to those shared parameters.

During a forward pass, however, the FFN does not directly exchange information between token positions.

---

## Limitations

The experiment still does not include:

- the FFN residual connection,
- normalization around the complete FFN sublayer,
- a complete Transformer block,
- dropout,
- stacked Transformer blocks,
- language-model head,
- vocabulary logits,
- next-token training,
- generation.

The FFN parameters are randomly initialized and have not yet learned meaningful transformations.

---

## Product Connection

The feed-forward network is a major computational component of Transformer models.

Attention allows contextual information to move between token positions.

The FFN then provides substantial nonlinear processing capacity at each position.

Modern Transformer architectures may use different activation functions and gated variants such as SwiGLU, but the principle of a position-wise nonlinear transformation remains fundamental.

---

## Check Yourself

### Does the FFN mix tokens?

No.

Each token is processed independently.

### Do tokens use different FFN weights?

No.

The same parameters are shared across all token positions.

### Why can the outputs still differ?

Because each token provides a different input to the same function.

### Can all tokens contribute to training the FFN?

Yes.

Loss gradients from positions using the shared FFN contribute to the same parameters.

### Does that mean tokens interact during the FFN forward pass?

No.

Shared parameter training and token interaction are different concepts.

### What mixes information between tokens?

Self-attention.

### What is the shape progression in this experiment?

```text
[3, 8]
↓
[3, 32]
↓
[3, 32]
↓
[3, 8]
```

### Why does the FFN return to `d_model`?

So its output remains compatible with the Transformer representation and the next residual connection.

### What comes next?

The second residual connection and normalization step, completing the structure needed to assemble a full Transformer block.