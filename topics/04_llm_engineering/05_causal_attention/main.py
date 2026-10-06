import math

import torch
import torch.nn as nn


# ============================================================
# 1. CREATE CORPUS AND VOCABULARY
# ============================================================

corpus = "hello ai\nhello model"

vocabulary = sorted(set(corpus))

token_to_id = {
    token: index
    for index, token in enumerate(vocabulary)
}

vocabulary_size = len(vocabulary)


# ============================================================
# 2. ENCODE SHORT SEQUENCE
# ============================================================

text = "hel"

tokens = list(text)

token_ids = [
    token_to_id[token]
    for token in tokens
]

token_ids_tensor = torch.tensor(
    token_ids,
    dtype=torch.long
)

sequence_length = len(tokens)


print("TEXT:")
print(text)

print()
print("TOKENS:")
print(tokens)


# ============================================================
# 3. TOKEN + POSITION EMBEDDINGS
# ============================================================

torch.manual_seed(42)

embedding_dimension = 4

token_embedding = nn.Embedding(
    vocabulary_size,
    embedding_dimension
)

position_embedding = nn.Embedding(
    20,
    embedding_dimension
)

position_ids = torch.arange(
    sequence_length,
    dtype=torch.long
)

token_vectors = token_embedding(
    token_ids_tensor
)

position_vectors = position_embedding(
    position_ids
)

x = token_vectors + position_vectors


print()
print("INPUT SHAPE:")
print(x.shape)


# ============================================================
# 4. CREATE Q, K AND V
# ============================================================

query_projection = nn.Linear(
    embedding_dimension,
    embedding_dimension,
    bias=False
)

key_projection = nn.Linear(
    embedding_dimension,
    embedding_dimension,
    bias=False
)

value_projection = nn.Linear(
    embedding_dimension,
    embedding_dimension,
    bias=False
)


queries = query_projection(x)
keys = key_projection(x)
values = value_projection(x)


# ============================================================
# 5. RAW ATTENTION SCORES
# ============================================================

raw_scores = (
    queries
    @
    keys.T
)

scaled_scores = (
    raw_scores
    /
    math.sqrt(embedding_dimension)
)


print()
print("SCALED ATTENTION SCORES:")
print(scaled_scores)


# ============================================================
# 6. CREATE CAUSAL MASK
# ============================================================

causal_mask = torch.triu(
    torch.ones(
        sequence_length,
        sequence_length,
        dtype=torch.bool
    ),
    diagonal=1
)


print()
print("CAUSAL MASK:")
print(causal_mask)


# ============================================================
# 7. APPLY CAUSAL MASK
# ============================================================

masked_scores = scaled_scores.masked_fill(
    causal_mask,
    float("-inf")
)


print()
print("MASKED ATTENTION SCORES:")
print(masked_scores)


# ============================================================
# 8. SOFTMAX
# ============================================================

attention_weights = torch.softmax(
    masked_scores,
    dim=-1
)


print()
print("CAUSAL ATTENTION WEIGHTS:")
print(attention_weights)

print()
print(
    "Row sums:",
    attention_weights.sum(dim=-1)
)


# ============================================================
# 9. COMPUTE ATTENTION OUTPUT
# ============================================================

attention_output = (
    attention_weights
    @
    values
)


print()
print("ATTENTION OUTPUT:")
print(attention_output)

print(
    "Attention output shape:",
    attention_output.shape
)


# ============================================================
# 10. INSPECT EACH TOKEN
# ============================================================

print()
print("TOKEN-BY-TOKEN ATTENTION:")

for index, token in enumerate(tokens):

    print()
    print(
        f"Token {repr(token)} "
        f"at position {index}:"
    )

    print(
        attention_weights[index].detach()
    )