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

ffn_hidden_dimension = 4 * d_model


print()
print("MODEL DIMENSIONS:")
print("d_model:", d_model)
print("num_heads:", num_heads)
print("head_dimension:", head_dimension)
print("ffn_hidden_dimension:", ffn_hidden_dimension)


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


# ============================================================
# 5. Q, K AND V PROJECTIONS
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


# ============================================================
# 9. ATTENTION OUTPUT PROJECTION
# ============================================================

output_projection = nn.Linear(
    d_model,
    d_model,
    bias=False
)

attention_output = output_projection(
    multi_head_output
)


# ============================================================
# 10. FIRST RESIDUAL CONNECTION
# ============================================================

attention_residual = (
    x
    +
    attention_output
)


# ============================================================
# 11. LAYER NORMALIZATION
# ============================================================

layer_norm = nn.LayerNorm(
    d_model
)

normalized_output = layer_norm(
    attention_residual
)


print()
print("INPUT TO FEED-FORWARD NETWORK:")
print(normalized_output)

print(
    "Input shape:",
    normalized_output.shape
)


# ============================================================
# 12. CREATE FEED-FORWARD NETWORK
# ============================================================

ffn_linear_1 = nn.Linear(
    d_model,
    ffn_hidden_dimension
)

ffn_activation = nn.GELU()

ffn_linear_2 = nn.Linear(
    ffn_hidden_dimension,
    d_model
)


# ============================================================
# 13. FIRST LINEAR TRANSFORMATION
# ============================================================

ffn_expanded = ffn_linear_1(
    normalized_output
)


print()
print("AFTER FIRST LINEAR LAYER:")
print(
    "Shape:",
    ffn_expanded.shape
)


# ============================================================
# 14. NONLINEAR ACTIVATION
# ============================================================

ffn_activated = ffn_activation(
    ffn_expanded
)


print()
print("AFTER GELU:")
print(
    "Shape:",
    ffn_activated.shape
)


# ============================================================
# 15. SECOND LINEAR TRANSFORMATION
# ============================================================

ffn_output = ffn_linear_2(
    ffn_activated
)


print()
print("FEED-FORWARD OUTPUT:")
print(ffn_output)

print(
    "FFN output shape:",
    ffn_output.shape
)


# ============================================================
# 16. INSPECT ONE TOKEN
# ============================================================

token_index = 1

print()
print("INSPECT TOKEN:")
print(repr(tokens[token_index]))

print()
print("Input representation:")
print(
    normalized_output[token_index].detach()
)

print()
print("Expanded representation shape:")
print(
    ffn_expanded[token_index].shape
)

print()
print("Expanded representation:")
print(
    ffn_expanded[token_index].detach()
)

print()
print("After GELU:")
print(
    ffn_activated[token_index].detach()
)

print()
print("Final FFN representation:")
print(
    ffn_output[token_index].detach()
)


# ============================================================
# 17. VERIFY TOKEN-INDEPENDENT PROCESSING
# ============================================================

single_token_output = ffn_linear_2(
    ffn_activation(
        ffn_linear_1(
            normalized_output[token_index]
        )
    )
)


print()
print("PROCESSING TOKEN ALONE MATCHES BATCHED RESULT:")
print(
    torch.allclose(
        single_token_output,
        ffn_output[token_index],
        atol=1e-6
    )
)


# ============================================================
# 18. MODIFY ANOTHER TOKEN
# ============================================================

modified_input = normalized_output.clone()

modified_input[0] = (
    modified_input[0]
    +
    100.0
)

modified_expanded = ffn_linear_1(
    modified_input
)

modified_activated = ffn_activation(
    modified_expanded
)

modified_output = ffn_linear_2(
    modified_activated
)


print()
print("CHANGE TOKEN 'h' ONLY:")

print(
    "h output unchanged:",
    torch.allclose(
        ffn_output[0],
        modified_output[0]
    )
)

print(
    "e output unchanged:",
    torch.allclose(
        ffn_output[1],
        modified_output[1]
    )
)

print(
    "l output unchanged:",
    torch.allclose(
        ffn_output[2],
        modified_output[2]
    )
)