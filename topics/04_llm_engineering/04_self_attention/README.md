# Experiment 16 — Self-Attention: Query, Key and Value

## Objective

How can each token in a sequence gather information from other tokens?

Previous experiments built the input pipeline:

```text
text
↓
tokens
↓
token IDs
↓
token embeddings
+
position embeddings
↓
input vectors
```

Each token now has a numerical representation containing token and positional information.

However, each token still needs a mechanism to interact with the other tokens in the sequence.

This experiment introduces a single-head self-attention mechanism using:

```text
Query
Key
Value
```

or:

```text
Q
K
V
```

The core attention pipeline is:

```text
Q @ Kᵀ
↓
attention scores
↓
scale
↓
softmax
↓
attention weights
↓
attention weights @ V
↓
contextual token representations
```

## Concepts

### Input sequence

The experiment uses the short sequence:

```text
hel
```

which produces:

```text
['h', 'e', 'l']
```

The token IDs were:

```text
tensor([5, 4, 7])
```

There are:

```text
3 tokens
```

and the embedding dimension is:

```text
4
```

Therefore the input tensor has shape:

```text
[3, 4]
```

which means:

```text
3 tokens
×
4 dimensions per token
```

### Input representations

After combining token and position embeddings, the verified input vectors were:

```text
h → [-1.5953,  0.1559,  2.6121,  1.8412]
e → [ 2.0096,  0.0158,  0.8878, -0.0063]
l → [ 0.1099,  1.3950, -2.1651,  0.1804]
```

with:

```text
Input shape: torch.Size([3, 4])
```

### Query, Key and Value

Each input token representation is transformed into three different vectors:

```text
Query
Key
Value
```

using three different linear projections:

```text
X ── Wq ──→ Q
X ── Wk ──→ K
X ── Wv ──→ V
```

Conceptually:

```text
Query = what is this token looking for?

Key = what can this token be matched against?

Value = what information can this token provide?
```

The projections are trainable parameters.

### Query shape

The verified Query tensor was:

```text
tensor([
    [ 0.7572, -0.0806,  1.5715, -0.8557],
    [-0.7142,  0.7165,  0.0548,  1.0221],
    [-1.0684, -1.4209, -0.3499, -0.8142]
])
```

with:

```text
Query shape: torch.Size([3, 4])
```

### Key shape

The verified Key tensor was:

```text
tensor([
    [ 0.5430, -0.4722, -1.3511, -0.1541],
    [ 0.2906,  0.6857,  0.9749,  0.2146],
    [-1.5803, -0.1261, -0.0155,  0.4918]
])
```

with:

```text
Key shape: torch.Size([3, 4])
```

### Value shape

The verified Value tensor was:

```text
tensor([
    [-0.9260, -1.5257,  0.7680, -0.2360],
    [-0.0049,  0.3068, -0.4013,  0.3190],
    [ 0.1699,  0.4392, -0.7151,  0.1447]
])
```

with:

```text
Value shape: torch.Size([3, 4])
```

## Attention Scores

The raw attention scores are calculated with:

```python
raw_scores = queries @ keys.T
```

The shapes are:

```text
Q      = [3, 4]
K      = [3, 4]
Kᵀ     = [4, 3]

[3, 4] @ [4, 3]
=
[3, 3]
```

The resulting matrix was:

```text
tensor([
    [-1.5422,  1.5131, -1.6316],
    [-0.9577,  0.5565,  1.5402],
    [ 0.6890, -1.8006,  1.4725]
])
```

with:

```text
Raw score shape: torch.Size([3, 3])
```

### Meaning of the attention score matrix

The matrix can be interpreted as:

```text
                 KEYS

              h        e        l

QUERY h     -1.5422   1.5131  -1.6316
      e     -0.9577   0.5565   1.5402
      l      0.6890  -1.8006   1.4725
```

Each row belongs to one Query token.

Each column belongs to one Key token.

For example:

```text
row 0, column 1
```

represents:

```text
Query(h) · Key(e)
```

### Manual dot-product verification

The Query for `"h"` was:

```text
[0.7572, -0.0806, 1.5715, -0.8557]
```

The Key for `"e"` was:

```text
[0.2906, 0.6857, 0.9749, 0.2146]
```

Their dot product is approximately:

```text
0.7572 × 0.2906
+
-0.0806 × 0.6857
+
1.5715 × 0.9749
+
-0.8557 × 0.2146

≈ 1.5131
```

which matches the raw attention score:

```text
h → e = 1.5131
```

## Scaled Attention Scores

The raw scores are divided by:

```text
sqrt(d_k)
```

In this experiment:

```text
d_k = 4
```

so:

```text
sqrt(4) = 2
```

The scaled scores were:

```text
tensor([
    [-0.7711,  0.7566, -0.8158],
    [-0.4789,  0.2783,  0.7701],
    [ 0.3445, -0.9003,  0.7363]
])
```

Scaling helps prevent large dot products from making the softmax distribution excessively extreme.

## Attention Weights

Softmax converts each row of scores into normalized attention weights:

```python
attention_weights = torch.softmax(
    scaled_scores,
    dim=-1
)
```

The verified result was:

```text
tensor([
    [0.1524, 0.7020, 0.1457],
    [0.1511, 0.3221, 0.5268],
    [0.3613, 0.1041, 0.5346]
])
```

with:

```text
Attention weight shape: torch.Size([3, 3])
```

Each row sums to approximately:

```text
1
```

The verified result was:

```text
Row sums:
tensor([1., 1., 1.])
```

### Interpretation

For token `"h"`:

```text
15.24% → h
70.20% → e
14.57% → l
```

For token `"e"`:

```text
15.11% → h
32.21% → e
52.68% → l
```

For token `"l"`:

```text
36.13% → h
10.41% → e
53.46% → l
```

These weights determine how much information each token receives from the available Value vectors.

## Attention Output

The final attention output is calculated with:

```python
attention_output = (
    attention_weights
    @
    values
)
```

The shapes are:

```text
attention weights = [3, 3]
values            = [3, 4]

[3, 3] @ [3, 4]
=
[3, 4]
```

The verified output was:

```text
tensor([
    [-0.1197,  0.0469, -0.2689,  0.2091],
    [-0.0519,  0.0997, -0.3900,  0.1433],
    [-0.2442, -0.2845, -0.1466,  0.0253]
])
```

with:

```text
Attention output shape: torch.Size([3, 4])
```

The sequence still contains:

```text
3 token representations
×
4 dimensions
```

but the new representations now combine information from multiple tokens.

## Manual Attention Output Verification

For token `"h"`, the attention weights were:

```text
[0.1524, 0.7020, 0.1457]
```

The Value vectors were:

```text
Value(h):
[-0.9260, -1.5257, 0.7680, -0.2360]

Value(e):
[-0.0049, 0.3068, -0.4013, 0.3190]

Value(l):
[0.1699, 0.4392, -0.7151, 0.1447]
```

Therefore:

```text
Output(h)
=
0.1524 × Value(h)
+
0.7020 × Value(e)
+
0.1457 × Value(l)
```

The approximate contributions were:

```text
from h:
[-0.1411, -0.2325,  0.1170, -0.0360]

from e:
[-0.0034,  0.2154, -0.2817,  0.2239]

from l:
[ 0.0248,  0.0640, -0.1042,  0.0211]
```

Adding them gives approximately:

```text
[-0.1198, 0.0468, -0.2689, 0.2091]
```

The program produced:

```text
[-0.1197, 0.0469, -0.2689, 0.2091]
```

The small difference comes from using rounded printed values during the manual calculation.

This verifies that the attention output is a weighted combination of Value vectors.

## Q, K and V Mental Model

A useful interpretation is:

```text
Query + Key
↓
determine attention weights
↓
WHO should I look at and HOW MUCH?
```

while:

```text
Value
↓
provides the information
↓
WHAT information should be transferred?
```

Therefore:

```text
Q and K
→ decide the weights

V
→ provides the content being mixed
```

## Self-Attention

This mechanism is called self-attention because Queries, Keys and Values all come from the same input sequence.

For:

```text
hel
```

the tokens compare themselves against tokens in:

```text
hel
```

The score matrix contains:

```text
h → h
h → e
h → l

e → h
e → e
e → l

l → h
l → e
l → l
```

Every token can therefore gather information from the same sequence.

## Contextual Representations

Before attention:

```text
h → representation mainly associated with h
e → representation mainly associated with e
l → representation mainly associated with l
```

After attention:

```text
h → weighted mixture of information from h, e and l
e → weighted mixture of information from h, e and l
l → weighted mixture of information from h, e and l
```

This is an important step toward contextual token representations.

## Hypothesis

A self-attention layer should:

1. generate Query, Key and Value vectors for each token,
2. compare every Query with every Key,
3. produce a square attention score matrix,
4. normalize each score row with softmax,
5. produce attention weights whose rows sum to 1,
6. use those weights to combine Value vectors,
7. produce one contextual output vector per input token.

## Implementation

The experiment:

1. Builds the character vocabulary.
2. Encodes the short sequence `hel`.
3. Creates token embeddings.
4. Creates position embeddings.
5. Combines them into input representations.
6. Creates trainable Query, Key and Value projections.
7. Generates Q, K and V.
8. Calculates `Q @ Kᵀ`.
9. Scales the scores by `sqrt(d_k)`.
10. Applies softmax.
11. Verifies that each attention row sums to 1.
12. Multiplies the attention weights by the Value matrix.
13. Inspects the attention computation for the first token.

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/04_self_attention/main.py
```

## Observed Results

The input sequence was:

```text
hel
```

with:

```text
Input shape: [3, 4]
```

The Query, Key and Value shapes were:

```text
Q = [3, 4]
K = [3, 4]
V = [3, 4]
```

The raw attention score shape was:

```text
[3, 3]
```

The attention weight matrix was:

```text
[
    [0.1524, 0.7020, 0.1457],
    [0.1511, 0.3221, 0.5268],
    [0.3613, 0.1041, 0.5346]
]
```

Each row summed to approximately:

```text
1
```

The final attention output shape was:

```text
[3, 4]
```

For token `"h"`:

```text
Attention weights:
[0.1524, 0.7020, 0.1457]
```

and the final output was:

```text
[-0.1197, 0.0469, -0.2689, 0.2091]
```

The output matched the weighted sum of the three Value vectors.

## Interpretation

The core transformation can now be understood as:

```text
INPUT X
│
├──→ Q
├──→ K
└──→ V
```

Then:

```text
Q @ Kᵀ
↓
similarity / compatibility scores
↓
scale
↓
softmax
↓
attention weights
```

Finally:

```text
attention weights @ V
↓
contextual output
```

The complete formula is:

```text
Attention(Q, K, V)
=
softmax(QKᵀ / sqrt(d_k)) V
```

The experiment demonstrates each component of this formula individually instead of treating it as a single black-box operation.

## Important Training Note

The Query, Key and Value projections in this experiment are randomly initialized.

Therefore the observed attention pattern:

```text
h → 70.20% attention to e
```

should not be interpreted as meaningful learned linguistic behavior.

No training has occurred.

During real model training:

```text
prediction
↓
loss
↓
backpropagation
↓
gradients for Wq, Wk and Wv
↓
optimizer
↓
updated attention behavior
```

This is similar to convolutional filters:

```text
random filters
↓
training
↓
useful learned filters
```

Self-attention begins with random projections and learns useful attention patterns through optimization.

## Limitations

This experiment intentionally uses a minimal self-attention implementation.

It does not yet include:

- causal masking,
- multi-head attention,
- output projection,
- residual connections,
- layer normalization,
- feed-forward networks,
- dropout,
- batching,
- transformer blocks,
- autoregressive training,
- next-token prediction.

The current attention mechanism allows every token to attend to every other token, including future positions.

This is not yet suitable for GPT-style autoregressive generation.

## Product Connection

### Concept

Language depends heavily on context.

The meaning and usefulness of a token often depend on surrounding tokens.

Self-attention provides a mechanism for token representations to exchange information.

### Implementation

The processing pipeline now includes:

```text
text
↓
tokenization
↓
token IDs
↓
token + position embeddings
↓
Q, K, V projections
↓
self-attention
↓
contextual token representations
```

### Product

In a large language model, this mechanism allows representations to incorporate information from other parts of the prompt.

Real Transformer models extend this idea using:

- many attention heads,
- many Transformer blocks,
- causal masking,
- residual connections,
- normalization,
- feed-forward networks.

## Check Yourself

### What does Query represent?

It is a learned projection used to determine what a token is looking for when comparing itself with Keys.

### What does Key represent?

It is a learned projection used to determine how relevant a token is to a Query.

### What does Value represent?

It contains the information that is actually combined after attention weights have been calculated.

### Why are Q, K and V different if they come from the same input?

They are produced using three different learned linear transformations:

```text
Wq
Wk
Wv
```

### Why does `Q @ Kᵀ` produce shape `[3, 3]`?

There are 3 Query tokens and 3 Key tokens.

Every Query is compared with every Key.

### What does one cell in the attention score matrix mean?

It is the dot product between one Query vector and one Key vector.

For example:

```text
row 0, column 1
=
Query(h) · Key(e)
```

### Why divide by `sqrt(d_k)`?

To control the magnitude of dot products before softmax, especially when the Key and Query dimensions are large.

### Why use softmax?

Softmax converts arbitrary scores into normalized positive weights whose row sums are approximately 1.

### What does an attention row represent?

It represents how one Query token distributes its attention across all Key tokens.

### What does `attention_weights @ values` do?

It creates a weighted mixture of Value vectors.

### Why is the attention output still `[3, 4]`?

There are still 3 token positions, and each output representation contains 4 dimensions.

### Are the current attention patterns meaningful?

Not yet.

The Q, K and V projections are randomly initialized and have not been trained.

### What is missing for GPT-style attention?

Causal masking.

A GPT-like model must prevent a token from attending to future tokens during autoregressive language modeling.

### What comes next?

The next experiment will introduce causal masking:

```text
self-attention
↓
prevent future-token access
↓
causal self-attention
```

This will move the implementation closer to the attention mechanism used in autoregressive GPT-style models.