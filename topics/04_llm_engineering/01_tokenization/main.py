import torch


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

print()
print("VOCABULARY:")
print(vocabulary)

print(
    "Vocabulary size:",
    len(vocabulary)
)


# ============================================================
# 3. CREATE TOKEN <-> ID MAPPINGS
# ============================================================

token_to_id = {
    token: index
    for index, token in enumerate(vocabulary)
}

id_to_token = {
    index: token
    for token, index in token_to_id.items()
}


print()
print("TOKEN TO ID:")
print(token_to_id)


# ============================================================
# 4. TOKENIZE TEXT
# ============================================================

text = "hello ai"

tokens = list(text)

print()
print("ORIGINAL TEXT:")
print(text)

print()
print("TOKENS:")
print(tokens)


# ============================================================
# 5. ENCODE TOKENS AS INTEGER IDs
# ============================================================

token_ids = [
    token_to_id[token]
    for token in tokens
]

token_ids_tensor = torch.tensor(
    token_ids,
    dtype=torch.long
)


print()
print("TOKEN IDs:")
print(token_ids)

print()
print("TOKEN ID TENSOR:")
print(token_ids_tensor)

print(
    "Tensor shape:",
    token_ids_tensor.shape
)

print(
    "Tensor dtype:",
    token_ids_tensor.dtype
)


# ============================================================
# 6. INSPECT INDIVIDUAL TOKENS
# ============================================================

print()
print("TOKEN DETAILS:")

for token, token_id in zip(
    tokens,
    token_ids
):

    print(
        f"{repr(token)} -> {token_id}"
    )


# ============================================================
# 7. DECODE TOKEN IDs BACK TO TEXT
# ============================================================

decoded_tokens = [
    id_to_token[token_id]
    for token_id in token_ids
]

decoded_text = "".join(
    decoded_tokens
)


print()
print("DECODED TOKENS:")
print(decoded_tokens)

print()
print("DECODED TEXT:")
print(decoded_text)

print()
print(
    "Matches original:",
    decoded_text == text
)