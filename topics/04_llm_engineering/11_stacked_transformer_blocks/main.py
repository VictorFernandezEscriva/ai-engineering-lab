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

        # Attention projections
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

        # First normalization
        self.layer_norm_1 = nn.LayerNorm(
            d_model
        )

        # Feed-forward network
        self.ffn_linear_1 = nn.Linear(
            d_model,
            ffn_hidden_dimension
        )

        self.ffn_activation = nn.GELU()

        self.ffn_linear_2 = nn.Linear(
            ffn_hidden_dimension,
            d_model
        )

        # Second normalization
        self.layer_norm_2 = nn.LayerNorm(
            d_model
        )


    def forward(self, x):

        sequence_length = x.shape[0]

        # ====================================================
        # ATTENTION
        # ====================================================

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

        # ====================================================
        # FIRST RESIDUAL + NORMALIZATION
        # ====================================================

        x = self.layer_norm_1(
            x
            +
            attention_output
        )

        # ====================================================
        # FEED-FORWARD NETWORK
        # ====================================================

        ffn_output = self.ffn_linear_2(
            self.ffn_activation(
                self.ffn_linear_1(
                    x
                )
            )
        )

        # ====================================================
        # SECOND RESIDUAL + NORMALIZATION
        # ====================================================

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

        layer_outputs = []

        for block in self.blocks:

            x = block(x)

            layer_outputs.append(x)

        return x, layer_outputs


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

vocabulary_size = len(
    vocabulary
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

sequence_length = len(
    tokens
)


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

print(
    "d_model:",
    d_model
)

print(
    "num_heads:",
    num_heads
)

print(
    "head_dimension:",
    d_model // num_heads
)

print(
    "ffn_hidden_dimension:",
    ffn_hidden_dimension
)

print(
    "num_layers:",
    num_layers
)


# ============================================================
# 6. TOKEN + POSITION EMBEDDINGS
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
print("STACK INPUT:")
print(x)

print(
    "Stack input shape:",
    x.shape
)


# ============================================================
# 7. CREATE TRANSFORMER STACK
# ============================================================

transformer_stack = TransformerStack(
    num_layers=num_layers,
    d_model=d_model,
    num_heads=num_heads,
    ffn_hidden_dimension=(
        ffn_hidden_dimension
    )
)


# ============================================================
# 8. VERIFY THAT BLOCK PARAMETERS ARE NOT SHARED
# ============================================================

block_1_weight = (
    transformer_stack
    .blocks[0]
    .query_projection
    .weight
)

block_2_weight = (
    transformer_stack
    .blocks[1]
    .query_projection
    .weight
)


print()
print(
    "BLOCK 1 AND BLOCK 2 SHARE "
    "THE SAME QUERY WEIGHT OBJECT:"
)

print(
    block_1_weight
    is
    block_2_weight
)


print()
print(
    "BLOCK 1 AND BLOCK 2 QUERY "
    "WEIGHTS HAVE IDENTICAL VALUES:"
)

print(
    torch.equal(
        block_1_weight,
        block_2_weight
    )
)


# ============================================================
# 9. FORWARD THROUGH THE STACK
# ============================================================

final_output, layer_outputs = (
    transformer_stack(x)
)


# ============================================================
# 10. INSPECT EACH LAYER
# ============================================================

for layer_index, layer_output in enumerate(
    layer_outputs,
    start=1
):

    print()
    print(
        f"AFTER TRANSFORMER BLOCK "
        f"{layer_index}:"
    )

    print(layer_output)

    print(
        "Shape:",
        layer_output.shape
    )


# ============================================================
# 11. INSPECT ONE TOKEN ACROSS DEPTH
# ============================================================

token_index = 1


print()
print("TRACK TOKEN:")
print(
    repr(
        tokens[token_index]
    )
)


print()
print("BEFORE BLOCKS:")

print(
    x[token_index].detach()
)


for layer_index, layer_output in enumerate(
    layer_outputs,
    start=1
):

    print()

    print(
        f"AFTER BLOCK {layer_index}:"
    )

    print(
        layer_output[
            token_index
        ].detach()
    )


# ============================================================
# 12. VERIFY REPRESENTATIONS CHANGE
# ============================================================

print()
print(
    "BLOCK 1 OUTPUT DIFFERENT "
    "FROM INPUT:"
)

print(
    not torch.allclose(
        x,
        layer_outputs[0]
    )
)


print()
print(
    "BLOCK 2 OUTPUT DIFFERENT "
    "FROM BLOCK 1:"
)

print(
    not torch.allclose(
        layer_outputs[0],
        layer_outputs[1]
    )
)


print()
print(
    "BLOCK 3 OUTPUT DIFFERENT "
    "FROM BLOCK 2:"
)

print(
    not torch.allclose(
        layer_outputs[1],
        layer_outputs[2]
    )
)


# ============================================================
# 13. VERIFY SHAPE PRESERVATION
# ============================================================

expected_shape = (
    sequence_length,
    d_model
)


all_shapes_correct = all(
    layer_output.shape
    ==
    expected_shape
    for layer_output
    in layer_outputs
)


print()
print(
    "ALL LAYERS PRESERVE "
    "[sequence_length, d_model]:"
)

print(
    all_shapes_correct
)


# ============================================================
# 14. FINAL OUTPUT
# ============================================================

print()
print("FINAL STACK OUTPUT:")

print(
    final_output
)

print(
    "Final output shape:",
    final_output.shape
)