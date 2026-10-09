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
        ffn_hidden_dimension,
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
            bias=False,
        )

        self.key_projection = nn.Linear(
            d_model,
            d_model,
            bias=False,
        )

        self.value_projection = nn.Linear(
            d_model,
            d_model,
            bias=False,
        )

        self.output_projection = nn.Linear(
            d_model,
            d_model,
            bias=False,
        )

        self.layer_norm_1 = nn.LayerNorm(
            d_model
        )

        self.ffn_linear_1 = nn.Linear(
            d_model,
            ffn_hidden_dimension,
        )

        self.ffn_activation = nn.GELU()

        self.ffn_linear_2 = nn.Linear(
            ffn_hidden_dimension,
            d_model,
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
            self.head_dimension,
        ).transpose(0, 1)

        keys = keys.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension,
        ).transpose(0, 1)

        values = values.reshape(
            sequence_length,
            self.num_heads,
            self.head_dimension,
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
                device=x.device,
            ),
            diagonal=1,
        )

        attention_scores = (
            attention_scores.masked_fill(
                causal_mask,
                float("-inf"),
            )
        )

        attention_weights = torch.softmax(
            attention_scores,
            dim=-1,
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
                self.d_model,
            )
        )

        attention_output = (
            self.output_projection(
                multi_head_output
            )
        )

        x = self.layer_norm_1(
            x + attention_output
        )

        ffn_output = self.ffn_linear_2(
            self.ffn_activation(
                self.ffn_linear_1(x)
            )
        )

        x = self.layer_norm_2(
            x + ffn_output
        )

        return x


# ============================================================
# 2. LANGUAGE MODEL
# ============================================================

class TinyLanguageModel(nn.Module):

    def __init__(
        self,
        vocabulary_size,
        max_sequence_length,
        d_model,
        num_heads,
        ffn_hidden_dimension,
        num_layers,
    ):
        super().__init__()

        self.token_embedding = nn.Embedding(
            vocabulary_size,
            d_model,
        )

        self.position_embedding = nn.Embedding(
            max_sequence_length,
            d_model,
        )

        self.blocks = nn.ModuleList(
            [
                TransformerBlock(
                    d_model=d_model,
                    num_heads=num_heads,
                    ffn_hidden_dimension=(
                        ffn_hidden_dimension
                    ),
                )
                for _ in range(num_layers)
            ]
        )

        self.lm_head = nn.Linear(
            d_model,
            vocabulary_size,
            bias=False,
        )


    def forward(self, token_ids):

        sequence_length = token_ids.shape[0]

        position_ids = torch.arange(
            sequence_length,
            device=token_ids.device,
        )

        x = (
            self.token_embedding(token_ids)
            +
            self.position_embedding(
                position_ids
            )
        )

        for block in self.blocks:
            x = block(x)

        logits = self.lm_head(x)

        return logits


# ============================================================
# 3. VOCABULARY
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

vocabulary_size = len(vocabulary)


# ============================================================
# 4. TRAINING EXAMPLE
# ============================================================

training_text = "hell"

input_text = training_text[:-1]
target_text = training_text[1:]

input_ids = torch.tensor(
    [
        token_to_id[token]
        for token in input_text
    ],
    dtype=torch.long,
)

target_ids = torch.tensor(
    [
        token_to_id[token]
        for token in target_text
    ],
    dtype=torch.long,
)


print("TRAINING TEXT:")
print(repr(training_text))

print()
print("INPUT:")
print(repr(input_text))

print()
print("TARGET:")
print(repr(target_text))

print()
print("INPUT IDS:")
print(input_ids)

print()
print("TARGET IDS:")
print(target_ids)


# ============================================================
# 5. CREATE MODEL
# ============================================================

torch.manual_seed(42)

model = TinyLanguageModel(
    vocabulary_size=vocabulary_size,
    max_sequence_length=20,
    d_model=8,
    num_heads=2,
    ffn_hidden_dimension=32,
    num_layers=3,
)


# ============================================================
# 6. FORWARD PASS
# ============================================================

logits = model(
    input_ids
)

# Keep the gradient of this non-leaf tensor
# so it can be inspected after backward().
logits.retain_grad()


print()
print("LOGITS SHAPE:")
print(logits.shape)


# ============================================================
# 7. LOSS
# ============================================================

criterion = nn.CrossEntropyLoss()

loss = criterion(
    logits,
    target_ids,
)


print()
print("LOSS:")
print(loss.item())


# ============================================================
# 8. SELECT PARAMETERS TO INSPECT
# ============================================================

token_embedding_weight = (
    model.token_embedding.weight
)

block_1_query_weight = (
    model
    .blocks[0]
    .query_projection
    .weight
)

block_3_ffn_weight = (
    model
    .blocks[2]
    .ffn_linear_2
    .weight
)

lm_head_weight = (
    model.lm_head.weight
)


# ============================================================
# 9. GRADIENTS BEFORE BACKWARD
# ============================================================

print()
print("GRADIENTS BEFORE BACKWARD:")

print(
    "Token embedding gradient:",
    token_embedding_weight.grad
)

print(
    "Block 1 query gradient:",
    block_1_query_weight.grad
)

print(
    "Block 3 FFN gradient:",
    block_3_ffn_weight.grad
)

print(
    "LM head gradient:",
    lm_head_weight.grad
)


# ============================================================
# 10. COPY WEIGHTS BEFORE BACKWARD
# ============================================================

token_embedding_before = (
    token_embedding_weight
    .detach()
    .clone()
)

block_1_query_before = (
    block_1_query_weight
    .detach()
    .clone()
)

lm_head_before = (
    lm_head_weight
    .detach()
    .clone()
)


# ============================================================
# 11. BACKPROPAGATION
# ============================================================

loss.backward()


# ============================================================
# 12. GRADIENTS AFTER BACKWARD
# ============================================================

print()
print("GRADIENTS AFTER BACKWARD:")

print(
    "Token embedding gradient exists:",
    token_embedding_weight.grad
    is not None
)

print(
    "Block 1 query gradient exists:",
    block_1_query_weight.grad
    is not None
)

print(
    "Block 3 FFN gradient exists:",
    block_3_ffn_weight.grad
    is not None
)

print(
    "LM head gradient exists:",
    lm_head_weight.grad
    is not None
)


# ============================================================
# 13. GRADIENT NORMS
# ============================================================

print()
print("GRADIENT NORMS:")

print(
    "Token embedding:",
    token_embedding_weight
    .grad
    .norm()
    .item()
)

print(
    "Block 1 query projection:",
    block_1_query_weight
    .grad
    .norm()
    .item()
)

print(
    "Block 3 FFN output projection:",
    block_3_ffn_weight
    .grad
    .norm()
    .item()
)

print(
    "LM head:",
    lm_head_weight
    .grad
    .norm()
    .item()
)


# ============================================================
# 14. INSPECT LOGIT GRADIENT
# ============================================================

print()
print(
    "GRADIENT WITH RESPECT TO LOGITS:"
)

print(
    logits.grad
)

print(
    "Logit gradient shape:",
    logits.grad.shape
)


# ============================================================
# 15. VERIFY FINAL-POSITION LOGIT GRADIENT
# ============================================================

probabilities = torch.softmax(
    logits.detach(),
    dim=1,
)

expected_logit_gradient = (
    probabilities.clone()
)

position_indices = torch.arange(
    target_ids.shape[0]
)

expected_logit_gradient[
    position_indices,
    target_ids
] -= 1.0

expected_logit_gradient /= (
    target_ids.shape[0]
)


print()
print(
    "EXPECTED LOGIT GRADIENT:"
)

print(
    expected_logit_gradient
)


print()
print(
    "LOGIT GRADIENT MATCH:"
)

print(
    torch.allclose(
        logits.grad,
        expected_logit_gradient,
        atol=1e-6,
    )
)


# ============================================================
# 16. VERIFY BACKWARD DID NOT CHANGE WEIGHTS
# ============================================================

print()
print(
    "TOKEN EMBEDDING WEIGHTS "
    "UNCHANGED AFTER BACKWARD:"
)

print(
    torch.equal(
        token_embedding_before,
        token_embedding_weight.detach(),
    )
)


print()
print(
    "BLOCK 1 QUERY WEIGHTS "
    "UNCHANGED AFTER BACKWARD:"
)

print(
    torch.equal(
        block_1_query_before,
        block_1_query_weight.detach(),
    )
)


print()
print(
    "LM HEAD WEIGHTS "
    "UNCHANGED AFTER BACKWARD:"
)

print(
    torch.equal(
        lm_head_before,
        lm_head_weight.detach(),
    )
)


# ============================================================
# 17. INSPECT ONE LM-HEAD GRADIENT VECTOR
# ============================================================

inspected_token = "l"

inspected_token_id = token_to_id[
    inspected_token
]


print()
print("INSPECT TOKEN:")
print(repr(inspected_token))

print(
    "Token ID:",
    inspected_token_id
)


print()
print(
    "LM HEAD GRADIENT VECTOR "
    "FOR TOKEN 'l':"
)

print(
    lm_head_weight
    .grad[
        inspected_token_id
    ]
)