# Experiment 20 — Layer Normalization

## Objective

Why do Transformers normalize token representations as they pass through many transformations?

The previous experiment produced a residual representation:

```text
original representation
+
attention update
=
residual representation
```

This experiment introduces Layer Normalization.

LayerNorm normalizes the feature dimensions of each token independently while preserving the tensor shape.

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
```

After causal multi-head attention, output projection and the residual connection, the representation has shape:

```text
[3, 8]
```

which means:

```text
3 tokens
×
8 features per token
```

The verified residual representation was:

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

---

## What LayerNorm Normalizes

LayerNorm operates independently on each token representation.

For:

```text
[3, 8]
```

it does not calculate one mean and variance across all 24 values.

Instead:

```text
h → normalize its 8 features

e → normalize its 8 features

l → normalize its 8 features
```

Conceptually:

```text
h  [x x x x x x x x]
   └──── LayerNorm ────┘

e  [x x x x x x x x]
   └──── LayerNorm ────┘

l  [x x x x x x x x]
   └──── LayerNorm ────┘
```

Each token receives its own mean and variance.

---

## Normalization Formula

For one token representation:

```text
x = [x1, x2, ..., x8]
```

LayerNorm first calculates:

```text
mean
```

and:

```text
variance
```

across those eight feature dimensions.

The normalized representation is:

```text
x_normalized =
(x - mean) / sqrt(variance + epsilon)
```

The small value `epsilon` improves numerical stability.

PyTorch uses:

```text
eps = 1e-5
```

by default for `nn.LayerNorm`.

---

## Why `unbiased=False`?

The manual verification uses:

```python
token_before.var(
    unbiased=False
)
```

because PyTorch LayerNorm uses the population variance.

That corresponds to dividing by:

```text
N
```

rather than:

```text
N - 1
```

Using the same definition is necessary for the manual calculation to match `nn.LayerNorm`.

---

## Inspecting Token `e`

Before LayerNorm:

```text
tensor([
    -0.8415,
    -1.9788,
    -0.6441,
     1.9831,
    -1.0040,
    -1.1580,
     1.9251,
    -0.8022
])
```

The measured statistics were:

```text
Mean:
-0.3150532841682434

Variance:
1.8595192432403564
```

These values are neither zero nor one.

---

## Manual Calculation

Consider the first feature:

```text
x1 = -0.8415
```

The mean is approximately:

```text
-0.315053
```

Therefore:

```text
x1 - mean

≈ -0.8415 - (-0.315053)

≈ -0.52645
```

The normalization denominator is approximately:

```text
sqrt(
    1.859519
    +
    0.00001
)

≈ 1.36364
```

Therefore:

```text
-0.52645
---------
 1.36364

≈ -0.3861
```

The first normalized value produced by PyTorch was:

```text
-0.3861
```

The manual calculation therefore matches the LayerNorm operation.

---

## Verified Normalized Output

The complete normalized tensor was:

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

The shape remained:

```text
[3, 8]
```

LayerNorm changes values.

It does not change the number of tokens or the model dimension.

---

## Statistics After LayerNorm

For token `"e"`:

```text
Mean:
-2.2351741790771484e-08
```

which is effectively:

```text
0
```

The variance was:

```text
0.9999945759773254
```

which is approximately:

```text
1
```

Therefore the experiment verified:

```text
before LayerNorm:

mean ≠ 0
variance ≠ 1

↓

LayerNorm

↓

after LayerNorm:

mean ≈ 0
variance ≈ 1
```

The tiny differences from exactly zero and one come from floating-point arithmetic and the numerical-stability epsilon.

---

## Learnable Parameters

PyTorch LayerNorm also contains trainable parameters.

They are commonly described as:

```text
gamma
```

for scaling and:

```text
beta
```

for shifting.

After normalization:

```text
output =
gamma × normalized
+
beta
```

The experiment verified their initial values.

### Gamma

```text
tensor([
    1.,
    1.,
    1.,
    1.,
    1.,
    1.,
    1.,
    1.
])
```

### Beta

```text
tensor([
    0.,
    0.,
    0.,
    0.,
    0.,
    0.,
    0.,
    0.
])
```

Initially:

```text
gamma = 1
beta = 0
```

so:

```text
output = normalized representation
```

During training, gamma and beta can change.

This gives the model the ability to learn useful scales and offsets after normalization.

---

## Manual Verification

The experiment independently calculated:

```text
(token - mean)
-----------------------------
sqrt(variance + epsilon)
```

and compared that result with PyTorch LayerNorm.

The result was:

```text
MANUAL NORMALIZATION MATCH:
True
```

This verifies that the observed output corresponds to the expected normalization operation.

---

## Hypothesis

Applying LayerNorm over `d_model` should:

1. normalize each token independently,
2. preserve tensor shape,
3. produce approximately zero mean for each normalized token,
4. produce approximately unit variance initially,
5. initialize gamma to one,
6. initialize beta to zero,
7. match a manual implementation of the normalization formula.

---

## Implementation

The experiment:

1. encodes `hel`,
2. creates token and positional representations,
3. performs causal multi-head attention,
4. applies the attention output projection,
5. applies the residual connection,
6. creates `nn.LayerNorm(d_model)`,
7. normalizes the residual representation,
8. inspects token `"e"`,
9. compares its statistics before and after normalization,
10. inspects gamma and beta,
11. manually calculates LayerNorm,
12. verifies the result against PyTorch.

---

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/08_layer_normalization/main.py
```

---

## Verified Shape Progression

```text
residual representation
[3, 8]

↓ LayerNorm

normalized representation
[3, 8]
```

For each token:

```text
[8 features]
↓
calculate mean and variance
↓
normalize 8 features
↓
[8 features]
```

---

## Interpretation

LayerNorm does not determine which tokens should interact.

That is the role of attention.

LayerNorm instead operates on the numerical representation of each token.

A useful separation is:

```text
ATTENTION
→ exchanges contextual information
```

```text
RESIDUAL CONNECTION
→ preserves a direct path for the previous representation
```

```text
LAYERNORM
→ normalizes the feature representation
```

These mechanisms solve different problems.

---

## Transformer Placement

This educational progression currently follows:

```text
Multi-Head Attention
↓
Output Projection
↓
Residual Connection
↓
LayerNorm
```

This resembles a post-normalization organization.

Transformer implementations can organize normalization differently.

Many modern decoder-only Transformers use pre-normalization variants:

```text
X
↓
LayerNorm
↓
Attention
↓
Residual Addition
```

The purpose of this experiment is first to understand LayerNorm itself.

The complete block organization will be studied explicitly when the Transformer block is assembled.

---

## Conclusion

The representation pipeline now contains:

```text
token + position representation
↓
causal multi-head attention
↓
attention output projection
↓
residual connection
↓
LayerNorm
```

LayerNorm preserves:

```text
sequence length
d_model
```

while transforming each token's feature values relative to its own mean and variance.

The experiment verified:

```text
mean ≈ 0
variance ≈ 1
```

for the initial normalized representation of token `"e"`.

---

## Limitations

The experiment still does not include:

- feed-forward networks,
- the second Transformer residual path,
- a complete Transformer block,
- dropout,
- stacked Transformer blocks,
- language-model head,
- vocabulary logits,
- next-token loss,
- model training,
- generation.

The attention projections and LayerNorm parameters have not been trained.

---

## Product Connection

Large language models repeatedly transform token representations through many Transformer blocks.

Normalization is one mechanism used to make those deep computations easier to optimize and numerically well behaved.

The exact normalization architecture varies across Transformer families, but the underlying idea of controlling intermediate representations remains fundamental.

---

## Check Yourself

### Does LayerNorm compare different tokens?

No.

Each token is normalized independently across its feature dimensions.

### For `[3, 8]`, what does LayerNorm normalize?

Each of the three rows independently across its eight values.

### Does LayerNorm change the shape?

No.

```text
[3, 8]
↓
LayerNorm
[3, 8]
```

### What happens to the mean initially?

It becomes approximately zero.

### What happens to the variance initially?

It becomes approximately one.

### Why only approximately?

Because of floating-point arithmetic and the added epsilon.

### What is epsilon for?

Numerical stability, including avoiding division by zero or extremely small denominators.

### What is gamma?

A trainable per-feature scale parameter.

### What is beta?

A trainable per-feature offset parameter.

### What are their initial values?

```text
gamma = 1
beta = 0
```

### Does LayerNorm remove the model's ability to learn different scales?

No.

Gamma and beta allow learned rescaling and shifting.

### What comes next?

The Feed-Forward Network.

Attention allows tokens to exchange information.

The feed-forward network will show how each token representation is then transformed independently through a small neural network.