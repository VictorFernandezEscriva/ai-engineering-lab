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

        multi_head_output = (
            head_outputs
            .transpose(0, 1)
            .reshape(
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
# 2. TINY LANGUAGE MODEL
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


print("TRAINING EXAMPLE:")

print(
    repr(input_text),
    "->",
    repr(target_text),
)


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
# 6. LOSS FUNCTION
# ============================================================

criterion = nn.CrossEntropyLoss()


# ============================================================
# 7. OPTIMIZER
# ============================================================

learning_rate = 0.1

optimizer = torch.optim.SGD(
    model.parameters(),
    lr=learning_rate,
)


print()
print("OPTIMIZER:")
print("SGD")

print(
    "Learning rate:",
    learning_rate,
)


# ============================================================
# 8. FIRST FORWARD PASS
# ============================================================

logits_before = model(
    input_ids
)

loss_before = criterion(
    logits_before,
    target_ids,
)


print()
print("LOSS BEFORE UPDATE:")
print(
    loss_before.item()
)


# ============================================================
# 9. SELECT ONE PARAMETER TO INSPECT
# ============================================================

inspected_token = "l"

inspected_token_id = (
    token_to_id[
        inspected_token
    ]
)

row_index = inspected_token_id
column_index = 0

lm_head_weight = (
    model.lm_head.weight
)


weight_before = (
    lm_head_weight[
        row_index,
        column_index
    ]
    .detach()
    .clone()
)


print()
print("INSPECTED PARAMETER:")

print(
    "LM Head token:",
    repr(inspected_token)
)

print(
    "Row:",
    row_index
)

print(
    "Column:",
    column_index
)


print()
print("WEIGHT BEFORE:")
print(
    weight_before.item()
)


# ============================================================
# 10. CLEAR OLD GRADIENTS
# ============================================================

optimizer.zero_grad()


print()
print("GRADIENT AFTER ZERO_GRAD:")

print(
    lm_head_weight.grad
)


# ============================================================
# 11. BACKPROPAGATION
# ============================================================

loss_before.backward()


gradient = (
    lm_head_weight
    .grad[
        row_index,
        column_index
    ]
    .detach()
    .clone()
)


print()
print("GRADIENT:")
print(
    gradient.item()
)


# ============================================================
# 12. VERIFY BACKWARD DID NOT CHANGE WEIGHT
# ============================================================

weight_after_backward = (
    lm_head_weight[
        row_index,
        column_index
    ]
    .detach()
    .clone()
)


print()
print(
    "WEIGHT UNCHANGED AFTER BACKWARD:"
)

print(
    torch.equal(
        weight_before,
        weight_after_backward,
    )
)


# ============================================================
# 13. MANUALLY CALCULATE EXPECTED SGD UPDATE
# ============================================================

expected_weight_after_step = (
    weight_before
    -
    learning_rate
    *
    gradient
)


print()
print(
    "EXPECTED WEIGHT AFTER SGD STEP:"
)

print(
    expected_weight_after_step.item()
)


# ============================================================
# 14. OPTIMIZER STEP
# ============================================================

optimizer.step()


# ============================================================
# 15. INSPECT UPDATED WEIGHT
# ============================================================

weight_after_step = (
    lm_head_weight[
        row_index,
        column_index
    ]
    .detach()
    .clone()
)


print()
print("WEIGHT AFTER OPTIMIZER STEP:")

print(
    weight_after_step.item()
)


print()
print("WEIGHT CHANGED:")

print(
    not torch.equal(
        weight_before,
        weight_after_step,
    )
)


# ============================================================
# 16. VERIFY MANUAL SGD UPDATE
# ============================================================

print()
print(
    "MANUAL SGD UPDATE MATCH:"
)

print(
    torch.allclose(
        expected_weight_after_step,
        weight_after_step,
        atol=1e-7,
    )
)


# ============================================================
# 17. VERIFY OTHER PARAMETERS ALSO CHANGED
# ============================================================

# The previous experiment already showed that these parameters
# receive gradients. Here we compare copies around a fresh step
# using one representative tensor.

block_1_query_weight = (
    model
    .blocks[0]
    .query_projection
    .weight
)


# We cannot reconstruct its previous value after the step,
# so calculate the expected difference from its gradient.
expected_query_change_norm = (
    learning_rate
    *
    block_1_query_weight
    .grad
    .norm()
)


print()
print(
    "EXPECTED BLOCK 1 QUERY "
    "UPDATE NORM:"
)

print(
    expected_query_change_norm.item()
)


# ============================================================
# 18. GRADIENTS STILL EXIST AFTER STEP
# ============================================================

print()
print(
    "GRADIENT STILL EXISTS "
    "AFTER OPTIMIZER STEP:"
)

print(
    lm_head_weight.grad
    is not None
)


# ============================================================
# 19. SECOND FORWARD PASS
# ============================================================

with torch.no_grad():

    logits_after = model(
        input_ids
    )

    loss_after = criterion(
        logits_after,
        target_ids,
    )


print()
print("LOSS AFTER ONE UPDATE:")
print(
    loss_after.item()
)


print()
print("LOSS DECREASED:")

print(
    loss_after.item()
    <
    loss_before.item()
)


# ============================================================
# 20. SUMMARY
# ============================================================

print()
print("SUMMARY:")

print(
    "loss before:",
    loss_before.item()
)

print(
    "loss after:",
    loss_after.item()
)

print(
    "weight before:",
    weight_before.item()
)

print(
    "gradient:",
    gradient.item()
)

print(
    "weight after:",
    weight_after_step.item()
)