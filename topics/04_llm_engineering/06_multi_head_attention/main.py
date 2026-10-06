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

assert d_model % num_heads == 0

head_dimension = d_model // num_heads


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
print("INPUT:")
print(x)

print(
    "Input shape:",
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


print()
print("Q shape before splitting:")
print(queries.shape)

print("K shape before splitting:")
print(keys.shape)

print("V shape before splitting:")
print(values.shape)


# ============================================================
# 6. SPLIT INTO MULTIPLE HEADS
# ============================================================

queries = queries.reshape(
    sequence_length,
    num_heads,
    head_dimension
)

keys = keys.reshape(
    sequence_length,
    num_heads,
    head_dimension
)

values = values.reshape(
    sequence_length,
    num_heads,
    head_dimension
)


print()
print("Q after reshape:")
print(queries.shape)


# Move head dimension first:
#
# [sequence, heads, head_dimension]
# ->
# [heads, sequence, head_dimension]

queries = queries.transpose(0, 1)
keys = keys.transpose(0, 1)
values = values.transpose(0, 1)


print()
print("Q after transpose:")
print(queries.shape)

print("K after transpose:")
print(keys.shape)

print("V after transpose:")
print(values.shape)


# ============================================================
# 7. ATTENTION SCORES FOR ALL HEADS
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


print()
print("ATTENTION SCORE SHAPE:")
print(attention_scores.shape)


# ============================================================
# 8. CREATE CAUSAL MASK
# ============================================================

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


# ============================================================
# 9. SOFTMAX
# ============================================================

attention_weights = torch.softmax(
    attention_scores,
    dim=-1
)


print()
print("ATTENTION WEIGHT SHAPE:")
print(attention_weights.shape)


for head_index in range(num_heads):

    print()
    print(f"HEAD {head_index + 1} ATTENTION:")

    print(
        attention_weights[
            head_index
        ].detach()
    )


# ============================================================
# 10. COMPUTE OUTPUT OF EACH HEAD
# ============================================================

head_outputs = (
    attention_weights
    @
    values
)


print()
print("HEAD OUTPUT SHAPE:")
print(head_outputs.shape)


# ============================================================
# 11. CONCATENATE HEADS
# ============================================================

# [heads, sequence, head_dimension]
# ->
# [sequence, heads, head_dimension]

head_outputs = head_outputs.transpose(
    0,
    1
)


print()
print("HEAD OUTPUTS AFTER TRANSPOSE:")
print(head_outputs.shape)


# Join the head dimensions:
#
# [sequence, heads, head_dimension]
# ->
# [sequence, d_model]

multi_head_output = head_outputs.reshape(
    sequence_length,
    d_model
)


print()
print("MULTI-HEAD OUTPUT:")
print(multi_head_output)

print(
    "Multi-head output shape:",
    multi_head_output.shape
)


# ============================================================
# 12. VERIFY CAUSAL BEHAVIOUR
# ============================================================

print()
print("TOKEN-BY-TOKEN ATTENTION:")

for head_index in range(num_heads):

    print()
    print(f"HEAD {head_index + 1}")

    for token_index, token in enumerate(tokens):

        print(
            f"{repr(token)} -> "
            f"{attention_weights[head_index, token_index].detach()}"
        )