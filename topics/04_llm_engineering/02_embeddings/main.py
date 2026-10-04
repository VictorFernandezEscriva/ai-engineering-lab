import torch
import torch.nn as nn


# ============================================================
# 1. CREATE A SMALL TEXT CORPUS
# ============================================================

corpus = "hello ai\nhello model"

print("CORPUS:")
print(corpus)


# ============================================================
# 2. BUILD CHARACTER VOCABULARY
# ============================================================

vocabulary = sorted(set(corpus))

token_to_id = {
    token: index
    for index, token in enumerate(vocabulary)
}

id_to_token = {
    index: token
    for token, index in token_to_id.items()
}


vocabulary_size = len(vocabulary)

print()
print("Vocabulary:")
print(vocabulary)

print(
    "Vocabulary size:",
    vocabulary_size
)


# ============================================================
# 3. ENCODE TEXT
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


print()
print("Text:")
print(text)

print(
    "Tokens:",
    tokens
)

print(
    "Token IDs:",
    token_ids_tensor
)


# ============================================================
# 4. CREATE EMBEDDING LAYER
# ============================================================

torch.manual_seed(42)

embedding_dimension = 4

embedding = nn.Embedding(
    num_embeddings=vocabulary_size,
    embedding_dim=embedding_dimension
)


print()
print("EMBEDDING LAYER:")
print(embedding)

print(
    "Embedding weight shape:",
    embedding.weight.shape
)


# ============================================================
# 5. CONVERT TOKEN IDs TO EMBEDDINGS
# ============================================================

embedded_tokens = embedding(
    token_ids_tensor
)


print()
print("EMBEDDED TOKENS:")
print(embedded_tokens)

print(
    "Embedded tensor shape:",
    embedded_tokens.shape
)


# ============================================================
# 6. INSPECT EACH TOKEN EMBEDDING
# ============================================================

print()
print("TOKEN EMBEDDINGS:")

for token, token_id, vector in zip(
    tokens,
    token_ids,
    embedded_tokens
):

    print(
        f"{repr(token)} "
        f"(ID {token_id}) "
        f"-> {vector.detach()}"
    )


# ============================================================
# 7. INSPECT EMBEDDING TABLE
# ============================================================

print()
print("FULL EMBEDDING TABLE:")

print(
    embedding.weight.detach()
)


# ============================================================
# 8. VERIFY EMBEDDING LOOKUP
# ============================================================

token = "h"

token_id = token_to_id[token]

table_vector = embedding.weight[
    token_id
]

lookup_vector = embedding(
    torch.tensor(token_id)
)


print()
print("LOOKUP VERIFICATION:")

print(
    "Token:",
    repr(token)
)

print(
    "Token ID:",
    token_id
)

print(
    "Vector directly from embedding table:",
    table_vector.detach()
)

print(
    "Vector returned by embedding layer:",
    lookup_vector.detach()
)

print(
    "Vectors match:",
    torch.allclose(
        table_vector,
        lookup_vector
    )
)


# ============================================================
# 9. VERIFY REPEATED TOKENS
# ============================================================

first_l_position = 2
second_l_position = 3

print()
print("REPEATED TOKEN VERIFICATION:")

print(
    "Token at position 2:",
    repr(tokens[first_l_position])
)

print(
    "Token at position 3:",
    repr(tokens[second_l_position])
)

print(
    "First vector:",
    embedded_tokens[
        first_l_position
    ].detach()
)

print(
    "Second vector:",
    embedded_tokens[
        second_l_position
    ].detach()
)

print(
    "Vectors match:",
    torch.allclose(
        embedded_tokens[first_l_position],
        embedded_tokens[second_l_position]
    )
)


# ============================================================
# 10. VERIFY EMBEDDINGS ARE TRAINABLE
# ============================================================

print()
print("TRAINABLE PARAMETERS:")

for name, parameter in embedding.named_parameters():

    print(
        f"{name}: "
        f"shape={parameter.shape}, "
        f"requires_grad={parameter.requires_grad}"
    )