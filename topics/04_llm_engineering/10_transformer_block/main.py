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

        # ----------------------------------------------------
        # Attention projections
        # ----------------------------------------------------

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

        # ----------------------------------------------------
        # First LayerNorm
        # ----------------------------------------------------

        self.layer_norm_1 = nn.LayerNorm(
            d_model
        )

        # ----------------------------------------------------
        # Feed-forward network
        # ----------------------------------------------------

        self.ffn_linear_1 = nn.Linear(
            d_model,
            ffn_hidden_dimension
        )

        self.ffn_activation = nn.GELU()

        self.ffn_linear_2 = nn.Linear(
            ffn_hidden_dimension,
            d_model
        )

        # ----------------------------------------------------
        # Second LayerNorm
        # ----------------------------------------------------

        self.layer_norm_2 = nn.LayerNorm(
            d_model
        )


    def forward(self, x):

        sequence_length = x.shape[0]

        # ====================================================
        # 1. Q, K AND V
        # ====================================================

        queries = self.query_projection(x)
        keys = self.key_projection(x)
        values = self.value_projection(x)

        # ====================================================
        # 2. SPLIT INTO HEADS
        # ====================================================

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

        # ====================================================
        # 3. ATTENTION SCORES
        # ====================================================

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

        # ====================================================
        # 4. CAUSAL MASK
        # ====================================================

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

        # ====================================================
        # 5. ATTENTION WEIGHTS
        # ====================================================

        attention_weights = torch.softmax(
            attention_scores,
            dim=-1
        )

        # ====================================================
        # 6. ATTENTION OUTPUT PER HEAD
        # ====================================================

        head_outputs = (
            attention_weights
            @
            values
        )

        # ====================================================
        # 7. CONCATENATE HEADS
        # ====================================================

        head_outputs = (
            head_outputs.transpose(0, 1)
        )

        multi_head_output = (
            head_outputs.reshape(
                sequence_length,
                self.d_model
            )
        )

        # ====================================================
        # 8. ATTENTION OUTPUT PROJECTION
        # ====================================================

        attention_output = (
            self.output_projection(
                multi_head_output
            )
        )

        # ====================================================
        # 9. FIRST RESIDUAL CONNECTION
        # ====================================================

        attention_residual = (
            x
            +
            attention_output
        )

        # ====================================================
        # 10. FIRST LAYERNORM
        # ====================================================

        normalized_attention = (
            self.layer_norm_1(
                attention_residual
            )
        )

        # ====================================================
        # 11. FEED-FORWARD NETWORK
        # ====================================================

        ffn_expanded = (
            self.ffn_linear_1(
                normalized_attention
            )
        )

        ffn_activated = (
            self.ffn_activation(
                ffn_expanded
            )
        )

        ffn_output = (
            self.ffn_linear_2(
                ffn_activated
            )
        )

        # ====================================================
        # 12. SECOND RESIDUAL CONNECTION
        # ====================================================

        ffn_residual = (
            normalized_attention
            +
            ffn_output
        )

        # ====================================================
        # 13. SECOND LAYERNORM
        # ====================================================

        block_output = (
            self.layer_norm_2(
                ffn_residual
            )
        )

        return {
            "attention_weights": attention_weights,
            "attention_output": attention_output,
            "attention_residual": attention_residual,
            "normalized_attention": normalized_attention,
            "ffn_output": ffn_output,
            "ffn_residual": ffn_residual,
            "block_output": block_output,
        }


# ============================================================
# 2. CREATE CORPUS AND VOCABULARY
# ============================================================

corpus = "hello ai\nhello model"

vocabulary = sorted(set(corpus))

token_to_id = {
    token: index
    for index, token in enumerate(vocabulary)
}

vocabulary_size = len(vocabulary)


# ============================================================
# 3. ENCODE SHORT SEQUENCE
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
# 4. MODEL DIMENSIONS
# ============================================================

d_model = 8
num_heads = 2
ffn_hidden_dimension = 32


print()
print("MODEL DIMENSIONS:")

print("d_model:", d_model)
print("num_heads:", num_heads)
print(
    "head_dimension:",
    d_model // num_heads
)
print(
    "ffn_hidden_dimension:",
    ffn_hidden_dimension
)


# ============================================================
# 5. TOKEN + POSITION EMBEDDINGS
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


print()
print("TRANSFORMER BLOCK INPUT:")
print(x)

print(
    "Input shape:",
    x.shape
)


# ============================================================
# 6. CREATE TRANSFORMER BLOCK
# ============================================================

transformer_block = TransformerBlock(
    d_model=d_model,
    num_heads=num_heads,
    ffn_hidden_dimension=(
        ffn_hidden_dimension
    )
)


# ============================================================
# 7. FORWARD PASS
# ============================================================

outputs = transformer_block(x)


# ============================================================
# 8. INSPECT FIRST SUBLAYER
# ============================================================

print()
print("ATTENTION OUTPUT:")
print(
    outputs[
        "attention_output"
    ]
)

print(
    "Attention output shape:",
    outputs[
        "attention_output"
    ].shape
)


print()
print("FIRST RESIDUAL OUTPUT:")
print(
    outputs[
        "attention_residual"
    ]
)

print(
    "First residual shape:",
    outputs[
        "attention_residual"
    ].shape
)


print()
print("AFTER FIRST LAYERNORM:")
print(
    outputs[
        "normalized_attention"
    ]
)


# ============================================================
# 9. INSPECT SECOND SUBLAYER
# ============================================================

print()
print("FFN OUTPUT:")
print(
    outputs[
        "ffn_output"
    ]
)

print(
    "FFN output shape:",
    outputs[
        "ffn_output"
    ].shape
)


print()
print("SECOND RESIDUAL OUTPUT:")
print(
    outputs[
        "ffn_residual"
    ]
)

print(
    "Second residual shape:",
    outputs[
        "ffn_residual"
    ].shape
)


# ============================================================
# 10. FINAL BLOCK OUTPUT
# ============================================================

print()
print("TRANSFORMER BLOCK OUTPUT:")
print(
    outputs[
        "block_output"
    ]
)

print(
    "Transformer block output shape:",
    outputs[
        "block_output"
    ].shape
)


# ============================================================
# 11. INSPECT ONE TOKEN
# ============================================================

token_index = 1

print()
print("INSPECT TOKEN:")
print(
    repr(
        tokens[token_index]
    )
)


print()
print("INPUT:")
print(
    x[token_index].detach()
)


print()
print("AFTER ATTENTION RESIDUAL + NORM:")
print(
    outputs[
        "normalized_attention"
    ][token_index].detach()
)


print()
print("FFN UPDATE:")
print(
    outputs[
        "ffn_output"
    ][token_index].detach()
)


print()
print("SECOND RESIDUAL:")
print(
    outputs[
        "ffn_residual"
    ][token_index].detach()
)


print()
print("FINAL BLOCK OUTPUT:")
print(
    outputs[
        "block_output"
    ][token_index].detach()
)


# ============================================================
# 12. VERIFY SECOND RESIDUAL MANUALLY
# ============================================================

manual_second_residual = (
    outputs[
        "normalized_attention"
    ][token_index]
    +
    outputs[
        "ffn_output"
    ][token_index]
)


print()
print(
    "SECOND RESIDUAL MANUAL MATCH:"
)

print(
    torch.allclose(
        manual_second_residual,
        outputs[
            "ffn_residual"
        ][token_index],
        atol=1e-6
    )
)


# ============================================================
# 13. VERIFY FINAL NORMALIZATION
# ============================================================

final_token = outputs[
    "block_output"
][token_index]


print()
print("FINAL TOKEN STATISTICS:")

print(
    "Mean:",
    final_token.mean().item()
)

print(
    "Variance:",
    final_token.var(
        unbiased=False
    ).item()
)