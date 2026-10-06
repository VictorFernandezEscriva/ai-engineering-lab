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
# 3. MODEL DIMENSIONS
# ============================================================

d_model = 8
num_heads = 2
head_dimension = d_model // num_heads

assert d_model % num_heads == 0


print()
print("MODEL DIMENSIONS:")

print("d_model:", d_model)
print("num_heads:", num_heads)
print("head_dimension:", head_dimension)


# ============================================================
# 4. TOKEN + POSITION EMBEDDINGS
# ============================================================

torch.manual_seed(42)

token_embedding = nn.Embedding(
    vocabulary_size,
    d_model
)

position_embedding = nn.Embedding(
    20,
    d_model
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
print("ORIGINAL INPUT X:")
print(x)

print(
    "Original input shape:",
    x.shape
)


# ============================================================
# 5. CREATE Q, K AND V
# ============================================================

query_projection = nn.Linear(
    d_model,
    d_model,
    bias=False
)

key_projection = nn.Linear(
    d_model,
    d_model,
    bias=False
)

value_projection = nn.Linear(
    d_model,
    d_model,
    bias=False
)

queries = query_projection(x)
keys = key_projection(x)
values = value_projection(x)


# ============================================================
# 6. SPLIT INTO HEADS
# ============================================================

queries = queries.reshape(
    sequence_length,
    num_heads,
    head_dimension
).transpose(0, 1)

keys = keys.reshape(
    sequence_length,
    num_heads,
    head_dimension
).transpose(0, 1)

values = values.reshape(
    sequence_length,
    num_heads,
    head_dimension
).transpose(0, 1)


print()
print("Q SHAPE AFTER SPLITTING:")
print(queries.shape)


# ============================================================
# 7. CAUSAL MULTI-HEAD ATTENTION
# ============================================================

attention_scores = (
    queries
    @
    keys.transpose(-2, -1)
)

attention_scores = (
    attention_scores
    /
    math.sqrt(head_dimension)
)

causal_mask = torch.triu(
    torch.ones(
        sequence_length,
        sequence_length,
        dtype=torch.bool
    ),
    diagonal=1
)

attention_scores = attention_scores.masked_fill(
    causal_mask,
    float("-inf")
)

attention_weights = torch.softmax(
    attention_scores,
    dim=-1
)

head_outputs = (
    attention_weights
    @
    values
)


print()
print("HEAD OUTPUT SHAPE:")
print(head_outputs.shape)


# ============================================================
# 8. CONCATENATE HEADS
# ============================================================

head_outputs = head_outputs.transpose(
    0,
    1
)

multi_head_output = head_outputs.reshape(
    sequence_length,
    d_model
)


print()
print("CONCATENATED MULTI-HEAD OUTPUT:")
print(multi_head_output)

print(
    "Concatenated output shape:",
    multi_head_output.shape
)


# ============================================================
# 9. OUTPUT PROJECTION
# ============================================================

output_projection = nn.Linear(
    d_model,
    d_model,
    bias=False
)

attention_output = output_projection(
    multi_head_output
)


print()
print("PROJECTED ATTENTION OUTPUT:")
print(attention_output)

print(
    "Projected attention output shape:",
    attention_output.shape
)


# ============================================================
# 10. RESIDUAL CONNECTION
# ============================================================

residual_output = (
    x
    +
    attention_output
)


print()
print("RESIDUAL OUTPUT:")
print(residual_output)

print(
    "Residual output shape:",
    residual_output.shape
)


# ============================================================
# 11. INSPECT ONE TOKEN
# ============================================================

token_index = 1

print()
print("INSPECT TOKEN:")
print(repr(tokens[token_index]))

print()
print("Original representation:")
print(
    x[token_index].detach()
)

print()
print("Attention update:")
print(
    attention_output[token_index].detach()
)

print()
print("Residual representation:")
print(
    residual_output[token_index].detach()
)


# ============================================================
# 12. MANUAL VERIFICATION
# ============================================================

manual_residual = (
    x[token_index]
    +
    attention_output[token_index]
)

print()
print("MANUAL RESIDUAL MATCH:")
print(
    torch.allclose(
        manual_residual,
        residual_output[token_index]
    )
)