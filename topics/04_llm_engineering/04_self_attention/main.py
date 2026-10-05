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
# 2. ENCODE A SHORT SEQUENCE
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


print("TEXT:")
print(text)

print()
print("TOKENS:")
print(tokens)

print()
print("TOKEN IDs:")
print(token_ids_tensor)


# ============================================================
# 3. TOKEN + POSITION EMBEDDINGS
# ============================================================

torch.manual_seed(42)

embedding_dimension = 4
sequence_length = len(tokens)

token_embedding = nn.Embedding(
    num_embeddings=vocabulary_size,
    embedding_dim=embedding_dimension
)

position_embedding = nn.Embedding(
    num_embeddings=20,
    embedding_dim=embedding_dimension
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
print("INPUT VECTORS:")
print(x)

print(
    "Input shape:",
    x.shape
)


# ============================================================
# 4. CREATE QUERY, KEY AND VALUE PROJECTIONS
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


print()
print("QUERIES:")
print(queries)
print("Query shape:", queries.shape)

print()
print("KEYS:")
print(keys)
print("Key shape:", keys.shape)

print()
print("VALUES:")
print(values)
print("Value shape:", values.shape)


# ============================================================
# 5. CALCULATE RAW ATTENTION SCORES
# ============================================================

raw_scores = queries @ keys.T


print()
print("RAW ATTENTION SCORES:")
print(raw_scores)

print(
    "Raw score shape:",
    raw_scores.shape
)


# ============================================================
# 6. SCALE ATTENTION SCORES
# ============================================================

scale = math.sqrt(embedding_dimension)

scaled_scores = raw_scores / scale


print()
print("SCALED ATTENTION SCORES:")
print(scaled_scores)


# ============================================================
# 7. CONVERT SCORES INTO ATTENTION WEIGHTS
# ============================================================

attention_weights = torch.softmax(
    scaled_scores,
    dim=-1
)


print()
print("ATTENTION WEIGHTS:")
print(attention_weights)

print()
print(
    "Attention weight shape:",
    attention_weights.shape
)

print(
    "Row sums:",
    attention_weights.sum(dim=-1)
)


# ============================================================
# 8. COMPUTE ATTENTION OUTPUT
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
# 9. INSPECT FIRST TOKEN
# ============================================================

print()
print("FIRST TOKEN ATTENTION:")

print(
    "Token:",
    repr(tokens[0])
)

print(
    "Attention weights:",
    attention_weights[0].detach()
)

print(
    "Values:"
)

for token, value in zip(
    tokens,
    values
):
    print(
        f"{repr(token)} -> "
        f"{value.detach()}"
    )

print()
print(
    "Output for first token:",
    attention_output[0].detach()
)