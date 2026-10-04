# Experiment 15 — Positional Embeddings

## Objective

How can a language model distinguish identical tokens that appear at different positions in a sequence?

Token embeddings tell the model **what token it is**, but by themselves they do not tell the model **where the token appears**.

For example, in:

```text
hello
```

the two `"l"` tokens have:

```text
same token
same token ID
same token embedding
```

but they appear at different positions.

This experiment introduces learnable positional embeddings so that token identity and token position can be combined.

The input representation becomes:

```text
token embedding
+
position embedding
=
combined input representation
```

## Concepts

### Sequence length

The input text was:

```text
hello ai
```

The character-level tokenizer produced:

```text
['h', 'e', 'l', 'l', 'o', ' ', 'a', 'i']
```

This sequence contains:

```text
8 tokens
```

Repeated tokens still count as separate token occurrences.

For example, the two `"l"` tokens occupy two different positions in the sequence.

Therefore:

```text
sequence length = 8
```

### Vocabulary vs sequence

The vocabulary contains unique tokens.

The sequence contains every token occurrence, including repeated tokens.

For example:

```text
"aaaa"
```

could have:

```text
vocabulary size = 1
sequence length = 4
```

All four tokens could share the same token ID while still occupying four different positions.

### Token embeddings

The token IDs for:

```text
hello ai
```

were:

```text
[5, 4, 7, 7, 9, 1, 2, 6]
```

The embedding dimension was:

```text
4
```

Therefore the token embedding tensor had shape:

```text
[8, 4]
```

which means:

```text
8 token occurrences
×
4 values per token
```

The verified token embedding shape was:

```text
torch.Size([8, 4])
```

### Position IDs

Each token occurrence receives a position ID.

For the 8-token sequence:

```text
hello ai
```

the position IDs were:

```text
[0, 1, 2, 3, 4, 5, 6, 7]
```

Conceptually:

```text
position 0 → h
position 1 → e
position 2 → l
position 3 → l
position 4 → o
position 5 → space
position 6 → a
position 7 → i
```

The two `"l"` tokens share the same token ID but have different position IDs.

### Position embedding table

The experiment created:

```python
position_embedding = nn.Embedding(
    num_embeddings=20,
    embedding_dim=4
)
```

The full position embedding table therefore has shape:

```text
[20, 4]
```

which means:

```text
20 possible positions
×
4 values per position
```

The current sequence only uses positions:

```text
0 through 7
```

so only 8 rows are selected from the table.

Therefore the positional vectors used for the current sequence have shape:

```text
[8, 4]
```

### Why token and position embeddings have the same shape

The experiment combines them using addition:

```python
input_vectors = token_vectors + position_vectors
```

For element-wise addition, the corresponding dimensions must be compatible.

Here:

```text
token embeddings:
[8, 4]

position embeddings:
[8, 4]
```

Therefore:

```text
[8, 4] + [8, 4] = [8, 4]
```

The first dimension is the sequence length.

The second dimension is the embedding dimension.

The embedding dimension must match because each token vector and each position vector are added element by element.

### Token information vs position information

A useful mental model is:

```text
token embedding
=
WHAT token is this?
```

while:

```text
position embedding
=
WHERE is this token?
```

Therefore:

```text
WHAT + WHERE
=
combined representation
```

### Repeated tokens

The text contains:

```text
hello
  ^^
```

Both `"l"` tokens have:

```text
token ID = 7
```

Therefore both retrieve the same row from the token embedding table.

The verified token embedding for both was:

```text
[ 1.3123,  0.6872, -1.0892, -0.3553]
```

and:

```text
Token embeddings match: True
```

However, the first `"l"` is at position 2 and the second `"l"` is at position 3.

Their position embeddings were different.

Position 2:

```text
[-1.2024, 0.7078, -1.0759, 0.5357]
```

Position 3:

```text
[1.1754, 0.5612, -0.4527, -0.7718]
```

Therefore their final combined vectors were also different.

Position 2:

```text
[0.1099, 1.3950, -2.1651, 0.1804]
```

Position 3:

```text
[2.4877, 1.2483, -1.5419, -1.1271]
```

and:

```text
Combined vectors match: False
```

This is the main result of the experiment.

### Trainable positional embeddings

The position embedding layer reported:

```text
weight: shape=torch.Size([20, 4]), requires_grad=True
```

Therefore the positional embedding table is a trainable model parameter.

During training, gradients can modify these vectors.

Conceptually:

```text
loss
↓
backpropagation
↓
position embedding gradients
↓
optimizer
↓
updated positional embeddings
```

## Hypothesis

Without positional information, identical tokens should produce identical token embeddings.

After adding different positional embeddings, identical tokens located at different sequence positions should produce different combined representations.

## Implementation

The experiment:

1. Builds the same character vocabulary used in previous experiments.
2. Encodes `hello ai` into token IDs.
3. Creates trainable token embeddings.
4. Generates position IDs for every token occurrence.
5. Creates trainable position embeddings.
6. Retrieves one positional vector per sequence position.
7. Adds token embeddings and position embeddings.
8. Compares the two repeated `"l"` tokens.
9. Verifies that their token embeddings are identical.
10. Verifies that their final combined representations are different.
11. Confirms that positional embeddings are trainable.

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/03_positional_embeddings/main.py
```

## Observed Results

The input was:

```text
hello ai
```

The tokens were:

```text
['h', 'e', 'l', 'l', 'o', ' ', 'a', 'i']
```

The token IDs were:

```text
tensor([5, 4, 7, 7, 9, 1, 2, 6])
```

### Token embeddings

The verified token embedding tensor was:

```text
tensor([
    [-0.7581,  1.0783,  0.8008,  1.6806],
    [ 1.6423, -0.1596, -0.4974,  0.4396],
    [ 1.3123,  0.6872, -1.0892, -0.3553],
    [ 1.3123,  0.6872, -1.0892, -0.3553],
    [ 1.1790, -0.4345, -1.3864, -1.2862],
    [ 0.6784, -1.2345, -0.0431, -1.6047],
    [-0.7521,  1.6487, -0.3925, -1.4036],
    [ 0.0349,  0.3211,  1.5736, -0.8455]
])
```

with:

```text
Token embedding shape: torch.Size([8, 4])
```

### Position IDs

The position IDs were:

```text
tensor([0, 1, 2, 3, 4, 5, 6, 7])
```

### Position embeddings

The verified position vectors were:

```text
tensor([
    [-0.8371, -0.9224,  1.8113,  0.1606],
    [ 0.3672,  0.1754,  1.3852, -0.4459],
    [-1.2024,  0.7078, -1.0759,  0.5357],
    [ 1.1754,  0.5612, -0.4527, -0.7718],
    [ 0.1453,  0.2311,  0.0087, -0.1423],
    [ 0.1971, -1.1441,  0.3383,  1.6992],
    [ 2.8140,  0.3598, -0.0898,  0.4584],
    [-0.5644,  1.0563, -1.4692,  1.4332]
])
```

with:

```text
Position embedding shape: torch.Size([8, 4])
```

### Combined representations

Token and position embeddings were added:

```text
token_vectors + position_vectors
```

producing:

```text
tensor([
    [-1.5953,  0.1559,  2.6121,  1.8412],
    [ 2.0096,  0.0158,  0.8878, -0.0063],
    [ 0.1099,  1.3950, -2.1651,  0.1804],
    [ 2.4877,  1.2483, -1.5419, -1.1271],
    [ 1.3243, -0.2034, -1.3777, -1.4285],
    [ 0.8755, -2.3787,  0.2953,  0.0945],
    [ 2.0619,  2.0085, -0.4823, -0.9452],
    [-0.5295,  1.3774,  0.1045,  0.5877]
])
```

with:

```text
Combined shape: torch.Size([8, 4])
```

### Repeated-token verification

The two `"l"` tokens had identical token embeddings:

```text
Token embeddings match: True
```

but different position embeddings.

As a result:

```text
Combined vectors match: False
```

### Trainable parameters

The position embedding layer reported:

```text
weight: shape=torch.Size([20, 4]), requires_grad=True
```

This confirms that the position embedding table can be optimized through backpropagation.

## Interpretation

Before adding positional information:

```text
position 2 → "l" → token embedding X
position 3 → "l" → token embedding X
```

The two representations are identical.

After adding positional information:

```text
position 2:

token embedding X
+
position embedding 2
=
combined vector A
```

and:

```text
position 3:

token embedding X
+
position embedding 3
=
combined vector B
```

Therefore:

```text
A != B
```

The model can now distinguish two occurrences of the same token based on their positions.

## Conclusion

The language-model input pipeline now contains:

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
combined input representations
```

The verified shapes were:

```text
sequence length = 8
embedding dimension = 4

token embeddings:
[8, 4]

position embeddings used:
[8, 4]

combined representations:
[8, 4]
```

The full positional embedding table was:

```text
[20, 4]
```

because the model supports 20 possible position IDs, while the current sequence only uses 8 of them.

The experiment demonstrated:

```text
same token
+
different position
=
different final representation
```

## Limitations

This experiment uses simple learned absolute positional embeddings.

It does not yet cover:

- sinusoidal positional encoding,
- relative positional representations,
- rotary positional embeddings,
- RoPE,
- attention,
- causal masking,
- multi-head attention,
- transformer blocks,
- language-model training.

Modern Transformer architectures may use different positional mechanisms, but learned positional embeddings provide a simple way to understand why positional information is required.

## Product Connection

### Concept

Language is ordered.

The meaning of a sequence depends not only on which tokens appear, but also on where they appear.

For example:

```text
dog bites man
```

and:

```text
man bites dog
```

contain similar tokens but have different structure and meaning.

A model therefore needs access to token-order information.

### Implementation

The current input representation is:

```text
token embedding
+
position information
```

This produces one position-aware representation for every token occurrence.

### Product

Before Transformer layers can reason over a prompt, the model needs representations that preserve both token identity and sequence structure.

Positional information helps provide that structure.

## Check Yourself

### Why are there 8 token embeddings even though some tokens repeat?

Because the sequence contains 8 token occurrences.

Repeated tokens still occupy separate positions in the sequence.

### Does the vocabulary contain duplicate tokens?

No.

The vocabulary contains unique token types.

### Why do the two `"l"` tokens have the same token embedding?

They both have token ID `7`, so they both retrieve the same row from the token embedding table.

### Why do the two `"l"` tokens get different final representations?

They use different position IDs:

```text
2
3
```

so they receive different positional embeddings.

### Why do token embeddings and position embeddings both have shape `[8, 4]`?

There are 8 token positions, and every representation uses 4 dimensions.

The two tensors are added element by element.

### Why is the full positional embedding table `[20, 4]`?

The experiment allows up to 20 position IDs.

Each position has a 4-dimensional vector.

### Why are only 8 positional vectors returned?

The current sequence only requests positions:

```text
0 through 7
```

### What does `requires_grad=True` mean?

The positional embedding table is trainable and can be updated through backpropagation.

### What comes next?

The current model representation contains:

```text
token identity
+
token position
```

The next step is self-attention, where each token can begin to gather information from other tokens in the sequence.