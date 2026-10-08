import torch


# ============================================================
# 1. VOCABULARY
# ============================================================

vocabulary = [
    "\n",
    " ",
    "a",
    "d",
    "e",
    "h",
    "i",
    "l",
    "m",
    "o",
]


print("VOCABULARY:")
print(vocabulary)


# ============================================================
# 2. VERIFIED NEXT-TOKEN LOGITS
# ============================================================

next_token_logits = torch.tensor(
    [
        -0.1707,
         0.0467,
        -0.3556,
         0.6598,
        -0.6396,
        -0.0453,
         0.5186,
        -0.3606,
        -0.0852,
        -0.8803,
    ],
    dtype=torch.float32
)


print()
print("NEXT-TOKEN LOGITS:")
print(next_token_logits)

print(
    "Shape:",
    next_token_logits.shape
)


# ============================================================
# 3. APPLY SOFTMAX
# ============================================================

probabilities = torch.softmax(
    next_token_logits,
    dim=0
)


print()
print("NEXT-TOKEN PROBABILITIES:")
print(probabilities)

print(
    "Shape:",
    probabilities.shape
)


# ============================================================
# 4. VERIFY PROBABILITY SUM
# ============================================================

print()
print("PROBABILITY SUM:")
print(
    probabilities.sum().item()
)


# ============================================================
# 5. PRINT TOKEN PROBABILITIES
# ============================================================

print()
print("PROBABILITY BY VOCABULARY TOKEN:")

for token, probability in zip(
    vocabulary,
    probabilities
):

    print(
        repr(token),
        "->",
        probability.item(),
        "(",
        probability.item() * 100,
        "%)"
    )


# ============================================================
# 6. HIGHEST LOGIT
# ============================================================

highest_logit_id = torch.argmax(
    next_token_logits
).item()


print()
print("HIGHEST LOGIT TOKEN:")
print(
    repr(
        vocabulary[
            highest_logit_id
        ]
    )
)


# ============================================================
# 7. HIGHEST PROBABILITY
# ============================================================

highest_probability_id = torch.argmax(
    probabilities
).item()


print()
print("HIGHEST PROBABILITY TOKEN:")
print(
    repr(
        vocabulary[
            highest_probability_id
        ]
    )
)


print()
print(
    "ARGMAX LOGIT MATCHES ARGMAX PROBABILITY:"
)

print(
    highest_logit_id
    ==
    highest_probability_id
)


# ============================================================
# 8. MANUAL STABLE SOFTMAX
# ============================================================

maximum_logit = torch.max(
    next_token_logits
)

shifted_logits = (
    next_token_logits
    -
    maximum_logit
)

exponentials = torch.exp(
    shifted_logits
)

manual_probabilities = (
    exponentials
    /
    exponentials.sum()
)


print()
print("MAXIMUM LOGIT:")
print(
    maximum_logit.item()
)


print()
print("SHIFTED LOGITS:")
print(
    shifted_logits
)


print()
print("EXPONENTIALS:")
print(
    exponentials
)


print()
print("MANUAL PROBABILITIES:")
print(
    manual_probabilities
)


print()
print("MANUAL SOFTMAX MATCH:")
print(
    torch.allclose(
        manual_probabilities,
        probabilities,
        atol=1e-6
    )
)


# ============================================================
# 9. INSPECT ONE TOKEN
# ============================================================

inspected_token = "l"

inspected_token_id = vocabulary.index(
    inspected_token
)


print()
print("INSPECT TOKEN:")
print(
    repr(
        inspected_token
    )
)

print(
    "Logit:",
    next_token_logits[
        inspected_token_id
    ].item()
)

print(
    "Probability:",
    probabilities[
        inspected_token_id
    ].item()
)

print(
    "Probability percent:",
    probabilities[
        inspected_token_id
    ].item() * 100
)