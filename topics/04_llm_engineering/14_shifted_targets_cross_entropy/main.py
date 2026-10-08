import torch
import torch.nn as nn


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

token_to_id = {
    token: index
    for index, token
    in enumerate(vocabulary)
}

id_to_token = {
    index: token
    for token, index
    in token_to_id.items()
}


print("VOCABULARY:")
print(vocabulary)


# ============================================================
# 2. CREATE SHIFTED INPUTS AND TARGETS
# ============================================================

training_text = "hell"

input_text = training_text[:-1]
target_text = training_text[1:]


print()
print("TRAINING TEXT:")
print(repr(training_text))

print()
print("INPUT TEXT:")
print(repr(input_text))

print()
print("TARGET TEXT:")
print(repr(target_text))


input_tokens = list(
    input_text
)

target_tokens = list(
    target_text
)


print()
print("INPUT TOKENS:")
print(input_tokens)

print()
print("TARGET TOKENS:")
print(target_tokens)


target_ids = [
    token_to_id[token]
    for token in target_tokens
]

target_ids_tensor = torch.tensor(
    target_ids,
    dtype=torch.long
)


print()
print("TARGET IDS:")
print(target_ids_tensor)

print(
    "Target shape:",
    target_ids_tensor.shape
)


# ============================================================
# 3. VERIFIED MODEL LOGITS
# ============================================================

logits = torch.tensor(
    [
        [
            -0.7904,
            -0.0962,
             0.0973,
            -0.2796,
            -0.1874,
            -0.0152,
             0.6590,
             0.0118,
             0.2709,
            -0.8143,
        ],
        [
             1.0319,
             0.8185,
            -0.1385,
             1.0284,
            -0.8016,
            -0.1323,
            -0.5960,
            -0.5799,
             0.3414,
            -0.7369,
        ],
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
    ],
    dtype=torch.float32
)


print()
print("LOGITS:")
print(logits)

print(
    "Logits shape:",
    logits.shape
)


# ============================================================
# 4. SHOW POSITION-TARGET PAIRS
# ============================================================

print()
print("NEXT-TOKEN TRAINING PAIRS:")

for position_index in range(
    len(input_tokens)
):

    context = input_text[
        :position_index + 1
    ]

    target = target_tokens[
        position_index
    ]

    target_id = target_ids[
        position_index
    ]

    print(
        repr(context),
        "->",
        repr(target),
        "(target ID:",
        target_id,
        ")"
    )


# ============================================================
# 5. CROSS-ENTROPY LOSS PER POSITION
# ============================================================

criterion_per_position = (
    nn.CrossEntropyLoss(
        reduction="none"
    )
)

losses = criterion_per_position(
    logits,
    target_ids_tensor
)


print()
print("LOSS PER POSITION:")
print(losses)


for position_index, loss in enumerate(
    losses
):

    context = input_text[
        :position_index + 1
    ]

    target = target_tokens[
        position_index
    ]

    print(
        repr(context),
        "->",
        repr(target),
        "| loss:",
        loss.item()
    )


# ============================================================
# 6. MEAN CROSS-ENTROPY LOSS
# ============================================================

criterion_mean = nn.CrossEntropyLoss()

mean_loss = criterion_mean(
    logits,
    target_ids_tensor
)


print()
print("MEAN CROSS-ENTROPY LOSS:")
print(
    mean_loss.item()
)


print()
print("MANUAL MEAN OF POSITION LOSSES:")
print(
    losses.mean().item()
)


print()
print("MEAN LOSS MATCH:")
print(
    torch.allclose(
        mean_loss,
        losses.mean(),
        atol=1e-6
    )
)


# ============================================================
# 7. SOFTMAX FOR EDUCATIONAL INSPECTION
# ============================================================

probabilities = torch.softmax(
    logits,
    dim=1
)


print()
print("PROBABILITY MATRIX:")
print(probabilities)

print(
    "Probability matrix shape:",
    probabilities.shape
)


# ============================================================
# 8. EXTRACT CORRECT-TOKEN PROBABILITIES
# ============================================================

position_indices = torch.arange(
    len(target_ids)
)

correct_token_probabilities = (
    probabilities[
        position_indices,
        target_ids_tensor
    ]
)


print()
print(
    "CORRECT-TOKEN PROBABILITY "
    "PER POSITION:"
)

print(
    correct_token_probabilities
)


for position_index, probability in enumerate(
    correct_token_probabilities
):

    context = input_text[
        :position_index + 1
    ]

    target = target_tokens[
        position_index
    ]

    print(
        repr(context),
        "->",
        repr(target),
        "| probability:",
        probability.item(),
        "| percent:",
        probability.item() * 100
    )


# ============================================================
# 9. MANUAL NEGATIVE LOG-LIKELIHOOD
# ============================================================

manual_losses = -torch.log(
    correct_token_probabilities
)


print()
print("MANUAL -LOG(PROBABILITY) LOSSES:")
print(
    manual_losses
)


print()
print(
    "MANUAL LOSSES MATCH "
    "CROSS-ENTROPY:"
)

print(
    torch.allclose(
        manual_losses,
        losses,
        atol=1e-6
    )
)


# ============================================================
# 10. INSPECT FINAL POSITION
# ============================================================

position_index = 2

context = input_text[
    :position_index + 1
]

correct_token = target_tokens[
    position_index
]

correct_token_id = target_ids[
    position_index
]

correct_probability = (
    correct_token_probabilities[
        position_index
    ]
)

position_loss = losses[
    position_index
]


print()
print("INSPECT FINAL POSITION:")

print(
    "Context:",
    repr(context)
)

print(
    "Correct next token:",
    repr(correct_token)
)

print(
    "Correct token ID:",
    correct_token_id
)

print(
    "Correct-token probability:",
    correct_probability.item()
)

print(
    "Correct-token probability percent:",
    correct_probability.item() * 100
)

print(
    "Cross-entropy loss:",
    position_loss.item()
)


# ============================================================
# 11. MANUAL FINAL-POSITION LOSS
# ============================================================

manual_final_loss = -torch.log(
    correct_probability
)


print()
print(
    "MANUAL FINAL-POSITION LOSS:"
)

print(
    manual_final_loss.item()
)


print()
print(
    "FINAL-POSITION LOSS MATCH:"
)

print(
    torch.allclose(
        manual_final_loss,
        position_loss,
        atol=1e-6
    )
)