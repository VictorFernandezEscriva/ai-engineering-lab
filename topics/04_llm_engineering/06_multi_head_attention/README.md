# Experiment 18 — Multi-Head Causal Self-Attention

## Objective

Why do Transformers use multiple attention heads instead of a single self-attention operation?

Previous experiments implemented:

```text
token representations
↓
Q, K, V
↓
causal self-attention
↓
contextual representations
```

A single attention head produces one attention pattern.

Multi-head attention allows several attention mechanisms to operate in parallel over different parts of the model representation.

This experiment implements two causal attention heads and verifies how tensor dimensions are split and later recombined.

---

## Concepts

### Model Dimension

The experiment uses:

```text
d_model = 8
```

This means that every token representation contains eight values.

For the sequence:

```text
hel
```

there are three tokens.

Therefore the input tensor has shape:

```text
[3, 8]
```

which means:

```text
3 tokens
×
8 dimensions per token
```

---

### Number of Heads

The experiment uses:

```text
num_heads = 2
```

The model dimension must be divisible by the number of heads:

```text
8 / 2 = 4
```

Therefore:

```text
head_dimension = 4
```

Each head operates on four dimensions.

Conceptually:

```text
token representation
[8]

↓ split

head 1 → [4]
head 2 → [4]
```

The model does not create sixteen dimensions.

The existing eight dimensions are divided between the two heads.

---

## Q, K and V Before Splitting

The input is projected into:

```text
Q
K
V
```

Each initially has shape:

```text
[3, 8]
```

The verified shapes were:

```text
Q: [3, 8]
K: [3, 8]
V: [3, 8]
```

This still means:

```text
3 tokens
×
8 dimensions
```

---

## Splitting Into Heads

The tensors are reshaped from:

```text
[3, 8]
```

to:

```text
[3, 2, 4]
```

which means:

```text
3 tokens
×
2 heads
×
4 dimensions per head
```

The values are not removed or duplicated.

Only their organization changes.

The experiment then transposes the tensor:

```text
[3, 2, 4]
↓
[2, 3, 4]
```

This makes the head dimension first:

```text
2 heads
×
3 tokens
×
4 dimensions
```

Conceptually:

```text
HEAD 1
├── h → [4 values]
├── e → [4 values]
└── l → [4 values]

HEAD 2
├── h → [4 values]
├── e → [4 values]
└── l → [4 values]
```

---

## Independent Attention Heads

Each head performs the same causal self-attention mechanism independently:

```text
Q @ Kᵀ
↓
scale
↓
causal mask
↓
softmax
↓
attention weights
↓
weights @ V
```

Because there are two heads and three tokens, the attention-weight tensor has shape:

```text
[2, 3, 3]
```

which means:

```text
2 heads
×
3 Query positions
×
3 Key positions
```

---

## Verified Attention Patterns

### Head 1

The verified causal attention weights were:

```text
tensor([
    [1.0000, 0.0000, 0.0000],
    [0.2019, 0.7981, 0.0000],
    [0.8050, 0.1011, 0.0939]
])
```

Interpretation:

```text
h:
100.00% → h

e:
20.19% → h
79.81% → e

l:
80.50% → h
10.11% → e
 9.39% → l
```

### Head 2

The verified weights were:

```text
tensor([
    [1.0000, 0.0000, 0.0000],
    [0.5276, 0.4724, 0.0000],
    [0.1246, 0.3816, 0.4937]
])
```

Interpretation:

```text
h:
100.00% → h

e:
52.76% → h
47.24% → e

l:
12.46% → h
38.16% → e
49.37% → l
```

---

## Why Multiple Heads Are Useful

The two heads process the same sequence but produce different attention distributions.

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

Therefore the two heads construct different contextual views of the same sequence.

This gives the model more representational flexibility than forcing all relationships through one attention distribution.

The model does not manually assign a specific linguistic role to each head.

Any useful specialization must emerge through training.

---

## Causal Behaviour

Both heads preserve causal masking.

For the first token:

```text
h → h
```

For the second:

```text
e → h, e
```

For the third:

```text
l → h, e, l
```

Future positions receive zero attention in every head.

---

## Attention Output Per Head

After:

```text
attention_weights @ values
```

the verified tensor shape was:

```text
[2, 3, 4]
```

which means:

```text
2 heads
×
3 tokens
×
4 output dimensions
```

Each head produces its own contextual representation.

---

## Concatenating Heads

The head output is first transposed:

```text
[2, 3, 4]
↓
[3, 2, 4]
```

and then reshaped:

```text
[3, 2, 4]
↓
[3, 8]
```

For one token:

```text
head 1 output → [4]
head 2 output → [4]
```

Concatenating them produces:

```text
[4] + [4]
↓
[8]
```

The final model dimension is therefore restored.

---

## Verified Shape Progression

The experiment verified:

```text
Input:
[3, 8]

Q / K / V:
[3, 8]

After reshape:
[3, 2, 4]

After transpose:
[2, 3, 4]

Attention scores:
[2, 3, 3]

Attention weights:
[2, 3, 3]

Head outputs:
[2, 3, 4]

After output transpose:
[3, 2, 4]

Final concatenated output:
[3, 8]
```

This is the central tensor-shape transformation of the experiment.

---

## Verified Final Output

The final concatenated multi-head representation was:

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

with:

```text
Multi-head output shape:
[3, 8]
```

---

## Why Scale by `sqrt(head_dimension)`?

Each attention head compares Query and Key vectors containing:

```text
4 dimensions
```

Therefore the attention scores are scaled by:

```text
sqrt(4)
```

rather than:

```text
sqrt(8)
```

The relevant dimension is the Query/Key dimension inside each attention head.

---

## Hypothesis

If the model representation is divided across multiple attention heads:

1. each head should perform causal attention independently,
2. different heads should be able to produce different attention distributions,
3. each head should operate on `d_model / num_heads` dimensions,
4. concatenating all heads should recover the original model dimension.

---

## Implementation

The experiment:

1. encodes the sequence `hel`,
2. creates 8-dimensional token representations,
3. generates Q, K and V,
4. reshapes each into two attention heads,
5. performs causal self-attention independently for both heads,
6. inspects their attention patterns,
7. computes one output per head,
8. concatenates the heads,
9. verifies that the final representation returns to dimension 8.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/06_multi_head_attention/main.py
```

---

## Interpretation

Single-head attention provides:

```text
one attention space
```

Multi-head attention provides:

```text
several attention spaces in parallel
```

Conceptually:

```text
                    ┌→ Head 1 → contextual view A
input representation
                    └→ Head 2 → contextual view B

                              ↓

                         concatenate

                              ↓

                  combined representation
```

Different heads can learn different relationships during training.

The current attention patterns are not yet meaningful linguistic patterns because the projections are randomly initialized.

---

## Conclusion

Multi-head attention extends the self-attention mechanism without changing its fundamental logic.

Each head still performs:

```text
Q + K
↓
attention weights

attention weights + V
↓
contextual information
```

The difference is that this process now happens multiple times in parallel.

For this experiment:

```text
d_model = 8

num_heads = 2

head_dimension = 4
```

Therefore:

```text
2 heads × 4 dimensions = 8 dimensions
```

The final output retains the same model dimension as the input.

---

## Limitations

This experiment does not yet include:

- attention output projection,
- residual connections,
- layer normalization,
- feed-forward networks,
- dropout,
- complete Transformer blocks,
- model training,
- language-model head,
- vocabulary logits.

The attention weights are produced by randomly initialized parameters.

They should not yet be interpreted as learned linguistic relationships.

---

## Product Connection

Modern Transformer models use multiple attention heads because different attention subspaces provide greater representational flexibility.

Instead of forcing the complete context relationship into one attention distribution:

```text
one sequence
→
one attention pattern
```

the model can learn:

```text
one sequence
→
multiple attention patterns
→
combined representation
```

This mechanism forms one of the central components of Transformer architectures.

---

## Check Yourself

### What does `d_model = 8` mean?

Each token is represented using eight values.

### What does `num_heads = 2` mean?

The attention mechanism operates using two attention heads in parallel.

### What is `head_dimension`?

```text
d_model / num_heads
```

In this experiment:

```text
8 / 2 = 4
```

### Do two heads create sixteen model dimensions?

No.

The existing eight dimensions are divided between the two heads.

### Why does `[3, 8]` become `[3, 2, 4]`?

Because the eight dimensions are reorganized as:

```text
2 heads
×
4 dimensions
```

for each of the three tokens.

### Why transpose to `[2, 3, 4]`?

It places the head dimension first so each attention head can be processed independently.

### Why is the attention-weight shape `[2, 3, 3]`?

There are:

```text
2 heads
3 Query positions
3 Key positions
```

### Do all heads produce the same attention weights?

No.

The experiment verified different distributions for Head 1 and Head 2.

### Are the current differences meaningful?

Not linguistically.

The model is untrained, so the current patterns come from random parameter initialization.

### What happens after the heads finish?

Their outputs are concatenated:

```text
[4] + [4]
↓
[8]
```

restoring the original `d_model`.

### What comes next?

The concatenated multi-head result still needs to be integrated into a Transformer block.

The next concepts are:

```text
attention output projection
↓
residual connection
↓
normalization
↓
feed-forward network
```