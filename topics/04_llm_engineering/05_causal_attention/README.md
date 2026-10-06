# Experiment 17 — Causal Self-Attention

## Objective

How can an autoregressive language model prevent tokens from accessing future information?

The previous experiment introduced self-attention:

```text
every token
↓
can attend to every token
```

For a GPT-style language model, this creates a problem.

When predicting the next token, the model must not access tokens that occur later in the sequence.

This experiment introduces a causal mask:

```text
past and present
✓ visible

future
✗ hidden
```

The resulting mechanism is called causal self-attention.

## Concepts

### Normal self-attention

Without a causal mask, the sequence:

```text
h e l
```

allows:

```text
h → h, e, l
e → h, e, l
l → h, e, l
```

Every Query can interact with every Key.

This is useful for understanding self-attention, but it is not suitable for autoregressive next-token prediction.

### Autoregressive prediction

A GPT-style model predicts tokens from left to right.

For example:

```text
h
↓
predict e
```

then:

```text
h e
↓
predict l
```

then:

```text
h e l
↓
predict next token
```

A position may therefore use past and current information, but not future information.

### Causal visibility

For:

```text
h e l
```

the allowed attention pattern is:

```text
h → h

e → h, e

l → h, e, l
```

Visualized as a matrix:

```text
             may attend to

             h     e     l

h            ✓     ✗     ✗
e            ✓     ✓     ✗
l            ✓     ✓     ✓
```

### Causal mask

The experiment created:

```text
tensor([
    [False,  True,  True],
    [False, False,  True],
    [False, False, False]
])
```

where:

```text
False = allowed
True  = masked
```

The upper triangular part represents future positions.

### Why the upper triangle is masked

For row 0:

```text
h
```

columns 1 and 2 correspond to:

```text
e
l
```

which are in the future.

For row 1:

```text
e
```

column 2 corresponds to:

```text
l
```

which is in the future.

For the final token:

```text
l
```

there are no later positions.

### Applying the mask

The scaled attention scores before masking were:

```text
tensor([
    [-0.7711,  0.7566, -0.8158],
    [-0.4789,  0.2783,  0.7701],
    [ 0.3445, -0.9003,  0.7363]
])
```

Future positions were replaced with:

```text
-inf
```

producing:

```text
tensor([
    [-0.7711,    -inf,    -inf],
    [-0.4789,  0.2783,    -inf],
    [ 0.3445, -0.9003,  0.7363]
])
```

### Why use negative infinity?

Softmax converts scores into normalized attention weights.

A value of:

```text
-inf
```

becomes effectively:

```text
0
```

after softmax.

Therefore future positions receive zero attention.

Conceptually:

```text
future score
↓
-inf
↓
softmax
↓
0 attention
```

## Causal Attention Weights

The verified attention weights were:

```text
tensor([
    [1.0000, 0.0000, 0.0000],
    [0.3193, 0.6807, 0.0000],
    [0.3613, 0.1041, 0.5346]
])
```

Each row sums to approximately:

```text
1
```

The verified result was:

```text
Row sums:
tensor([1.0000, 1.0000, 1.0000])
```

### Token `h`

The first token received:

```text
[1.0000, 0.0000, 0.0000]
```

Therefore:

```text
100% → h
0%   → e
0%   → l
```

The token cannot access future information.

### Token `e`

The second token received:

```text
[0.3193, 0.6807, 0.0000]
```

Therefore:

```text
31.93% → h
68.07% → e
0%     → l
```

The token can access:

```text
h e
```

but cannot access:

```text
l
```

### Token `l`

The final token received:

```text
[0.3613, 0.1041, 0.5346]
```

Therefore:

```text
36.13% → h
10.41% → e
53.46% → l
```

Because it is the final token, all positions are available.

## Effect of Masking Before Softmax

In the previous experiment, token `"e"` had attention weights approximately:

```text
[0.1511, 0.3221, 0.5268]
```

After causal masking, access to `"l"` is removed.

The new weights became:

```text
[0.3193, 0.6807, 0.0000]
```

The remaining probability is redistributed across the allowed positions.

This happens because masking is applied before softmax:

```text
scores
↓
apply mask
↓
softmax
```

not after softmax.

## Attention Output

The verified attention output was:

```text
tensor([
    [-0.9260, -1.5257,  0.7680, -0.2360],
    [-0.2990, -0.2783, -0.0280,  0.1418],
    [-0.2442, -0.2845, -0.1466,  0.0253]
])
```

with:

```text
Attention output shape:
torch.Size([3, 4])
```

The model still produces:

```text
3 token positions
×
4 dimensions
```

### First token output

The first token has:

```text
attention weights =
[1, 0, 0]
```

Therefore:

```text
output(h)
=
1 × Value(h)
+
0 × Value(e)
+
0 × Value(l)
```

so:

```text
output(h) = Value(h)
```

This was verified by the experiment.

## Attention Does Not Predict the Next Token

Causal self-attention does not itself choose the next token.

Its job is to create contextual token representations while preventing access to future information.

The broader language-model pipeline is:

```text
tokens
↓
embeddings
↓
causal self-attention
↓
Transformer layers
↓
final token representations
↓
language-model output layer
↓
one logit per vocabulary token
↓
softmax / sampling
↓
next token
```

### Attention vs vocabulary prediction

Attention answers:

```text
Which tokens in the available context should influence this representation?
```

The language-model output layer answers:

```text
Which token from the complete vocabulary should come next?
```

These are different operations.

### Example

Suppose the vocabulary contains:

```text
a
e
h
l
o
```

After processing:

```text
h
```

causal attention can only use information available from `"h"`.

Later, a language-model output layer could produce scores such as:

```text
a → 0.2
e → 3.8
h → -0.4
l → 1.1
o → 0.3
```

The highest score could correspond to:

```text
e
```

Therefore the model could predict `"e"` even though `"e"` was not visible to the attention mechanism.

The prediction comes from learned model parameters, not from looking at the future answer.

## Training With Shifted Targets

For a sequence such as:

```text
h e l l o
```

language-model training can use:

```text
INPUT:
h e l l

TARGET:
e l l o
```

Conceptually:

```text
h       → predict e

h e     → predict l

h e l   → predict l

h e l l → predict o
```

The causal mask prevents each position from seeing the target token directly.

This forces the model to learn:

```text
available context
↓
predict what comes next
```

rather than:

```text
look at future answer
↓
copy it
```

## Hypothesis

Applying a causal mask before softmax should:

1. preserve access to current and previous positions,
2. remove access to future positions,
3. produce exactly zero attention for masked positions,
4. preserve attention-row sums of approximately 1,
5. maintain one output vector for every input token.

## Implementation

The experiment:

1. Encodes the short sequence `hel`.
2. Creates token and positional embeddings.
3. Generates Query, Key and Value vectors.
4. Calculates scaled attention scores.
5. Creates an upper-triangular causal mask.
6. Replaces future scores with negative infinity.
7. Applies softmax.
8. Verifies that future attention weights become zero.
9. Computes the weighted combination of Value vectors.
10. Inspects attention token by token.

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/05_causal_attention/main.py
```

## Observed Results

The input was:

```text
hel
```

with:

```text
Input shape:
[3, 4]
```

The causal mask was:

```text
[
    [False, True,  True],
    [False, False, True],
    [False, False, False]
]
```

The masked scores were:

```text
[
    [-0.7711, -inf,    -inf],
    [-0.4789, 0.2783,  -inf],
    [ 0.3445, -0.9003, 0.7363]
]
```

The final causal attention weights were:

```text
[
    [1.0000, 0.0000, 0.0000],
    [0.3193, 0.6807, 0.0000],
    [0.3613, 0.1041, 0.5346]
]
```

This verifies:

```text
h → h

e → h,e

l → h,e,l
```

Future-token attention was exactly zero.

## Interpretation

Normal self-attention allows:

```text
h → h,e,l
e → h,e,l
l → h,e,l
```

Causal self-attention changes this to:

```text
h → h
e → h,e
l → h,e,l
```

This creates the information restriction required by autoregressive language models.

The mask does not tell the model what token comes next.

It only controls what contextual information is allowed when constructing each representation.

## Conclusion

The language-model pipeline now includes:

```text
text
↓
tokens
↓
token IDs
↓
token + positional embeddings
↓
Q, K, V
↓
scaled attention scores
↓
causal mask
↓
softmax
↓
causal attention
↓
contextual representations
```

The experiment verified that:

```text
future position
↓
masked with -inf
↓
softmax
↓
attention weight = 0
```

This prevents future-token leakage during autoregressive language-model training.

## Limitations

This experiment still does not implement a complete GPT model.

It does not yet include:

- multi-head attention,
- attention output projection,
- residual connections,
- layer normalization,
- feed-forward networks,
- complete Transformer blocks,
- vocabulary logits,
- language-model head,
- cross-entropy next-token loss,
- autoregressive generation,
- multiple Transformer layers.

The Q, K and V projections are also still randomly initialized and have not been trained.

## Product Connection

### Concept

Autoregressive language models generate text from left to right.

They must predict future tokens using only information that is already available.

### Implementation

Causal masking enforces:

```text
current position
↓
can use past and present
↓
cannot use future
```

### Product

During text generation, a model repeatedly performs:

```text
current context
↓
predict next token
↓
append token
↓
use expanded context
↓
predict again
```

Causal attention is one of the mechanisms that makes this autoregressive behavior possible.

## Check Yourself

### Does causal attention choose the next token?

No.

It constructs contextual representations while preventing access to future tokens.

### When does the model compare against the vocabulary?

After the Transformer representations are produced.

A language-model output layer generates one logit for every vocabulary token.

### Why can `"h"` predict `"e"` if `"h"` cannot look at `"e"`?

Because the model learns from training examples that certain contexts make certain future tokens likely.

Its final representation is projected into vocabulary logits.

It does not need to directly observe the future token.

### What can token `"h"` attend to in `hel`?

Only:

```text
h
```

### What can token `"e"` attend to?

```text
h
e
```

### What can token `"l"` attend to?

```text
h
e
l
```

### Why are future scores replaced with `-inf`?

Because softmax converts them into zero attention weight.

### Why is masking applied before softmax?

So softmax redistributes all probability only across allowed positions.

### What does `[1, 0, 0]` mean for `"h"`?

The token takes 100% of its attention information from its own Value vector and none from future tokens.

### What comes next?

The next major step is to extend one attention mechanism into multiple parallel attention heads.

After that, the remaining pieces will begin forming a complete Transformer block and eventually a language model that produces vocabulary logits and predicts the next token.