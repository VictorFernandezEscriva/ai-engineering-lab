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
# 2. ENCODE TEXT
# ============================================================

text = "hello ai"

tokens = list(text)

token_ids = [
    token_to_id[token]
    for token in tokens
]

token_ids_tensor = torch.tensor(
    token_ids,
    dtype=torch.long
)


print("Text:", text)
print("Tokens:", tokens)
print("Token IDs:", token_ids_tensor)


# ============================================================
# 3. CREATE TOKEN EMBEDDINGS
# ============================================================

torch.manual_seed(42)

embedding_dimension = 4

token_embedding = nn.Embedding(
    num_embeddings=vocabulary_size,
    embedding_dim=embedding_dimension
)


token_vectors = token_embedding(
    token_ids_tensor
)


print()
print("TOKEN EMBEDDINGS:")
print(token_vectors)

print(
    "Token embedding shape:",
    token_vectors.shape
)


# ============================================================
# 4. CREATE POSITION IDS
# ============================================================

sequence_length = len(tokens)

position_ids = torch.arange(
    sequence_length,
    dtype=torch.long
)


print()
print("POSITION IDS:")
print(position_ids)


# ============================================================
# 5. CREATE POSITION EMBEDDINGS
# ============================================================

max_sequence_length = 20

position_embedding = nn.Embedding(
    num_embeddings=max_sequence_length,
    embedding_dim=embedding_dimension
)


position_vectors = position_embedding(
    position_ids
)


print()
print("POSITION EMBEDDINGS:")
print(position_vectors)

print(
    "Position embedding shape:",
    position_vectors.shape
)


# ============================================================
# 6. COMBINE TOKEN AND POSITION EMBEDDINGS
# ============================================================

input_vectors = (
    token_vectors
    +
    position_vectors
)


print()
print("COMBINED INPUT VECTORS:")
print(input_vectors)

print(
    "Combined shape:",
    input_vectors.shape
)


# ============================================================
# 7. COMPARE REPEATED TOKENS
# ============================================================

first_l_position = 2
second_l_position = 3


print()
print("REPEATED TOKEN COMPARISON")

print(
    "Token at position 2:",
    repr(tokens[first_l_position])
)

print(
    "Token at position 3:",
    repr(tokens[second_l_position])
)


print()
print("Token embedding at position 2:")
print(
    token_vectors[first_l_position].detach()
)

print("Token embedding at position 3:")
print(
    token_vectors[second_l_position].detach()
)


print()
print(
    "Token embeddings match:",
    torch.allclose(
        token_vectors[first_l_position],
        token_vectors[second_l_position]
    )
)


print()
print("Position embedding at position 2:")
print(
    position_vectors[first_l_position].detach()
)

print("Position embedding at position 3:")
print(
    position_vectors[second_l_position].detach()
)


print()
print("Combined vector at position 2:")
print(
    input_vectors[first_l_position].detach()
)

print("Combined vector at position 3:")
print(
    input_vectors[second_l_position].detach()
)


print()
print(
    "Combined vectors match:",
    torch.allclose(
        input_vectors[first_l_position],
        input_vectors[second_l_position]
    )
)


# ============================================================
# 8. VERIFY TRAINABLE POSITION EMBEDDINGS
# ============================================================

print()
print("POSITION EMBEDDING PARAMETERS:")

for name, parameter in position_embedding.named_parameters():

    print(
        f"{name}: "
        f"shape={parameter.shape}, "
        f"requires_grad={parameter.requires_grad}"
    )