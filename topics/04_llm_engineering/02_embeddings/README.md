# Experiment 14 — Token Embeddings

## Objective

How are token IDs converted into numerical representations that a neural network can learn from?

The previous experiment introduced:

```text
text
↓
tokens
↓
token IDs
```

However, token IDs are only identifiers.

For example:

```text
"h" → 5
```

does not mean that the token `"h"` has the numerical meaning `5`.

This experiment introduces token embeddings:

```text
token ID
↓
embedding lookup
↓
vector representation
```

No training is performed yet.

The goal is to understand how `nn.Embedding` maps integer token IDs to trainable vectors.

## Concepts

### Token IDs are identifiers

The verified vocabulary was:

```text
['\n', ' ', 'a', 'd', 'e', 'h', 'i', 'l', 'm', 'o']
```

with:

```text
Vocabulary size: 10
```

The mapping included:

```text
"h" → 5
"e" → 4
"l" → 7
"o" → 9
```

These numbers are identifiers.

They do not represent semantic magnitude.

### Embedding layer

The experiment creates:

```python
embedding = nn.Embedding(
    num_embeddings=10,
    embedding_dim=4
)
```

This creates a trainable table with shape:

```text
[10, 4]
```

which means:

```text
10 rows
4 values per row
```

Each row corresponds to one token ID.

Conceptually:

```text
token ID 0 → embedding row 0
token ID 1 → embedding row 1
token ID 2 → embedding row 2
...
token ID 9 → embedding row 9
```

### Embedding lookup

If:

```text
"h" → token ID 5
```

then the embedding layer performs conceptually:

```text
embedding.weight[5]
```

and returns the vector stored in row 5.

The verified vector for token `"h"` was:

```text
[-0.7581, 1.0783, 0.8008, 1.6806]
```

The token ID itself is not mathematically transformed into that vector.

It is used as an index.

### Embedding table

The verified embedding table had shape:

```text
torch.Size([10, 4])
```

The complete table was:

```text
[[ 1.9269,  1.4873,  0.9007, -2.1055],
 [ 0.6784, -1.2345, -0.0431, -1.6047],
 [-0.7521,  1.6487, -0.3925, -1.4036],
 [-0.7279, -0.5594, -0.7688,  0.7624],
 [ 1.6423, -0.1596, -0.4974,  0.4396],
 [-0.7581,  1.0783,  0.8008,  1.6806],
 [ 0.0349,  0.3211,  1.5736, -0.8455],
 [ 1.3123,  0.6872, -1.0892, -0.3553],
 [-1.4181,  0.8963,  0.0499,  2.2667],
 [ 1.1790, -0.4345, -1.3864, -1.2862]]
```

Each row belongs to one vocabulary token.

### Sequence embeddings

The text:

```text
hello ai
```

was encoded as:

```text
[5, 4, 7, 7, 9, 1, 2, 6]
```

This sequence has:

```text
8 token IDs
```

Each token ID is mapped to a vector of size 4.

Therefore:

```text
[8]
↓ embedding
[8, 4]
```

The verified embedded tensor shape was:

```text
torch.Size([8, 4])
```

This means:

```text
8 tokens
4 embedding values per token
```

### Repeated tokens

The text contains two consecutive `"l"` tokens:

```text
hello
  ^^
```

Both have:

```text
token ID = 7
```

The verified vectors were:

```text
First "l":
[ 1.3123,  0.6872, -1.0892, -0.3553]

Second "l":
[ 1.3123,  0.6872, -1.0892, -0.3553]
```

and:

```text
Vectors match: True
```

This confirms that the same token ID retrieves the same embedding vector.

At this stage, token position is not represented.

### Trainable embeddings

The embedding layer reported:

```text
weight:
shape=torch.Size([10, 4])
requires_grad=True
```

This means the embedding table is a trainable parameter.

During future language-model training:

```text
prediction
↓
loss
↓
backpropagation
↓
embedding gradients
↓
optimizer
↓
updated embedding vectors
```

The vectors can therefore change as the model learns.

### Initial embeddings are not meaningful yet

The embedding values in this experiment were initialized before any training.

Therefore:

```text
[-0.7581, 1.0783, 0.8008, 1.6806]
```

should not yet be interpreted as a learned linguistic meaning for `"h"`.

The values are initial model parameters.

Meaningful representations only emerge through training.

## Hypothesis

The embedding layer should:

1. create one vector for every vocabulary token,
2. use token IDs as row indices,
3. return one vector for every token in the input sequence,
4. return the same vector for repeated identical token IDs,
5. expose trainable parameters.

## Implementation

The experiment:

1. Defines the same small text corpus as the tokenizer experiment.
2. Builds the character vocabulary.
3. Encodes `hello ai` as token IDs.
4. Creates an embedding layer with dimension 4.
5. Converts all token IDs into embedding vectors.
6. Inspects the full embedding table.
7. Verifies that token ID `5` selects row `5`.
8. Verifies that repeated `"l"` tokens produce identical embeddings.
9. Verifies that the embedding weights require gradients.

## Run

Run from the repository root:

```bash
python topics/04_llm_engineering/02_embeddings/main.py
```

## Observed Results

The verified vocabulary was:

```text
['\n', ' ', 'a', 'd', 'e', 'h', 'i', 'l', 'm', 'o']
```

with:

```text
Vocabulary size: 10
```

The text:

```text
hello ai
```

was encoded as:

```text
tensor([5, 4, 7, 7, 9, 1, 2, 6])
```

### Embedding layer

The verified layer was:

```text
Embedding(10, 4)
```

with:

```text
Embedding weight shape:
torch.Size([10, 4])
```

### Embedded sequence

The output was:

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

with shape:

```text
torch.Size([8, 4])
```

### Token lookup verification

For:

```text
Token: 'h'
Token ID: 5
```

the vector directly stored in:

```text
embedding.weight[5]
```

was:

```text
[-0.7581, 1.0783, 0.8008, 1.6806]
```

The vector returned through the embedding layer was identical.

Verification produced:

```text
Vectors match: True
```

### Repeated token verification

Both `"l"` tokens had token ID:

```text
7
```

and both returned:

```text
[1.3123, 0.6872, -1.0892, -0.3553]
```

Verification produced:

```text
Vectors match: True
```

### Trainable parameters

The embedding layer reported:

```text
weight:
shape=torch.Size([10, 4])
requires_grad=True
```

This confirms that the table can be updated through backpropagation.

## Interpretation

The experiment demonstrates that an embedding layer behaves conceptually like a trainable lookup table.

The transformation is:

```text
TOKEN

"h"

↓

TOKEN ID

5

↓

LOOKUP

embedding.weight[5]

↓

EMBEDDING VECTOR

[-0.7581, 1.0783, 0.8008, 1.6806]
```

For a complete sequence:

```text
8 token IDs
↓
embedding lookup
↓
8 embedding vectors
```

The shape changes from:

```text
[8]
```

to:

```text
[8, 4]
```

The original integer IDs are therefore replaced by dense vector representations.

These vectors are not fixed semantic definitions.

They are model parameters that can be optimized during training.

## Conclusion

This experiment establishes the second major stage of the language-model input pipeline:

```text
text
↓
tokens
↓
token IDs
↓
embedding vectors
```

Token IDs are only lookup indices.

The embedding layer converts those indices into trainable vector representations.

The verified experiment demonstrated:

```text
vocabulary size = 10
embedding dimension = 4
embedding table shape = [10, 4]
sequence length = 8
embedded sequence shape = [8, 4]
```

The same token ID retrieves the same embedding vector.

The embedding table also has:

```text
requires_grad=True
```

so it can later be learned through backpropagation.

## Limitations

This experiment deliberately avoids several concepts that will be introduced later.

It does not yet include:

- embedding training,
- language-model loss,
- contextual representations,
- positional information,
- attention,
- transformer blocks,
- batching,
- real subword tokenizers,
- large vocabularies,
- semantic similarity analysis.

The embedding dimension of 4 is intentionally tiny for inspection.

Real language models normally use much larger embedding dimensions.

## Product Connection

### Concept

LLMs require numerical representations of text.

Token IDs identify vocabulary entries, while embeddings provide trainable vector representations.

### Implementation

The input pipeline now contains:

```text
text
↓
tokenizer
↓
token IDs
↓
embedding table
↓
embedding vectors
```

### Product

In a production language model, a tokenizer may generate thousands of possible token IDs.

Each ID selects a learned vector from a large embedding table.

Those embeddings become the first neural representation processed by the Transformer.

## Check Yourself

### Is token ID `5` itself the embedding?

No.

It is an index used to select an embedding row.

### What does `nn.Embedding(10, 4)` mean?

It creates:

```text
10 embedding rows
4 values per row
```

Therefore the parameter matrix has shape:

```text
[10, 4]
```

### Why does `"hello ai"` produce shape `[8, 4]`?

The sequence contains 8 tokens.

Each token receives a 4-dimensional embedding.

### Why do the two `"l"` tokens have identical vectors?

They have the same token ID.

The same token ID selects the same row from the embedding table.

### Does the embedding vector already contain learned linguistic meaning?

Not in this experiment.

The embeddings have been initialized but not trained.

### Are embeddings trainable?

Yes.

The verified parameter has:

```text
requires_grad=True
```

so gradients can be calculated and an optimizer can update the embedding table.

### Why use vectors instead of token IDs directly?

Token IDs are arbitrary identifiers.

Embedding vectors provide a continuous numerical representation that neural-network layers can process and learn.

### What comes next?

The current pipeline is:

```text
text
↓
tokens
↓
token IDs
↓
embeddings
```

The next problem is that identical tokens currently receive identical vectors regardless of where they appear.

The next experiment will introduce **positional information** so the model can distinguish where each token appears in the sequence.