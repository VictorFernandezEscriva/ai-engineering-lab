import math

import torch
import torch.nn as nn


# ============================================================
# 1. TRANSFORMER BLOCK
# ============================================================

class TransformerBlock(nn.Module):

    def __init__(
        self,
        d_model,
        num_heads,
        ffn_hidden_dimension
    ):
        super().__init__()

        assert d_model % num_heads == 0

        self.d_model = d_model
        self.num_heads = num_heads
        self.head_dimension = (
            d_model // num_heads
        )

        self.query_projection = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

        self.key_projection = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

        self.value_projection = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

        self.output_projection = nn.Linear(
            d_model,
            d_model,
            bias=False
        )

        self.layer_norm_1 = nn.LayerNorm(
            d_model
        )

        self.ffn_linear_1 = nn.Linear(
            d_model,
            ffn_hidden_dimension
        )

        self.ffn_activation = nn.GELU()

        self.ffn_linear_2 = nn.Linear(
            ffn_hidden_dimension,
            d_model
        )

        self.layer_norm_2 = nn.LayerNorm(
            d_model
        )


    def forward(self, x):

        sequence_length = x.shape[0]

        queries = self.query_projection(x)
        keys = self.key_projection(x)
        values = self.value_projection(x)

        queries = queries.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension
        ).transpose(0, 1)

        keys = keys.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension
        ).transpose(0, 1)

        values = values.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension
        ).transpose(0, 1)

        attention_scores = (
            queries
            @
            keys.transpose(-2, -1)
        )

        attention_scores = (
            attention_scores
            /
            math.sqrt(
                self.head_dimension
            )
        )

        causal_mask = torch.triu(
            torch.ones(
                sequence_length,
                sequence_length,
                dtype=torch.bool,
                device=x.device
            ),
            diagonal=1
        )

        attention_scores = (
            attention_scores.masked_fill(
                causal_mask,
                float("-inf")
            )
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

        head_outputs = (
            head_outputs.transpose(0, 1)
        )

        multi_head_output = (
            head_outputs.reshape(
                sequence_length,
                self.d_model
            )
        )

        attention_output = (
            self.output_projection(
                multi_head_output
            )
        )

        x = self.layer_norm_1(
            x
            +
            attention_output
        )

        ffn_output = self.ffn_linear_2(
            self.ffn_activation(
                self.ffn_linear_1(
                    x
                )
            )
        )

        x = self.layer_norm_2(
            x
            +
            ffn_output
        )

        return x


# ============================================================
# 2. TRANSFORMER STACK
# ============================================================

class TransformerStack(nn.Module):

    def __init__(
        self,
        num_layers,
        d_model,
        num_heads,
        ffn_hidden_dimension
    ):
        super().__init__()

        self.blocks = nn.ModuleList(
            [
                TransformerBlock(
                    d_model=d_model,
                    num_heads=num_heads,
                    ffn_hidden_dimension=(
                        ffn_hidden_dimension
                    )
                )
                for _ in range(
                    num_layers
                )
            ]
        )


    def forward(self, x):

        for block in self.blocks:
            x = block(x)

        return x


# ============================================================
# 3. CREATE CORPUS AND VOCABULARY
# ============================================================

corpus = "hello ai\nhello model"

vocabulary = sorted(
    set(corpus)
)

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

vocabulary_size = len(
    vocabulary
)


print("VOCABULARY:")
print(vocabulary)

print()
print(
    "VOCABULARY SIZE:",
    vocabulary_size
)


# ============================================================
# 4. ENCODE SHORT SEQUENCE
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


print()
print("TEXT:")
print(text)

print()
print("TOKENS:")
print(tokens)


# ============================================================
# 5. MODEL DIMENSIONS
# ============================================================

d_model = 8
num_heads = 2
ffn_hidden_dimension = 32
num_layers = 3


print()
print("MODEL DIMENSIONS:")

print("d_model:", d_model)
print("num_heads:", num_heads)
print(
    "ffn_hidden_dimension:",
    ffn_hidden_dimension
)
print(
    "num_layers:",
    num_layers
)


# ============================================================
# 6. EMBEDDINGS
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

x = (
    token_vectors
    +
    position_vectors
)


# ============================================================
# 7. TRANSFORMER STACK
# ============================================================

transformer_stack = TransformerStack(
    num_layers=num_layers,
    d_model=d_model,
    num_heads=num_heads,
    ffn_hidden_dimension=(
        ffn_hidden_dimension
    )
)

final_representations = (
    transformer_stack(x)
)


print()
print("FINAL TRANSFORMER REPRESENTATIONS:")
print(final_representations)

print(
    "Shape:",
    final_representations.shape
)


# ============================================================
# 8. LANGUAGE-MODEL HEAD
# ============================================================

lm_head = nn.Linear(
    d_model,
    vocabulary_size,
    bias=False
)


logits = lm_head(
    final_representations
)


print()
print("VOCABULARY LOGITS:")
print(logits)

print(
    "Logits shape:",
    logits.shape
)


# ============================================================
# 9. INSPECT TOKEN POSITION "e"
# ============================================================

position_index = 1

position_representation = (
    final_representations[
        position_index
    ]
)

position_logits = logits[
    position_index
]


print()
print("INSPECT POSITION:")
print(
    position_index
)

print(
    "Current token:",
    repr(
        tokens[position_index]
    )
)


print()
print("FINAL REPRESENTATION:")
print(
    position_representation.detach()
)


print()
print("LOGITS BY VOCABULARY TOKEN:")

for token_id, logit in enumerate(
    position_logits
):

    print(
        repr(
            id_to_token[token_id]
        ),
        "->",
        logit.item()
    )


# ============================================================
# 10. TOKEN WITH HIGHEST LOGIT
# ============================================================

highest_logit_token_id = torch.argmax(
    position_logits
).item()

highest_logit_token = (
    id_to_token[
        highest_logit_token_id
    ]
)


print()
print("HIGHEST LOGIT TOKEN ID:")
print(
    highest_logit_token_id
)

print()
print("HIGHEST LOGIT TOKEN:")
print(
    repr(
        highest_logit_token
    )
)

print()
print("HIGHEST LOGIT VALUE:")
print(
    position_logits[
        highest_logit_token_id
    ].item()
)


# ============================================================
# 11. INSPECT LM HEAD WEIGHT FOR ONE TOKEN
# ============================================================

inspected_token = "l"

inspected_token_id = (
    token_to_id[
        inspected_token
    ]
)

inspected_weight = (
    lm_head.weight[
        inspected_token_id
    ]
)


print()
print(
    "INSPECT VOCABULARY TOKEN:"
)

print(
    repr(
        inspected_token
    )
)

print(
    "Token ID:",
    inspected_token_id
)


print()
print(
    "LM HEAD WEIGHT VECTOR:"
)

print(
    inspected_weight.detach()
)


# ============================================================
# 12. MANUAL LOGIT CALCULATION
# ============================================================

manual_logit = torch.dot(
    position_representation,
    inspected_weight
)

automatic_logit = (
    position_logits[
        inspected_token_id
    ]
)


print()
print(
    "MANUAL LOGIT FOR TOKEN 'l':"
)

print(
    manual_logit.item()
)


print()
print(
    "AUTOMATIC LOGIT FOR TOKEN 'l':"
)

print(
    automatic_logit.item()
)


print()
print(
    "MANUAL LOGIT MATCH:"
)

print(
    torch.allclose(
        manual_logit,
        automatic_logit,
        atol=1e-6
    )
)

# ============================================================
# 13. NEXT-TOKEN LOGITS FOR THE FULL CONTEXT
# ============================================================

next_token_logits = logits[-1]


print()
print("FULL CONTEXT:")
print(repr(text))


print()
print("NEXT-TOKEN LOGITS:")
print(next_token_logits.detach())

print(
    "Next-token logits shape:",
    next_token_logits.shape
)


next_token_id = torch.argmax(
    next_token_logits
).item()

next_token = id_to_token[
    next_token_id
]


print()
print("GREEDY NEXT TOKEN ID:")
print(next_token_id)

print()
print("GREEDY NEXT TOKEN:")
print(
    repr(next_token)
)